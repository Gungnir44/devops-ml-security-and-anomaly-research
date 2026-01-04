"""
Compare Features Between Main and Hardened Branches

Analyzes differences in all 208 features between branches to quantify
security improvements and code changes.
"""

import pandas as pd
import sys
from pathlib import Path


def compare_branches(main_file, hardened_file, output_dir="output"):
    """Compare feature vectors from two branches."""

    print("=" * 80)
    print("BRANCH COMPARISON ANALYSIS")
    print("=" * 80)
    print()

    # Load data
    print(f"[*] Loading main branch data from: {main_file}")
    main_df = pd.read_csv(main_file)

    print(f"[*] Loading hardened branch data from: {hardened_file}")
    hardened_df = pd.read_csv(hardened_file)

    print()
    print(f"[*] Main branch features: {len(main_df.columns)}")
    print(f"[*] Hardened branch features: {len(hardened_df.columns)}")
    print()

    # Find differences
    differences = []
    identical = []

    for col in main_df.columns:
        if col in hardened_df.columns:
            main_val = main_df[col].iloc[0]
            hard_val = hardened_df[col].iloc[0]

            if main_val != hard_val:
                # Calculate percent change
                if main_val != 0:
                    pct_change = ((hard_val - main_val) / main_val) * 100
                else:
                    pct_change = float('inf') if hard_val != 0 else 0

                differences.append({
                    'feature': col,
                    'main': main_val,
                    'hardened': hard_val,
                    'change': hard_val - main_val,
                    'pct_change': pct_change
                })
            else:
                identical.append(col)

    # Create comparison dataframe
    diff_df = pd.DataFrame(differences)
    if not diff_df.empty:
        diff_df = diff_df.sort_values('pct_change', key=lambda x: abs(x), ascending=False)

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"Total features compared:     {len(main_df.columns)}")
    print(f"Features with differences:   {len(differences)} ({len(differences)/len(main_df.columns)*100:.1f}%)")
    print(f"Identical features:          {len(identical)} ({len(identical)/len(main_df.columns)*100:.1f}%)")
    print()

    # =========================================================================
    # TOP DIFFERENCES
    # =========================================================================
    if not diff_df.empty:
        print("=" * 80)
        print("TOP 20 DIFFERENCES (by % change)")
        print("=" * 80)
        print()

        # Format for display
        top_20 = diff_df.head(20).copy()
        top_20['pct_change'] = top_20['pct_change'].apply(lambda x: f"{x:+.1f}%" if abs(x) != float('inf') else "NEW" if x > 0 else "REMOVED")
        top_20['change'] = top_20['change'].apply(lambda x: f"{x:+.2f}")

        print(top_20[['feature', 'main', 'hardened', 'change', 'pct_change']].to_string(index=False))
        print()

        # =========================================================================
        # SECURITY-FOCUSED ANALYSIS
        # =========================================================================
        security_keywords = ['vuln', 'security', 'secret', 'container', 'iac', 'sast', 'npm', 'python', 'cve', 'cwe']
        security_features = diff_df[diff_df['feature'].str.contains('|'.join(security_keywords), case=False)]

        if not security_features.empty:
            print("=" * 80)
            print("SECURITY FEATURE CHANGES")
            print("=" * 80)
            print()

            sec_display = security_features.copy()
            sec_display['pct_change'] = sec_display['pct_change'].apply(lambda x: f"{x:+.1f}%" if abs(x) != float('inf') else "NEW" if x > 0 else "REMOVED")
            sec_display['change'] = sec_display['change'].apply(lambda x: f"{x:+.2f}")

            print(sec_display[['feature', 'main', 'hardened', 'change', 'pct_change']].to_string(index=False))
            print()

            # Security improvement score
            security_improvements = len(security_features[security_features['change'] < 0])
            security_regressions = len(security_features[security_features['change'] > 0])

            print(f"Security improvements: {security_improvements}")
            print(f"Security regressions:  {security_regressions}")
            print()

        # =========================================================================
        # CODE CHANGE ANALYSIS
        # =========================================================================
        code_keywords = ['commit', 'lines', 'files', 'author', 'branch', 'pull_request']
        code_features = diff_df[diff_df['feature'].str.contains('|'.join(code_keywords), case=False)]

        if not code_features.empty:
            print("=" * 80)
            print("CODE CHANGE FEATURE DIFFERENCES")
            print("=" * 80)
            print()

            code_display = code_features.copy()
            code_display['pct_change'] = code_display['pct_change'].apply(lambda x: f"{x:+.1f}%" if abs(x) != float('inf') else "NEW" if x > 0 else "REMOVED")
            code_display['change'] = code_display['change'].apply(lambda x: f"{x:+.2f}")

            print(code_display[['feature', 'main', 'hardened', 'change', 'pct_change']].to_string(index=False))
            print()

        # =========================================================================
        # CI/CD ANALYSIS
        # =========================================================================
        cicd_keywords = ['pipeline', 'deployment', 'dora', 'lead_time', 'mttr', 'workflow']
        cicd_features = diff_df[diff_df['feature'].str.contains('|'.join(cicd_keywords), case=False)]

        if not cicd_features.empty:
            print("=" * 80)
            print("CI/CD FEATURE DIFFERENCES")
            print("=" * 80)
            print()

            cicd_display = cicd_features.copy()
            cicd_display['pct_change'] = cicd_display['pct_change'].apply(lambda x: f"{x:+.1f}%" if abs(x) != float('inf') else "NEW" if x > 0 else "REMOVED")
            cicd_display['change'] = cicd_display['change'].apply(lambda x: f"{x:+.2f}")

            print(cicd_display[['feature', 'main', 'hardened', 'change', 'pct_change']].to_string(index=False))
            print()

    # =========================================================================
    # SAVE RESULTS
    # =========================================================================
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Save full comparison
    full_comparison_file = output_path / "branch_comparison_full.csv"
    if not diff_df.empty:
        diff_df.to_csv(full_comparison_file, index=False)
        print(f"[+] Full comparison saved to: {full_comparison_file}")

    # Save summary
    summary_file = output_path / "branch_comparison_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("BRANCH COMPARISON SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total features: {len(main_df.columns)}\n")
        f.write(f"Differences: {len(differences)} ({len(differences)/len(main_df.columns)*100:.1f}%)\n")
        f.write(f"Identical: {len(identical)} ({len(identical)/len(main_df.columns)*100:.1f}%)\n")
        f.write("\n")

        if not diff_df.empty:
            f.write("Top 10 Differences:\n")
            f.write("-" * 80 + "\n")
            for _, row in diff_df.head(10).iterrows():
                f.write(f"{row['feature']}: {row['main']} -> {row['hardened']} ({row['pct_change']:+.1f}%)\n")

    print(f"[+] Summary saved to: {summary_file}")
    print()

    print("=" * 80)
    print("[+] Branch comparison complete!")
    print("=" * 80)


def main():
    if len(sys.argv) < 3:
        print("Usage: python compare_branches.py <main_features.csv> <hardened_features.csv> [output_dir]")
        print()
        print("Example:")
        print("  python compare_branches.py output/features_main_branch.csv output/features_hardened_branch.csv")
        sys.exit(1)

    main_file = sys.argv[1]
    hardened_file = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "output"

    # Validate files exist
    if not Path(main_file).exists():
        print(f"[!] Error: Main branch file not found: {main_file}")
        sys.exit(1)

    if not Path(hardened_file).exists():
        print(f"[!] Error: Hardened branch file not found: {hardened_file}")
        sys.exit(1)

    compare_branches(main_file, hardened_file, output_dir)


if __name__ == "__main__":
    main()
