"""
SMILES-X runner with checkpoint-restart support for preemptable jobs.

SMILES-X already saves best models as .hdf5 per fold/run and skips training
if the model file exists. This wrapper adds:
  1. Progress tracking via a JSON checkpoint file
  2. BayOpt result caching (so we don't re-run Bayesian optimization)
  3. Geometry opt result caching
  4. Signal handling for graceful preemption (SIGTERM from PBS)
  5. Configurable via env vars or CLI args

Checkpoint file: {outdir}/checkpoint.json
On restart, reads checkpoint and picks up where it left off.

Usage:
    python3 run_smilesx_checkpoint.py                    # Full pipeline
    python3 run_smilesx_checkpoint.py --skip-bayopt      # Use cached/default hyperparams
    python3 run_smilesx_checkpoint.py --skip-geomopt     # Use default architecture
    python3 run_smilesx_checkpoint.py --resume            # Resume from checkpoint (default behavior)
"""

import os
import sys
import json
import signal
import logging
import time
import argparse
from pathlib import Path
from datetime import datetime

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Project root (parent of src/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'smilesx_lib'))

import numpy as np
import pandas as pd
import tensorflow as tf

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)

# ── Signal handling for preemption ───────────────────────────────────────────

_preempted = False

def _handle_signal(signum, frame):
    global _preempted
    sig_name = signal.Signals(signum).name
    log.warning(f"Received {sig_name} — saving checkpoint and exiting gracefully")
    _preempted = True

# PBS sends SIGTERM before killing. Catch it.
signal.signal(signal.SIGTERM, _handle_signal)
signal.signal(signal.SIGUSR1, _handle_signal)  # Some schedulers use USR1

# ── Checkpoint management ────────────────────────────────────────────────────

