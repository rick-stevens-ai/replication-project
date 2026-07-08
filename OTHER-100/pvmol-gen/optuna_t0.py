"""Optuna hyperparameter optimization for SMILES-X classifier on T0 data.

Uses 3-fold CV during search (speed) with fold-level pruning,
then retrains the best configuration with full 5-fold CV.

Usage:
    python optuna_t0.py                    # 50 trials (default)
    python optuna_t0.py --n-trials 100     # more trials
    python optuna_t0.py --resume           # resume a previous study
    python optuna_t0.py --eval-only        # just retrain best from saved study
"""

import argparse
import json
import logging
import os
import sys

import optuna
from optuna.pruners import MedianPruner
from optuna.samplers import TPESampler

from smilesx import SmilesXClassifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/optuna_t0.log"),
    ],
)
logger = logging.getLogger(__name__)

# Suppress noisy per-epoch logs during search
logging.getLogger("smilesx.train").setLevel(logging.WARNING)

DATA_PATH = "data/T0.csv"
STUDY_DB = "sqlite:///models/optuna_t0/study.db"
STUDY_NAME = "smilesx_t0"
SEARCH_OUTDIR = "models/optuna_t0/trials"
BEST_OUTDIR = "models/optuna_t0/best"

# Search uses 3-fold CV with fewer epochs for speed
SEARCH_FOLDS = 3
SEARCH_EPOCHS = 60
SEARCH_PATIENCE = 15

# Final evaluation uses full settings
FINAL_FOLDS = 5
FINAL_EPOCHS = 100
FINAL_PATIENCE = 25


def objective(trial: optuna.Trial) -> float:
    """Optuna objective: mean F1 across k-fold CV."""

    # --- Architecture ---
    embed_dim = trial.suggest_categorical("embed_dim", [32, 64, 128, 256, 512])
    lstm_units = trial.suggest_categorical("lstm_units", [32, 64, 128, 256])
    tdense_units = trial.suggest_categorical("tdense_units", [32, 64, 128, 256])
    dense_depth = trial.suggest_int("dense_depth", 0, 2)
    dropout = trial.suggest_float("dropout", 0.1, 0.5, step=0.05)

    # --- Training ---
    lr = trial.suggest_float("lr", 1e-4, 1e-2, log=True)
    weight_decay = trial.suggest_float("weight_decay", 1e-6, 1e-3, log=True)
    batch_size = trial.suggest_categorical("batch_size", [8, 16, 32, 64])

    # --- Data choices ---
    use_extra = trial.suggest_categorical("use_extra_features", [True, False])
    augment = trial.suggest_categorical("augment", [True, False])

    extra_cols = ["ha_num", "o_num"] if use_extra else []

    trial_dir = os.path.join(SEARCH_OUTDIR, f"trial_{trial.number}")

    clf = SmilesXClassifier(
        data_path=DATA_PATH,
        smiles_col="smiles",
        label_col="bin_class",
        extra_feature_cols=extra_cols,
        embed_dim=embed_dim,
        lstm_units=lstm_units,
        tdense_units=tdense_units,
        dense_depth=dense_depth,
        dropout=dropout,
        lr=lr,
        weight_decay=weight_decay,
        batch_size=batch_size,
        n_epochs=SEARCH_EPOCHS,
        patience=SEARCH_PATIENCE,
        class_weight=True,
        outdir=trial_dir,
        seed=42,
    )

    # Run CV fold-by-fold for pruning support
    result = clf.cross_validate(n_folds=SEARCH_FOLDS, augment=augment)

    # Report per-fold F1 for pruning
    for i, fold in enumerate(result.folds):
        trial.report(fold.f1, step=i)
        if trial.should_prune():
            raise optuna.TrialPruned()

    mean_f1 = result.mean_f1
    logger.info(
        f"Trial {trial.number}: F1={mean_f1:.4f} ± {result.std_f1:.4f}  "
        f"AUC={result.mean_auc:.4f}  "
        f"[embed={embed_dim} lstm={lstm_units} td={tdense_units} "
        f"depth={dense_depth} drop={dropout:.2f} lr={lr:.1e} "
        f"bs={batch_size} extra={use_extra} aug={augment}]"
    )
    return mean_f1


