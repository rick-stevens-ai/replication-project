# MFEM — Replication Report (Wave 4)

**Author:** Ollie (OpenClaw subagent, Claude Opus 4.7 via Argo)
**Date:** 2026-06-16
**Bundle:** `~/Dropbox/REPLICATE-PROJECT/PDE-replications/mfem-wave4/`

## Paper

- **Title:** MFEM: A modular finite element methods library
- **Authors / Venue:** Anderson, Andrej, Barker, Bramwell, Camier, Cerveny, Dobrev, Dudouit, Fisher, Kolev, Pazner, Stowell, Tomov, Akkerman, Dahm, Medina, Zampini — *Computers & Mathematics with Applications* 81 (2021), 42–74. (LLNL preprint LLNL-JRNL-789493.)
- **DOI:** [10.1016/j.camwa.2020.06.009](https://doi.org/10.1016/j.camwa.2020.06.009)
- **Code:** https://github.com/mfem/mfem (C++ core) and https://github.com/mfem/PyMFEM (Python bindings)
- **License:** **BSD-3-Clause** (verified 2026-06-16 from https://github.com/mfem/mfem/blob/master/LICENSE).

## Claims tested

| ID | Claim |
|----|-------|
| C1 | MFEM is openly available under a permissive BSD-3-Clause license, with public source and an active maintainer (LLNL). |
| C2 | PyMFEM provides Python bindings for the MFEM C++ core, installable via `pip` and runnable on a workstation. |
| C3 | The library ships canonical example problems (Poisson, elasticity, Maxwell, ...) that reproduce textbook FEM convergence rates. |

## Method (attempted) and Outcome

We attempted the standard install path:

```
python3.12 -m venv venv
source venv/bin/activate
pip install mfem
```

This triggers a source build of PyMFEM (which compiles the MFEM C++ core via SWIG + setuptools). On CherryRd (macOS Tahoe 26.x), the build pulled in `numba` and `llvmlite` as transitive dependencies and **failed at the `llvmlite` ffi build step**:

```
File "<string>", line 62, in build_library_files
File ".../subprocess.py", line 571, in run
  raise CalledProcessError(retcode, process.args, ...)
subprocess.CalledProcessError: Command '['.../python3.12',
  '.../llvmlite_*/ffi/build.py']' returned non-zero exit status 1.
ERROR: Failed building wheel for llvmlite
Failed to build mfem numba llvmlite
```

The root cause is an LLVM toolchain mismatch on the macOS Tahoe host: `llvmlite` on Python 3.12 / macOS-26 currently lacks pre-built wheels on PyPI for our platform triple, and the source build needs a matching LLVM that is not installed system-wide.

### What is achievable within the 5-minute MFEM time-box

- ✅ License verified BSD-3 (C1).
- ✅ Both `mfem/mfem` and `mfem/PyMFEM` GitHub repos confirmed reachable, active, and BSD-licensed (C1).
- ❌ Live import / canonical example run could not complete within the time-box because of the `llvmlite` build failure (C2 partially: pip *attempted* a build but did not finish).
- ❌ Therefore no live convergence rate or output to compare against the paper (C3 untested).

We did **not** try the C++-only escape route (`brew install mfem` + build a stand-alone Ex1 driver) because the brief explicitly time-boxed the MFEM attempt at 5 minutes.

## Results vs Paper

No numerical results obtained.

## Verdict

**NO-GO** — install path blocked within the time budget. The MFEM paper's claims about library openness and breadth of examples are verifiable by inspection (see Evidence below), but a live replication of any numerical example was not achieved on this attempt.

| ID | Verdict | Evidence |
|----|---------|----------|
| C1 (open / BSD) | ✅ Verified by inspection | LICENSE file in `mfem/mfem` repo |
| C2 (PyMFEM installable) | ❌ Blocked on this host | `llvmlite` ffi build failed on macOS Tahoe + Python 3.12 |
| C3 (canonical examples reproduce textbook rates) | ⏸ Untested | install never reached the example-running phase |

## Coverage / Agreement

- **Coverage / 10:** 1 — openness check only; no numerical experiment.
- **Agreement / 10:** n/a — no numbers to compare.

## Resources

- CherryRd, single CPU.
- Wall-clock: ~5 min spent on the pip install before it failed at the `llvmlite` step.
- 0 GB GPU.

## Tools / Datasets / Hardware

- **Tools (attempted):** `pip install mfem` (PyMFEM source-build path).
- **Datasets:** None reached.
- **Hardware:** CherryRd (macOS Tahoe 26.x, Python 3.12 in `mfem-wave4/venv/`).

## Limitations / Rationale for NO-GO

- **macOS Tahoe + Python 3.12 + llvmlite source build.** This is a known-flaky combo. The PyMFEM authors themselves recommend building MFEM C++ first via `brew` or CMake, then `pip install pymfem --no-deps`; the unmodified `pip install mfem` path is unreliable on bleeding-edge macOS versions.
- **5-minute time-box exhausted.** Per the Wave-4 brief, MFEM was the most likely NO-GO candidate; the time budget was capped at 5 minutes for that reason.
- **Recoverable later.** This NO-GO is *install-time*, not *scientific*. The library is openly licensed, the C++ core builds reliably on Linux, and PyMFEM works on Linux + Python 3.11; a future replication on a Linux node (Aurora, uicgpu, hcdgx2, ...) is the obvious next step.

## Evidence files

- `evidence/install_failure.log` — pip transcript with the `llvmlite` ffi build error (written below).
- This REPORT.md.

## Recommended next attempt

1. Run on `uicgpu` (Ubuntu) with Python 3.11.
2. `brew/apt install mfem` to get a working C++ MFEM, then `pip install pymfem --no-deps` to skip the troublesome llvmlite path.
3. Run `examples/ex1.py` (Poisson on a square) and `examples/ex9.py` (DG advection) and verify convergence rates.

## Bottom line

MFEM is unambiguously open (BSD-3) and well documented; the live Python install path failed within the 5-minute time-box on macOS Tahoe due to a `llvmlite` toolchain issue. **Verdict: NO-GO (install-time, not scientific). The paper's openness claim survives by inspection; its numerical claims await a Linux retry.**
