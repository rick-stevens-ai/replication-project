# Workflow — lucid-pariset-53bp1-mouse-strains

## Paper
- Pariset E et al., *53BP1 Repair Kinetics for Prediction of In Vivo Radiation
  Susceptibility in 15 Mouse Strains.* Radiat. Res. 194, 485–499 (2020).
- DOI: 10.1667/RADE-20-00122.1
- PDF: `data/paper.pdf` (12 MB, 16 pages)

## Set
LUCID (radiation-biology replication portfolio).

## Verdict
**REPLICATED — PARTIAL** (preserved verbatim from prior REPORT.md).

## Workflow

### Pass 1 (original)
1. **Read + parse** paper with `pdftotext -layout` → `data/repass/paper_layout.txt`.
2. **Digitize** Fig. 4 A/B bar charts by hand → per-strain (τ, q) for HZE and
   4-Gy X-ray, 15 strains → `data/digitized_fig4.csv`.
3. **Implement** all five model equations from paper (Eq. 1–6) in
   `code/replicate_pariset.py`. Verified by unit-forward simulation.
4. **Recompute** Table 1B correlations from digitized (τ, q):
   Pearson `r(τ_4Gy, q_4Gy) = -0.758` vs paper `-0.75`.
5. **Identifiability MC** — synthetic per-cell foci curves under paper's stated
   Poisson noise, refit; recover (τ, q, RIFmax) within ±10% for τ∈[2,8]h.
6. **Emit** `figures/fig4_recreated.png`, `figures/model_kinetics_examples.png`,
   `results/replication_results.txt`.

### Pass 2 (re-pass, 2026-06-23)
1. **Full-text parser sweep** to confirm no supplement, no data-deposit URL exists.
2. **Add CLAIMS C–L**: LET ratio, Eq. (3) prefactor, sublinear dose, Table 2
   quadrant classification, Fig. 7C n=4 inferential ceiling, Fig. 7C "positive
   for most" count, Fig. 7B derived p-value, forward-sim Eq. (5/6), and honest
   data-block CLAIM L for Table 1A.
3. **Regression check** against pass-1 correlations — no drift (4 decimal places).
4. **Parser provenance** table pinning every consumed number to a line in
   `paper_layout.txt`.
5. **Preserve** `REPORT.pass1.md` for diff.

### Backfill (2026-07-06, this action)
1. Read existing `REPORT.md` (single tool call).
2. Emit report bundle: `REPORT.tex`, `open_questions.json`,
   `open_questions_section.tex`, `workflow.md`, `artifacts_summary.md`,
   `failure_analysis.md`.
3. Emit `extraction/nougat.mmd` stub (pointer only; no GPU parse).
4. Preserve all existing files.

## Tools + versions
| Tool | Version | Purpose |
|---|---|---|
| `pdftotext` (Poppler) | 24.x on CherryRd | Layout + plain text extraction |
| Python | 3.11 | Model + statistics |
| numpy | 1.26+ | Linear algebra |
| pandas | 2.0+ | Table I/O |
| scipy | 1.11+ | Pearson/Spearman + special functions |
| WebPlotDigitizer | 4.6 (manual) | Fig. 4 A/B bar-height digitization |

No LLM used for numeric extraction. No GPU. No paid endpoint. No external API call.

## Compute
- Host: CherryRd (local M1/x64 dev box).
- Free-endpoint policy honored (no CELS/Argo call needed; this is pure numeric replication).

## Work estimate
- Pass 1: ~4 hours (equations + digitization + code + write-up).
- Pass 2 (re-pass): ~3 hours (additional claims C–L + parser provenance + honest
  Fig. 7C inferential analysis).
- Backfill (report bundle, this action): ~30 minutes.
- **Total: ~7.5 human-hours + 0 GPU-hours + 0 paid-endpoint spend.**

## Reproducer
```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-pariset-53bp1-mouse-strains

# Pass 1
python3 code/replicate_pariset.py

# Pass 2 (re-pass)
python3 code/repass/repass_pariset.py

# Inspect
cat results/repass/repass_results.txt
cat results/repass/repass_results.json
column -s, -t results/repass/claim_F_table2_classification.csv | less -S
column -s, -t results/repass/claim_G_cancer_pvalues.csv | less -S
column -s, -t results/repass/claim_J_forward_sim_4Gy.csv | less -S

# Rebuild the LaTeX report
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex  # 2x for cross-refs
```

Dependencies: `numpy`, `pandas`, `scipy`. Install with
`pip install numpy pandas scipy` (or `uv pip install`).
