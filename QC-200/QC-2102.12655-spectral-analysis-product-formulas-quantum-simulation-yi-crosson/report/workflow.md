# Workflow — arXiv:2102.12655 replication (QC-200 wave)

## Objective
Independently reproduce the reproducible core of Yi & Crosson (2021),
"Spectral Analysis of Product Formulas for Quantum Simulation": the
scaling of 1st/2nd/4th-order product-formula errors and the paper's
central qualitative claim that state-fidelity Trotter error on a
structured initial state is a much tighter error measure than the
operator-norm bound.

## Steps executed (chronological)
1. **Set up target dir.** `mkdir -p QC-200/QC-2102.12655-.../{work,extraction,report/evidence}`.
2. **Fetch paper.** `curl https://arxiv.org/pdf/2102.12655 -o paper.pdf` (497 KB, 20 pages).
3. **PDF-to-text.** `pdftotext` (raw + `-layout`) into `work/paper.txt` and `work/paper_layout.txt`.
4. **Verify identity.** Confirmed title "Spectral Analysis of Product Formulas for Quantum Simulation" and authors "Changhao Yi, Elizabeth Crosson" (UNM) from the PDF front matter. Matches scout summary.
5. **Read paper, extract testable claims.** See `REPORT.tex` §Claims table (C1..C7). Only C1–C4 are testable at n≤6 qubits without a full QPE/DAS pipeline.
6. **Fallback extraction artifacts.** Marker and Nougat are not installed on this host; there is no pre-parsed copy in the central corpus. To keep the 8-artifact contract, `extraction/marker.md` and `extraction/nougat.mmd` were populated from `pdftotext -layout` / `pdftotext` respectively, with an explicit fallback banner in each file. See `failure_analysis.md`.
7. **Implement the reproduction.** `report/evidence/trotter_scaling.py`:
   - Build TFIM $H = H_1+H_2$ on $n\in\{4,6\}$ qubits (open boundary, $J=h=1$) with explicit Pauli kron products.
   - Compute reference $U_{\text{ex}}=e^{-iHt}$ with `scipy.linalg.expm`.
   - Implement $S_1$ (1st-order Lie-Trotter), $S_2$ (symmetric Strang), $S_4$ (Suzuki–Yoshida) as explicit products of layer exponentials.
   - Sweep $\delta t\in\{0.5,0.25,0.125,0.0625,0.03125\}$; apply the formula L=t/dt times.
   - Compute $\|U_{\text{ex}}-U_{\text{ap}}\|_2$ (op-norm) and $1-|\langle\psi_{\text{ex}}|\psi_{\text{ap}}\rangle|^2$ (state infidelity from H ground state).
   - Also compute the standard operator-norm Trotter bound $L\delta t^{2}\|[H_1,H_2]\|/2$ and the bound/actual ratio.
   - Log-log-fit slopes.
   - Dump `trotter_scaling.json`.
8. **Plot.** `report/evidence/make_plot.py` → `report/evidence/trotter_scaling.png` (two-panel log-log; op-norm and state-infidelity, both for n=4 and n=6).
9. **Write reports.**
   - `REPORT.tex` (main narrative + tables + verdict + open questions).
   - `open_questions.json` (5 heavy-duty follow-ons with basis and next_steps).
   - `artifacts_summary.md`, `failure_analysis.md`, this `workflow.md`.
10. **Attempt LaTeX compile** (optional per brief); if `pdflatex` available produce `REPORT.pdf`.

## Tools / codes / versions
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13 (system) | driver |
| numpy | 2.4.3 | linear algebra, Kron products |
| scipy | 1.18.0 | `scipy.linalg.expm`, `norm(ord=2)` |
| matplotlib | (installed with numpy stack) | log-log plots |
| pdftotext (poppler) | system | PDF text extraction (fallback for Marker/Nougat) |
| curl | system | arXiv fetch |

## Effort estimate
- Paper fetch + skim: ~5 min.
- Reproduction code + debug (Suzuki-4 recursion sign check): ~10 min.
- Sweep + plot: ~1 min of CPU (all n≤6 matrices, dense, dt down to 1/32 → 32 steps × O(64³) each; trivially fast on a laptop).
- Report writing (LaTeX + JSON + markdowns): ~15 min.
- **Total wall time: ~30 min.** Zero external API calls; all local numpy/scipy; no paid endpoint used.

## Provenance
Everything runs locally on `CherryRd`. No LLM judge invoked (not needed
for a scaling-law replication; verdict is fully determined by the slopes
in `trotter_scaling.json`, which are numerically unambiguous).
