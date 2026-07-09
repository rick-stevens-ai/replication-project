# Artifact Harvest — MFEM (Wave 4)

## What we tried to install

- `mfem` (PyMFEM v4.x) from PyPI. License: BSD-3-Clause (matches `mfem/mfem` C++ core).
- Transitive deps the source-build pulled in: `numba`, `llvmlite`, `numpy`, `scipy`, `setuptools`, `wheel`.

## What landed in `venv/` despite the failure

After the failed install, the venv contains only the base toolchain (`pip==26.1.2`, `setuptools==82.0.1`, `wheel==0.47.0`, `packaging==26.2`). No `mfem`, `numba`, or `llvmlite` ended up importable.

## License

- `mfem/mfem`: BSD-3-Clause (https://github.com/mfem/mfem/blob/master/LICENSE).
- `mfem/PyMFEM`: same BSD-3 (https://github.com/mfem/PyMFEM/blob/master/LICENSE).
- Free for commercial use.

## Friction tags

- `:llvmlite-macos-tahoe` — `llvmlite` source build on macOS Tahoe 26.x + Python 3.12 fails with `ffi/build.py` non-zero exit. No prebuilt wheels for this triple on PyPI yet. Same issue reported elsewhere for `numba` chains on macOS 14+ until LLVM 17/18 wheels catch up.
- `:transitive-llvmlite` — neither MFEM nor PyMFEM strictly need llvmlite for the core solve; it gets pulled in by an indirect optional dep (numba, likely via a SciPy contrib path). Could be sidestepped with `pip install pymfem --no-deps` after a working numpy/scipy.
- `:cxx-build-recommended` — the upstream README in fact recommends `brew install mfem` first, then PyMFEM with `--no-deps`. The naked `pip install mfem` path is friction-prone.

## What to harvest instead

- The C++ core (`mfem/mfem`) is straightforwardly buildable with CMake on any Linux host; no Python in the loop. For real numerical replication, that's the right path.
- A Linux host (uicgpu / Aurora / hcdgx2) with Python 3.11 + apt llvm-15 would almost certainly succeed in the PyMFEM install.
