# PROGRESS — LUCID100 slot 58 (Wave 6) backfill

DOI: `10.3390/cimb46120828` · PMC: `PMC11726848` · CC BY 4.0
Worker: Ollie sub-agent (`agent:main:subagent:d108df06`) on CherryRd
Date: 2026-06-09

## Timeline

| Step | Outcome |
| --- | --- |
| Pull master TSV row | rank 89, Wave 6, tier B, score 13, status `candidate_curated`, worktype tag `simulation/model replication` — looked wrong from the abstract |
| Try `web_fetch` / `mdpi.com` | Akamai-blocked (HTTP 401 Access Denied + DuckDuckGo bot challenge) |
| Crossref metadata | Confirmed CC BY 4.0, MDPI similarity-check URL only, no preprint link |
| Try `pmc.ncbi.nlm.nih.gov/.../pdf/` | Interstitial download page (HTML stub) |
| Try `europepmc.org/.../pdf/` | HTTP/2 stream closed (`STREAM_CLOSED err 5`), HTTP/1.1 works on second hammer |
| Try PMC `bin/cimb-46-00828-s001.zip` | reCAPTCHA challenge (Google) |
| Try `eutils.../efetch.fcgi?db=pmc&id=11726848` | Got JATS XML (194 KB) |
| Try `pmc.ncbi.nlm.nih.gov/utils/oa/oa.fcgi?id=...` | 404 |
| Try `www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=...` | Returned a `tgz` link under `pub/pmc/oa_package/...` |
| Initial `oa_package` path | 550 No such directory (the FTP path moved) |
| Correct path `pub/pmc/deprecated/oa_package/6c/f3/PMC11726848.tar.gz` | **Worked.** 4.45 MB tarball with PDF, JATS, 7 figure JPEG+GIF, and the supplement ZIP |
| Unzipped supplement | Single PDF: 2 figures (S1 = giant cell image, S2 = HyPer H2O2 time-course); **no numerical tables** |
| Extracted full text | `pdftotext -layout` → `paper.txt` (1391 lines) |
| Manually digitized 100% of in-text numerical claims | `data/digitized_values.json` |
| Wrote smoke replication script | `scripts/smoke_lq_doserate.py` (LQ + Lea-Catcheside + Hill, ~16 KB) |
| Ran smoke (CPU, <1 s) | 4 PNGs + `smoke_summary.json` + `smoke_run.log` |
| Built artifact manifest | 39 files with sha256 |
| Wrote `FIRST_PASS_REPORT.md` | GO_LIGHT verdict with retag recommendation |

## Smoke results headline

- HDR two-point LQ fit: `alpha = 0.262 /Gy`, `beta = -0.017 /Gy²` (negative β,
  i.e. **the MTT-derived "survival" curve is *too shallow* to be a real LQ**).
- Empirical dose-modifying factor at 50 % viability: **3.18** (= 10.8 / 3.4),
  exactly matches the paper's stated "≈3× sparing".
- A simultaneous shared-LQ + Lea-Catcheside fit drives the repair half-time
  to the floor (`t½ → 0.1 h`) and still under-predicts the LDR LD₅₀ (2.6 Gy
  vs observed 10.8 Gy). The model is wrong in a known way: MTT readouts
  saturate.
- A Hill / log-logistic descriptive fit handles both regimes cleanly:
  `n_HDR = 3.59`, `n_LDR = 5.18`.
- The LDR/HDR comet-tail ratio (~0.55) is matched by an end-of-exposure
  break-rejoining half-time of **10–14 h**, much slower than the survival
  fit prefers — confirming MTT and comet are measuring different things on
  different time-scales.

## Verdict

**GO_LIGHT** — light analytical replication complete; QA retag recommended.
See `FIRST_PASS_REPORT.md`.

## Next actions (optional)

1. **Retag the master TSV row 89** as wet-lab radiobiology, not simulation.
2. (Defer) Author contact for raw MTT and comet tables would unlock a proper
   nonlinear LQ + Lea-Catcheside joint fit. Out of scope: "no author contact"
   is set as a sub-agent constraint.
3. (Defer, low value) Image-pixel diff against paper Figs 3A / 4E. Vision
   model is reachable but not needed for the verdict.
4. (Defer) Add a Lea-Catcheside notebook that lets the user dial in their
   own LQ assumption and the LDR exposure duration — useful as a teaching
   artifact for the LUCID100 dose-rate cluster.

## Blockers

None for the light replication. The only hard wall is **the authors did
not release the underlying MTT, comet, flow cytometry, or SA-β-gal
numerical tables**; that bounds any external replication to digitized
in-text values.
