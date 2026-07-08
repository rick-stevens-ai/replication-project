# Artifact Harvest

Every external artifact pulled during this replication, with URL, size, checksum.

## Direct downloads

| URL | Local path | Size | sha256 (16-char prefix) | Fetched |
|-----|-----------|------|------------------------|---------|
| https://arxiv.org/pdf/quant-ph/0503205 | `paper.pdf` | 138,309 B | `2ec4612be55f2cda` | 2026-07-06 14:08 CDT |

## Copies from central corpus

The 8-artifact standard says: "Source of truth for Marker/Nougat parses is the central corpus if already parsed; copy the resolved file into the dir."

| Source | Local path | Size | sha256 (16-char prefix) | Notes |
|--------|-----------|------|------------------------|-------|
| `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0503205-different-kind-quantum-search/extraction/marker.md` | `extraction/marker.md` | 24,715 B | `d4a2517b43c61014` | Header notes it is a `pdftotext` fallback (Marker not installed on the parse host, 2026-07-05) |
| `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0503205-different-kind-quantum-search/extraction/nougat.mmd` | `extraction/nougat.mmd` | 31,534 B | `42a7c4f0dbad44c9` | Real Nougat parse |

## Python packages installed (in `work/.venv`, cached from PyPI)

| Package | Version | Source |
|---------|---------|--------|
| numpy | 2.5.1 | PyPI wheel |
| matplotlib | 3.11.0 | PyPI wheel |
| (transitive: contourpy, cycler, fonttools, kiwisolver, packaging, pillow, pyparsing, python-dateutil, six) | latest as of 2026-07-06 | PyPI |

## LLM endpoint used (no data pulled, but recorded for provenance)

| Endpoint | Model | Purpose | Cost |
|----------|-------|---------|------|
| `http://127.0.0.1:44497/v1/chat/completions` (Argo proxy, local) | `argo:gpt-4o` | LLM-judge scoring | Free (Argo internal) |

## Not fetched
- No arXiv source `.tar.gz` (paper is short; PDF suffices for reading).
- No external code (Grover has no reference implementation; wrote our own from equations).
- No dataset (algorithm has no dataset; problem is pure quantum-circuit sim on N=16).
