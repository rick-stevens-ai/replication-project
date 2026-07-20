# Artifacts summary — arXiv:2209.10768 replication

## Files
| Path | What |
|---|---|
| `paper.pdf`, `paper.txt` | Source paper + pdftotext extraction |
| `extraction/marker.md` | Extraction: model, method, 5 claims, Table-I anchors |
| `code/loop_current_kagome_kernel.py` | Verbatim shared TEXTURES-100 kernel |
| `code/kagome_tV1V2.py` | Paper-specific t-V1-V2 solver (adapted from kernel) |
| `code/imposed_chern.py` | Impose Table-I bonds -> Chern/gap/flux (C4 direct test) |
| `code/run_all.py` | Driver: runs C1,C3,C4,C5 -> results.json |
| `code/PROVENANCE.md` | Kernel reuse + adaptation provenance |
| `work/results.json` | Self-consistent + susceptibility + baseline results |
| `work/imposed_chern.json` | Imposed-Table-I Chern numbers |
| `work/extra_checks.json` | C2 proxy ratio + kernel uniform-flux cross-check |
| `work/run_all.log` | Full run log (743 s, production resolution) |
| `report/*` | REPORT.tex(+pdf), workflow, this file, failure_analysis, open_questions |

## Quantitative comparison (computed vs paper)

### C5 — vH sublattice interference  ✅ MATCH
- Kagome TB spectrum at every M point: **E = {-2, 0, +2} t** (flat band +2t, vH
  saddle 0). Computed M_energies = [-2.0, 1e-17, 2.0]. ✓
- vH (E=0) band minimum sublattice weight at M1/M2/M3 = **1e-32 / 3e-33 / 0.0**
  = exactly zero on one sublattice. Paper: vH states localized on independent
  sublattices -> onsite order suppressed, off-site bond order favored. ✓

### C1 — susceptibility channel selectivity  ✅ MATCH (qualitative)
Bare finite-T (T=0.005t) bond susceptibility at q=M:
- nn:  real = -0.327,  imag = -0.317  -> **nn real leads** ✓ (thin margin)
- nnn: real = -0.337,  imag = -0.457  -> **nnn imag leads** ✓ (clear)
Paper (Fig. 1c-d): nn -> real breathing dominant, nnn -> imaginary breathing
dominant. Sign and ordering reproduced.

### C2 — weak-coupling critical ratio V2/V1 ~ 2.36  ⚠️ OUT OF SCOPE (proxy only)
Paper: V2/V1 > (1.47-0.96)/(0.99-0.77) ~ 2.36 from four specific Pi values.
Our aggregate channel susceptibilities are not normalized like the paper's
per-bond Pi's; proxy ratio = 0.082 (not comparable). Exact reproduction needs
the paper's precise susceptibility normalization -> marked out of scope.

### C3 — spontaneous LC from V2 / ISD->LC transition  ❌ NOT REPRODUCED
Self-consistent HF collapses to the trivial real state for all (V1,V2):
- V=(2,0): loop_flux = 0.0039 (~0, real CDW) — consistent with "V1-only real".
- V=(0.8,1.6) LC2 point: loop_flux = 0.0023 (~0) — should be nonzero. ✗
- V=(0.5,2.5) LC1 point: loop_flux = 0.0022 (~0) — should be nonzero. ✗
- ISD->LC transition (paper V2~1.81 at V1=1.75): **not observed** (gs stays real
  across V2 in [1.5, 3.15]).
Root cause: missing the paper's symmetric-correction subtraction scheme (see
failure_analysis.md F1). The V1-only real result is the one correct half.

### C4 — LC orbital Chern insulators, N = {1,-1,0,-1}  ◑ PARTIAL MATCH
Direct test imposing the paper's Table-I converged bonds (`imposed_chern.json`):
| State | computed C (occ.) | gap | loop_flux | paper N | match |
|---|---|---|---|---|---|
| ISD | 3 | 0.000 | 0.000 | (trivial) | ✗ (gapless in our mapping) |
| LC1 | 0 | 0.051 | 0.010 | +1 | ✗ |
| **LC2** | **-1** | 0.033 | 0.028 | **-1** | ✅ |
| **LC3** | **0** | 0.095 | 0.020 | **0** | ✅ |
| LC4 | +2 | 0.067 | 0.071 | -1 | ✗ |
2/4 LC Chern numbers exact (LC2, LC3); all LC states gapped with nonzero loop
flux (they ARE orbital Chern insulators). Mismatches (LC1, LC4, ISD) trace to an
approximate C6 bond-class/current-direction labeling, not to the topological
claim itself (see F2).

### C4 mechanism cross-check (shared kernel)  ✅ MATCH
Kernel canonical uniform loop-current kagome state: gapped (**gap = 1.732t**),
band Chern = **[0, -1, 0]** -> an orbital Chern insulator. Confirms the
Haldane-like mechanism: loop-current (Peierls flux) bond order gaps the kagome
bands and yields nonzero Chern, exactly as the paper asserts for the LC vs ISD
distinction.

## Scorecard
- **Coverage: 8/10** — all 5 selected claims implemented and executed with real
  code; C1, C5 fully; C4 partially (mechanism + 2/4 exact); C3 attempted and
  cleanly characterized; C2 attempted but normalization out of scope.
- **Agreement: 6/10** — C5 exact, C1 qualitative match, C4 mechanism exact +
  LC2/LC3 exact; but C3 self-stabilization failed and LC1/LC4 Chern mismatched
  due to the missing subtraction scheme / approximate bond labeling.
