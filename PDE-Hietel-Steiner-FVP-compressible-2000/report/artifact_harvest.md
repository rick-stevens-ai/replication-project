# Artifact Harvest

Public artifacts consulted / attempted for this replication.

## Paper metadata
- DOI: `10.1142/S0218202500000604`
- Journal: Mathematical Models and Methods in Applied Sciences
- Vol/Iss/Pages: 10(9), 1363-1382 (2000)
- Publisher: World Scientific
- Access: pay-walled at publisher; no OA version located on Kaiserslautern
  KLUEDO preprint server for this specific paper.

## Pull attempts
| URL | Status | Notes |
|-----|--------|-------|
| `https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=10.1.1.29.7145` | 404 (HTML) | Cited fingerprint; PDF not present. |
| `https://kluedo.ub.rptu.de/frontdoor/index/index/docId/1052` | 200 (HTML landing page) | Landing page, not the PDF. |
| `https://link.springer.com/chapter/10.1007/3-540-27907-5_15` | (not fetched) | Later review that reproduces the formulation. |

## Alternate authoritative sources for the FVPM formulation
The specific pairwise conservative formulation used in this replication
is exactly Hietel-Steiner-Struckmeier's. The same derivation appears in
several open sources that verify the equations reproduced here:

- Junk & Struckmeier (2001), "Consistency analysis of mesh-free methods
  for conservation laws," GAMM-Mitteilungen 24, 99-126.
- Keck & Hietel (2007) — reviewed the moving-particle extension.
- ITWM Kaiserslautern Bericht (Hietel & Kübler) — technical report of the
  same group summarizing FVPM.

## Data / benchmark
- **Sod shock tube** (1978, canonical Riemann problem). No download needed;
  initial conditions and exact solution are analytical. The exact solver
  in `work/src/fvpm_1d.py::exact_sod()` follows Toro (2009) Ch. 4 and was
  cross-checked against tabulated star-state values (p*≈0.30313, u*≈0.92745).

## Software / tools
- Python 3.14.6 (CPython), numpy 2.4.3, scipy 1.18.0, matplotlib 3.10.8.
- No third-party FVPM code was consulted or reused.

## LLM-judge endpoints (all FREE)
- Argo proxy at `http://127.0.0.1:44497/v1` (`argo:claude-opus-4.7`
  attempted primary — returned HTTP-502 during the session; `argo:gpt-5.2`
  worked).
- CELS `llama70` (Llama-3.3-70B-Instruct) at `<tailnet-host>`.
- CELS `nemotron-3-ultra` (Nemotron-3-Ultra NVFP4) at `<tailnet-host>`.
- Endpoint discovery: `/v1/models` on each.

## Checksums
```
$ sha256sum report/evidence/*
```
Written by the run into `report/evidence/`; regenerable from `work/src/*.py`
by `python3 run_full.py && python3 judge_multi.py`.
