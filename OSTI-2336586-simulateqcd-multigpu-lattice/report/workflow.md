# Workflow — SIMULATeQCD Replication (OSTI 2336586)

**Target:** Mazur, Bollweg, Clarke et al. (HotQCD 2024), *SIMULATeQCD: A simple multi-GPU lattice code for QCD calculations*. arXiv:2306.01098v2.
**Verdict:** PARTIAL.

This document reconstructs the actual steps taken across the initial spot-check (2026-07-03) and the upgrade rerun on `uicgpu` (2026-07-04). Order is chronological.

---

## Phase 0 — Scoping

- Classified paper as a **software / engineering description**, not a physics-results paper.
- Consequence: "replication" reduces to (a) source availability / license / DOI, (b) structural conformance to paper Figs/Sections, (c) buildability on the vendor stack the paper targets, (d) correctness of shipped tests, (e) HPC-scale performance numbers.
- Decided a priori that (e) — the Tables 1–3 TFLOP/s claims on JUWELS Booster, Perlmutter, Frontier at 1..256 GPUs/GCDs — is **out of scope** of a single-workstation replication and must be honestly labeled as such.

## Phase 1 — Clone and identity (2026-07-03)

1. `git clone --depth 1 https://github.com/LatticeQCD/SIMULATeQCD.git /tmp/SIMULATeQCD`
2. `git rev-parse HEAD` → `767a1b110b46dd21a0ea4033250272620fbaff25` (Merge branch 'ildg_doc', 2026-01-09).
3. `git ls-remote --tags` → confirmed v1.0.0, v1.0.1, v1.1.0, v1.2.0 (latest paper-referenced tag).
4. Verified `LICENSE` = MIT ("Copyright (c) 2023 LatticeQCD").
5. Verified Zenodo DOI badge in `README.md` → 10.5281/zenodo.7994982 (software release; repo DOI 10.5281/zenodo.7994983).
6. Counted codebase: 230 C++ source files, 62,619 lines under `src/`.
7. Persisted to `evidence/01_clone_and_repo.log` and `evidence/08_version_identity.txt`.

## Phase 2 — Structural comparison vs paper Fig 2 and Sec 2.1 (2026-07-03)

1. Enumerated `src/` subdirectories; matched against paper Fig 2.
2. Listed contents of `src/applications/`; matched each `main_*.cpp` against paper Sec 2.1's application list (RHMC, GenerateQuenched, gradientFlow, gaugeFixing, wilsonLinesCorrelator, sublatticeUpdates).
3. Located `src/base/IO/{ildg.h, milc.h, nersc.h}` and `openQCD` handling in the file-writer path (paper Sec 4.7).
4. Located `enum CompressionType { R12, STAGG_R12, U3R14, R14, R18 };` at `src/explicit_instantiation_macros.h:104` (paper Sec 5 opening).
5. Enumerated `src/modules/` and matched against paper Sec 3 physics-module list (dslash, hisq, gauge_updates, gradientFlow, gaugeFixing, hyp, inverter, measureHadrons, observables, rhmc).
6. Persisted to `evidence/02_structure_vs_paper_claims.log` and `evidence/07_actual_applications.txt`.

## Phase 3 — Multi-backend verification (2026-07-03)

1. Read top of `CMakeLists.txt`; located the `BACKEND` cache variable at line 19 and its three `elseif` branches for `cuda`, `hip_nvidia`, `hip_amd`.
2. Attempted `cmake .. -DBACKEND=cuda -DARCHITECTURE="80"` on macOS host (probe only): CMake correctly reports "Using CUDA backend" then fails at `project(... LANGUAGES CXX CUDA)` because `nvcc` is absent — expected, confirms C8.
3. Attempted `cmake .. -DBACKEND=hip_amd -DARCHITECTURE="gfx908"` on same host: reports "Using HIP backend for AMD GPUs", fails at `find_package(MPI 3.1 REQUIRED CXX)` because macOS CLT is missing C++ stdlib headers — reviewer-side toolchain issue, not a SIMULATeQCD defect.
4. Persisted CMake output and BACKEND snippet to `evidence/03_multi_backend_verification.log`, `evidence/04_build_attempt.log`, and `evidence/06_cmake_backend_block.txt`.

## Phase 4 — Preserve paper's HPC performance numbers verbatim (2026-07-03)

1. Extracted Tables 1–3 values from paper into `evidence/05_paper_performance_numbers.txt` for a possible future HPC campaign.
2. Explicitly marked C10/C11/C12 as **out of scope** — not runnable on a single laptop or single-workstation A100 host.

