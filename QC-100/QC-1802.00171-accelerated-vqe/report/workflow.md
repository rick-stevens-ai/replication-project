# Workflow — QC-1802.00171-accelerated-vqe

## Inputs
- Paper: arXiv 1802.00171v3 (Wang, Higgott, Brierley 2018 / PRL 122, 140504 (2019)).
- Source files: `paper/1802.00171.pdf`, `paper/1802.00171.txt` (pdftotext).
- Public reference values: H₂/STO-3G FCI equilibrium energy E = −1.13727 Ha (Peruzzo 2014, O'Malley 2016, McClean 2016).

## Environment
- Python 3.12.13 venv (`.venv/`), macOS 26.3 (Intel), single CPU.
- PennyLane 0.45.1 + pennylane-qchem, PySCF 2.13.1, OpenFermion 1.7.1, numpy 2.5.0, scipy 1.18.0, matplotlib.
- No GPU, no HPC, no proprietary data.

## Reproduction pipeline
```
python3.12 -m venv .venv && source .venv/bin/activate
pip install pennylane openfermion pyscf numpy scipy matplotlib

python code/vqe_h2.py           # ~69 s — writes evidence/vqe_h2_*.{json,csv}, figures/vqe_h2_pes.png
python code/alpha_qpe_rfpe.py   # ~few min — writes evidence/alpha_qpe_*.{json,csv}, figures/alpha_qpe_rfpe_fig5.png
```

## Steps
1. **VQE / H₂ (Claim C1).** For 10 bond lengths R ∈ [0.6, 3.0] bohr, build the JW-mapped 4-qubit Hamiltonian via `qml.qchem.molecular_hamiltonian`, compute FCI via direct diagonalisation, run UCCSD ansatz (3 variational params) with Adam (lr=0.1, tol=1e-8, ≤250 iters) on `default.qubit` (seed 42). Compare energies to FCI in mHa.
2. **α-QPE / RFPE Fig. 5 (Claims C2, C3).** numpy implementation of Sec.~II.A / App.~A. Prior N(π, 1); per iteration k draw M_k = ⌈1/σ_k^α⌉ clipped to [1, 10^7], θ = μ_k, sample outcome E ∼ Bernoulli((1+cos(Mφ−θ−Eπ))/2); rejection-filter 600 particles from N(μ_k, σ_k²), refit Gaussian. Sweep α ∈ {0, 0.25, 0.5, 0.75, 1.0}, 200 trials × 60 iterations each, seed 1802.
3. **Analysis.** Compute median r_k = σ_k trace per α, fit log-linear slope on k ∈ [10, 60], compare fan against paper Fig. 5 envelope.

## Determinism
- All runs use fixed seeds (42 for VQE, 1802 for RFPE).
- Repeat runs verified bit-identical outputs.

## Provenance
- Raw run outputs preserved under `report/evidence/` (JSON + CSV).
- Figures in `figures/`.
- Software versions frozen in `report/evidence/versions.txt`.
- No LLM inference in the pipeline; LLM used only to compose the narrative report.
