"""
Central configuration for the Replicate pipeline.
All paths, hyperparameters, and thresholds in one place.
"""
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models"
RESULTS_DIR = ROOT / "results"
LOG_DIR = ROOT / "logs"

# Raw input data
T0_FILE = DATA_DIR / "T0.csv"  # Author's exact 314 labeled molecules

# Intermediate data
T_AUG_FILE = DATA_DIR / "t_aug_pubchem.csv"  # PubChem augmented
T1_FILE = DATA_DIR / "t1_class1.csv"  # Combined class 1 molecules

# Generative cycle outputs
GEN_CYCLE_DIR = DATA_DIR / "gen_cycles"

# Filter outputs
PROPERTIES_FILE = RESULTS_DIR / "all_properties.csv"
FILTERED_FILE = RESULTS_DIR / "filtered_molecules.csv"
SELECTED_FILE = RESULTS_DIR / "selected_molecules.csv"

# ─── Stage 1: Classifier ────────────────────────────────
CLASSIFIER_DIR = MODEL_DIR / "smilesx_classifier"
CLASSIFICATION_THRESHOLD = 0.47  # Optimized, not default 0.5
PCE_THRESHOLD = 0.10  # ΔPCEnorm ≥ 0.10 → class 1
PCE_TOP_THRESHOLD = 0.16  # Top performers for PubChem similarity search
CV_FOLDS = 5
CLASSIFIER_EPOCHS = 100
CLASSIFIER_BATCH_SIZE = 32
CLASSIFIER_LR = 1e-4

# ─── Stage 1b: PubChem Augmentation ─────────────────────
TANIMOTO_THRESHOLD = 0.80
PUBCHEM_MAX_RESULTS = 100  # Per query molecule

# ─── Stage 2: Generative Model ──────────────────────────
GPT2_MODEL_NAME = "gpt2"
GPT2_DIR = MODEL_DIR / "gpt2_finetuned"
NUM_GEN_CYCLES = 3
SMILES_AUGMENTATIONS = 5
GEN_TARGET_PER_CYCLE = 100_000
GEN_TEMPERATURE = 0.9
GEN_MAX_LENGTH = 100
GPT2_TRAIN_EPOCHS = 100
GPT2_BATCH_SIZE = 2  # Paper uses 2 explicitly — match for fidelity
GPT2_WARMUP_STEPS = 500
GPT2_WEIGHT_DECAY = 0.01
GPT2_EARLY_STOPPING_PATIENCE = 5

# ─── Stage 3: Filtering ─────────────────────────────────
SA_MAX = 6.0
HBD_RANGE = (0, 2)
HBA_RANGE = (2, 5)
TPSA_RANGE = (50.0, 120.0)
GAP_RANGE = (1.5, 5.0)  # eV — requires xTB or DFT
DIPOLE_RANGE = (1.5, 4.0)  # Debye — requires xTB or DFT
NUM_CLUSTERS = 10
XTB_WORKERS = 40

# ─── Device ──────────────────────────────────────────────
def get_device() -> str:
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"

DEVICE = get_device()
