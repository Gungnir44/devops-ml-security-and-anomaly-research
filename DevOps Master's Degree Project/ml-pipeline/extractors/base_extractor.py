"""
Base Extractor Class

All feature extractors inherit from this base class.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
import yaml
from loguru import logger


class BaseExtractor(ABC):
    """
    Abstract base class for all feature extractors.

    Each extractor is responsible for extracting a category of features
    from the collected data sources.
    """

    def __init__(self, data_dir: Path, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the extractor.

        Args:
            data_dir: Path to the research data directory
            config: Optional configuration dictionary
        """
        self.data_dir = Path(data_dir)
        self.config = config or {}
        self.features: Dict[str, Any] = {}

        # Load feature definitions
        self.feature_definitions = self._load_feature_definitions()

        logger.info(f"Initialized {self.__class__.__name__}")

    def _load_feature_definitions(self) -> Dict[str, Any]:
        """Load feature definitions from YAML."""
        definitions_path = Path(__file__).parent.parent / "feature_definitions.yaml"

        if definitions_path.exists():
            with open(definitions_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            logger.warning(f"Feature definitions not found at {definitions_path}")
            return {}

    @abstractmethod
    def extract(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Extract features for the specified time window.

        Args:
            start_time: Start of the time window (None = all data)
            end_time: End of the time window (None = now)
            **kwargs: Additional extraction parameters

        Returns:
            Dictionary of feature names to values
        """
        pass

    @abstractmethod
    def get_feature_names(self) -> List[str]:
        """
        Get the list of feature names this extractor provides.

        Returns:
            List of feature names
        """
        pass

    def get_feature_count(self) -> int:
        """Get the number of features this extractor provides."""
        return len(self.get_feature_names())

    def validate_features(self, features: Dict[str, Any]) -> bool:
        """
        Validate that extracted features match expected schema.

        Args:
            features: Extracted features dictionary

        Returns:
            True if valid, False otherwise
        """
        expected_names = set(self.get_feature_names())
        actual_names = set(features.keys())

        if expected_names != actual_names:
            missing = expected_names - actual_names
            extra = actual_names - expected_names

            if missing:
                logger.warning(f"Missing features: {missing}")
            if extra:
                logger.warning(f"Unexpected features: {extra}")

            return False

        return True

    def to_dataframe(self, features: Dict[str, Any]) -> pd.DataFrame:
        """
        Convert features dictionary to pandas DataFrame.

        Args:
            features: Extracted features

        Returns:
            DataFrame with single row of features
        """
        return pd.DataFrame([features])

    def _find_files(
        self,
        pattern: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Path]:
        """
        Find files matching pattern within time window.

        Args:
            pattern: Glob pattern to match
            start_time: Optional start time filter
            end_time: Optional end time filter

        Returns:
            List of matching file paths
        """
        files = list(self.data_dir.rglob(pattern))

        if start_time or end_time:
            filtered_files = []
            for file_path in files:
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)

                if start_time and file_time < start_time:
                    continue
                if end_time and file_time > end_time:
                    continue

                filtered_files.append(file_path)

            return filtered_files

        return files

    def _safe_divide(self, numerator: float, denominator: float, default: float = 0.0) -> float:
        """
        Safely divide two numbers, returning default if denominator is zero.

        Args:
            numerator: Numerator
            denominator: Denominator
            default: Default value if division by zero

        Returns:
            Result of division or default
        """
        if denominator == 0:
            return default
        return numerator / denominator

    def __repr__(self) -> str:
        """String representation of the extractor."""
        return f"{self.__class__.__name__}(features={self.get_feature_count()})"