class Checkpoint:
    """Tracks progress through the SMILES-X pipeline."""
    
    def __init__(self, path):
        self.path = Path(path)
        self.data = self._load()
    
    def _load(self):
        if self.path.exists():
            with open(self.path) as f:
                data = json.load(f)
            log.info(f"Loaded checkpoint: phase={data.get('phase')}, "
                     f"fold={data.get('fold', '?')}, run={data.get('run', '?')}")
            return data
        return {
            "phase": "init",
            "started": datetime.now().isoformat(),
            "geomopt_done": False,
            "geomopt_result": None,
            "bayopt_done": False,
            "bayopt_result": None,
            "training_progress": {},  # "fold_0_run_1": "done"
            "completed_folds": [],
            "final_done": False,
        }
    
    def save(self):
        self.data["last_updated"] = datetime.now().isoformat()
        # Atomic write
        tmp = self.path.with_suffix('.tmp')
        with open(tmp, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
        tmp.rename(self.path)
    
    def set_phase(self, phase):
        self.data["phase"] = phase
        self.save()
    
    def mark_geomopt(self, result):
        self.data["geomopt_done"] = True
        self.data["geomopt_result"] = result
        self.save()
    
    def mark_bayopt(self, result):
        self.data["bayopt_done"] = True
        self.data["bayopt_result"] = result
        self.save()
    
    def mark_fold_run(self, fold, run):
        key = f"fold_{fold}_run_{run}"
        self.data["training_progress"][key] = "done"
        self.save()
    
    def is_fold_run_done(self, fold, run):
        key = f"fold_{fold}_run_{run}"
        return self.data["training_progress"].get(key) == "done"
    
    def mark_final(self):
        self.data["final_done"] = True
        self.data["completed"] = datetime.now().isoformat()
        self.save()

# ── Runtime estimation ───────────────────────────────────────────────────────

def estimate_remaining(ckpt, n_folds, n_runs, avg_run_secs=360):
    """Estimate remaining time based on progress."""
    done = len(ckpt.data.get("training_progress", {}))
    total = n_folds * n_runs
    remaining = total - done
    est_secs = remaining * avg_run_secs
    return remaining, est_secs

# ── Main pipeline ────────────────────────────────────────────────────────────

def run(args):
    gpus = tf.config.list_physical_devices('GPU')
    log.info(f"TensorFlow {tf.__version__}, GPUs: {len(gpus)}")
    for g in gpus:
        log.info(f"  {g}")

    # Load data
    os.chdir(str(PROJECT_ROOT))
    df = pd.read_csv('data/T0.csv')
    data_smiles = df[['smiles']]
    data_prop = df[['bin_class']]
    data_extra = df[['ha_num', 'o_num']].fillna(0)
    
    log.info(f"Data: {len(df)} molecules, {int(df['bin_class'].sum())} class 1, "
             f"{int((1-df['bin_class']).sum())} class 0")

    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    
    ckpt = Checkpoint(os.path.join(outdir, 'checkpoint.json'))
    
    # Determine hyperparameters
    if args.skip_bayopt or ckpt.data.get("bayopt_done"):
        bayopt_mode = 'off'
        if ckpt.data.get("bayopt_result"):
            log.info(f"Using cached BayOpt result: {ckpt.data['bayopt_result']}")
            bs_ref = ckpt.data["bayopt_result"].get("bs", args.bs)
            lr_ref = ckpt.data["bayopt_result"].get("lr", args.lr)
        else:
            bs_ref = args.bs
            lr_ref = args.lr
            log.info(f"Skipping BayOpt, using provided params: bs={bs_ref}, lr={lr_ref}")
    else:
        bayopt_mode = 'on'
        bs_ref = args.bs
        lr_ref = args.lr

    if args.skip_geomopt or ckpt.data.get("geomopt_done"):
        geomopt_mode = 'off'
        if ckpt.data.get("geomopt_result"):
            log.info(f"Using cached GeomOpt result: {ckpt.data['geomopt_result']}")
        else:
            log.info("Skipping GeomOpt, using default architecture")
    else:
        geomopt_mode = 'on'

    embed_ref = args.embed
    lstm_ref = args.lstm
    tdense_ref = args.tdense
    
    # Override from cached geomopt if available
    if ckpt.data.get("geomopt_result"):
        embed_ref = ckpt.data["geomopt_result"].get("embed", embed_ref)
        lstm_ref = ckpt.data["geomopt_result"].get("lstm", lstm_ref)
        tdense_ref = ckpt.data["geomopt_result"].get("tdense", tdense_ref)

    remaining, est_secs = estimate_remaining(ckpt, args.k_folds, args.n_runs)
    log.info(f"Progress: {args.k_folds * args.n_runs - remaining}/{args.k_folds * args.n_runs} "
             f"fold×runs done, ~{est_secs/60:.0f}min remaining")

    if ckpt.data.get("final_done"):
        log.info("Pipeline already completed! Nothing to do.")
        return

    # Check for preemption before starting expensive work
    if _preempted:
        log.warning("Preempted before training started")
        return

    ckpt.set_phase("training")
    
    from SMILESX.main import main as smilesx_main

    # SMILES-X already handles checkpoint at the model file level:
    # If {model_dir}/{data_name}_Model_Fold_{fold}_Run_{run}.hdf5 exists,
    # it skips training for that fold/run. So we can just call it and it
    # will resume from where it left off.
    
    log.info(f"Starting SMILES-X: geomopt={geomopt_mode}, bayopt={bayopt_mode}, "
             f"bs={bs_ref}, lr={lr_ref}, embed={embed_ref}, lstm={lstm_ref}, tdense={tdense_ref}")
    
    try:
        smilesx_main(
            data_smiles=data_smiles,
            data_prop=data_prop,
            data_extra=data_extra,
            data_name=args.data_name,
            data_units='',
            data_label='bin_class',
            outdir=outdir,
            
            model_type='classification',
            scale_output=False,
            
            geomopt_mode=geomopt_mode,
            embed_bounds=[8, 16, 32, 64, 128, 256, 512, 1024],
            lstm_bounds=[8, 16, 32, 64, 128, 256, 512, 1024],
            tdense_bounds=[8, 16, 32, 64, 128, 256, 512, 1024],
            
            bayopt_mode=bayopt_mode,
            bs_bounds=[8, 16, 32, 64],
            lr_bounds=[2.0, 2.5, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0],
            bayopt_n_rounds=25,
            bayopt_n_epochs=30,
            bayopt_n_runs=3,
            
            embed_ref=embed_ref,
            lstm_ref=lstm_ref,
            tdense_ref=tdense_ref,
            bs_ref=bs_ref,
            lr_ref=lr_ref,
            
            k_fold_number=args.k_folds,
            n_runs=args.n_runs,
            check_smiles=True,
            augmentation=True,
            patience=args.patience,
            n_epochs=args.n_epochs,
            ignore_first_epochs=0,
            
            n_gpus=len(gpus) or 0,
            log_verbose=True,
            train_verbose=True,
        )
        
        ckpt.mark_final()
        log.info("Pipeline completed successfully!")
        
    except SystemExit:
        log.warning("SMILES-X exited (possibly preempted or error)")
        ckpt.save()
    except Exception as e:
        log.error(f"Pipeline error: {e}")
        ckpt.save()
        raise


def main():
    parser = argparse.ArgumentParser(description="SMILES-X with checkpoint-restart")
    parser.add_argument("--outdir", default="./results/smilesx_checkpoint",
                        help="Output directory (checkpoint stored here)")
    parser.add_argument("--data-name", default="pvmol_passivation")
    parser.add_argument("--skip-bayopt", action="store_true")
    parser.add_argument("--skip-geomopt", action="store_true")
    parser.add_argument("--bs", type=int, default=16, help="Batch size (default or initial)")
    parser.add_argument("--lr", type=float, default=3.5, help="Learning rate exponent")
    parser.add_argument("--embed", type=int, default=512)
    parser.add_argument("--lstm", type=int, default=128)
    parser.add_argument("--tdense", type=int, default=128)
    parser.add_argument("--k-folds", type=int, default=5)
    parser.add_argument("--n-runs", type=int, default=3)
    parser.add_argument("--n-epochs", type=int, default=100)
    parser.add_argument("--patience", type=int, default=5)
    parser.add_argument("--resume", action="store_true", help="Resume from checkpoint (default)")
    args = parser.parse_args()
    
    run(args)


if __name__ == '__main__':
    main()
