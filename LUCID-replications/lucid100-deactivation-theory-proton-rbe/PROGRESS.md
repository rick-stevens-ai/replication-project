# PROGRESS — Slot 36 (Deactivation Theory)

| Time (CDT) | Step | Status |
|---|---|---|
| 2026-06-09 13:53 | Subagent launched; launching record present in subagent-progress | ✅ |
| 2026-06-09 13:53 | Created repo folder `lucid100-deactivation-theory-proton-rbe/{artifacts,code,figures,reports}` | ✅ |
| 2026-06-09 13:54 | Attempted Springer PDF — returned HTML paywall stub (saved as `springer_landing.html`) | ⚠️ paywalled |
| 2026-06-09 13:54 | Unpaywall lookup → arXiv 1901.08194 OA copy | ✅ |
| 2026-06-09 13:54 | Downloaded `artifacts/paper.pdf` (9.7 MB, SHA-256 efd4ec…21e5) | ✅ |
| 2026-06-09 13:54 | `pdftotext -layout` → `artifacts/paper.txt` (1730 lines) | ✅ |
| 2026-06-09 13:55 | Searched manuscript: NO GitHub / supplement / deposited data references | ❌ no code |
| 2026-06-09 13:55 | Extracted core equations: Eq.1 (DSB master), Eq.6–8 (renormalized rates), Eq.15 (LQ power series), Eq.21–22 (α/β in z_D), Eq.32 (working linear LET form), Eq.40 (birth-death), Eq.46–53 (SFeff, TCP) | ✅ |
| 2026-06-09 13:56 | Wrote `code/smoke_deactivation.py` implementing Eq. 32 + Eq. 21–22 truncation, parametrized for H460 NSCLC | ✅ |
| 2026-06-09 13:56 | Ran smoke; produced 3 figures + JSON | ✅ |
| 2026-06-09 13:57 | Authored README.md, ARTIFACT_MANIFEST.md, FIRST_PASS_REPORT.md | ✅ |
| 2026-06-09 13:57 | Updated subagent-progress JSON to `first_pass_complete` | ✅ |

## Next actions (if escalated)

1. Pull Guan et al. 2015 (Sci. Rep. 5:9850) raw clonogenic data; fit α_i, b_i coefficients of Eqs. 21–22 to enable quantitative Fig.6 reproduction.
2. Replicate Abolfath et al. 2017 (Sci. Rep. 7:8340, ref [42]) 3D global-fit procedure to recover authors' polynomial coefficients.
3. (Optional) Monte-Carlo the Eq. 40 birth–death chain (N₀ ~ 10⁶ cells, 1 mm voxel) to validate Eq. 50 SF_eff under realistic in-vitro dose-rate timing.
4. No author contact required for any of the above.

## Blockers

- Authors do not publish coefficient tables or fit residuals — quantitative reproduction of Figs. 6–9 requires re-running the 3D global fit from raw data.
- No published code repository.
