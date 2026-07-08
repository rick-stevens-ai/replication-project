# Workflow — QC-2007.04424-mog-vqe-multiobjective

## Reproducibility recipe

All steps run inside a fresh venv on macOS / Linux (m1 or uicgpu).

### 0. Fetch source
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2007.04424-mog-vqe-multiobjective
# work/paper.pdf and work/paper.txt already staged from arXiv 2007.04424
```

### 1. Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pennylane==0.45.1 pennylane-lightning openfermion==1.7.1 \
            openfermionpyscf pyscf==2.13.1 scipy numpy
```

### 2. Baselines (FCI, HF, UCCSD, HEA)
Run inside `code/mog_vqe_h2.py`. Emits reference energies, UCCSD (18 CNOTs)
and HEA (L=1..6) sweep.
```bash
python code/mog_vqe_h2.py 2>&1 | tee report/evidence/run_h2.log
```
Outputs:
- `report/evidence/mog_vqe_h2_result.json`
- `report/evidence/mog_vqe_h2_pareto.csv`

### 3. Directed enumeration (Pareto elbow at k=2,3,4)
```bash
python code/refine_min_cnots.py 2>&1 | tee report/evidence/run_refined.log
```
Outputs:
- `report/evidence/mog_vqe_h2_refined.json`

### 4. Regenerate PDF report (optional)
```bash
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```

## Time budget

| Step | Wall clock (m1 CPU) |
|------|---------------------|
| Env install | 3 min |
| Baselines + main NSGA-II | ~11 min (single seed, pop 16 x gen 6) |
| Directed enumeration | ~9 min |
| **Total** | **~25 min** |

## Reproducibility notes
- All RNG seeds documented in the scripts (fixed for HEA sweep and enumeration;
  NSGA-II single-seed by design — extending to multi-seed is Q1/Q3 territory).
- Numpy state-vector simulator in `code/refine_min_cnots.py` is verified to reproduce
  PennyLane's HF energy exactly to double precision (see log header).
- No PennyLane/PySCF version mismatch land-mines observed on 3.14.6.
- No paid endpoints, no cloud compute needed. Everything CPU-local.
