#!/usr/bin/env python3
"""Environment verification for PVMol-Gen replication on Polaris."""
import sys, os, time, traceback

print("=" * 70)
print("  POLARIS ENVIRONMENT CHECK")
print(f"  Host: {os.uname().nodename}")
print(f"  Time: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
print(f"  Python: {sys.version}")
print(f"  Prefix: {sys.prefix}")
print("=" * 70)

checks = {}

# 1. Core packages
for pkg, min_ver in [("numpy", "1.24"), ("pandas", "2.0"), ("scipy", "1.10"), ("sklearn", "1.2")]:
    try:
        mod = __import__(pkg)
        v = mod.__version__
        ok = tuple(int(x) for x in v.split(".")[:2]) >= tuple(int(x) for x in min_ver.split("."))
        checks[pkg] = f"{'OK' if ok else 'WARN'} {v} (need >={min_ver})"
    except Exception as e:
        checks[pkg] = f"FAIL: {e}"

# 2. TensorFlow + Keras
try:
    import tensorflow as tf
    checks["tensorflow"] = f"OK {tf.__version__}"
    # GPU check
    gpus = tf.config.list_physical_devices("GPU")
    checks["tf_gpu"] = f"OK {len(gpus)} GPU(s): {[g.name for g in gpus]}" if gpus else "WARN: no GPUs"
    try:
        import keras
        checks["keras"] = f"OK {keras.__version__}"
    except Exception as e:
        checks["keras"] = f"FAIL: {e}"
except Exception as e:
    checks["tensorflow"] = f"FAIL: {e}"
    checks["tf_gpu"] = "SKIP (no TF)"
    checks["keras"] = "SKIP (no TF)"

# 3. PyTorch
try:
    import torch
    checks["pytorch"] = f"OK {torch.__version__}"
    if torch.cuda.is_available():
        checks["torch_gpu"] = f"OK {torch.cuda.device_count()} GPU(s): {torch.cuda.get_device_name(0)}"
        # Quick tensor op
        t = torch.randn(10, 10, device="cuda")
        r = t @ t.T
        checks["torch_cuda_op"] = f"OK (matmul on GPU worked)"
    else:
        checks["torch_gpu"] = "WARN: CUDA not available"
except Exception as e:
    checks["pytorch"] = f"FAIL: {e}"
    checks["torch_gpu"] = "SKIP"

# 4. RDKit
try:
    from rdkit import Chem, __version__ as rdkit_ver
    from rdkit.Chem import AllChem, Descriptors
    mol = Chem.MolFromSmiles("NCCCCCCN")
    assert mol is not None
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
    checks["rdkit"] = f"OK {rdkit_ver} (SMILES parse + Morgan FP work)"
except Exception as e:
    checks["rdkit"] = f"FAIL: {e}"

# 5. Transformers (for GPT-2 Stage 2)
try:
    import transformers
    checks["transformers"] = f"OK {transformers.__version__}"
    # Check GPT-2 availability (don't load full model, just tokenizer)
    from transformers import GPT2Tokenizer
    tok = GPT2Tokenizer.from_pretrained("gpt2")
    checks["gpt2_tokenizer"] = "OK (loaded)"
except Exception as e:
    checks["transformers"] = f"FAIL: {e}"

# 6. SMILES-X library
try:
    sys.path.insert(0, os.path.expanduser("~/pvmol-gen"))
    from smilesx_lib.SMILESX import model, token
    checks["smilesx_lib"] = "OK (model + token imported)"
    # Quick forward pass
    import numpy as np
    test_model = model.LSTMAttModel.create(
        input_tokens=50, vocab_size=36, embed_units=32, lstm_units=16,
        tdense_units=16, extra_dim=2, model_type="classification"
    )
    x_smi = np.zeros((2, 50), dtype=np.int32)
    x_ext = np.zeros((2, 2), dtype=np.float32)
    pred = test_model.predict({"smiles": x_smi, "extra": x_ext}, verbose=0)
    checks["smilesx_fwd"] = f"OK (forward pass shape={pred.shape}, range=[{pred.min():.3f}, {pred.max():.3f}])"
except Exception as e:
    checks["smilesx_lib"] = f"FAIL: {e}"
    checks["smilesx_fwd"] = f"SKIP"
    traceback.print_exc()

# 7. optuna (used in bayopt)
try:
    import optuna
    checks["optuna"] = f"OK {optuna.__version__}"
except Exception as e:
    checks["optuna"] = f"FAIL: {e}"

# 8. Data files
data_dir = os.path.expanduser("~/pvmol-gen/data")
for fname in ["dataset.xlsx", "puchem_aug.csv", "t1_class1.csv"]:
    path = os.path.join(data_dir, fname)
    if os.path.exists(path):
        sz = os.path.getsize(path)
        checks[f"data/{fname}"] = f"OK ({sz:,} bytes)"
    else:
        checks[f"data/{fname}"] = "MISSING"

# 9. Our PyTorch classifier
try:
    sys.path.insert(0, os.path.expanduser("~/pvmol-gen/src"))
    from stage1_classifier import SmilesXClassifier
    checks["pytorch_classifier"] = "OK (imported)"
except Exception as e:
    checks["pytorch_classifier"] = f"FAIL: {e}"

# Print results
print("\n" + "=" * 70)
print("  RESULTS")
print("=" * 70)
fails = 0
warns = 0
for k, v in checks.items():
    status = "✓" if v.startswith("OK") else ("⚠" if v.startswith("WARN") or v.startswith("SKIP") else "✗")
    if v.startswith("FAIL"): fails += 1
    if v.startswith("WARN"): warns += 1
    print(f"  {status} {k:25s} {v}")

print("\n" + "=" * 70)
print(f"  SUMMARY: {len(checks)} checks, {len(checks)-fails-warns} OK, {warns} WARN, {fails} FAIL")
print("=" * 70)
