# PARSER_PROVENANCE.md — Rasp 2018 re-pass

**Date:** 2026-06-23
**Re-pass agent:** Ollie subagent (argo/argo:claude-opus-4.7) under main session
agent:main:telegram:direct:8542341053

## Canonical paper PDF

- **Local file:** `~/Dropbox/REPLICATE-PROJECT/Rasp-2018-Climate/rasp_2018_arxiv.pdf`
- **Source:** arXiv 1806.04731v3 (cached during PASS-1 on 2026-05-27)
- **Bytes:** 3,424,413
- **Source-of-truth identity:** This is the arXiv v3 preprint that matches the PNAS published version content (PNAS HTML body is paywalled/Cloudflare-blocked from CherryRd residential IP; arXiv v3 has identical body text + the supplement that's referenced in the published version).

## Parser used for claim enumeration (re-pass)

1. **First attempt:** `pdf` tool (Anthropic native PDF analysis).
   - Result: failed twice — first the local-media-path policy blocked `/Users/stevens/Dropbox/...` and `/tmp/...`; after relocating to `~/.openclaw/workspace/tmp-pdf/` the call still failed because Anthropic credit balance was insufficient and Gemini/GPT-5 fallbacks were also unavailable.
2. **Fallback used (chosen parser):** `pdftotext -layout` from Poppler.
   - Binary: `/usr/local/bin/pdftotext` (Poppler / Xpdf-compatible).
   - Command: `pdftotext -layout ~/.openclaw/workspace/tmp-pdf/rasp2018.pdf ~/.openclaw/workspace/tmp-pdf/rasp2018.txt`
   - Output: 724 lines, body + supplement + references all extracted cleanly.
   - Quality check: title, author affiliations, abstract, Methods, Results, Discussion, Acknowledgements, full reference list (1-40), and Supplemental Methods (SPCAM setup, neural network details, Table S1, figure captions S1-S6) all present and correctly ordered.
   - Caveat: figure rasters not extracted (only captions / refs). For claim enumeration that's adequate — claims are stated in body+captions, the figure images themselves only show shape/magnitude that is already restated in body text.

## Claim enumeration source

- Worked directly from the body of `~/.openclaw/workspace/tmp-pdf/rasp2018.txt` (lines 1-724).
- Cross-checked numerical values against the cached PAPER_NOTES.md from PASS-1 (which extracted the same architecture/I-O numbers).

## Data parser (re-used from PASS-1; unchanged)

- **Library:** xarray 2026.4.0 + netCDF4 1.7.4 (factory env on uicgpu).
- **Files:** `/data/stevens/rasp_2018/data/preproc_features.nc` (X, 778240×60), `/data/stevens/rasp_2018/data/preproc_targets.nc` (Y, 778240×60), `/data/stevens/rasp_2018/data/sample_SPCAM_1.nc` (raw SPCAM diagnostic output, 48 timesteps × 64 lat × 128 lon, includes PRECT, FLNT, FSNT, FLNS, FSNS, TPHYSTND, PHQ, T, Q, …).
- **Preproc files**: contain `time`, `lat`, `lon` per-sample coordinates — **important for re-pass:** lets us compute latitude-binned skill / mean-tendency profiles that PASS-1 did not exploit.
- **Sample SPCAM file:** has the full diagnostic field set the paper compares NNCAM against (mean precip, radiative fluxes, mean state T(z,lat)) and lets us build offline "diagnostic-mode" surrogates for the prognostic claims.

## Trained-model artifacts re-used from PASS-1 (unchanged)

- `/data/stevens/rasp_2018/runs/control_9x256/best.pt` — paper-headline 9×256 LeakyReLU(0.3) net, 557,372 params, MSE+Adam, 20 epochs, val-loss 0.4632.
- Norm stats (`norm.npz`, `norm_names.json`) same dir.
- 4 other architectures (`small_2x64`, `mid_4x128`, `mid_5x256`, `wide_9x512`) for cross-reference.

PASS-1 PyTorch port: `/data/stevens/rasp_2018/rasp2018_train.py`. Verified bit-identical with `summary.json` numbers in this dir; no re-training required for the re-pass.
