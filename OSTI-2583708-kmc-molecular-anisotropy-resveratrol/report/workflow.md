# Workflow & tools & effort estimate

## End-to-end workflow

```
┌─ 1. Fetch paper (OSTI open PDF, uicgpu → local scp)
│
├─ 2. Extract paper text
│   ├─ pdftotext -layout (poppler 26.06.0)
│   ├─ pdftotext plain
│   └─ IOPscience HTML scrape for table structure
│      → extraction/marker.md
│      → extraction/nougat.mmd
│
├─ 3. Public code discovery
│   ├─ GitHub API: tdjanic-snl/spparks branches → master, nonorth, resveratrol
│   ├─ Clone shallow branches into work/
│   └─ Full-history clone for master ↔ resveratrol diff
│
├─ 4. Build SPPARKS (on uicgpu, 8×A100 machine, 255 cores, 2 TB RAM)
│   ├─ Copy resveratrol branch: scp -r → ~/replicate/osti-2583708/spparks-resv
│   ├─ Write Makefile.uic (mpicxx, -std=c++17, -O2, no JPEG)
│   ├─ make uic -j 8 → src/spk_uic (895 KB)
│   └─ Verify version banner ("SPPARKS 27 Nov 2024")
│
├─ 5. Smoke tests
│   ├─ HCP lattice + hex region — 512 sites, 12 neighbors ✓
│   ├─ 3D-random deposition (incident (0,0,0)) — accepted ✓
│   └─ nonlinear + tree solver — runs cleanly
│
├─ 6. Paper-scale sweep
│   ├─ 48×16×24 HCP box (36 864 sites, box (56, 13.86, 39.19), xy-tilt 8)
│   ├─ Nucleus block(20 28 6 10 10 14), i.e. ~8×4×4
│   ├─ T = 0.0270 eV/k_B, ν = 0.1 s⁻¹, capture 5.0 Å, coord [1,9]
│   ├─ 10 seeds in parallel, 2000 KMC-time units each
│   └─ (Surrogate) isotropic monotonic ecoord ladder n → -0.2n eV
│
├─ 7. Analyze
│   ├─ Parse SPPARKS text dumps in Python
│   ├─ Compute span_x, span_y, span_z of OCCUPIED sites at final frame
│   ├─ Sort → L (largest), M (middle), S (smallest)
│   └─ W:L = S/L, H:L = M/L; mean ± std across 10 seeds
│
└─ 8. Report writing
    ├─ report/REPORT.md (main report + open questions)
    ├─ report/REPORT.tex (LaTeX, section-by-section)
    ├─ report/{brief.md, attempt_log.md, artifact_harvest.md}
    ├─ report/{workflow.md, artifacts_summary.md, failure_analysis.md}
    ├─ report/open_questions.json (5 open questions, each with next_steps)
    └─ report/evidence/{dump.sweep_seed1.txt, log.sweep_seed1.txt, aspect_ratio_sweep.json}
```

## Tools & versions

| Tool | Version | Where | Purpose |
|---|---|---|---|
| SSH mesh | OpenSSH 9.x | local ↔ uicgpu | Compute offload |
| curl | 8.x | local & uicgpu | Paper + repo fetch |
| pdftotext (poppler) | 26.06.0 | local | Text extraction |
| git | 2.x | local & uicgpu | Clone + diff |
| GCC / g++ | 12.x | uicgpu | SPPARKS compile |
| mpicxx / mpich | system | uicgpu | MPI wrapper |
| SPPARKS | 27 Nov 2024 (fork commit f6bcc3b, branch resveratrol) | uicgpu | KMC engine |
| Python | 3.x | uicgpu & local | Dump parsing |
| jq / python -c json | — | local | JSON assembly |

**Code / scripts written for this replication (in `work/runs/`)**
- `in.hcp_test` — HCP + hex region + 3D deposition smoke test (~25 lines).
- `in.paper_scale` — 48×16×24 paper-scale KMC input (~30 lines).
- `in.sweep_seed1` — representative per-seed sweep input.
- `sweep.sh` — 10-seed parallel driver (~30 lines bash).
- `MAKE/Makefile.uic` — mpicxx build config (adapted from Makefile.g++; ~50 lines).
- Python dump-parser + aspect-ratio computer (~25 lines Python, embedded in the exec calls).

Total NEW code written: ~130 LOC + a build Makefile.

## Effort estimate

- **Compute wall-clock**: ~5 minutes (SPPARKS build ~2 min, 10-seed KMC sweep ~4 s per seed in parallel, all analysis interactive).
- **Human/agent wall-clock**: ~15 minutes end-to-end (fetch → build → run → report). Report writing dominates.
- **Cognitive**: moderate. The trap was noticing that the `resveratrol` GitHub branch does NOT actually contain the `disphere` / `resv` extensions the paper says are on it. Easy to miss if one only runs the infrastructure test and reports "everything works" — but that would be a false positive.
- **Resources**: local venv (no venv actually needed; used system Python), 1 CPU node of uicgpu at load ~1%.
