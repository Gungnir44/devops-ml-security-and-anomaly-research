#!/usr/bin/env python3
"""
Research Visualization Suite
=============================

Creates comprehensive visualizations for DevOps ML Security research.

Generates:
1. Security improvement comparison charts
2. Feature correlation heatmaps
3. Time-series trends
4. Model performance comparison
5. ROC and Precision-Recall curves
6. Feature distribution plots
7. Class separation visualizations

Usage:
    python create_visualizations.py [--data-file FILE] [--all] [--security] [--models] [--trends]
"""

import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class ResearchVisualizer:
    """Create comprehensive visualizations for research."""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path(__file__).parent / "visualizations"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.data_dir = Path(__file__).parent / "output"
        self.results_dir = Path(__file__).parent / "results"

        print("=" * 80)
        print("Research Visualization Suite")
        print("=" * 80)
        print(f"Output directory: {self.output_dir}")

    def create_security_comparison(self):
        """Create bar chart comparing security metrics (main vs hardened)."""
        print("\n[1/8] Creating security comparison chart...")

        # Load baseline comparison data
        main_file = self.data_dir / "features_main_branch.csv"
        hardened_file = self.data_dir / "features_hardened_local.csv"

        if not main_file.exists() or not hardened_file.exists():
            print("  [Skip] Baseline comparison files not found")
            return

        df_main = pd.read_csv(main_file)
        df_hardened = pd.read_csv(hardened_file)

        # Security metrics to compare
        security_metrics = {
            'Critical\nVulnerabilities': 'vuln_critical_count',
            'High\nVulnerabilities': 'vuln_high_count',
            'Medium\nVulnerabilities': 'vuln_medium_count',
            'Container\nVulnerabilities': 'container_vulnerabilities',
            'Container\nMisconfigs': 'container_misconfigurations',
            'SAST\nCode Smells': 'sast_code_smells',
            'IaC\nMisconfigs': 'iac_misconfigurations',
            'Security\nRisk Score': 'security_risk_score'
        }

        # Extract values
        main_values = []
        hardened_values = []
        labels = []

        for label, col in security_metrics.items():
            if col in df_main.columns:
                main_values.append(df_main[col].values[0])
                hardened_values.append(df_hardened[col].values[0])
                labels.append(label)

        # Create figure
        fig, ax = plt.subplots(figsize=(14, 8))

        x = np.arange(len(labels))
        width = 0.35

        bars1 = ax.bar(x - width/2, main_values, width, label='Main (Vulnerable)',
                       color='#e74c3c', alpha=0.8)
        bars2 = ax.bar(x + width/2, hardened_values, width, label='Hardened (Secured)',
                       color='#2ecc71', alpha=0.8)

        # Customize
        ax.set_xlabel('Security Metrics', fontsize=12, fontweight='bold')
        ax.set_ylabel('Count / Score', fontsize=12, fontweight='bold')
        ax.set_title('Security Improvement: Main vs Hardened Branch',
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{int(height)}',
                           ha='center', va='bottom', fontsize=9)

        plt.tight_layout()

        output_file = self.output_dir / "security_comparison.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  [OK] Saved: {output_file.name}")
        plt.close()

    def create_feature_correlation_heatmap(self, dataset_file: Path = None):
        """Create correlation heatmap for top features."""
        print("\n[2/8] Creating feature correlation heatmap...")

        if dataset_file is None:
            dataset_file = self.data_dir / "synthetic_dataset.csv"

        if not dataset_file.exists():
            print(f"  [Skip] Dataset not found: {dataset_file}")
            return

        df = pd.read_csv(dataset_file)

        # Drop metadata columns
        metadata_cols = ['date', 'branch', 'label', 'timestamp', 'synthetic', 'source']
        df_features = df.drop(metadata_cols, axis=1, errors='ignore')

        # Select top 20 features by variance (most informative)
        variances = df_features.var().sort_values(ascending=False)
        top_20_features = variances.head(20).index.tolist()

        df_top = df_features[top_20_features]

        # Compute correlation matrix
        corr_matrix = df_top.corr()

        # Create heatmap
        fig, ax = plt.subplots(figsize=(14, 12))

        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, square=True, linewidths=0.5,
                   cbar_kws={"shrink": 0.8}, ax=ax, annot_kws={'fontsize': 7})

        ax.set_title('Feature Correlation Heatmap (Top 20 Features by Variance)',
                     fontsize=14, fontweight='bold', pad=20)

        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.yticks(rotation=0, fontsize=8)
        plt.tight_layout()

        output_file = self.output_dir / "feature_correlation_heatmap.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  [OK] Saved: {output_file.name}")
        plt.close()

    def create_time_series_trends(self, dataset_file: Path = None):
        """Create time-series trend plots."""
        print("\n[3/8] Creating time-series trends...")

        if dataset_file is None:
            dataset_file = self.data_dir / "synthetic_dataset.csv"

        if not dataset_file.exists():
            print(f"  [Skip] Dataset not found: {dataset_file}")
            return

        df = pd.read_csv(dataset_file)

        if 'date' not in df.columns or 'branch' not in df.columns:
            print("  [Skip] No time-series data available")
            return

        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])

        # Key security metrics to track over time
        metrics_to_plot = [
            ('vuln_critical_count', 'Critical Vulnerabilities'),
            ('vuln_high_count', 'High Vulnerabilities'),
            ('container_vulnerabilities', 'Container Vulnerabilities'),
            ('security_risk_score', 'Security Risk Score')
        ]

        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        axes = axes.flatten()

        for idx, (col, title) in enumerate(metrics_to_plot):
            if col not in df.columns:
                continue

            ax = axes[idx]

            # Separate by branch
            df_main = df[df['branch'] == 'main'].sort_values('date')
            df_hardened = df[df['branch'] == 'hardened'].sort_values('date')

            # Plot lines
            ax.plot(df_main['date'], df_main[col], marker='o', linewidth=2,
                   markersize=6, label='Main (Vulnerable)', color='#e74c3c')
            ax.plot(df_hardened['date'], df_hardened[col], marker='s', linewidth=2,
                   markersize=6, label='Hardened (Secured)', color='#2ecc71')

            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.set_xlabel('Date', fontsize=10)
            ax.set_ylabel('Count / Score', fontsize=10)
            ax.legend(fontsize=9)
            ax.grid(True, alpha=0.3)

            # Rotate x-axis labels
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.suptitle('Security Metrics Over Time', fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()

        output_file = self.output_dir / "time_series_trends.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  [OK] Saved: {output_file.name}")
        plt.close()

    def create_feature_distributions(self, dataset_file: Path = None):
        """Create distribution plots for key features."""
        print("\n[4/8] Creating feature distribution plots...")

        if dataset_file is None:
            dataset_file = self.data_dir / "synthetic_dataset.csv"

        if not dataset_file.exists():
            print(f"  [Skip] Dataset not found: {dataset_file}")
            return

        df = pd.read_csv(dataset_file)

        # Key features to visualize
        features_to_plot = [
            'vuln_critical_count',
            'vuln_high_count',
            'container_vulnerabilities',
            'sast_code_smells',
            'security_risk_score',
            'pipeline_runs_failed'
        ]

        # Filter to features that exist
        features_to_plot = [f for f in features_to_plot if f in df.columns]

        if not features_to_plot:
            print("  [Skip] No features found to plot")
            return

        n_plots = len(features_to_plot)
        n_cols = 3
        n_rows = (n_plots + n_cols - 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
        axes = axes.flatten() if n_plots > 1 else [axes]

        for idx, feature in enumerate(features_to_plot):
            ax = axes[idx]

            # Separate by class
            if 'label' in df.columns:
                vulnerable = df[df['label'] == 1][feature]
                secured = df[df['label'] == 0][feature]

                # Create histograms
                ax.hist(vulnerable, bins=10, alpha=0.6, label='Vulnerable',
                       color='#e74c3c', edgecolor='black')
                ax.hist(secured, bins=10, alpha=0.6, label='Secured',
                       color='#2ecc71', edgecolor='black')

                ax.set_title(feature.replace('_', ' ').title(), fontsize=10, fontweight='bold')
                ax.set_xlabel('Value', fontsize=9)
                ax.set_ylabel('Frequency', fontsize=9)
                ax.legend(fontsize=8)
                ax.grid(axis='y', alpha=0.3)

        # Hide unused subplots
        for idx in range(len(features_to_plot), len(axes)):
            axes[idx].axis('off')

        plt.suptitle('Feature Distributions: Vulnerable vs Secured',
                     fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()

        output_file = self.output_dir / "feature_distributions.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  [OK] Saved: {output_file.name}")
        plt.close()

    def create_class_separation_scatter(self, dataset_file: Path = None):
        """Create scatter plot showing class separation."""
        print("\n[5/8] Creating class separation visualization...")

        if dataset_file is None:
            dataset_file = self.data_dir / "synthetic_dataset.csv"

        if not dataset_file.exists():
            print(f"  [Skip] Dataset not found: {dataset_file}")
            return

        df = pd.read_csv(dataset_file)

        if 'label' not in df.columns:
            print("  [Skip] No labels found in dataset")
            return

        # Drop metadata
        metadata_cols = ['date', 'branch', 'label', 'timestamp', 'synthetic', 'source']
        df_features = df.drop(metadata_cols, axis=1, errors='ignore')

        # Use PCA for dimensionality reduction to 2D
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_features)

        # Apply PCA
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)

        # Create scatter plot
        fig, ax = plt.subplots(figsize=(12, 8))

        vulnerable = df['label'] == 1
        secured = df['label'] == 0

        ax.scatter(X_pca[vulnerable, 0], X_pca[vulnerable, 1],
                  c='#e74c3c', label='Vulnerable (Main)',
                  s=100, alpha=0.6, edgecolors='black', linewidth=1)
        ax.scatter(X_pca[secured, 0], X_pca[secured, 1],
                  c='#2ecc71', label='Secured (Hardened)',
                  s=100, alpha=0.6, edgecolors='black', linewidth=1)

        ax.set_xlabel(f'First Principal Component ({pca.explained_variance_ratio_[0]:.1%} variance)',
                     fontsize=11)
        ax.set_ylabel(f'Second Principal Component ({pca.explained_variance_ratio_[1]:.1%} variance)',
                     fontsize=11)
        ax.set_title('Class Separation Visualization (PCA)', fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)

        # Add annotation
        total_variance = sum(pca.explained_variance_ratio_[:2])
        ax.text(0.02, 0.98, f'Total variance explained: {total_variance:.1%}',
               transform=ax.transAxes, fontsize=10,
               verticalalignment='top', bbox=dict(boxstyle='round',
               facecolor='wheat', alpha=0.5))

        plt.tight_layout()

        output_file = self.output_dir / "class_separation_pca.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  [OK] Saved: {output_file.name}")
        plt.close()

    def create_model_performance_comparison(self):
        """Create model performance comparison chart."""
        print("\n[6/8] Creating model performance comparison...")

        comparison_file = self.results_dir / "model_comparison.csv"

        if not comparison_file.exists():
            print("  [Skip] Model comparison file not found")
            print("        Train multiple models first with:")
            print("        python train_baseline_models.py --data-file output/synthetic_dataset.csv")
            return

        df = pd.read_csv(comparison_file)

        # Create grouped bar chart
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']

        # Filter to numeric metrics
        metrics = [m for m in metrics if m in df.columns]

        if not metrics:
            print("  [Skip] No metrics found in comparison file")
            return

        fig, ax = plt.subplots(figsize=(14, 8))

        x = np.arange(len(df))
        width = 0.2

        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']

        for idx, metric in enumerate(metrics):
            offset = width * (idx - len(metrics)/2 + 0.5)
            bars = ax.bar(x + offset, df[metric], width,
                         label=metric, color=colors[idx], alpha=0.8)

            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=8)

        ax.set_xlabel('Models', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score', fontsize=12, fontweight='bold')
        ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(df['Model'])
        ax.legend(fontsize=10)
        ax.set_ylim([0, 1.1])
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        output_file = self.output_dir / "model_performance_comparison.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  [OK] Saved: {output_file.name}")
        plt.close()

    def create_top_features_chart(self):
        """Create horizontal bar chart of top features."""
        print("\n[7/8] Creating top features chart...")

        # Find any feature importance file
        importance_files = list(self.results_dir.glob("feature_importance_*.csv"))

        if not importance_files:
            print("  [Skip] No feature importance files found")
            return

        # Use the first one (or combine multiple)
        df_importance = pd.read_csv(importance_files[0])

        # Get top 15 features
        top_15 = df_importance.head(15)

        fig, ax = plt.subplots(figsize=(12, 10))

        # Create horizontal bar chart (reversed so #1 is on top)
        y_pos = np.arange(len(top_15))
        ax.barh(y_pos, top_15['importance'], color='#3498db', alpha=0.8, edgecolor='black')

        ax.set_yticks(y_pos)
        ax.set_yticklabels(top_15['feature'].apply(lambda x: x.replace('_', ' ').title()))
        ax.invert_yaxis()  # Top feature at the top
        ax.set_xlabel('Importance Score', fontsize=12, fontweight='bold')
        ax.set_title('Top 15 Most Important Features for Security Classification',
                     fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)

        # Add value labels
        for i, (idx, row) in enumerate(top_15.iterrows()):
            ax.text(row['importance'], i, f" {row['importance']:.4f}",
                   va='center', fontsize=9)

        plt.tight_layout()

        output_file = self.output_dir / "top_features_horizontal.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  [OK] Saved: {output_file.name}")
        plt.close()

    def create_summary_dashboard(self):
        """Create a single summary dashboard with multiple panels."""
        print("\n[8/8] Creating summary dashboard...")

        # Load data
        main_file = self.data_dir / "features_main_branch.csv"
        hardened_file = self.data_dir / "features_hardened_local.csv"

        if not main_file.exists() or not hardened_file.exists():
            print("  [Skip] Baseline files not found")
            return

        df_main = pd.read_csv(main_file)
        df_hardened = pd.read_csv(hardened_file)

        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # Panel 1: Security metrics comparison
        ax1 = fig.add_subplot(gs[0, :2])
        security_cols = ['vuln_critical_count', 'vuln_high_count', 'vuln_medium_count',
                        'container_vulnerabilities', 'sast_code_smells']
        security_cols = [c for c in security_cols if c in df_main.columns]

        x = np.arange(len(security_cols))
        width = 0.35
        main_vals = [df_main[c].values[0] for c in security_cols]
        hard_vals = [df_hardened[c].values[0] for c in security_cols]

        ax1.bar(x - width/2, main_vals, width, label='Main', color='#e74c3c', alpha=0.8)
        ax1.bar(x + width/2, hard_vals, width, label='Hardened', color='#2ecc71', alpha=0.8)
        ax1.set_xticks(x)
        ax1.set_xticklabels([c.replace('_', '\n') for c in security_cols], fontsize=8)
        ax1.set_ylabel('Count')
        ax1.set_title('Security Metrics Comparison', fontweight='bold')
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)

        # Panel 2: Improvement percentages
        ax2 = fig.add_subplot(gs[0, 2])
        improvements = []
        labels = []
        for col in security_cols:
            main_val = df_main[col].values[0]
            hard_val = df_hardened[col].values[0]
            if main_val > 0:
                improvement = ((main_val - hard_val) / main_val) * 100
                improvements.append(improvement)
                labels.append(col.split('_')[0])

        colors_pie = ['#2ecc71' if imp > 50 else '#f39c12' for imp in improvements]
        ax2.pie(improvements, labels=labels, autopct='%1.0f%%', colors=colors_pie, startangle=90)
        ax2.set_title('Improvement %', fontweight='bold')

        # Panel 3: Sample statistics
        ax3 = fig.add_subplot(gs[1, :])
        ax3.axis('off')

        stats_text = f"""
        RESEARCH DATASET SUMMARY

        Main Branch (Vulnerable):
        - Critical Vulnerabilities: {df_main['vuln_critical_count'].values[0] if 'vuln_critical_count' in df_main.columns else 'N/A'}
        - High Vulnerabilities: {df_main['vuln_high_count'].values[0] if 'vuln_high_count' in df_main.columns else 'N/A'}
        - Container Issues: {df_main['container_vulnerabilities'].values[0] if 'container_vulnerabilities' in df_main.columns else 'N/A'}
        - Security Risk Score: {df_main['security_risk_score'].values[0] if 'security_risk_score' in df_main.columns else 'N/A'}

        Hardened Branch (Secured):
        - Critical Vulnerabilities: {df_hardened['vuln_critical_count'].values[0] if 'vuln_critical_count' in df_hardened.columns else 'N/A'}
        - High Vulnerabilities: {df_hardened['vuln_high_count'].values[0] if 'vuln_high_count' in df_hardened.columns else 'N/A'}
        - Container Issues: {df_hardened['container_vulnerabilities'].values[0] if 'container_vulnerabilities' in df_hardened.columns else 'N/A'}
        - Security Risk Score: {df_hardened['security_risk_score'].values[0] if 'security_risk_score' in df_hardened.columns else 'N/A'}

        Overall Improvement: {len([i for i in improvements if i >= 100])} metrics at 100% improvement
        """

        ax3.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                verticalalignment='center', bbox=dict(boxstyle='round',
                facecolor='wheat', alpha=0.3))

        # Panel 4: Feature count
        ax4 = fig.add_subplot(gs[2, 0])
        categories = ['Security\n(21)', 'CI/CD\n(35)', 'Code\n(25)', 'Containers\n(24)',
                     'Deploy\n(22)', 'Infra\n(40)', 'Access\n(28)', 'Network\n(15)']
        counts = [21, 35, 25, 24, 22, 40, 28, 15]
        colors_bar = sns.color_palette("husl", len(categories))

        ax4.bar(range(len(categories)), counts, color=colors_bar, alpha=0.8, edgecolor='black')
        ax4.set_xticks(range(len(categories)))
        ax4.set_xticklabels(categories, fontsize=8)
        ax4.set_ylabel('Feature Count')
        ax4.set_title('Features by Category (208 total)', fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)

        # Panel 5: Research timeline
        ax5 = fig.add_subplot(gs[2, 1:])
        ax5.axis('off')

        timeline_text = """
        RESEARCH TIMELINE

        Week 1: Baseline Collection     [DONE]
        Week 2: Weekly Data Collection  [IN PROGRESS]
        Week 3: Model Training          [PLANNED]
        Week 4: Final Experiments       [PLANNED]

        Current Status:
        - Infrastructure: READY
        - Synthetic Data: 30 samples
        - Models Trained: Random Forest (100% accuracy)
        - Visualizations: 8 types generated

        Next Steps:
        1. Continue weekly data collection
        2. Train on real data (Week 2+)
        3. Compare model performance
        4. Write thesis chapters
        """

        ax5.text(0.1, 0.5, timeline_text, fontsize=10, family='monospace',
                verticalalignment='center', bbox=dict(boxstyle='round',
                facecolor='lightblue', alpha=0.3))

        plt.suptitle('DevOps ML Security Research - Summary Dashboard',
                     fontsize=16, fontweight='bold', y=0.98)

        output_file = self.output_dir / "summary_dashboard.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  [OK] Saved: {output_file.name}")
        plt.close()

    def generate_all(self, dataset_file: Path = None):
        """Generate all visualizations."""
        print("\nGenerating all visualizations...")

        self.create_security_comparison()
        self.create_feature_correlation_heatmap(dataset_file)
        self.create_time_series_trends(dataset_file)
        self.create_feature_distributions(dataset_file)
        self.create_class_separation_scatter(dataset_file)
        self.create_model_performance_comparison()
        self.create_top_features_chart()
        self.create_summary_dashboard()

        print("\n" + "=" * 80)
        print("Visualization Generation Complete!")
        print("=" * 80)
        print(f"\nAll visualizations saved to: {self.output_dir}")
        print(f"\nGenerated files:")

        for viz_file in sorted(self.output_dir.glob("*.png")):
            size_kb = viz_file.stat().st_size / 1024
            print(f"  - {viz_file.name} ({size_kb:.1f} KB)")


