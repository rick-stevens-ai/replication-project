# Failure analysis

## 1. Prior-attempt root cause (why we needed to resume at all)

The dir was found with `paper.pdf` (990 KB) but no `REPORT.md`, no extraction files, and no 5-report companions. Working directory `work/` existed. Root cause (inferred from the subagent brief): **analysis-first, artifact-last execution**. The previous attempt started implementing the VD+CC pipeline (likely with Qiskit-Aer + FakeHanoi) and hit the wall time before writing any report artifact.

**Lesson applied here:** wrote `REPORT.md` with a PARTIAL verdict *before* running any code. Even if all sub-primitives had failed, the artifact would exist and the wave would have a legible verdict rather than a silent stall.

## 2. Live failure encountered: Pauli-twirl vs Peng-2019 QPD

**First attempt at `cut_demo.py`** used the identity
$$ \mathrm{Id}(\rho) = \frac{1}{2}\sum_{P \in \{I, X, Y, Z\}} P \rho P $$
as the wire-cut decomposition, on the assumption that this is the "standard Pauli-basis cut" used by the paper.

**Result:** uncut=1.0, reconstructed=0.5, mismatch=0.5.

**Diagnosis:** the Pauli twirl $\frac{1}{2}\sum P \rho P$ is the *completely depolarizing channel* (maps every state to $I/2$), **not** the identity channel. It equals the identity only on $I/2$ itself.

The correct Peng-Horsman-Rudolph-Ying-Zhao 2019 wire-cut QPD is
$$ \mathrm{Id}(\rho) = \sum_{i=1}^{8} c_i \, \sigma_i^{\rm prep} \operatorname{Tr}(\sigma_i^{\rm meas} \rho) $$
with 8 terms: 2 measure-$I$-and-prep-computational-basis pairs (coeff $+1/2$ each) + 2 measure-$X$-and-prep-$X$-eigenstate pairs (coeff $\pm 1/2$) + 2 measure-$Y$-and-prep-$Y$-eigenstate pairs (coeff $\pm 1/2$) + 2 measure-$Z$-and-prep-$Z$-eigenstate pairs (coeff $\pm 1/2$). Sum of $|c_i| = 4 = 4^1$ (overhead for 1 cut).

**Fix:** rewrote `cut_demo.py` with the correct 8-term decomposition; reconstructed=1.0, diff=0.0.

**Time cost:** ~5 minutes (one wrong run + verbose-comment rewrite).

**Root-cause lesson (for `memory/failure-log.md`):**
> Circuit-cutting is *not* the same as Pauli twirl. The Pauli twirl decomposition
> `Id = (1/2) sum_P P·P` is a channel-average that maps to `I/2`, not to the input state.
> For wire cuts, use the 8-term QPD with measure-and-prepare pairs and signed coefficients,
> or equivalently the 6-term reduced form (dropping the two `I`-measure pairs and rewriting).
> Overhead is `4^K` for K cuts, not `2^K`.

## 3. Environment failures — none

- pdftotext worked.
- Python 3 + NumPy worked.
- No Qiskit needed (avoided by scope choice).
- No Argo API calls needed (all math was analytic).

## 4. Standing tooling gaps documented

- `marker-pdf` not installed; `extraction/marker.md` is a labeled pdftotext fallback.
- `nougat-ocr` not installed; `extraction/nougat.mmd` is a labeled surrogate.

Both gaps are pre-existing in this workspace and were flagged appropriately in the extraction files themselves.
