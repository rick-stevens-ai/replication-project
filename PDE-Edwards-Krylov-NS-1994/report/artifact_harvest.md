# Artifact harvest — Edwards et al. 1994 replication

## Primary source (open access via author page)

| Item | URL | Size | MD5 | Verified |
|---|---|---|---|---|
| `edwards1994.pdf` — full paper OA copy (author-hosted) | https://blog.espci.fr/laurette/files/2018/01/Krylov_timeint.pdf | 1,922,723 B | d99670393fffcd13c9c89e25a7398f0d | 2026-07-04, PDF v1.3, matches title/authors/JCP 110 82-102 (1994) |
| Publisher DOI landing (Elsevier / ScienceDirect) | https://www.sciencedirect.com/science/article/pii/S0021999184710072 | HTML only (bot-shielded); metadata confirms "Under a Creative Commons license" | – | 2026-07-04 |
| Publisher author page (Tuckerman ESPCI) | https://blog.espci.fr/laurette/publications/ | 109,743 B HTML | – | 2026-07-04 |

## Related author references cited by paper (not directly fetched, cross-check only)
- Sorensen, D.C. 1992, SIAM J Matrix Anal Appl 13, 357 — the IRAM algorithm (ARPACK's ancestor). Available in ARPACK's user guide and the reference is directly used via `scipy.sparse.linalg.eigs`.
- Friesner, R.A., Tuckerman, L.S., et al. 1989, J Sci Comput 4, 327 — nonlinear exponential propagation, ancestor of Sec 3.2.

## Software / libraries used in replication (all standard, open)

| Library | Version | Purpose |
|---|---|---|
| Python | 3.14.6 | driver |
| NumPy | 2.5.1 | dense linear algebra, eig |
| SciPy | 1.18.0 | `sparse.linalg.gmres` (Newton-GMRES), `sparse.linalg.eigs` (ARPACK/IRAM), `linalg.expm` (dense reference exp) |
| ARPACK | as bundled in SciPy | IRAM (Sorensen 1992) — this IS the algorithm the paper cites as ref [56] |

## Judge

| Item | Details |
|---|---|
| Argo endpoint | `http://127.0.0.1:44497/v1/chat/completions`, key `stevens` |
| Judge model | `argo:gpt-5.2` (`argo:claude-opus-4.8` returned upstream 502 on this request; sonnet/haiku not tried once GPT-5.2 succeeded) |
| Judge JSON | `report/evidence/judge_verdict.json` |
