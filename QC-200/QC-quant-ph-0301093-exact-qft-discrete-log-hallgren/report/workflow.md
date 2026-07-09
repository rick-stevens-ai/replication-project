# Workflow — Independent Replication of Mosca & Zalka (2003)

**Paper:** arXiv:quant-ph/0301093 — Michele Mosca & Christof Zalka, "Exact quantum Fourier transforms and discrete logarithm algorithms" (Univ. Waterloo, Jan 2003, 10 pp.).

**Replication date:** 2026-07-05
**Host:** CherryRd (macOS 25.3.0, x64)
**Time budget:** ~1 hour (single subagent turn)

## 0. Setup
```bash
mkdir -p ~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0301093-exact-qft-discrete-log-hallgren/{work,extraction,report/evidence}
```

## 1. Paper retrieval
```bash
cd work
curl -sSL -o paper.pdf https://arxiv.org/pdf/quant-ph/0301093
pdftotext -layout paper.pdf paper.txt   # 447 lines, ~27 KB
cp paper.pdf ../paper.pdf
```
Authors verified from arXiv metadata + PDF: Mosca & Zalka. (Task brief tentatively cited "Hallgren" — this was corrected.)

## 2. Reading pass
Extracted three checkable claims:
| id | claim | location |
|---|---|---|
| C1 | Target unitary is DFT_N for arbitrary N | Sec 2 (paper eq. after abstract) |
| C5 | Shor dlog on cyclic group of prime order p has success prob 1 - 1/p | Sec 3 |
| C6 | Average eigenvalue-estimation success p_bar = (1/p) Σ f²(k/p) → ≈ 0.4514 | Sec 4.1 |

## 3. Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install --quiet qiskit qiskit-aer numpy scipy sympy
```
Pinned:
- Python 3 (system)
- **numpy 2.5.1**
- **scipy 1.18.0**
- **sympy 1.14.0**
- **qiskit 2.5.0**
- **qiskit-aer 0.17.2**

## 4. Simulation scripts
All in `report/evidence/`:

### 4a. `exact_qft_verify.py`
- Builds explicit DFT_N for N ∈ {2,3,4,5,6,7,8,11,15,16,17,31,32}
- Checks `||F F^† - I||_F` and formula compliance on `F|x=1>`
- Cross-checks Qiskit's `QuantumCircuit + QFT + Operator(qc)` vs DFT_N for n_qubits = 1..5
- **Output**: `results_qft.json` — max unitarity error 4.0e-14, max formula error 3.5e-16, Qiskit residual 3.8e-14

### 4b. `pbar_success_prob.py`
- Evaluates p_bar(p, N) for p ∈ {7,11,31,61,127,251,509,1021} × N ∈ {N_min, 2·N_min, 4·N_min}
- Computes ∫₀¹ sinc²(πz) dz numerically → **0.451412**
- Paper: 0.4514 → |Δ| = 1.2e-5
- **Output**: `results_pbar.json`

### 4c. `shor_dlog_p7.py`
- For p ∈ {7, 11}, every a ∈ {0..p-1}:
  - Prepare post-oracle state (x0 = 0)
  - Apply QFT_p ⊗ QFT_p (as explicit DFT unitary)
  - Enumerate full (c, d) distribution
  - Recover a = d · c⁻¹ mod p for c ≠ 0
- Also averages over x0 as sanity
- **Output**: `results_dlog.json` — success prob = 1 - 1/p to 1e-16 for both primes

## 5. Execution
```bash
python3 report/evidence/exact_qft_verify.py
python3 report/evidence/pbar_success_prob.py
python3 report/evidence/shor_dlog_p7.py
```
Total wall-clock: < 10 seconds. No GPU. No paid APIs. No LLM calls.

## 6. Report
- `report/REPORT.tex` — full section-by-section replication report (this is the canonical narrative)
- `report/open_questions.json` — 5 heavy-duty open questions grounded in the actual replication
- `report/artifacts_summary.md` — inventory
- `report/failure_analysis.md` — honest failure/friction analysis
- `extraction/marker.md`, `extraction/nougat.mmd` — labelled-fallback text extractions (pdftotext) since Marker and Nougat are not installed on this host

## Tools & versions
| Tool | Purpose | Version |
|---|---|---|
| curl | fetch arxiv PDF | system |
| pdftotext | text extraction (fallback for Marker/Nougat) | poppler-utils (system) |
| Python | driver | 3 (system) |
| numpy | linear algebra | 2.5.1 |
| scipy | numerics | 1.18.0 |
| sympy | prime detection | 1.14.0 |
| qiskit | reference QFT circuit | 2.5.0 |
| qiskit-aer | (loaded but statevector done by numpy directly for dim ≤ 121) | 0.17.2 |
| Marker | PDF-to-markdown | NOT INSTALLED (fallback used) |
| Nougat | PDF-to-markdown | NOT INSTALLED (fallback used) |
| LaTeX | REPORT.tex compilation | on host (not verified in this session) |
| Argo LLM proxy | scoring | NOT INVOKED (self-verdict) |

## Estimate of work done
- **Reading + comprehension**: ~10 min (paper is 10pp, dense but self-contained)
- **Coding + debugging**: ~20 min (one convention slip on QFT+/−sign for dlog that took ~5 min to unwind by tracing (c+ad) mod r for a=2, p=7 — recovered by matching paper's exact Sec 3 setup, prime-order cyclic group)
- **Writing**: ~15 min
- **Total**: ~45 min elapsed

## Reproducibility
- All source files are deterministic (no randomness, fixed x0).
- Re-running any script in a fresh venv with the pinned versions above should produce byte-identical JSON to floating-point machine tolerance.
- The `venv/` is local to the target dir; discard and rebuild from `pip install ...` in section 3.
