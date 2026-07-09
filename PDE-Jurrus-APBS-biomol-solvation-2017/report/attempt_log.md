# Attempt Log — Jurrus-APBS-2017 replication

**Runner:** Ollie subagent, 2026-07-06 10:10 CDT → 10:30 CDT (~20 min).

## Timeline

- **10:10** — Read WAVE_BRIEF_2026-07-01.md. Created target dir tree (extraction/, report/evidence/, work/).
- **10:10-10:14** — Attempted PDF fetch from CherryRd:
  - `https://pmc.ncbi.nlm.nih.gov/articles/PMC5734301/pdf/PRO-27-112.pdf` → 1.8KB HTML (403 wrapper)
  - `https://europepmc.org/backend/ptpmcrender.fcgi?accid=PMC5734301&blobtype=pdf` → 1.8KB HTML
  - `https://onlinelibrary.wiley.com/doi/pdf/10.1002/pro.3280` → 5KB Cloudflare challenge
  - **Root cause:** From CherryRd (Ollie's default network) PMC + Wiley return either 403 wrappers or Cloudflare bot challenges.
- **10:14** — Failed over to `ssh uicgpu` (proxied network via ALCF Squid). Same tried URLs failed same way. But `https://europepmc.org/articles/PMC5734301?pdf=render` succeeded — 1.71 MB PDF, verified `PDF document, version 1.5`.
- **10:14** — `scp uicgpu:/tmp/apbs.pdf` back to workspace as `paper.pdf`.
- **10:15** — Confirmed via unpaywall that Wiley "publisher pdfdirect" was the "best" OA URL (bronze OA); Wiley + PMC both Cloudflare-blocked, europepmc render endpoint is the reliable fallback.
- **10:15-10:16** — marker extraction: env `/data/stevens/envs/marker` (NOT the `marker` conda env under `/gpustor/stevens/anaconda3`; that one was empty of the `marker_single` binary). `marker_single /tmp/apbs-jurrus.pdf --output_dir /tmp/apbs-jurrus-work --output_format markdown` → 51s → `apbs-jurrus.md` (555 lines) + figures. Copied back to `extraction/marker.md`.
- **10:16-10:17** — nougat extraction: first attempt OOM'd on GPU 0 (79 GB card, but 60 GB already in use by another process). Retried with `CUDA_VISIBLE_DEVICES=6` (GPU 6 fully free) + `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`. Success in 19 s. `apbs-jurrus.mmd` (415 lines) → `extraction/nougat.mmd`.
- **10:17** — Discovered pre-existing conda env `/data/stevens/envs/apbs-repl` with APBS 3.4.1 + PDB2PQR 3.6.1 (previous replication attempt). Saved 15+ min of install time.
- **10:18** — Downloaded 1FAS.pdb (75 KB, 470 heavy atoms) and 1CRN.pdb (49 KB, 327 heavy atoms) from RCSB direct.
- **10:18** — Ran `pdb2pqr30 --ff=AMBER --apbs-input <mol>.in <mol>.pdb <mol>.pqr` on both. 1FAS: clean, disulfide bridges updated, waters optimized (some skipped). 1CRN: clean, no repair needed. Both wrote auto-generated APBS input file with mg-auto grid sizing.
- **10:18** — Noticed pdb2pqr's auto-generated input had `write pot dx 1fas.pqr` (would overwrite PQR!). sed-fixed to `1fas_pot` / `1crn_pot`.
- **10:18** — Ran `apbs 1fas.in`: 2.6 s wall, converged, E_total = 1.0959e5 kJ/mol. Wrote 22 MB DX file (129×97×129 = 1.6M points).
- **10:18** — Ran `apbs 1crn.in`: 1.5 s wall, converged, E_total = 3.5009e4 kJ/mol. Wrote 13 MB DX file (97³ = 912k points).
- **10:19** — Additional runs:
  - 1CRN + 0.15 M NaCl (LPBE): E = 3.5005e4 kJ/mol, Debye length = 7.86 Å ✓.
  - 1FAS + 0.15 M NaCl (NPBE nonlinear): E = 1.0957e5 kJ/mol (0.02% off LPBE, expected).
- **10:19** — Attempted `geoflow-auto` on 1FAS. Parser rejected input (APBS Appendix parameters insufficient — needed keywords only in examples/geoflow/). Logged as "attempted, not achieved" rather than a bug.
- **10:20** — Ran python numpy analysis on DX files → min/max/mean/std potential (kT/e and mV). Wrote `report/evidence/potential_stats.json`.
- **10:22** — LLM judge call:
  - argo:claude-opus-4.7 via `http://localhost:44497/v1/chat/completions` → 400 "Failed to parse upstream response"
  - argo:claude-opus-4.7 via LiteLLM aggregator `http://<tailnet-aggregator>:4000/v1` → same 502
  - argo:gpt-5.2 via LiteLLM aggregator → SUCCESS. Verdict: PARTIAL, coverage 0.55, agreement 0.75.
  - Root cause: Claude Opus 4.7/4.8 Argo endpoint intermittent (known issue per TOOLS.md).
- **10:25-10:30** — Wrote all 8 artifacts: paper.pdf, extraction/marker.md, extraction/nougat.mmd, REPORT.md, REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md.

## What worked
- europepmc.org `?pdf=render` endpoint as reliable PDF fallback when PMC/Wiley Cloudflare-block from CherryRd.
- Pre-existing apbs-repl conda env → immediate use, no install time.
- pdb2pqr30 auto-generates a working APBS input file (paper's key user-experience claim).
- 1FAS and 1CRN as sanity-check pair (charged vs neutral protein).
- LPBE↔NPBE cross-check as an internal consistency test.

## What failed / had to work around
- CherryRd → PMC / Wiley direct fetches: 403 / Cloudflare.
- Nougat OOM on default GPU 0 → forced to GPU 6.
- pdb2pqr's default `write pot dx <mol>.pqr` filename would overwrite the PQR file — worth patching upstream.
- geoflow-auto input parsing rejected — Appendix documentation insufficient (this became Open Question Q1).
- Argo Claude Opus judge endpoint down → fell back to gpt-5.2 (still free per project rules).

## Files produced
See `report/artifacts_summary.md`.
