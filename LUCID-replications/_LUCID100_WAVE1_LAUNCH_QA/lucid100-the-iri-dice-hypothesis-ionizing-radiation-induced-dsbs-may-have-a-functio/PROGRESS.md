# Progress — The IRI-DICE hypothesis (Langen et al. 2020)

## 2026-06-09 — first-pass complete (slot 8 subagent)

- Artifact harvest: paper.pdf (645 KB, SHA-256 `ba50883…fadc36`) and paper.txt downloaded from Springer (CC-BY 4.0 OA). No supplementary, no code, no data accession exists — paper has 1 cartoon figure, 0 tables, 0 equations.
- Worktype "omics/signature replication" inherited from master TSV is **mis-categorised**: this is a pure hypothesis paper with no signature to replicate. Recommendation logged in `FIRST_PASS_REPORT.md` to re-tag in master TSV.
- Replication scope decided: **minimal toy MC scaffold** of the computational programme the authors themselves outline in §"Approaches to test IRI-DICE". Other scope options (exact rerun, figure digitization, full reimplementation) are N/A because no quantitative target exists.
- Smoke run `python3 code/iri_dice_toy_mc.py --ncells 3000 --seed 0` executed in <2 s; produced 3 PNGs and `summary.json` under `artifacts/figs/`.
- Smoke run reproduces 3 of the 4 computationally-testable narrative claims of the paper at default parameters:
  - diversity (per-cell heterogeneity of responses) ✓
  - suppression dominance over overexpression (~25×) ✓
  - repair-threshold non-monotonicity (perturbation peaks near ~0.5 Gy and drops at higher doses) ✓
  - claim 5 (LET dependence) not implemented in smoke run; trivial scaffold extension.
- No author contact. No paid endpoints. No heavy compute. Pure local Python + numpy on CherryRd.

Status: **first-pass replication complete**. No further automated work warranted on *this* paper. Logical follow-on (separate slot, not this one) would be Iannelli et al. 2017 (Nat Commun 8:15656) — the cis-effect dataset IRI-DICE rests on, which does have public GEO data.

Next: see `FIRST_PASS_REPORT.md` § "Next actions" for the prioritized list.
