# Artifact Harvest

Public artifacts fetched and used in this replication.

| # | Artifact | URL | Size | SHA-256 (head 16) | Notes |
|---|---|---|---|---|---|
| 1 | `paper.pdf` | https://www.osti.gov/servlets/purl/2928634 | 27,531,740 B | see below | Full journal PDF via OSTI purl. Fetched from uicgpu (proxied). |
| 2 | Extracted plain text | (derived) `tmp-osti-2928634.txt` on cherryrd | 82,104 B | (derived) | PyMuPDF text extraction of paper.pdf. |
| 3 | Julia code repo (cited as "Diamzon, 2024") | Not fetched | — | — | Paper cites its own repo but does NOT print a URL. We deliberately did not chase it — the replication is stronger as an independent re-implementation from the paper text. |
| 4 | Lux.jl / Makie.jl | (referenced by paper's cite of Danisch & Krumbiegel 2021; Pal 2023) | — | — | Not fetched; not needed for PyTorch re-implementation. |

Checksum of the paper PDF (for future reference):
```
$ sha256sum paper.pdf
```
Ran on m1 host, output SHA-256 not persisted here (can be regenerated with above command).

**No data was downloaded from external biology / physics databases.** The reproducible core is a synthetic operator (Eq. 63) and a fresh MLP; both are generated at run-time from the code in `work/`. The only external artifact is the paper PDF itself.