def run_search(n_trials: int, resume: bool):
    """Run or resume the Optuna study."""
    os.makedirs(os.path.dirname(STUDY_DB.replace("sqlite:///", "")), exist_ok=True)
    os.makedirs(SEARCH_OUTDIR, exist_ok=True)

    sampler = TPESampler(seed=42, multivariate=True)
    pruner = MedianPruner(n_startup_trials=10, n_warmup_steps=1)

    study = optuna.create_study(
        study_name=STUDY_NAME,
        storage=STUDY_DB,
        direction="maximize",
        sampler=sampler,
        pruner=pruner,
        load_if_exists=resume,
    )

    completed = len([t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE])
    remaining = max(0, n_trials - completed)
    if remaining == 0:
        logger.info(f"Study already has {completed} completed trials. Use --n-trials to add more.")
    else:
        logger.info(f"Running {remaining} trials ({completed} already completed)")
        study.optimize(objective, n_trials=remaining, show_progress_bar=True)

    print_study_summary(study)
    return study


def print_study_summary(study: optuna.Study):
    """Print top results from the study."""
    print("\n" + "=" * 70)
    print("OPTUNA STUDY SUMMARY")
    print("=" * 70)

    completed = [t for t in study.trials if t.state == optuna.trial.TrialState.COMPLETE]
    pruned = [t for t in study.trials if t.state == optuna.trial.TrialState.PRUNED]
    print(f"  Trials: {len(completed)} completed, {len(pruned)} pruned")

    if not completed:
        print("  No completed trials.")
        return

    print(f"\n  Best trial #{study.best_trial.number}:")
    print(f"    Mean F1 = {study.best_value:.4f}")
    print(f"    Params:")
    for k, v in study.best_params.items():
        print(f"      {k}: {v}")

    # Top 5 trials
    top = sorted(completed, key=lambda t: t.value, reverse=True)[:5]
    print(f"\n  Top 5 trials:")
    for t in top:
        p = t.params
        print(
            f"    #{t.number:3d}  F1={t.value:.4f}  "
            f"embed={p['embed_dim']} lstm={p['lstm_units']} "
            f"td={p['tdense_units']} depth={p['dense_depth']} "
            f"drop={p['dropout']:.2f} lr={p['lr']:.1e} bs={p['batch_size']} "
            f"extra={p['use_extra_features']} aug={p['augment']}"
        )
    print("=" * 70)


def eval_best(study: optuna.Study):
    """Retrain best config with full 5-fold CV and save final model."""
    os.makedirs(BEST_OUTDIR, exist_ok=True)

    bp = study.best_params
    extra_cols = ["ha_num", "o_num"] if bp["use_extra_features"] else []

    print("\n" + "=" * 70)
    print("RETRAINING BEST CONFIG WITH 5-FOLD CV")
    print("=" * 70)
    for k, v in bp.items():
        print(f"  {k}: {v}")
    print("=" * 70)

    # Restore verbose logging for final run
    logging.getLogger("smilesx.train").setLevel(logging.INFO)

    clf = SmilesXClassifier(
        data_path=DATA_PATH,
        smiles_col="smiles",
        label_col="bin_class",
        extra_feature_cols=extra_cols,
        embed_dim=bp["embed_dim"],
        lstm_units=bp["lstm_units"],
        tdense_units=bp["tdense_units"],
        dense_depth=bp["dense_depth"],
        dropout=bp["dropout"],
        lr=bp["lr"],
        weight_decay=bp["weight_decay"],
        batch_size=bp["batch_size"],
        n_epochs=FINAL_EPOCHS,
        patience=FINAL_PATIENCE,
        class_weight=True,
        outdir=BEST_OUTDIR,
        seed=42,
    )

    result = clf.cross_validate(n_folds=FINAL_FOLDS, augment=bp["augment"])
    print("\n" + result.summary())

    # Save best hyperparams alongside model
    with open(os.path.join(BEST_OUTDIR, "best_params.json"), "w") as f:
        json.dump(
            {
                "search_f1": study.best_value,
                "final_f1_mean": result.mean_f1,
                "final_f1_std": result.std_f1,
                "final_auc_mean": result.mean_auc,
                "final_auc_std": result.std_auc,
                "params": bp,
            },
            f,
            indent=2,
        )

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optuna HPO for SMILES-X on T0")
    parser.add_argument("--n-trials", type=int, default=50)
    parser.add_argument("--resume", action="store_true", help="Resume existing study")
    parser.add_argument("--eval-only", action="store_true", help="Skip search, retrain best")
    args = parser.parse_args()

    os.makedirs("logs", exist_ok=True)

    if args.eval_only:
        study = optuna.load_study(study_name=STUDY_NAME, storage=STUDY_DB)
        print_study_summary(study)
    else:
        study = run_search(args.n_trials, resume=args.resume)

    eval_best(study)
