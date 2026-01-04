#!/usr/bin/env python3
"""
Synthetic Data Generator for ML Pipeline Testing
=================================================

Generates realistic synthetic samples based on baseline data.

Usage:
    python generate_synthetic_data.py [--samples 15] [--variation realistic]

Options:
    --samples N       Number of samples per class (default: 15)
    --variation TYPE  Type of variation: realistic, conservative, aggressive (default: realistic)
"""

import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta


class SyntheticDataGenerator:
    """Generate synthetic security data samples."""

    def __init__(self, n_samples_per_class=15, variation_type='realistic'):
        self.n_samples = n_samples_per_class
        self.variation_type = variation_type
        self.output_dir = Path(__file__).parent / "output"
        self.output_dir.mkdir(exist_ok=True)

        # Set random seed for reproducibility
        np.random.seed(42)

    def load_baseline_data(self):
        """Load baseline comparison data."""
        print("=" * 80)
        print("Loading Baseline Data")
        print("=" * 80)

        main_file = self.output_dir / "features_main_branch.csv"
        hardened_file = self.output_dir / "features_hardened_local.csv"

        if not main_file.exists() or not hardened_file.exists():
            print(f"[!] Baseline files not found:")
            print(f"    {main_file}")
            print(f"    {hardened_file}")
            return None, None

        df_main = pd.read_csv(main_file)
        df_hardened = pd.read_csv(hardened_file)

        print(f"Main branch: {len(df_main)} samples, {len(df_main.columns)} features")
        print(f"Hardened branch: {len(df_hardened)} samples, {len(df_hardened.columns)} features")

        return df_main, df_hardened

    def generate_variants(self, df_base, label, class_name):
        """Generate synthetic variants of a baseline sample."""
        print(f"\nGenerating {self.n_samples} {class_name} samples...")

        variants = []
        base_sample = df_base.iloc[0]  # Get the single baseline row

        for i in range(self.n_samples):
            variant = pd.DataFrame([base_sample.copy()])

            # Apply variation based on feature types
            for col in variant.columns:
                if variant[col].dtype in ['int64', 'float64']:
                    variant[col] = self._apply_variation(
                        variant[col].values[0],
                        col,
                        label
                    )

            variants.append(variant)

        df_variants = pd.concat(variants, ignore_index=True)
        df_variants['label'] = label
        df_variants['synthetic'] = True
        df_variants['source'] = class_name

        print(f"  Generated {len(df_variants)} {class_name} samples")

        return df_variants

    def _apply_variation(self, value, column_name, label):
        """Apply realistic variation to a feature value."""

        # Zero values stay zero (mostly)
        if value == 0:
            # Secured branch: Stay at 0 (99% of time)
            if label == 0:
                return 0 if np.random.random() < 0.99 else np.random.randint(0, 2)
            # Vulnerable branch: Sometimes introduce issues
            else:
                return 0 if np.random.random() < 0.7 else np.random.randint(0, 3)

        # Feature-specific variations
        if self.variation_type == 'realistic':
            variation_factor = self._get_realistic_variation(column_name, label)
        elif self.variation_type == 'conservative':
            variation_factor = 0.05  # 5% variation
        elif self.variation_type == 'aggressive':
            variation_factor = 0.25  # 25% variation
        else:
            variation_factor = 0.1  # 10% variation

        # Apply variation
        if 'count' in column_name or 'total' in column_name:
            # Discrete counts: Use Poisson distribution
            lambda_param = max(0.1, value)
            new_value = np.random.poisson(lambda_param)
        elif 'percent' in column_name or 'rate' in column_name:
            # Percentages: Keep in range [0, 100]
            noise = np.random.normal(0, variation_factor * value)
            new_value = max(0, min(100, value + noise))
        elif 'duration' in column_name or 'time' in column_name or 'seconds' in column_name:
            # Timing metrics: Log-normal distribution (realistic for timings)
            log_value = np.log(max(0.1, value))
            log_noise = np.random.normal(0, variation_factor)
            new_value = np.exp(log_value + log_noise)
        else:
            # Generic numeric: Gaussian noise
            noise = np.random.normal(0, variation_factor * abs(value))
            new_value = value + noise

        # Ensure non-negative for counts
        if 'count' in column_name or 'total' in column_name:
            new_value = max(0, int(new_value))

        return new_value

    def _get_realistic_variation(self, column_name, label):
        """Get realistic variation factor based on feature type."""

        # Security metrics: More variation for vulnerable, stable for secured
        if any(keyword in column_name for keyword in ['vuln', 'security', 'secret']):
            return 0.20 if label == 1 else 0.05  # 20% vs 5%

        # CI/CD timing: Natural variation
        elif any(keyword in column_name for keyword in ['duration', 'time', 'seconds']):
            return 0.15  # 15% variation

        # Container/Pod metrics: Some variation
        elif any(keyword in column_name for keyword in ['container', 'pod', 'node']):
            return 0.10  # 10% variation

        # Network/Resource metrics: Higher variation
        elif any(keyword in column_name for keyword in ['network', 'cpu', 'memory', 'disk']):
            return 0.20  # 20% variation

        # Code metrics: Low variation (code doesn't change much)
        elif any(keyword in column_name for keyword in ['commit', 'lines', 'files']):
            return 0.05  # 5% variation

        # Default
        else:
            return 0.10  # 10% variation

    def add_time_series_metadata(self, df):
        """Add time-series metadata to make it look like weekly collection."""
        print("\nAdding time-series metadata...")

        # Create timestamps spanning 2 weeks
        base_date = datetime(2025, 11, 22)  # Start 2 weeks before current data
        dates = []
        branches = []

        # Distribute samples across dates
        samples_per_class = len(df[df['label'] == 1])

        for i in range(len(df)):
            # Alternate between main and hardened
            label = df.iloc[i]['label']
            branch = 'main' if label == 1 else 'hardened'
            branches.append(branch)

            # Assign dates (spread across 2 weeks)
            day_offset = (i % samples_per_class) % 14
            date = base_date + timedelta(days=day_offset)
            dates.append(date.strftime('%Y-%m-%d'))

        df['date'] = dates
        df['branch'] = branches
        df['timestamp'] = pd.to_datetime(dates)

        print(f"  Date range: {min(dates)} to {max(dates)}")

        return df

    def validate_dataset(self, df):
        """Validate the generated dataset."""
        print("\n" + "=" * 80)
        print("Dataset Validation")
        print("=" * 80)

        print(f"\nTotal samples: {len(df)}")
        print(f"Features: {len(df.columns) - 4}")  # Exclude label, synthetic, source, timestamp

        print(f"\nClass distribution:")
        print(f"  Vulnerable (main): {sum(df['label'] == 1)}")
        print(f"  Secured (hardened): {sum(df['label'] == 0)}")

        print(f"\nDate range: {df['date'].min()} to {df['date'].max()}")
        print(f"Unique dates: {df['date'].nunique()}")

        # Check for any invalid values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        invalid_counts = {
            'negative': sum((df[numeric_cols] < 0).any()),
            'infinite': sum(np.isinf(df[numeric_cols]).any()),
            'nan': sum(df[numeric_cols].isna().any())
        }

        if any(invalid_counts.values()):
            print(f"\n[!] Warning: Found invalid values:")
            for issue, count in invalid_counts.items():
                if count > 0:
                    print(f"    {issue}: {count} columns")
        else:
            print(f"\n[OK] All values valid (no negatives, infinites, or NaNs)")

        # Sample statistics
        print(f"\nSample feature statistics:")

        # Security metrics comparison
        security_cols = [col for col in df.columns if 'vuln' in col or 'security' in col][:5]
        if security_cols:
            print(f"\nTop security features (main vs hardened):")
            for col in security_cols:
                main_mean = df[df['label'] == 1][col].mean()
                hardened_mean = df[df['label'] == 0][col].mean()
                print(f"  {col:40s} Main: {main_mean:6.2f}  Hardened: {hardened_mean:6.2f}")

        return True

    def save_dataset(self, df):
        """Save the synthetic dataset."""
        print("\n" + "=" * 80)
        print("Saving Dataset")
        print("=" * 80)

        # Save full dataset
        output_file = self.output_dir / "synthetic_dataset.csv"
        df.to_csv(output_file, index=False)
        print(f"[OK] Saved: {output_file.name}")
        print(f"     Size: {output_file.stat().st_size / 1024:.1f} KB")

        # Save separate class files (for compatibility)
        df_main = df[df['label'] == 1].drop(['label', 'synthetic', 'source'], axis=1)
        df_hardened = df[df['label'] == 0].drop(['label', 'synthetic', 'source'], axis=1)

        main_file = self.output_dir / "synthetic_main_samples.csv"
        hardened_file = self.output_dir / "synthetic_hardened_samples.csv"

        df_main.to_csv(main_file, index=False)
        df_hardened.to_csv(hardened_file, index=False)

        print(f"[OK] Saved: {main_file.name} ({len(df_main)} samples)")
        print(f"[OK] Saved: {hardened_file.name} ({len(df_hardened)} samples)")

        # Create README
        readme_file = self.output_dir / "SYNTHETIC_DATA_README.md"
        with open(readme_file, 'w') as f:
            f.write("# Synthetic Dataset\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Purpose:** ML pipeline testing and validation\n\n")
            f.write(f"## Statistics\n\n")
            f.write(f"- Total samples: {len(df)}\n")
            f.write(f"- Vulnerable (main): {sum(df['label'] == 1)}\n")
            f.write(f"- Secured (hardened): {sum(df['label'] == 0)}\n")
            f.write(f"- Features: {len(df.columns) - 4}\n")
            f.write(f"- Date range: {df['date'].min()} to {df['date'].max()}\n\n")
            f.write(f"## Variation Type\n\n")
            f.write(f"- Type: {self.variation_type}\n")
            f.write(f"- Samples per class: {self.n_samples}\n\n")
            f.write(f"## Important Note\n\n")
            f.write(f"This is **synthetic data** generated for pipeline testing.\n\n")
            f.write(f"- Use for: ML pipeline validation, code testing, initial experiments\n")
            f.write(f"- Do NOT use for: Final thesis results, published papers\n")
            f.write(f"- Real data: Collect via weekly automated collection over 4 weeks\n\n")
            f.write(f"## Files\n\n")
            f.write(f"- `synthetic_dataset.csv` - Combined dataset with labels\n")
            f.write(f"- `synthetic_main_samples.csv` - Vulnerable samples only\n")
            f.write(f"- `synthetic_hardened_samples.csv` - Secured samples only\n\n")
            f.write(f"## Train Models\n\n")
            f.write(f"```bash\n")
            f.write(f"python train_baseline_models.py --data-file output/synthetic_dataset.csv\n")
            f.write(f"```\n")

        print(f"[OK] Saved: {readme_file.name}")

        return output_file

    def generate(self):
        """Run the complete synthetic data generation pipeline."""
        print("=" * 80)
        print("Synthetic Data Generator")
        print("=" * 80)
        print(f"Samples per class: {self.n_samples}")
        print(f"Variation type: {self.variation_type}")

        # Load baseline
        df_main, df_hardened = self.load_baseline_data()

        if df_main is None or df_hardened is None:
            return None

        # Generate variants
        df_main_variants = self.generate_variants(df_main, label=1, class_name='vulnerable')
        df_hardened_variants = self.generate_variants(df_hardened, label=0, class_name='secured')

        # Combine
        df_combined = pd.concat([df_main_variants, df_hardened_variants], ignore_index=True)

        # Add time-series metadata
        df_combined = self.add_time_series_metadata(df_combined)

        # Shuffle
        df_combined = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)

        # Validate
        self.validate_dataset(df_combined)

        # Save
        output_file = self.save_dataset(df_combined)

        print("\n" + "=" * 80)
        print("Synthetic Data Generation Complete!")
        print("=" * 80)
        print(f"\n[OK] Dataset ready: {output_file}")
        print(f"\nNext step:")
        print(f"  python train_baseline_models.py --data-file {output_file}")

        return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic security data for ML pipeline testing"
    )
    parser.add_argument(
        '--samples',
        type=int,
        default=15,
        help='Number of samples per class (default: 15)'
    )
    parser.add_argument(
        '--variation',
        type=str,
        default='realistic',
        choices=['realistic', 'conservative', 'aggressive'],
        help='Type of variation to apply (default: realistic)'
    )

    args = parser.parse_args()

    # Generate data
    generator = SyntheticDataGenerator(
        n_samples_per_class=args.samples,
        variation_type=args.variation
    )

    output_file = generator.generate()

    if output_file:
        print("\n[OK] Ready to train models!")
    else:
        print("\n[!] Generation failed - check baseline data files")


if __name__ == "__main__":
    main()
