# Workflow — Independent Replication of arXiv:quant-ph/0102014

**Paper:** Ivanyos, Magniez, Santha (2001), *Efficient quantum algorithms for
some instances of the non-Abelian hidden subgroup problem*.
**Replication target:** Theorem 13, §6 — HSP for `G = N ⋊ Z_2` with `N` an
elementary abelian 2-group.
**Verdict:** REPLICATED.

## Step-by-step

### 1. Paper acquisition + read (~10 min)
```
mkdir -p work
curl -sL https://arxiv.org/pdf/quant-ph/0102014 -o work/paper.pdf
cp work/paper.pdf paper.pdf
pdftotext work/paper.pdf work/paper_plain.txt
pdftotext -layout work/paper.pdf work/paper.txt
```
Read the abstract, §2 (preliminaries), §3 (Beals-Babai foundation), and in
detail §5-6 (Theorems 11 & 13). Identify §6's `F(0,x)=f(x), F(1,x)=f(xz)`
construction as the concrete testable claim (see REPORT.tex §Claims table).

### 2. Environment setup (~2 min)
```
python3 -m venv .venv
source .venv/bin/activate
pip install --quiet qiskit qiskit-aer numpy
```
- Python 3.14.6 (Homebrew macOS 25.3.0)
- NumPy 2.5.1
- Qiskit 2.5.0
- Qiskit-Aer 0.17.2

### 3. Exploratory / negative-control build (~15 min)
Wrote `code/dihedral_hsp.py` first, implementing the same
`F(0,x)/F(1,x)` construction but on plain dihedral `D_n = Z_n ⋊ Z_2`.
Result confirmed the paper's hypothesis: full 100 %-on-lattice behaviour
only occurs when `2d ≡ 0 (mod n)`, i.e. when `N` is (or contains) a
2-torsion element — which is precisely why §6 requires `N` elementary
abelian 2. This is preserved as a negative control in
`report/evidence/dihedral_hsp_results.json`.

### 4. Full IMS §6 simulation (~30 min)
Wrote `code/ims_theorem13.py` implementing:
1. Random invertible `σ ∈ GL_k(F_2)` (rank test via F_2 Gaussian elim).
2. Non-trivial fixed vector `u` of `σ` (F_2 kernel of `σ−I`).
3. Semidirect-product multiplication `(x1,b1)(x2,b2) = (x1 ⊕ σ^{b1}(x2), b1⊕b2)`.
4. Coset-label oracle `f: G → labels`.
5. Auxiliary function `F(b,x) = f((x,0) · z^b)` on `Z_2 × F_2^k`.
6. Reduced density matrix `ρ = MM†` on the `(k+1)`-qubit group register,
   representing the state after preparing coset states and tracing out `f`.
7. Fourier sampling via `H^⊗(k+1)`; readout diagonal of `FρF†`.
8. Basis-collection recovery of `K` from `K^⊥` samples over `F_2`.
9. `K = (K^⊥)^⊥` via brute enumeration (dim ≤ 7).

Ran `python3 code/ims_theorem13.py` on `k = 2, 3, 4, 5, 6` × 3 seeds =
15 instances. Wall time: **0.05 s**. Results saved to
`code/ims_theorem13_results.json` and mirrored in
`report/evidence/ims_theorem13_results.json`.

### 5. LLM-judge verdict (~1 min)
Queried `argo:gpt-5.2` at `http://localhost:44497/v1/chat/completions`
(free Argo endpoint per QC wave brief, `Authorization: Bearer stevens`)
with a structured JSON-only prompt describing the paper claim, the exact
15-instance results, and asking for a verdict. Judge returned
`verdict = REPLICATED` with the justification quoted in REPORT.tex §Verdict.

### 6. Report assembly (~15 min)
- `report/REPORT.tex` — LaTeX-native full report (this is the canonical
  deliverable per REPLICATION_DIR_STANDARD_2026-07-05 artifact #4).
- `report/open_questions.json` — 5 heavy-duty new open questions, each
  with `q`, `basis`, `next_steps` — grounded in what the replication
  actually observed (Q1 = |G/N| non-cyclic regime; Q2 = |H| scaling;
  Q3 = query-complexity constant; Q4 = non-elementary-abelian N;
  Q5 = quantum lower bound).
- `report/workflow.md` — this file.
- `report/artifacts_summary.md` — full inventory + traces.
- `report/failure_analysis.md` — honest failure analysis (Marker/Nougat
  unavailable; PDF-text fallback; missing Theorems 8/11 direct
  replications).

## Tools used
| Tool | Version | Role |
|---|---|---|
| Python | 3.14.6 | driver |
| NumPy | 2.5.1 | dense linear algebra (density matrix, Hadamard, F_2 GE) |
| Qiskit | 2.5.0 | version import for provenance (statevector done in NumPy directly for speed at n≤7 qubits) |
| Qiskit-Aer | 0.17.2 | version import for provenance |
| Poppler `pdftotext` | Homebrew | PDF → text fallback for extraction/marker.md, extraction/nougat.mmd |
| Argo LLM gateway | localhost:44497 | free LLM-judge (`argo:gpt-5.2`) |
| curl | macOS system | LLM-judge invocation |

## Estimate of work done
- Paper reading + claim identification: ~10 min
- Environment setup: ~2 min
- Negative-control code (dihedral, wrong hypothesis): ~15 min
- Faithful IMS §6 code + 15-instance run: ~30 min
- LLM judge round-trip: ~1 min
- Report assembly (all 8 artifacts): ~30 min
- **Total: ~90 min single-agent time.**

## Not attempted (deferred, see failure_analysis.md)
- Theorem 8 (normal HSP in solvable / permutation groups) — would need
  a Beals-Babai composition-series simulator, out of QC-100 scope.
- Theorem 11 (small commutator subgroup, e.g. extra-special p-groups) —
  would need a working simulation of the commutator-subgroup enumeration
  outer loop; scope creep.
- Non-cyclic G/N side of Theorem 13 — bigger register, still tractable
  but not covered by this wave (see Open Question Q1).
