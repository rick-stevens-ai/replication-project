# Artifact harvest

| # | Kind | URL / source | Local path | Size | Notes |
|---|------|--------------|------------|------|-------|
| 1 | Paper PDF | https://arxiv.org/pdf/quant-ph/9607014 | paper.pdf | 77176 B | 2 pages, v2 (7 Jan 1999) |
| 2 | Marker parse | copied from sibling `QC-200/.../extraction/marker.md` (pdftotext fallback — Marker binary not installed in that env) | extraction/marker.md | 13488 B | full paper text |
| 3 | Nougat parse | copied from sibling `QC-200/.../extraction/nougat.mmd` | extraction/nougat.mmd | 7209 B | equations preserved |

No external datasets used — this paper is a pure algorithms/complexity result, so replication data = random permutation tables generated in-process (seeded, reproducible).

## Software / models used

| Component | Version / id |
|-----------|--------------|
| Python | 3.14.6 (Homebrew) |
| numpy | 2.4.3 |
| LLM judge endpoint | http://localhost:44497/v1 (Argo, key=stevens, FREE) |
| Judge model (accepted) | argo:gpt-5.2 (fallback after argo:claude-opus-4.7/4.8 502) |

## Checksums (SHA-256)

```
ff5c2ff71415e22f0ddf799b31e9b82d1990db9c1fc9d62ea2aabea5907e06cf  paper.pdf
7893a81c98090bafe91bb72bb19e14aa950f456ce728be6c4835706c800e446d  extraction/marker.md
db639da18b407d23c83f4a77f1f1ef7f0f219fa6f45a646411717322bcf2eb87  extraction/nougat.mmd
```
