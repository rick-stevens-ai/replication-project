# Artifact Harvest

| Artifact | Source | Fetched via | Size | Notes |
|---|---|---|---|---|
| `work/yang-gao-2017.pdf` | https://thermalscience.rs/pdfs/papers-2016/TSCI160411246Y.pdf (redirect from thermalscience.vinca.rs) | `ssh uicgpu` (uicgpu proxied fetch; local direct fetch was blocked by 503 from doiserbia and expired-cert on vinca.rs) | 990,362 B | Full open-access PDF, CC BY-NC-ND 4.0. `pdftotext` extracted 1030 lines of text into `work/yg.txt` (mirror at `~/.openclaw/workspace/tmp/yg.txt`). |
| CrossRef metadata | https://api.crossref.org/works/10.2298/TSCI160411246Y | local `curl` | ~4 KB | Confirmed title, authors, journal issue, page range 133-140. |

No code was released with the paper; no supplementary data.  All artifacts are derived
from the open-access PDF and standard mathematical operations (SymPy 1.14.0, NumPy
2.4.3).

## Failed / attempted sources

- `https://doiserbia.nb.rs/img/doi/0354-9836/2017/0354-9836170024*.pdf` — 503 Service Unavailable (both host and https variants).
- `https://scindeks-clanci.ceon.rs/data/pdf/0354-9836/2017/0354-98361700133Y.pdf` — 404.
- `http://thermalscience.vinca.rs/pdfs/papers-2016/TSCI160411246Y.pdf` — expired SSL certificate blocked strict fetch; `-k` unlocked it and it 301-redirects to `https://thermalscience.rs/...` (successful path used above).
