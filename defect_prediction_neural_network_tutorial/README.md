# Software Defect Prediction Tutorial

Learn to predict software defects using NASA metrics data. You will try three classical methods, pick the best input feature, then train a neural network that achieves the highest accuracy.

This tutorial is based on [defect_prediction.ipynb](defect_prediction.ipynb) and the NASA PROMISE dataset ([JM1](http://promise.site.uottawa.ca/SERepository/datasets/jm1.arff) / [CM1](http://promise.site.uottawa.ca/SERepository/datasets/cm1.arff)).

## What you will build

| Step | Method | Goal |
|------|--------|------|
| 1 | Logistic regression | Notebook baseline (~73% AUC) |
| 2 | Gradient boosted trees | Stronger tabular baseline |
| 3 | Feature comparison | Swap the 6th feature (`i` → `total_Opnd`) |
| 4 | Neural network | Best result (~79% AUC on CM1) |

## Setup

Requires Python 3.10+.

```bash
cd defect_prediction_neural_network_tutorial

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/download_data.py  # skip if data/raw/jm1.csv already exists
```

Downloading pytorch libraries for neural network training takes a few minutes:
2026-06-08 16:52:32.862 [info]    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 88.0/88.0 MB 477.0 kB/s  0:03:04

All scripts resolve paths from the project root (`src/paths.py`), so they work even if you run them from another directory:

```bash
python /path/to/accuracy/scripts/01_logistic_regression.py
```

## Tutorial steps

Run these in order. Each step prints its results to the terminal.

### Step 1 — Logistic regression

Uses six features from the notebook: `loc`, `d`, `locCodeAndComment`, `v(g)`, `uniq_Opnd`, `i`.

```bash
python scripts/01_logistic_regression.py
```

**Expected:** AUC-ROC around **0.727** on an 80/20 split of JM1.

### Step 2 — Gradient boosted trees

Same features and split as Step 1, using scikit-learn's gradient boosted trees.

```bash
python scripts/02_gradient_boosted_trees.py
```

**Expected:** AUC-ROC similar to or slightly above Step 1.

### Step 3 — Pick the best 6th feature

Five features stay fixed. This step tries every other NASA metric as the 6th input and ranks them.

```bash
python scripts/03_compare_features.py
```

**Expected output (top of ranking):**

Testing 16 options for the 6th feature slot

Rank  Feature               AUC-ROC
------------------------------------
1     total_Opnd             0.7319 <-- best
2     lOComment              0.7308
3     branchCount            0.7308
4     ev(g)                  0.7305
5     lOBlank                0.7305
6     iv(g)                  0.7300
7     i                      0.7296
8     b                      0.7275
9     e                      0.7273
10    t                      0.7273
11    v                      0.7273
12    n                      0.7269
13    lOCode                 0.7260
14    total_Op               0.7221
15    uniq_Op                0.7198
16    l                      0.7117

The default 6th feature `i` is good, but **`total_Opnd`** scores highest. Update the config:

```yaml
# config/default.yaml
variant_feature: total_Opnd
```

### Step 4 — Train the neural network

Trains on all of **JM1** and evaluates on **CM1** (a different NASA project). This is harder than Steps 1–3 but reflects real cross-project prediction.

```bash
python scripts/04_train_neural_network.py
```
Note: You can train a 92M param model in about 2 minutes on an M4 Pro Max Chip, and even if it is slower, watching the process is both fun and educational! No external GPUs needed, trains locally.

**Expected:** ~92M parameter model, 20 epochs. Best validation AUC around **0.79** with `total_Opnd`:

```
Epoch 20/20 | val_auc=0.7887
```

With the default feature `i`, expect val AUC around **0.77**.

## Project layout

```
accuracy/
├── README.md
├── defect_prediction.ipynb       # original notebook exercise
├── requirements.txt
├── config/default.yaml           # edit variant_feature after Step 3
├── data/raw/
│   ├── jm1.csv                   # training project
│   └── cm1.csv                   # evaluation project
└── scripts/
    ├── download_data.py
    ├── 01_logistic_regression.py
    ├── 02_gradient_boosted_trees.py
    ├── 03_compare_features.py
    └── 04_train_neural_network.py
```

## Results summary

Typical AUC-ROC scores from this tutorial:

| Step | Method | Split | ~AUC |
|------|--------|-------|------|
| 1 | Logistic regression | JM1 holdout | 0.727 |
| 2 | Gradient boosted trees | JM1 holdout | 0.73+ |
| 3 | Best feature (`total_Opnd`) | JM1 holdout | 0.732 |
| 4 | Neural network (`i`) | JM1 → CM1 | 0.767 |
| 4 | Neural network (`total_Opnd`) | JM1 → CM1 | **0.789** |

Metrics are saved under `checkpoints/` after each step.

## The six features

From the notebook, five metrics are fixed and one is swappable:

| # | Feature | Description |
|---|---------|-------------|
| 1 | `loc` | McCabe line count |
| 2 | `d` | Halstead difficulty |
| 3 | `locCodeAndComment` | Lines of code and comments |
| 4 | `v(g)` | Cyclomatic complexity |
| 5 | `uniq_Opnd` | Unique operands |
| 6 | *swappable* | Default `i`; tutorial picks `total_Opnd` |

All 21 available metrics are listed in `src/data/nasa_preprocessing.py`.

## Going further

- Try different feature combinations in `config/default.yaml`
- Lower `training.learning_rate` if validation AUC bounces between epochs
- The neural network already uses Adam — tuning learning rate and epochs is the next lever
- If prompted by the instructor, play around with subbing out other features rather than just the 6th to see if you can further improve predictive accuracy!

## License

NASA PROMISE data: see [PROMISE repository](http://promise.site.uottawa.ca/SERepository) attribution guidelines.
Coveros AI for Testers training material all rights reserved
Collaborated with Professional AI Agents LLC
