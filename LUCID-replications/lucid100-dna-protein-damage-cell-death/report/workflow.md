# Workflow, tools, and reproducer

## Paper
Shuryak & Brenner (2012), *Mechanistic Analysis of the Contributions of DNA and Protein
Damage to Radiation-Induced Cell Death*. Radiat. Res. 178(1):17-24.
DOI: 10.1667/RR2877.1 · PMID 22687051 · PMC3580191.

## Environment
- **Host:** CherryRd (macOS, CPU only). No GPU used.
- **Python:** system Python 3 with NumPy + Matplotlib (standard scientific stack).
- **Compute:** ~1 second of CPU for the full forward simulation over all 10 rows.
- **Endpoints (paid or free):** none. Model math is pure NumPy; report writing uses local
  editor. LaTeX build is optional and local (`pdflatex report/REPORT.tex`).

## Tools
| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.x | model + smoke run |
| NumPy | latest | vector math |
| Matplotlib | latest | survival plots |
| `curl` | system | PMC OAI-PMH fetch + Unpaywall API |
| LaTeX (pdflatex) | any | build `REPORT.pdf` from `REPORT.tex` |

## Work estimate
- Paper harvest (PMC JATS + Unpaywall + EuropePMC): ~30 min
- JATS -> Python model transcription: ~1 hr
- Smoke run + summary CSVs + plots: ~15 min
- Report write-up (this backfill): ~30 min
- **Total first-pass replication:** ~2.5 hr of a single subagent
- **Missing quantitative refit** (blocked): would add ~1 day
  (WebPlotDigitizer on Krisko & Radman 2010 Fig. 2 in an interactive browser --- ~4 hr;
  SciPy `dual_annealing` refit with bootstrap CIs --- ~2 hr; figure overlays --- ~1 hr)

## Reproducer
```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-dna-protein-damage-cell-death

# (1) Rebuild all 11 CSVs + 2 plots (idempotent, ~1 s):
python3 scripts/smoke_shuryak_2012.py --plot

# (2) Inspect the qualitative map:
cat results/summary.csv

# (3) Re-render this report to PDF (optional; requires local LaTeX):
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex

# (4) Re-fetch the source paper's JATS XML (idempotent, ~2 s):
curl -sL 'https://www.ncbi.nlm.nih.gov/pmc/utils/oai/oai.cgi?verb=GetRecord&identifier=oai:pubmedcentral.nih.gov:3580191&metadataPrefix=pmc' \
  -o artifacts/paper_oai.xml

# (5) Re-check open-access status via Unpaywall:
curl -sL 'https://api.unpaywall.org/v2/10.1667/RR2877.1?email=rick.stevens.ai@gmail.com' \
  -o artifacts/unpaywall.json
```

## Blockers (durable notes)
- **Krisko & Radman 2010 PNAS 107:14373 raw F(D) and S(D)** are figure-only, no tabular SI.
  All headless attempts against PMC/EuropePMC image endpoints return reCAPTCHA HTML.
  PNAS direct PDF returns HTTP 403 to `curl`. Requires an interactive browser session
  plus WebPlotDigitizer.
- **Authors' FORTRAN random-restart simulated-annealing fitter** is not on GitHub, Zenodo,
  or Figshare. GitHub user search `igorshuryak` returns 0 hits; code search
  `Shuryak Krisko Radman` returns 0 hits. Would need to be requested by email from
  Igor Shuryak at Columbia CRR.

## Verification checklist
- [x] All 5 model equations transcribed verbatim from JATS XML
- [x] All 10 strain/radiation rows forward-simulated
- [x] `results/summary.csv` produces monotone-decreasing `S` in `D` for every row
- [x] `Q1 * Q2 == S` to display precision (invariant of the model)
- [x] `Q1 == 1` throughout $\lambda$ IC rows (structural: $S = Q_2$ for lambda IC)
- [x] Dominant-mechanism assignments match paper Table 2 in all 10 cells
- [ ] Numeric $S$ values match paper within one order of magnitude (blocked on real $F(D)$)
- [ ] 95% CIs on $(K_\text{dam}, K_\text{rep}, X)$ re-derived (blocked on real $F(D)$ + refit)
- [ ] Figures 3, 4, 5 re-rendered (not done this pass; requires additional plotting code)
