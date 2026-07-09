# LUCID100 slot 59 — Brahme (2026) "Improving radiation therapy efficacy ..."

- **Paper:** Brahme A. (2026) "Improving radiation therapy efficacy considering DNA repair, TP53 mutations, microscopic heterogeneity, and low- and high-dose apoptosis." *Frontiers in Oncology* 15:1703503. DOI: [10.3389/fonc.2025.1703503](https://doi.org/10.3389/fonc.2025.1703503)
- **Master row:** LUCID100 rank 90, Wave 6, slot 59 (TSV: `/Users/stevens/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv`)
- **Worktype in master:** `omics/signature replication` ← **MISLABELED**, should be retagged.
- **Recommended retag:** `mechanistic / radiotherapy theory review` (single-author conceptual review of light-ion radiation therapy with the author's RHR / extreme-value TCP framework).
- **Open access:** ✅ CC-BY, Frontiers OA PDF retrieved.
- **Code / data released by author:** ❌ None. No data-availability statement, no code repository, no supplementary data. All figures are stated as "modified from" Brahme's prior book/papers (refs 7, 9 in particular).

## Verdict (first-pass)

**GO (smoke-only; reduced replication)**. The paper is a narrative review whose *primary first-principles content* (DDSB physics, RHR formulation, LDA/HDA, fractionation window, He-Li-B ion advocacy) all references previous work. It contains exactly **one explicit closed-form equation** (Equation 1, the extreme-value rewriting of the Poisson tumor-control probability), plus four quoted statistical constants of that distribution. Those are fully reproducible and were reproduced here to ≥4 d.p.

A more ambitious replication (the RHR cell-survival formula, the apoptosis fits in Figs. 9–10, 13, 17, 18, the optimal weekly fractionation schedule of Fig. 14) requires the author's prior papers / book (refs 7, 9, 10, 15) for parameter values, fitted curves, and the experimental data points — none of which are released in machine-readable form here.

## What is in this folder

- `README.md` — this file
- `PROGRESS.md` — run-by-run log
- `ARTIFACT_MANIFEST.md` — every file with provenance + role
- `FIRST_PASS_REPORT.md` — verdict, scope, equations, gaps
- `artifacts/` — raw paper + bibliographic JSON
- `code/tcp_extreme_value_smoke.py` — reduced smoke replication of Eq. 1
- `results/tcp_eq1_smoke.json` — numerical pass/fail of Eq. 1 forms & stats
- `figures/tcp_eq1_vs_dose.png` — TCP(D) curve at N0 = 1e7, D0 = 1 Gy
- `logs/tcp_eq1_smoke.log` — run log

## How to re-run the smoke

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-rt-dna-repair-tp53-apoptosis-model
python3 code/tcp_extreme_value_smoke.py
```

Runtime <1 s on CPU. Requires `numpy` + (optional) `matplotlib`.

## QA recommendation back to the master TSV

- **Retag worktype** from `omics/signature replication` → `mechanistic / radiotherapy review (RHR / extreme-value TCP)`.
- **Keep**: relevant to LUCID radiation-biology coverage (TP53 ↔ DDR ↔ low-dose apoptosis ↔ fractionation), but flag as **author-perspective review with no released code/data**.
- No author contact attempted (per task brief).
