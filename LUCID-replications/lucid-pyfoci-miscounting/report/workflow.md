# Workflow — PyFoci miscounting replication

## Pipeline (as executed)

1. **PDF acquisition** — LUCID corpus already staged `artifacts/paper.pdf`
   (SHA-256 pointed to in `extraction/nougat.mmd`); DOI 10.1038/s42003-022-03585-5.
2. **Text extraction** — `pdftotext -layout artifacts/paper.pdf artifacts/parse/paper.txt`
   (663 lines). Marker MMD not required; paper has a clean native text layer.
3. **Artifact harvest** —
   - PyFoci source: `git clone gitlab.com/PRECISE-RT/releases/pyfoci code/pyfoci`
   - Colab mirror: `git clone github.com/SamPIngram/PyFoci_Colab code/PyFoci_Colab`
   - Figshare bundle: `curl -L doi.org/10.48420/14398790 -o data/figshare.zip && unzip`
   - Yields 24 microscope/mag count parquets, 1 deconv parquet, 1 3D-stack
     parquet, 7 `P_Values_Fig*` tables, `Repair - DSBMarker/*`, `Vertices/`,
     `SDDs/`.
4. **Re-pass compute** — `code/repass_extended.py` (520 LOC, pure stdlib +
   pandas + pyarrow + numpy + scipy + matplotlib). Runs entirely on CherryRd
   local CPU. No API calls.
5. **Verdict aggregation** — per-claim JSON summaries land in
   `results/repass/*_summary.json`; top-line `results/repass/ALL_CLAIMS_SUMMARY.json`.
6. **Figure regeneration (partial)** — `figures/repass/fig3_kinetics.png`,
   `fig4_airyscan_mag.png`, `fig5_voxel.png` — analog reproductions only.
7. **Report writing** — this backfill (2026-07-06) — REPORT.tex + open_questions
   + workflow/artifacts/failure_analysis + extraction stub.

## Tools & versions (verified during re-pass 2026-06-23)

| Tool | Version | Purpose |
|---|---|---|
| poppler `pdftotext` | 24.x (macOS Homebrew) | PDF -> text |
| Python | 3.14 (CherryRd local) | driver runtime |
| pandas | 2.x | parquet I/O |
| pyarrow | 17.x | parquet backend |
| numpy | 2.x | numerics |
| scipy | 1.14.x | Mann-Whitney U, Spearman |
| matplotlib | 3.9.x | analog figure regen |
| Argo proxy | localhost:44497 (unused for this re-pass) | reasoning fallback if needed |

**Not used** (this run): Argo, Sophia, CELS, OpenRouter, any paid API.
**Blocked env** (F6): Python 3.11 + numba (would unlock Claim 5 raw-pipeline rerun).

## Work estimate

| Phase | Wall-clock | Notes |
|---|---|---|
| Initial pass (2026-05-29) | ~2 h | Dataset-only, verdict PARTIAL |
| Re-pass extension (2026-06-23) | ~4 h | Adds Claims 7-13 with quantitative repro |
| Backfill artifacts (2026-07-06) | ~30 min | REPORT.tex + 6 companion files |
| **Total to REPLICATED** | **~6.5 h** | Excludes Claim-5 raw-pipeline rerun |
| Claim-5 rerun (estimated) | +4-8 h | Setup Python 3.11 venv, pip install pyfoci, rerun 4 radiations x 24 configs; not attempted |

## Reproducer

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-pyfoci-miscounting

# Verify artifacts on disk
ls data/extracted/*.parquet | wc -l          # expect 24
ls data/extracted/Explicit_PValues/          # expect P_Values_Fig* files
ls artifacts/paper.pdf artifacts/parse/paper.txt

# Rerun the numerical re-pass (no API calls, ~5 min local)
.venv/bin/python code/repass_extended.py

# Auditor checks
cat results/repass/ALL_CLAIMS_SUMMARY.json
head -20 results/repass/mw_fig1.csv
ls figures/repass/
```

Auditor expectation: `ALL_CLAIMS_SUMMARY.json` reports 12 REPLICATED, 1 BLOCKED
(Claim 5), and `mw_fig1.csv` shows 120/120 direction and 120/120 within-1.5-OoM.

## Optional: unblock Claim 5

```bash
python3.11 -m venv .venv311
source .venv311/bin/activate
pip install numba pandas numpy scipy scikit-image
pip install -e code/pyfoci
python code/pyfoci/run_pipeline.py --config code/pyfoci/configs/airyscan_x63.yaml \
    --radiations Co60,P1.7,P7.15,P27.95 --dose 2.0 --nreps 100 \
    --out data/rerun_pipeline/
# Then diff data/rerun_pipeline/*.parquet against data/extracted/*.parquet
```

If the diff is within stochastic tolerance (bootstrap on cells), Claim 5
flips from BLOCKED to REPLICATED and the overall verdict is unchanged at
REPLICATED but with 13/13 coverage.
