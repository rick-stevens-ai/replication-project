# Artifacts Summary — SIMULATeQCD Replication (OSTI 2336586)

**Paper:** Mazur, Bollweg, Clarke, et al. (HotQCD), *SIMULATeQCD: A simple multi-GPU lattice code for QCD calculations*. BNL-225460-2024-JAAM. arXiv:2306.01098v2 [hep-lat]. To be published in *Computer Physics Communications*, March 2024.
**Code:** https://github.com/LatticeQCD/SIMULATeQCD (MIT). Zenodo DOI 10.5281/zenodo.7994983 (repo) / 10.5281/zenodo.7994982 (software release).
**Verdict:** PARTIAL.

---

## Upstream artifacts (paper-side, unmodified)

| Artifact | Source | Purpose in this replication |
|---|---|---|
| Paper PDF (arXiv:2306.01098v2) | arXiv | Ground-truth statement of every claim tested (C1–C12). |
| GitHub repo `LatticeQCD/SIMULATeQCD` | GitHub | Source under review. Cloned at HEAD `767a1b110b46dd21a0ea4033250272620fbaff25` (2026-07-03) and at `c0a4a19` on uicgpu (2026-07-04). |
| Release tag `v1.2.0` | GitHub | Paper-contemporaneous release. Confirmed present via `git ls-remote --tags`. |
| Zenodo record 10.5281/zenodo.7994982 | Zenodo | Software-release DOI referenced in README badge. Existence verified. |
| Bundled `test_conf/*` configs | In-repo | Ground-truth gauge configurations with NERSC-header `PLAQUETTE` fields used as the reference values for `compressionTest`. |
| Paper Tables 1–3 | Paper | Multi-node TFLOP/s values on JUWELS Booster / Perlmutter / Frontier. Preserved verbatim; **not** re-run. |

## Locally produced artifacts (all in `report/`)

### Primary reports
| File | Contents |
|---|---|
| `REPORT.md` | Canonical Markdown replication report (§1 paper, §2 claims table, §3 method, §4 results, §5 verdict + §5.4 real-rerun evidence table). |
| `REPORT.tex` | Detailed LaTeX rendering of the same, with an added §GENUINE CRITIQUE that honestly limits every claim. |
| `workflow.md` | Chronological reconstruction of every step taken across the initial spot-check and the uicgpu rerun. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Every failure encountered, its root cause, and its correct attribution (reviewer vs framework). |
| `open_questions.json` | Five open scientific/engineering questions grounded in this paper's scope (cross-vendor portability, exascale HMC scaling, mixed-precision physics impact, ML-accelerated sampling, sustainable-software-engineering plan). |

### Evidence (all in `report/evidence/`)
| File | Produced by | Contents |
|---|---|---|
| `01_clone_and_repo.log` | Phase 1 | `git clone` output, HEAD commit hash, tag listing, license header, DOI badge line, LOC count. |
| `02_structure_vs_paper_claims.log` | Phase 2 | Side-by-side of paper Fig 2 subdirs vs actual `src/` subdirs; Sec 2.1 app names vs actual `main_*.cpp`. |
| `03_multi_backend_verification.log` | Phase 3 | CMake output for `BACKEND=cuda` and `BACKEND=hip_amd` configure attempts. |
| `04_build_attempt.log` | Phase 3 | Full CMake configure attempts on macOS and their (expected) failure modes. |
| `05_paper_performance_numbers.txt` | Phase 4 | Verbatim extraction of Tables 1–3 for a possible future HPC campaign. |
| `06_cmake_backend_block.txt` | Phase 3 | Snippet of `CMakeLists.txt` showing the `BACKEND` selector. |
| `07_actual_applications.txt` | Phase 2 | Full `ls src/applications/` listing. |
| `08_version_identity.txt` | Phase 1 | Pinned commit, date, tag. |
| `10_confReadWriteTest_run.log` | Phase 6a (uicgpu) | Full `confReadWriteTest` output: ILDG checksums (`12ec367d`/`90a40185`), 0-fault link-by-link compare, "All tests passed!". |
| `11_compressionTest_run.log` | Phase 6b (uicgpu) | Full `compressionTest` output: plaquette **0.6382** across R18/R14/R12/U3R14. |
| `12_nersc_header_plaquette.txt` | Phase 7 | Output of independent `/tmp/parse_nersc.py`: `l20t20b06498a_nersc.302500 → 0.6381995717`; `nersc.l8t4b3360_bieHB → 0.311637549`. |

### Ancillary
| Artifact | Location | Purpose |
|---|---|---|
| `/tmp/parse_nersc.py` (60 LOC Python) | uicgpu | Code-free NERSC header re-parser; produces `evidence/12_...`. Deliberately independent of SIMULATeQCD to defeat the "self-consistent but wrong" failure mode. |

## Codebase-under-test snapshot

- **Repo:** LatticeQCD/SIMULATeQCD
- **Clone commit (2026-07-03):** `767a1b110b46dd21a0ea4033250272620fbaff25`
- **Rerun commit (2026-07-04, uicgpu):** `c0a4a19`
- **License:** MIT
- **Size:** 230 C++ source files, 62,619 lines under `src/`
- **Paper-referenced tag:** `v1.2.0` (present)

## Host of record

- **uicgpu.cs.uic.edu** — 8× NVIDIA A100 80 GB PCIe, sm_80.
- CUDA + MPI stack (versions as installed on host).
- Build backend used: `BACKEND=cuda`, `ARCHITECTURE="80"`.

## What is NOT in this artifact set (deliberately)

- **No Perlmutter, JUWELS Booster, or Frontier runs.** Requires HPC allocations outside the replication budget.
- **No AMD MI250X or MI300X runs.** No local hardware; HIP path verified only via CMake configure on macOS.
- **No SYCL / Intel PVC / Aurora runs.** Back end does not exist; only NVIDIA + AMD are supported today.
- **No RHMC / GenerateQuenched / gradientFlow full-application runs.** Only the shipped `confReadWriteTest` and `compressionTest` were executed.
- **No physics-observable comparison against published HotQCD ensembles.** Multi-month HPC project, out of scope.
- **No mixed-precision (FP16/BF16/TF32/FP8) study.** Would need custom kernel variants; not exercised.

Every "NOT" above is the reason the verdict is PARTIAL (not REPLICATED) and each is flagged as an open question in `open_questions.json` where appropriate.

## Integrity notes

- Every numerical value quoted (`0.6382`, `0.6381995717`, `0.311637549`, `12ec367d`, `90a40185`, `0 faults`) is traceable to a specific log in `evidence/`.
- Every value quoted from the paper (11.4 TFLOP/s, 1.36 TB/s, 5.07 → 96.47, 1.36 → 120.44, 1.63 → 40.63, 0.93 → 165.72) is verbatim from the paper and is preserved in `evidence/05_paper_performance_numbers.txt`.
- No number in this replication was fabricated, extrapolated, or padded.
