# Artifact harvest

Every public artifact pulled during this replication.

| Artifact | URL | Access | Size | SHA-256 |
|---|---|---|---|---|
| paper.pdf | https://arxiv.org/pdf/quant-ph/0410184 | HTTP GET, public | 111,420 B | `a13d655d7dd8f605374458f750fd2d8f98fa3253ec03bf76b151f7d81d43d9c0` |

No datasets, no supplementary material, no code repositories were released
by the authors of this 2004 paper (predates the widespread convention of
publishing accompanying code). All the code in this replication is our own
independent reimplementation of the Fig 1, 2, 4, 5 constructions.

## LLM API usage (all free per lab standing policy)

| Endpoint | Model | Calls | Purpose |
|---|---|---|---|
| Argo proxy (localhost:44497) | argo:claude-opus-4.8 | 1 (failed 500) | LLM-judge verdict |
| Argo proxy (localhost:44497) | argo:gpt-5.2 | 1 (success) | LLM-judge verdict |

## Tools / library versions harvested

| Package | Version | Source |
|---|---|---|
| Qiskit | 2.5.0 | pip |
| Qiskit-Aer | (latest via pip) | pip |
| Python | 3.14.x | system |
| pdftotext (poppler) | 25.x | system |
