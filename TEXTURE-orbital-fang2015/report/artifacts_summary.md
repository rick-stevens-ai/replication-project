# Artifacts Summary — TEXTURE-orbital-fang2015

| Artifact | Path | Description |
|---|---|---|
| Paper | `paper.pdf` | Fang et al. 2015 review (arXiv:1508.07414) |
| Text extract | `extraction/marker.md` | pdftotext extraction of full paper |
| Method extract | `report/method_extract.md` | Pre-existing method/target notes |
| Model code | `code/osep_model.py` | Minimal 2nd-order Jahn-Teller vibronic OSEP model |
| Results JSON | `work/results.json` | Per-claim pass/fail + quantitative outcomes |
| BTO curves | `work/bto_curves.csv` | E(Q) vs Ti displacement for OSEP shifts 0..2.5 eV |
| BTO well depth | `work/bto_welldepth.csv` | Depth/\|Q*\| per shift + fine critical-shift scan |
| PTO curves | `work/pto_curves.csv` | PTO base / Ti-3d-down / Pb-6s-up E(Q) |
| Figure 1b replica | `work/fig_bto_doublewell.png` | Double wells collapsing with OSEP up-shift |
| Well-depth trend | `work/fig_bto_welldepth_vs_shift.png` | Depth vs OSEP shift, ~2 eV quench marked |
| Report | `report/REPORT.tex` | Full write-up + verdict |
| Open questions | `report/open_questions.json` | 5 new questions w/ basis + next steps |
| Workflow | `report/workflow.md` | Reproduction steps |
| Failure analysis | `report/failure_analysis.md` | What went wrong / limits |

## Claim outcomes (from work/results.json)
- **C1 BTO double well** — PASS. Depth 10.5 meV, |Q*| = 0.122 A.
- **C2 OSEP ~2 eV quench** — PASS. s_crit = 2.00 eV (analytic), 1.69 eV (grid);
  depth collapses 10.5 -> 4.2 -> 1.4 -> 0.27 -> 0 meV over shifts 0 -> 2 eV.
- **C3 hybridization mechanism** — PASS. corr(depth, 1/gap) = 0.999, monotone.
- **C4 PTO Ti-3d >> Pb-6s** — PASS. Deepening 28.3 meV (Ti-3d down) vs 2.95 meV
  (Pb-6s up); both positive, Ti dominant.

## Verdict
**REPLICATED (mechanism-level, tractable surrogate).**
Coverage **6/10** · Agreement **8/10**.
