# Workflow — replication of arXiv:2209.10768

Paper: Dong, Wang, Zhou, *Loop-current charge density wave driven by long-range
Coulomb repulsion on the kagomé lattice* (PRB / arXiv:2209.10768v2, 2023).

## 0. Inputs
- `paper.pdf` (fetched) -> `paper.txt` via `pdftotext -layout`.
- Shared reusable kernels (both copied to `code/` with provenance):
  - `loop_current_meanfield_kernel.py` (the assigned minimal kernel: kagome
    geometry, Peierls-flux bond-current `J_ij=-2 Im[H_ij rho_ji]`, triangle
    loop-order, finite-field loop susceptibility). Proven on tazai2022.
  - `loop_current_kagome_kernel.py` (larger sibling kernel: adds a built-in
    Fukui–Hatsugai–Suzuki Chern routine + multipole/patch classifiers), used for
    the FHS Chern algorithm pattern.

## RECONCILIATION NOTE
Two concurrent replication passes ran on this directory and were merged into one
coherent deliverable. Pass A built the RPA/Stoner weak-coupling C3 test and the
self-consistent-HF C4; Pass B built `imposed_chern.py` (paper-OP topological
test) and this workflow/failure documentation. The final `work/results.json`
merges both: C3 uses the Stoner criterion (SUPPORT); C4 uses imposed paper OPs
(LC2/LC3 exact). Both kernels are retained in `code/`.

## 1. Extraction
Read paper, isolated the model (Eq. 6, single-orbital t-V1-V2), mean-field
decoupling (Eq. 20, complex bond OPs on nn+nnn), vH filling n=5/12, and the
five ground states (ISD + LC1..4) with Table I converged bond values and the
claimed total Chern numbers N = {1,-1,0,-1}. Written to `extraction/marker.md`.

## 2. Selected machine-checkable claims
- **C1** susceptibility channel selectivity (nn real vs nnn imaginary at q=M).
- **C2** weak-coupling critical ratio V2/V1 ~ 2.36.
- **C3** spontaneous loop-current order requires sufficiently large V2; V1-only
  gives a real CDW; first-order ISD->LC transition (~1.81 at V1=1.75).
- **C4** LC states are gapped orbital Chern insulators, total N = {1,-1,0,-1}.
- **C5** vH sublattice interference suppresses onsite order -> off-site bond order.

## 3. Implementation (`code/`)
- `loop_current_kagome_kernel.py` — verbatim shared kernel (provenance in
  `code/PROVENANCE.md`).
- `kagome_tV1V2.py` — paper-specific solver ADAPTED from the kernel:
  * kagome 3x3 TB with corrected C3-symmetric half-bond vectors (all three M
    points give E={-2,0,2}t);
  * finite-T bare bond susceptibility (Lindhard) at q=M for the four
    real/imag x nn/nnn channels (C1);
  * 2x2 (12-site) supercell enumerator + 12x12 mean-field Bloch H (Eq. 20);
  * self-consistent Hartree–Fock loop with complex nn+nnn bond OPs (C3);
  * gauge-invariant triangle plaquette-flux loop-current order parameter
    (raw Im(chi_ij) is gauge dependent and must NOT be used);
  * Fukui–Hatsugai Chern of the 5 occupied bands on the folded BZ (C4).
- `imposed_chern.py` — imposes the paper's OWN Table-I converged bond values as
  the mean field and computes Chern + gap + loop flux for ISD, LC1..4 (direct
  test of the topological claim C4, independent of self-consistent convergence).
- `run_all.py` — runs C1, C3, C4, C5, writes `work/results.json`.

## 4. Runs (`work/`)
- `python3 run_all.py` -> `work/results.json`, `work/run_all.log`.
- `python3 imposed_chern.py` -> `work/imposed_chern.json`.
- Cross-check of the loop-current mechanism using the kernel's canonical
  uniform-flux state (gapped, band Chern = -1) recorded in the report.

## 5. Comparison + verdict
Quantitative comparison of computed vs paper values in
`report/artifacts_summary.md`; negative/partial results and root causes in
`report/failure_analysis.md`; 5 open questions in `report/open_questions.json`;
narrative + verdict + Coverage/Agreement scores in `REPORT.tex` (-> PDF).

## Reproduce
```
cd code
python3 run_all.py          # ~4-6 min ; add --quick for a fast smoke run
python3 imposed_chern.py    # ~1 min
```
Dependencies: python3 + numpy only. t=1 energy unit throughout.
