#!/usr/bin/env python3
"""
Replicate Pipeline — Full orchestrator.

Runs all stages sequentially:
  Stage 1:  Train SMILES-X classifier (5-fold CV)
  Stage 1b: PubChem augmentation → build T1 dataset
  Stage 2:  Iterative GPT-2 generation (3 cycles)
  Stage 3:  Physicochemical filtering → candidate selection

Usage:
  python run_pipeline.py                     # Full pipeline
  python run_pipeline.py --stage 1           # Just classifier
  python run_pipeline.py --stage 1b          # Just PubChem augmentation
  python run_pipeline.py --stage 2           # Just generation
  python run_pipeline.py --stage 3           # Just filtering
  python run_pipeline.py --stage 3 --no-xtb  # Filtering without xTB
"""
import argparse
import logging
import time

from config import DATA_DIR, MODEL_DIR, RESULTS_DIR, LOG_DIR, CLASSIFIER_DIR, GEN_CYCLE_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "pipeline.log"),
    ]
)
logger = logging.getLogger(__name__)


def run_stage1():
    logger.info("━━━ Stage 1: SMILES-X Classifier ━━━")
    from stage1_classifier import load_t0_data, run_cross_validation
    CLASSIFIER_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    df = load_t0_data()
    metrics, _ = run_cross_validation(df)
    import pandas as pd
    pd.DataFrame(metrics).to_csv(RESULTS_DIR / "classifier_cv_results.csv", index=False)
    logger.info("Stage 1 complete.")


def run_stage1b():
    logger.info("━━━ Stage 1b: PubChem Augmentation ━━━")
    from stage1b_pubchem_augment import run_pubchem_augmentation, build_t1_dataset
    run_pubchem_augmentation()
    build_t1_dataset()
    logger.info("Stage 1b complete.")


def run_stage2():
    logger.info("━━━ Stage 2: Iterative GPT-2 Generation ━━━")
    from stage2_generator import run_generative_cycles
    GEN_CYCLE_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    run_generative_cycles()
    logger.info("Stage 2 complete.")


def run_stage3(use_xtb: bool = True):
    logger.info("━━━ Stage 3: Filtering & Selection ━━━")
    from stage3_filter import run_stage3 as _run
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    _run(use_xtb=use_xtb)
    logger.info("Stage 3 complete.")


def main():
    parser = argparse.ArgumentParser(description="Replicate Pipeline")
    parser.add_argument("--stage", choices=["1", "1b", "2", "3", "all"],
                        default="all", help="Which stage to run")
    parser.add_argument("--no-xtb", action="store_true",
                        help="Skip xTB in stage 3")
    args = parser.parse_args()

    # Ensure directories exist
    for d in [DATA_DIR, MODEL_DIR, RESULTS_DIR, LOG_DIR, CLASSIFIER_DIR, GEN_CYCLE_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    start = time.time()

    if args.stage in ("1", "all"):
        run_stage1()
    if args.stage in ("1b", "all"):
        run_stage1b()
    if args.stage in ("2", "all"):
        run_stage2()
    if args.stage in ("3", "all"):
        run_stage3(use_xtb=not args.no_xtb)

    elapsed = time.time() - start
    logger.info(f"Pipeline finished in {elapsed/3600:.1f} hours")


if __name__ == "__main__":
    main()
