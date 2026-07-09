# PROGRESS — LUCID replication: Ac-225 vs Lu-177 in vitro dose-effect

- **Status:** DONE
- **Verdict:** PARTIAL / SPOT-CHECK
- **Started:** 2026-05-30 17:21 CDT
- **Finished:** 2026-05-30 17:35 CDT
- **Target:** Ruigrok et al., "In vitro dose-effect relationships of actinium-225 and lutetium-177", DOI 10.1007/s00259-022-05821-w
- **Output:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-actinium-lutetium-dose-effect/`

## Log

- 17:21 — workspace created, PROGRESS.md and JSON progress files initialized.
- 17:22 — PDF extracted with pdftotext; full text + Tables 1-3 transcribed.
- 17:24 — GO decision: paper has explicit fitted α parameters, RBE, dose tables,
  and S-values; ample quantitative content to replicate.
- 17:26 — Figure 3 (clonogenic survival panels) and Figure 4 (dose-response)
  rendered to PNG via `pdftoppm -r 250` and read by the image tool. Two
  independent digitization reads recorded.
- 17:30 — Replication code written: `code/replicate_lucid.py`.
- 17:32 — Run #1. Read1 gave α(Lu)=0.33, α(Ac)=1.09, RBE=3.33. Off but RBE
  ratio close.
- 17:33 — Run #2 with read2 digitization. α(Ac)=0.64±0.05, matches paper
  (0.67±0.06) within 1σ. α(Lu)=0.22, within 2σ. RBE recovered 2.96–3.33.
- 17:34 — Dosimetry pipeline check shows constant-ratio agreement
  (1.28× Lu, 2.4× Ac). Confirms math chain; identifies the simplifications
  (instant-uptake approximation vs paper's full TAC) as the source of the
  constant factor.
- 17:35 — REPORT.md and README.md written. Progress JSON updated to status=done.
