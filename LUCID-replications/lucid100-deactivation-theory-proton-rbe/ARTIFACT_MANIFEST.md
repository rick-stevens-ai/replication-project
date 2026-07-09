# ARTIFACT_MANIFEST — Slot 36

Source paper: arXiv 1901.08194v1 / DOI 10.1140/epjd/e2019-90263-5

| Path | SHA-256 | Bytes | Notes |
|---|---|---|---|
| artifacts/paper.pdf | efd4ec417f3fbce6e0a1a5f1a409fd2560257add2d7b2e2933b141963b3621d5 | 9 698 814 | arXiv OA copy (Springer paywalled) |
| artifacts/paper.txt | 6060104f734acc21224ca67d1c476f07de5bdd543d93cf4c4c60639cfda0dfcb | — | `pdftotext -layout` extraction, 1730 lines |
| artifacts/springer_landing.html | ef12c600df852c075cf1725db383991dd47ff1938056261599c582b1e9c176b5 | 374 876 | Springer paywall page (saved as evidence of failed PDF route) |
| code/smoke_deactivation.py | 10fa919dc335f5247470e2ce5d0751cbaf4e5a22b9c263df8f57be81f997d1a6 | 7 881 | Minimal SF(D,LET) replication, H460 NSCLC, 6 smoke checks |
| smoke_test.json | 3241aeadd3b396b68f948d0613f10817540c8f52df7885c443b5193096639165 | — | All 6 checks PASS |
| figures/alpha_beta_vs_LET.png | 0bfa3c110129f5e0251627b35dd30520c129a337c5f06ccdaa0e04359620011d | — | α, β vs LET_d (compare paper Fig. 5) |
| figures/sf_vs_dose_H460.png | 6702e7abb365324599df98bf72a67d9dfbb427f9fc28b6d84402a2e4dbc219cb | — | SF(D) curves at 5 LET values (compare Fig. 6) |
| figures/rbe_vs_LET.png | 461e61167b366078dbf85d59cbeb46e0c639ae0ba3ff1df6f1d112dd3ad55e04 | — | RBE_10% vs LET_d |

## Code / data references absent in paper

- No GitHub or Bitbucket repo cited
- No supplementary material file
- No data deposit (Zenodo, Figshare, Dryad, OSF) cited
- Authors point only to companion paper Abolfath et al. 2017 Sci. Rep. 7:8340 (ref [42]) for the 3D global-fit method — also no code/data deposit there

## Underlying experimental data (external, not harvested here)

| Dataset | Source | Status |
|---|---|---|
| H460 / H1437 NSCLC clonogenic SF(D, LET) | Guan et al. Sci. Rep. 5:9850 (2015) | Open access (Nature), would need download for full numerical replication |
| Bronk et al. unpublished γ-H2AX persistent foci | Cited in §III B; not yet published as of paper date | Inaccessible — would require author contact (skipped per task brief) |
