# Brief — MFEM Replication (Wave 4)

**Paper:** Anderson et al. "MFEM: A modular finite element methods library." *Comput. Math. Appl.* 81 (2021), 42–74. DOI: 10.1016/j.camwa.2020.06.009.
**Upstream code:** https://github.com/mfem/mfem (C++) and https://github.com/mfem/PyMFEM (Python).
**Wave:** PDE-collection Wave 4.
**Date:** 2026-06-16.

## Goal

Install MFEM via PyMFEM on CherryRd (CPU) and run *one canonical example* (Poisson on a square or 1-D Laplace) to verify open availability and textbook FEM convergence rate.

## Pre-flight expectation

PyMFEM on macOS Tahoe + Python 3.12 is known-flaky (SWIG-bound source build that pulls llvmlite transitively). The brief explicitly time-boxes MFEM at **5 minutes** with permission to flip to a documentation-only NO-GO if install fails — the most likely outcome on this host.

## Pass / fall-back criteria

- **PASS:** `pip install mfem` succeeds, `import mfem.ser as mfem` works, one example runs.
- **NO-GO (acceptable):** install fails within 5 min → document the failure, verify license + openness by inspection, recommend a Linux retry.

## Time budget

5 minutes for install attempt. If fails, switch to NO-GO + write REPORT.md from license-inspection evidence.

## Compute

CherryRd CPU; no GPU; no HPC.