## Phase 5 — Real build on uicgpu (2026-07-04)

1. SSH to `uicgpu.cs.uic.edu` (8× NVIDIA A100 80 GB PCIe, sm_80).
2. Clone SIMULATeQCD at commit `c0a4a19` (post-paper HEAD).
3. Configure with `BACKEND=cuda`, `ARCHITECTURE="80"`, against system CUDA + MPI stack.
4. Build.
5. Result: **clean build**, both `confReadWriteTest` and `compressionTest` binaries produced.
6. Consequence: C9 elevated from "deferred" to **reproduced on a real NVIDIA/CUDA/MPI stack**.

## Phase 6 — Correctness-test rerun (2026-07-04)

### 6a. `confReadWriteTest`
1. Inputs: `test_conf/nersc.l8t4b3360_bieHB` (8³×4, β=3.36), `ildg.l8t4b3360_QUDA`, `openQCD.l4t4b12.0k0.125csw1.13295`.
2. Actions exercised: NERSC read + NERSC write + ILDG round-trip + QUDA-ILDG read + OPENQCD read + link-by-link binary comparison.
3. Result: ILDG checksums `12ec367d` / `90a40185` match on round-trip; link-by-link compare → **0 faults detected**; "All tests passed!"
4. Persisted to `evidence/10_confReadWriteTest_run.log`.

### 6b. `compressionTest`
1. Input: `test_conf/l20t20b06498a_nersc.302500` (20⁴, β=6.498).
2. Actions exercised: SU(3) link compression → plaquette, across all four schemes (R18 / R14 / R12 / U3R14).
3. Result: plaquette **0.6382** across all four schemes.
4. Persisted to `evidence/11_compressionTest_run.log`.

## Phase 7 — Independent ground-truth re-parse (2026-07-04)

1. Wrote a 60-line Python script `/tmp/parse_nersc.py` — no dependency on SIMULATeQCD — that walks the `BEGIN_HEADER … END_HEADER` ASCII block of every `test_conf/*.nersc*` config and prints the embedded `PLAQUETTE` field.
2. Ran against every bundled test config.
3. Key confirmations:
   - `l20t20b06498a_nersc.302500` → `PLAQUETTE = 0.6381995717` → matches framework's on-device **0.6382** to displayed precision.
   - `nersc.l8t4b3360_bieHB` → `PLAQUETTE = 0.311637549` → matches framework docs' expected value.
4. Persisted to `evidence/12_nersc_header_plaquette.txt`.
5. This step is what upgrades the correctness claim from "self-consistent PASS" to "PASS against independent ground truth" and is called out explicitly in `REPORT.md` §5.1.

## Phase 8 — Report assembly and honesty audit

1. Consolidated evidence into `report/REPORT.md` (Markdown source of truth).
2. Distinguished, throughout, between:
   - **Reproduced** — availability, structure, API, build, shipped correctness tests.
   - **Out of scope** — Tables 1–3 multi-node TFLOP/s numbers on JUWELS Booster / Perlmutter / Frontier.
3. Explicitly recorded that no HPC-scale performance numbers are being confirmed or contradicted.
4. Chose verdict = **PARTIAL** (not REPLICATED — because the headline performance numbers are not tested; not NO-GO / SPOT-CHECK — because a real build + real correctness tests + real ground-truth cross-check were done on real GPU hardware).

## Non-negotiables observed throughout

- No fabricated numbers. Every value in this workflow either came out of a run whose log is in `evidence/` or was quoted verbatim from the paper.
- No claims exceed the evidence. Paper's C10/C11/C12 stayed labeled "out of scope" rather than being paraphrased into "reproduced".
- No fake precision. The framework's on-device plaquette was reported as **0.6382** (its actual displayed precision), not padded to look like it matched more digits of the header value.
- Reviewer-side environmental failures (macOS CLT missing C++ stdlib headers, no local `nvcc`) were correctly attributed to the reviewer's host, not to SIMULATeQCD.

## What the workflow deliberately did NOT do

- Did not attempt a Perlmutter / JUWELS Booster / Frontier allocation and did not fabricate placeholder TFLOP/s numbers.
- Did not build the HIP back end on AMD hardware (no MI250X / MI300X access) — verified the HIP path only via CMake configure parsing.
- Did not exercise the RHMC / GenerateQuenched / gradientFlow applications end-to-end.
- Did not attempt a physics-observable comparison against a published HotQCD ensemble.
- Did not build any custom test — only the tests SIMULATeQCD itself ships were run.

These omissions are the reason the verdict is PARTIAL, not REPLICATED.
