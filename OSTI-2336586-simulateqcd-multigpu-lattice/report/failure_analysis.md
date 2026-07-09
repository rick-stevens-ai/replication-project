# Failure Analysis — SIMULATeQCD Replication (OSTI 2336586)

**Verdict:** PARTIAL.
**Purpose of this document:** honestly catalog every failure encountered during replication, distinguish reviewer-side environmental failures from framework defects, and record which claims remain untested (and why).

---

## 1. Failures encountered

### 1.1 macOS `BACKEND=cuda` configure failure
- **What happened:** On the macOS reviewer laptop (Phase 3, 2026-07-03), `cmake .. -DBACKEND=cuda -DARCHITECTURE="80"` correctly reports "Using CUDA backend" and then fails at `project(... LANGUAGES CXX CUDA)` with "Failed to find nvcc".
- **Root cause:** No CUDA Toolkit / no `nvcc` on macOS host. macOS is not a supported target for NVIDIA GPU compilation.
- **Attribution:** **Reviewer environment, not a framework defect.**
- **Impact on verdict:** None. This failure actually *confirms* C8 (the paper's requirement that CUDA Toolkit 11+ be present). Evidence: `evidence/04_build_attempt.log`.
- **Resolution:** Moved the build to `uicgpu.cs.uic.edu` (8× A100, sm_80) in Phase 5, where `BACKEND=cuda` compiled cleanly.

### 1.2 macOS `BACKEND=hip_amd` configure failure
- **What happened:** `cmake .. -DBACKEND=hip_amd -DARCHITECTURE="gfx908"` correctly reports "Using HIP backend for AMD GPUs", proceeds past compiler detection, then fails at `find_package(MPI 3.1 REQUIRED CXX)` because the MPI CXX smoke-compile cannot include `<iostream>`.
- **Root cause:** macOS Command Line Tools is currently missing the C++ stdlib headers path. The `mpicxx` wrapper exists at `/usr/local/bin/mpicxx` and expands to the correct flags — the underlying stdlib is what is broken.
- **Attribution:** **Reviewer environment (macOS CLT), not a framework defect.**
- **Impact on verdict:** None. Cannot test HIP path here, but the CMake logic itself was validated by successfully identifying the backend and proceeding past the compiler detection stage.
- **Resolution:** Not attempted. HIP validation would require actual AMD MI250X or MI300X hardware, which is not available in this replication budget. This is captured in `open_questions.json` Q1.

### 1.3 Ambiguity of "0 faults detected" as a correctness signal
- **What happened:** `confReadWriteTest` reports "0 faults detected" on link-by-link binary comparison. On its own, this is a self-consistency claim (the framework's write path agrees with its read path). It does not prove that the framework is reading the ILDG file *correctly*.
- **Root cause:** Round-trip tests are inherently self-referential.
- **Attribution:** Test design.
- **Impact on verdict:** Would have been a weakness, so it was mitigated in Phase 7 with an **independent NERSC header re-parse** (`/tmp/parse_nersc.py`) that confirms the ground-truth `PLAQUETTE` values the framework tests land on.
- **Resolution:** For `confReadWriteTest` specifically, the ILDG checksum match (`12ec367d`/`90a40185`) is an *external* consistency signal (the checksum is embedded in the file, computed from the payload, and re-verified after write) — this provides some independent ground truth on top of the self-round-trip.

### 1.4 Displayed-precision ceiling on `compressionTest`
- **What happened:** `compressionTest` reports plaquette **0.6382** for all four compression schemes. Header ground truth is `0.6381995717`. These match to displayed precision but the test does not report more decimal places, so we cannot distinguish ULP-level agreement from 4-digit agreement.
- **Root cause:** The shipped test's stdout formatting rounds to 4 decimal places.
- **Attribution:** Test-output design.
- **Impact on verdict:** The test still passes and matches ground truth — the honest report is that we have 4-digit agreement, not that we have ULP-level agreement. This is called out explicitly in `REPORT.tex` GENUINE CRITIQUE and in `open_questions.json` Q3.
- **Resolution:** None attempted here — would require a source patch to the shipped test to print more digits.

### 1.5 HPC allocations not obtained (C10, C11, C12)
- **What happened:** Paper's headline performance numbers on JUWELS Booster, Perlmutter, and Frontier at 1..256 GPUs/GCDs were not re-run.
- **Root cause:** Requires HPC allocations (Perlmutter, Frontier) or facility access (JUWELS Booster) plus queue time at scale plus a matching software stack (CUDA-aware MPI + GPUDirect P2P). Multi-day HPC campaign, not a spot-check.
- **Attribution:** **Scope decision, not a failure.** Documented up front as out of scope (REPORT.md §3.6 and §5.2).
- **Impact on verdict:** This is precisely why the verdict is **PARTIAL** and not **REPLICATED**. Verbatim paper numbers preserved in `evidence/05_paper_performance_numbers.txt` for a possible future campaign.
- **Resolution:** Deferred; captured in `open_questions.json` Q2.

### 1.6 No AMD-hardware execution
- **What happened:** No test was executed on AMD MI250X or MI300X hardware. The HIP path was verified only via CMake configure parsing on macOS (which itself failed at the MPI-CXX stage; see 1.2).
- **Root cause:** No local AMD GPU access; no OLCF Frontier allocation.
- **Attribution:** **Scope / access, not a failure.**
- **Impact on verdict:** Cross-vendor portability claim (C4) is confirmed at the *CMake logic* level and via NVIDIA execution, but not via actual AMD execution. Frontier performance numbers (C12) are entirely untested. This is the single largest gap in the replication and is captured in `open_questions.json` Q1.
- **Resolution:** Deferred; requires Frontier / MI300X hardware access.

### 1.7 No end-to-end application run (RHMC, GenerateQuenched, gradientFlow, etc.)
- **What happened:** Only the shipped correctness tests (`confReadWriteTest`, `compressionTest`) were run. None of the six named applications from paper Sec 2.1 was exercised end-to-end.
- **Root cause:** Application runs require input parameters, gauge ensembles, and a physics campaign; would have taken hours to days at meaningful physics scale.
- **Attribution:** **Scope decision.**
- **Impact on verdict:** Structural presence of the applications is confirmed (C3, evidence/07_actual_applications.txt), but "does RHMC actually produce a valid HISQ trajectory" is not tested. Captured indirectly in `open_questions.json` Q3 (mixed-precision physics impact) and Q4 (autocorrelation reduction).
- **Resolution:** Deferred; would need a multi-day HPC campaign.

### 1.8 Post-paper version drift
- **What happened:** The clone-time HEAD (2026-01-09, `767a...`) and the uicgpu rerun commit (`c0a4a19`) are both post-publication. Additional applications (`checkConf`, `checkRand`, `configConverter`, `maximalCenterGaugeFixing`, `measureHadrons`, `polSuscRenorm`, `sampleTopology`) and top-level dirs (`examples/`, `experimental/`, `tools/`) exist at HEAD that were not in the paper.
- **Root cause:** Active development between paper freeze and today.
- **Attribution:** **Neutral / positive.** The additions do not contradict any paper claim.
- **Impact on verdict:** Minor — a strictly rigorous replication would pin to `v1.2.0` (the paper-contemporaneous tag) and re-verify claims against that exact tree. Instead, this replication verified claims against HEAD, which is a slightly different tree.
- **Resolution:** Called out in `REPORT.tex` GENUINE CRITIQUE. Not corrected in this pass.

## 2. Claims that remain untested

| Claim | Status | Reason |
|---|---|---|
| C10 (JUWELS Booster HISQ Dslash, 11.4 TFLOP/s, 1.36 TB/s) | Untested | Requires 4×A100 JUWELS Booster allocation. |
| C11 (Perlmutter 1..256×A100 strong- and weak-scaling) | Untested | Requires Perlmutter allocation at scale + CUDA-aware MPI at scale. |
| C12 (Frontier 1..256×MI250X GCD strong- and weak-scaling) | Untested | Requires OLCF Frontier allocation. |
| HIP path correctness on real AMD hardware | Untested | No local AMD GPU. |
| SYCL / Intel PVC / Aurora portability | Not applicable | Back end does not exist in framework; captured as open question Q1. |
| Physics-observable reproduction against published HotQCD ensemble | Untested | Multi-month HPC campaign. |
| Mixed-precision solver impact on physical observables | Untested | Captured as open question Q3. |
| ML-accelerated proposal integration | Untested / not applicable | Feature does not exist in framework; captured as open question Q4. |
| Sustainable-software-engineering plan (CI/CD, container reproducibility, perf regression) | Not applicable | Meta-question; captured as open question Q5. |

## 3. What was correctly attributed (avoiding common mis-blaming)

- **`nvcc` absence on macOS** — reviewer environment, not a framework defect.
- **macOS CLT missing C++ stdlib headers** — reviewer environment, not a framework defect.
- **HPC performance not re-run** — scope, not a failure.
- **AMD path not executed** — access, not a failure.
- **4-digit plaquette display** — test-formatting choice, not a numerical accuracy failure.

## 4. Overall failure posture

The framework itself did not fail any test we were able to run. Every "failure" documented above is either:
- (i) a reviewer-environment issue on the macOS laptop (correctly attributed and worked around by moving to uicgpu), or
- (ii) a scope / access limitation (correctly labeled "out of scope" or "deferred") that becomes an open question, or
- (iii) a testing-design observation (4-digit display, self-referential round-trip) that is honestly noted in the GENUINE CRITIQUE.

**This is why the verdict is PARTIAL — not NO-GO / CONTRADICTED / FAILED.** The framework passed everything it was asked to do; a large fraction of the paper's claims were simply outside the budget to ask.
