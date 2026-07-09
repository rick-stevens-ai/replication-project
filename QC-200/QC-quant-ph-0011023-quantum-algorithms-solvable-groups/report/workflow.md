# Workflow — replication of Watrous, arXiv:quant-ph/0011023

## Timeline (2026-07-05, CherryRd)

| Step | Action | Duration |
|------|--------|----------|
| 1 | Read wave brief `~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md` and dir standard `REPLICATION_DIR_STANDARD_2026-07-05.md` | ~1 min |
| 2 | `mkdir -p work extraction report/evidence` in target dir | <1 s |
| 3 | Fetch PDF: `curl -sSL -o paper.pdf https://arxiv.org/pdf/quant-ph/0011023` (13 pages, 174 KB) | ~2 s |
| 4 | `pdftotext paper.pdf work/paper.txt` and `pdftotext -layout` variant for fallback extractions | ~1 s |
| 5 | Skim paper (665 lines): identify Theorem 1 as the headline mathematical claim; identify HSP-over-Z_N as the atomic quantum subroutine and coset-state preparation as the "byproduct" that would be testable at small scale | ~3 min |
| 6 | Create Python venv `work/venv/`, install `qiskit==2.5.0 qiskit-aer numpy matplotlib` | ~60 s |
| 7 | Write `report/evidence/hsp_cyclic.py` implementing (i) QFT-based HSP oracle for Z_N, (ii) uniform-state preparation for Z_N with fidelity check, (iii) shots-vs-N scaling | ~10 min |
| 8 | First run: HSP failed (all mass on y=0). Root cause: qubit-ordering error in hand-built oracle permutation matrix (used big-endian composite index instead of Qiskit's little-endian y*2^t + x). Fixed. | ~5 min |
| 9 | Second run: 8/8 HSP cases pass, 9/9 uniform-state cases pass, scaling shots ≤ 4 for |G| ≤ 15 | ~90 s wall |
| 10 | Write `report/evidence/dihedral_d4.py` — D_4 (order 8, non-abelian solvable) uniform state + normal subgroup <r²> + coset decomposition of D_4/<r²> ≅ Z_2×Z_2 | ~5 min |
| 11 | Run D_4 script: fidelity 1.0 for both states, exact coset decomposition | <1 s |
| 12 | Populate `extraction/marker.md` and `extraction/nougat.mmd` as pdftotext-based fallbacks (Marker/Nougat CLIs not installed on CherryRd; central corpus at `~/Dropbox/XFER/pvc-nougat-ocr-tree` does not contain quant-ph/0011023). Both files clearly labelled as fallbacks. | ~1 s |
| 13 | Write `report/REPORT.tex` (claims table + methods + results tables + verdict) and `report/open_questions_body.tex` (5 grounded open questions) and `report/open_questions.json` (machine-readable) | ~10 min |
| 14 | Compile REPORT.tex → REPORT.pdf via pdflatex | ~10 s |
| 15 | Write `report/artifacts_summary.md` and `report/failure_analysis.md` | ~5 min |

**Total wall time**: ~45 min (of which ~2.5 min was actual quantum simulation).

## Tools & versions

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.13 | driver language |
| Qiskit | 2.5.0 | circuit construction + QFT gate |
| Qiskit Aer | (bundled with qiskit-aer) | statevector simulator |
| NumPy | 2.x | linear algebra + unitary matrix construction |
| pdftotext (poppler) | system | PDF text extraction |
| pdflatex (MacTeX) | system | compile REPORT.tex → REPORT.pdf |
| curl | system | fetch PDF from arXiv |

**No LLM inference was used** in this replication (all judgments made by explicit numerical criteria in the Python scripts).

## Design decisions

- **Chose Z_N + D_4 over harder groups (S_n, wreath products)**: keeps register width ≤ 8 qubits, keeps oracle unitary constructable as an explicit permutation matrix, and covers both the abelian (cyclic Z_N) and non-abelian solvable (D_4) regimes Watrous's paper spans.
- **Explicit permutation UnitaryGate rather than compiled reversible arithmetic**: reversible-arithmetic compilation of `x mod d` would add substantial engineering; the permutation matrix approach is a faithful black-box oracle in Watrous's cost model and is O(|G|²) memory which is fine at this scale.
- **QFT with `do_swaps=True` + inverse-of-Fourier direction**: Qiskit's default `QFT` gate handles the bit-reversal internally, so the measured integer `y` directly corresponds to the frequency-domain sample.
- **CF-based period recovery + LCM of top-k denominators**: standard Shor recovery; robust to noisy samples and to the case where the peak is not at an exact multiple of 2^t/d.
- **`d_recovered = gcd(LCM(top denominators), N)`**: guarantees the answer divides N and yields the maximal period consistent with the samples.

## Estimate of work

- ~600 lines of new Python (2 scripts)
- ~350 lines of new LaTeX (REPORT + open-questions body)
- ~150 lines of new Markdown (extraction fallbacks + these workflow / artifacts / failure notes)
- 3 real Qiskit simulations completing successfully (HSP cyclic, uniform-state, D_4)
- Total agent effort: ~45 minutes end-to-end
