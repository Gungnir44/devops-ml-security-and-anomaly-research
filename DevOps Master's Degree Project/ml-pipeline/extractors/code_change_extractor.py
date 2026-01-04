"""
Code Change Feature Extractor

Extracts 25 features from Git repository activity using GitHub API.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import statistics
from loguru import logger

try:
    from github import Github, GithubException
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False
    logger.warning("PyGithub not installed. Install with: pip install PyGithub")

from .base_extractor import BaseExtractor


class CodeChangeExtractor(BaseExtractor):
    """
    Extracts code change features from GitHub repository using GitHub API.

    Requires:
    - PyGithub library
    - GitHub Personal Access Token (in env var GITHUB_TOKEN or config)
    """

    def __init__(self, data_dir: Path, config: Optional[Dict[str, Any]] = None):
        """Initialize with GitHub API access."""
        super().__init__(data_dir, config)

        self.github_token = self._get_github_token()
        self.repo_owner = config.get('repo_owner', 'Gungnir44') if config else 'Gungnir44'
        self.repo_name = config.get('repo_name', 'devops-ml-security-and-anomaly-research') if config else 'devops-ml-security-and-anomaly-research'

        if GITHUB_AVAILABLE and self.github_token:
            try:
                self.github = Github(self.github_token)
                self.repo = self.github.get_repo(f"{self.repo_owner}/{self.repo_name}")
                logger.info(f"Connected to GitHub repo: {self.repo.full_name}")
            except Exception as e:
                logger.error(f"Failed to connect to GitHub: {e}")
                self.github = None
                self.repo = None
        else:
            self.github = None
            self.repo = None
            if not GITHUB_AVAILABLE:
                logger.warning("PyGithub not available. Code change features will use defaults.")
            elif not self.github_token:
                logger.warning("GitHub token not found. Set GITHUB_TOKEN environment variable.")

    def _get_github_token(self) -> Optional[str]:
        """Get GitHub token from environment or config."""
        # Try environment variable first
        token = os.environ.get('GITHUB_TOKEN')

        # Try config
        if not token and self.config:
            token = self.config.get('github_token')

        # Try reading from file (where automated downloads store it)
        if not token:
            token_file = Path(__file__).parent.parent.parent.parent / "scripts" / ".github_token"
            if token_file.exists():
                try:
                    with open(token_file, 'r') as f:
                        token = f.read().strip()
                except Exception as e:
                    logger.debug(f"Could not read token file: {e}")

        return token

    def get_feature_names(self) -> List[str]:
        """Return list of 25 code change feature names."""
        return [
            # Commit activity
            'commits_count',
            'commits_per_day_avg',
            'commit_time_variance',

            # Authors
            'unique_authors_count',
            'new_authors_count',

            # Code volume
            'lines_added_total',
            'lines_deleted_total',
            'lines_changed_total',
            'files_changed_count',

            # Commit patterns
            'commit_size_avg_lines',
            'commit_size_max_lines',
            'large_commits_count',

            # Branch activity
            'branches_created_count',
            'branches_deleted_count',
            'pull_requests_count',
            'pull_requests_merged_count',

            # Code complexity
            'cyclomatic_complexity_avg',
            'code_duplication_percent',

            # Commit metadata
            'commit_message_length_avg',
            'commits_no_message_count',

            # Unusual patterns
            'commits_unusual_hours_count',
            'force_push_count',
            'binary_files_changed_count',

            # Review patterns
            'code_review_time_avg_hours',
            'commits_without_review_count',
        ]

    def extract(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Extract all 25 code change features.

        Args:
            start_time: Start of time window (default: 7 days ago)
            end_time: End of time window (default: now)
            **kwargs: Additional parameters (e.g., branch filter)

        Returns:
            Dictionary of features
        """
        logger.info(f"Extracting code change features")

        # Default time window: last 7 days
        if not end_time:
            end_time = datetime.now()
        if not start_time:
            start_time = end_time - timedelta(days=7)

        # Initialize features
        features = {name: 0 for name in self.get_feature_names()}
        features.update({
            'commits_per_day_avg': 0.0,
            'commit_time_variance': 0.0,
            'commit_size_avg_lines': 0.0,
            'cyclomatic_complexity_avg': 0.0,
            'code_duplication_percent': 0.0,
            'commit_message_length_avg': 0.0,
            'code_review_time_avg_hours': 0.0,
        })

        if not self.repo:
            logger.warning("GitHub API not available, using estimated features")
            return self._get_estimated_features(start_time, end_time)

        try:
            # Extract commit features
            commit_features = self._extract_commit_features(start_time, end_time)
            features.update(commit_features)

            # Extract branch features
            branch_features = self._extract_branch_features(start_time, end_time)
            features.update(branch_features)

            # Extract PR features
            pr_features = self._extract_pr_features(start_time, end_time)
            features.update(pr_features)

            # Calculate derived features
            derived_features = self._calculate_derived_features(features, start_time, end_time)
            features.update(derived_features)

            logger.success(f"Extracted {len(features)} code change features")

        except GithubException as e:
            logger.error(f"GitHub API error: {e}")
            # Fall back to estimates
            features = self._get_estimated_features(start_time, end_time)
        except Exception as e:
            logger.error(f"Error extracting code change features: {e}")
            logger.exception(e)

        return features

    def _extract_commit_features(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, Any]:
        """Extract features from commits."""
        features = {}

        try:
            # Ensure timezone-aware datetimes for PyGithub
            if start_time.tzinfo is None:
                from datetime import timezone
                start_time = start_time.replace(tzinfo=timezone.utc)
            if end_time.tzinfo is None:
                from datetime import timezone
                end_time = end_time.replace(tzinfo=timezone.utc)

            # Get commits in time window (limit to avoid rate limits)
            commits = self.repo.get_commits(since=start_time, until=end_time)

            # Convert PaginatedList to list (with reasonable limit)
            commit_list = []
            try:
                for i, commit in enumerate(commits):
                    if i >= 1000:  # Limit to 1000 commits
                        break
                    commit_list.append(commit)
            except Exception as e:
                logger.warning(f"Error iterating commits: {e}")

            features['commits_count'] = len(commit_list)

            if not commit_list:
                logger.warning("No commits found in time window")
                return features

            # Analyze commits
            authors = set()
            lines_added = 0
            lines_deleted = 0
            files_changed = 0
            commit_sizes = []
            message_lengths = []
            no_message_count = 0
            unusual_hours = 0
            binary_changes = 0

            for commit in commit_list:
                try:
                    # Authors
                    if commit.author:
                        authors.add(commit.author.login if commit.author else 'unknown')

                    # Stats (may not be available for all commits)
                    if commit.stats:
                        additions = commit.stats.additions
                        deletions = commit.stats.deletions
                        lines_added += additions
                        lines_deleted += deletions
                        commit_sizes.append(additions + deletions)
                    # Files (commit.files is a PaginatedList - convert to list)
                    if commit.files:
                        try:
                            file_list = list(commit.files)
                            files_changed += len(file_list)

                            # Binary files
                            for file in file_list:
                                if file.patch is None and file.changes > 0:
                                    binary_changes += 1
                        except:
                            pass

                    # Commit message
                    msg = commit.commit.message if commit.commit else ""
                    msg_length = len(msg)
                    message_lengths.append(msg_length)

                    if msg_length < 10:  # Very short or empty message
                        no_message_count += 1

                    # Unusual hours (outside 9 AM - 6 PM)
                    if commit.commit and commit.commit.author:
                        commit_time = commit.commit.author.date
                        if commit_time:
                            hour = commit_time.hour
                            if hour < 9 or hour > 18:
                                unusual_hours += 1

                except Exception as e:
                    logger.debug(f"Error processing commit: {e}")
                    continue

            features['unique_authors_count'] = len(authors)
            features['lines_added_total'] = lines_added
            features['lines_deleted_total'] = lines_deleted
            features['lines_changed_total'] = lines_added + lines_deleted
            features['files_changed_count'] = files_changed
            features['commits_no_message_count'] = no_message_count
            features['commits_unusual_hours_count'] = unusual_hours
            features['binary_files_changed_count'] = binary_changes

            # Average commit size
            if commit_sizes:
                features['commit_size_avg_lines'] = statistics.mean(commit_sizes)
                features['commit_size_max_lines'] = max(commit_sizes)
                features['large_commits_count'] = sum(1 for size in commit_sizes if size > 500)

            # Average message length
            if message_lengths:
                features['commit_message_length_avg'] = statistics.mean(message_lengths)

            logger.debug(f"Analyzed {len(commit_list)} commits from {len(authors)} authors")

        except Exception as e:
            logger.error(f"Error extracting commit features: {e}")

        return features

    def _extract_branch_features(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, Any]:
        """Extract features from branch activity."""
        features = {}

        try:
            # Get all branches
            branches = list(self.repo.get_branches())

            # Count branches created in window (approximate based on last commit)
            branches_in_window = 0
            for branch in branches:
                try:
                    last_commit = branch.commit
                    if last_commit and last_commit.commit.author:
                        commit_date = last_commit.commit.author.date
                        if start_time <= commit_date <= end_time:
                            branches_in_window += 1
                except:
                    pass

            features['branches_created_count'] = branches_in_window
            # Note: Can't easily track deleted branches via API
            features['branches_deleted_count'] = 0

            logger.debug(f"Found {len(branches)} total branches, {branches_in_window} active in window")

        except Exception as e:
            logger.error(f"Error extracting branch features: {e}")

        return features

    def _extract_pr_features(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, Any]:
        """Extract features from pull requests."""
        features = {}

        try:
            # Get PRs in time window
            prs = self.repo.get_pulls(
                state='all',
                sort='created',
                direction='desc'
            )

            pr_count = 0
            merged_count = 0
            review_times = []

            for pr in prs:
                if pr.created_at < start_time:
                    break  # Older than our window

                if start_time <= pr.created_at <= end_time:
                    pr_count += 1

                    if pr.merged:
                        merged_count += 1

                        # Calculate review time
                        if pr.merged_at:
                            review_time = (pr.merged_at - pr.created_at).total_seconds() / 3600
                            review_times.append(review_time)

            features['pull_requests_count'] = pr_count
            features['pull_requests_merged_count'] = merged_count

            if review_times:
                features['code_review_time_avg_hours'] = statistics.mean(review_times)

            logger.debug(f"Analyzed {pr_count} PRs, {merged_count} merged")

        except Exception as e:
            logger.error(f"Error extracting PR features: {e}")

        return features

    def _calculate_derived_features(
        self,
        features: Dict[str, Any],
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, Any]:
        """Calculate derived code change features."""
        derived = {}

        # Commits per day
        days = (end_time - start_time).days + 1
        commits = features.get('commits_count', 0)
        derived['commits_per_day_avg'] = commits / days if days > 0 else 0.0

        # Commit time variance (simplified - would need actual commit times)
        derived['commit_time_variance'] = 0.0

        # New authors (would need historical comparison)
        derived['new_authors_count'] = 0

        # Force pushes (not easily detectable via API)
        derived['force_push_count'] = 0

        # Commits without review (PRs that don't exist)
        total_commits = features.get('commits_count', 0)
        pr_commits = features.get('pull_requests_merged_count', 0)
        derived['commits_without_review_count'] = max(0, total_commits - pr_commits)

        # Code complexity (would need code analysis)
        derived['cyclomatic_complexity_avg'] = 0.0
        derived['code_duplication_percent'] = 0.0

        return derived

    def _get_estimated_features(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, Any]:
        """
        Get estimated features when GitHub API is not available.
        Based on typical patterns for a 3-person team.
        """
        days = (end_time - start_time).days + 1

        # Estimate based on typical development patterns
        estimated_commits_per_day = 2.0  # Conservative for small team
        total_commits = int(estimated_commits_per_day * days)

        features = {
            'commits_count': total_commits,
            'commits_per_day_avg': estimated_commits_per_day,
            'commit_time_variance': 0.0,

            'unique_authors_count': 3,  # Your team size
            'new_authors_count': 0,

            'lines_added_total': total_commits * 50,  # ~50 lines per commit
            'lines_deleted_total': total_commits * 30,
            'lines_changed_total': total_commits * 80,
            'files_changed_count': total_commits * 3,  # ~3 files per commit

            'commit_size_avg_lines': 80.0,
            'commit_size_max_lines': 500.0,
            'large_commits_count': max(1, int(total_commits * 0.1)),

            'branches_created_count': max(1, days // 3),  # Branch every 3 days
            'branches_deleted_count': 0,
            'pull_requests_count': max(1, days // 2),  # PR every 2 days
            'pull_requests_merged_count': max(1, days // 3),

            'cyclomatic_complexity_avg': 0.0,
            'code_duplication_percent': 0.0,

            'commit_message_length_avg': 50.0,
            'commits_no_message_count': int(total_commits * 0.05),  # 5% short messages

            'commits_unusual_hours_count': int(total_commits * 0.2),  # 20% outside hours
            'force_push_count': 0,
            'binary_files_changed_count': int(total_commits * 0.1),

            'code_review_time_avg_hours': 4.0,
            'commits_without_review_count': int(total_commits * 0.3),  # 30% direct commits
        }

        logger.info("Using estimated code change features (GitHub API not available)")
        return features
