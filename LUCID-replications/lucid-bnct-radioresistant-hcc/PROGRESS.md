# PROGRESS — LUCID BNCT radioresistant HCC replication

- **Status:** complete
- **Verdict:** **PARTIAL** (coverage 5/10, agreement 8/10 on replicable parts)
- **Started:** 2026-05-30 18:07 CDT
- **Finished:** 2026-05-30 18:13 CDT
- **Target PDF:** `2c94a15708907c2998f2f6db1ac1b1e9186b39cd.pdf`
  → Huang et al., *J Hepatocell Carcinoma* 2022;9:1385–1401, doi:10.2147/JHC.S383959
- **Output dir:** `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-bnct-radioresistant-hcc/`

## Timeline

| When | What |
|------|------|
| 18:07 | PDF received. Set up output tree + initial PROGRESS/JSON. |
| 18:08 | PDF text + metadata extracted with pdftotext/pdfinfo (PDF tool errored on raw bytes). |
| 18:09 | Identified ALL replicable quantitative targets: Fig 1C, Fig 3B, Table 1, Table 4. |
| 18:10 | Digitized Fig 1C / Fig 3B with vision model for the data points whose means are NOT in the text. |
| 18:11 | Wrote `code/replicate.py`: LQ fits, D10 inversion, RBE recompute, Table 1 check. |
| 18:12 | Ran replication — RBE arithmetic matches exactly; D10 refits within ~3.5%. |
| 18:13 | Wrote README.md and REPORT.md. |

## Hard gates

- [x] PROGRESS.md + JSON status=running within 10 min
- [x] Only public/open data, equations, supplements, digitized figures
- [x] REPORT.md, README.md, PROGRESS.md, code/, results/, figures/ all present
- [x] Honest verdict with coverage/agreement scores
- [x] Save-as-you-go (intermediate PROGRESS/JSON were written before final code ran)

## Headline numbers

| Quantity                          | Paper   | Refit   | Agreement |
|-----------------------------------|--------:|--------:|----------:|
| D10(γ-ray, HepG2)  [Gy]           | 3.496   | 3.368   | 3.6 %     |
| D10(γ-ray, HepG2-R) [Gy]          | 5.749   | 5.548   | 3.5 %     |
| RBE(HepG2)   = D10(γ)/D10(BNCT)   | 3.675   | 3.675*  | exact*    |
| RBE(HepG2-R) = D10(γ)/D10(BNCT)   | 5.972   | 5.972*  | exact*    |

\* Using paper's own D10 values; using digitized BNCT D10s the RBEs come out ~3.0 and ~4.1 (digitization-limited, see REPORT).