def main():
    parser = argparse.ArgumentParser(description="Create research visualizations")
    parser.add_argument(
        '--data-file',
        type=str,
        help='Dataset file to visualize (default: synthetic_dataset.csv)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Generate all visualizations (default if no specific type selected)'
    )
    parser.add_argument(
        '--security',
        action='store_true',
        help='Generate only security comparison visualizations'
    )
    parser.add_argument(
        '--models',
        action='store_true',
        help='Generate only model performance visualizations'
    )
    parser.add_argument(
        '--trends',
        action='store_true',
        help='Generate only time-series trend visualizations'
    )

    args = parser.parse_args()

    # Create visualizer
    visualizer = ResearchVisualizer()

    # Determine dataset file
    dataset_file = None
    if args.data_file:
        dataset_file = Path(args.data_file)

    # Generate visualizations
    if args.all or not (args.security or args.models or args.trends):
        # Generate all if no specific type selected or --all specified
        visualizer.generate_all(dataset_file)
    else:
        if args.security:
            visualizer.create_security_comparison()
            visualizer.create_feature_distributions(dataset_file)

        if args.models:
            visualizer.create_model_performance_comparison()
            visualizer.create_top_features_chart()

        if args.trends:
            visualizer.create_time_series_trends(dataset_file)
            visualizer.create_feature_correlation_heatmap(dataset_file)

        print(f"\n[OK] Selected visualizations saved to: {visualizer.output_dir}")


if __name__ == "__main__":
    main()
