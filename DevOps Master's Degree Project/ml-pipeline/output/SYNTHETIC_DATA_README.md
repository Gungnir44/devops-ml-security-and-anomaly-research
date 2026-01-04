# Synthetic Dataset

**Generated:** 2025-12-06 23:59:32

**Purpose:** ML pipeline testing and validation

## Statistics

- Total samples: 30
- Vulnerable (main): 15
- Secured (hardened): 15
- Features: 210
- Date range: 2025-11-22 to 2025-12-05

## Variation Type

- Type: realistic
- Samples per class: 15

## Important Note

This is **synthetic data** generated for pipeline testing.

- Use for: ML pipeline validation, code testing, initial experiments
- Do NOT use for: Final thesis results, published papers
- Real data: Collect via weekly automated collection over 4 weeks

## Files

- `synthetic_dataset.csv` - Combined dataset with labels
- `synthetic_main_samples.csv` - Vulnerable samples only
- `synthetic_hardened_samples.csv` - Secured samples only

## Train Models

```bash
python train_baseline_models.py --data-file output/synthetic_dataset.csv
```
