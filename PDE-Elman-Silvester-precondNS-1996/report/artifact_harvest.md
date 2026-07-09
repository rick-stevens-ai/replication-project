# Artifact harvest

| Artifact | Source | Verified | Notes |
|---|---|---|---|
| Paper PDF `elman_silvester_1996.pdf` | UMD DRUM open-access: https://drum.lib.umd.edu/bitstreams/6d1ae6c6-5e07-4089-9163-5f84445047e5/download | MD5 `7e3868edaa8abdd23489c4e22faafaff`, 476,300 B, 19 pages | Author preprint / tech-report version (CS-TR-3283, UMIACS-TR-94-66, June 1994) that matches the published SIAM 1996 paper. Published SIAM version paywalled. |
| Semantic Scholar metadata | https://api.semanticscholar.org/graph/v1/paper/DOI:10.1137/0917004 | citationCount = 259 as of 2026-07-04 | S2 auth used (S2 key from keychain) |
| Reference author codebase | IFISS MATLAB toolkit (Elman/Silvester/Wathen) — https://www.manchester.ac.uk/ifiss/ | not downloaded — implemented from scratch | The IFISS package is the canonical implementation of this preconditioner family; our replication is intentionally an independent Python reimplementation, not a rerun of IFISS. |

No datasets to download — this is a synthetic PDE benchmark. All numerical inputs (geometry,
BCs, wind field, viscosities, meshes) are specified in the paper.


## Verdict

**Verdict: NO-GO**. — no replication evidence; code written but never run, empty evidence dir, no results.json

<!-- census-verdict: NO-GO assigned 2026-07-08 by LLM judge (Argo Opus) -->
