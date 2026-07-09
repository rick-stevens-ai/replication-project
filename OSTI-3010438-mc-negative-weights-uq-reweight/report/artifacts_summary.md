# Artifacts summary — OSTI 3010438 replication

## Public artifacts pulled

| Artifact | URL | Size | Format | Local path |
|----------|-----|------|--------|------------|
| Paper PDF | https://www.osti.gov/servlets/purl/3010438 | 9,155,983 B | PDF v1.4 | `paper.pdf`, `work/paper.pdf` |

## Downstream artifacts NOT pulled (would be needed for C7)

| Artifact | URL | Notes |
|----------|-----|-------|
| ATLAS DAOD_PHYSLITE electroweak samples (Sherpa V+jets) | https://opendata.cern.ch (DOI 10.7483/OPENDATA.ATLAS.K5-SU.X65Y) | Ref [16]; multi-TB, requires OpenData tools |
| ATLAS DAOD_PHYSLITE Higgs nominal samples (Powheg VH) | https://opendata.cern.ch (DOI 10.7483/OPENDATA.ATLAS.Z2J9.709J) | Ref [18] |
| ATLAS event-generation metadata (cross sections) | https://opendata.atlas.cern/docs/data/for_research/evgen_metadata | Ref [30] |

## Generated artifacts

| File | Format | Bytes | Description |
|------|--------|-------|-------------|
| `extraction/pdftotext.txt` | text | ~50 kB | linear extraction of paper (equations preserved) |
| `extraction/marker.md` | markdown | 3 kB | proxy Marker extraction with key equations |
| `extraction/nougat.mmd` | mmd | 3 kB | proxy Nougat extraction with LaTeX-form equations |
| `work/replicate_double_slit.py` | python | 23 kB | main replication code, six subclaim tests |
| `work/make_plots.py` | python | 5 kB | Fig. 2/3 replication plots |
| `work/llm_judge.py` | python | 5 kB | Argo LLM-judge invocation |
| `report/evidence/c0_analytic_sanity.json` | json | 326 B | analytic identity checks |
| `report/evidence/c1_sample_scaling.json` | json | 3.5 kB | Eq. 1 MC-vs-analytic table |
| `report/evidence/c2_c3_c4_double_slit_summary.json` | json | 1 kB | main double-slit stats + 30-rep unbiasedness |
| `report/evidence/c4_double_slit_histograms.csv` | csv | 18 kB | per-bin nominal, reweighted, truth, pulls, var ratios |
| `report/evidence/c5_closure_summary.json` | json | 240 B | P+ closure pulls |
| `report/evidence/c5_pplus_histograms.csv` | csv | 6 kB | per-bin P+ histograms (nom/rw/pos/neg) |
| `report/evidence/c6_uncertainty_threshold.json` | json | 1.3 kB | Eq. 38 fully-correlated toy sweep |
| `report/evidence/fig2_replication.png` | png | 77 kB | replicated Fig. 2 (P_base/P_interf, g(p)) |
| `report/evidence/fig3_replication.png` | png | 117 kB | replicated Fig. 3 (nom/rw/truth histograms + pulls + var ratio) |
| `report/evidence/llm_judge.json` | json | ~3 kB | LLM-judge per-claim status + overall verdict |
| `report/evidence/run_stdout.txt` | text | ~3 kB | full replication run stdout |
