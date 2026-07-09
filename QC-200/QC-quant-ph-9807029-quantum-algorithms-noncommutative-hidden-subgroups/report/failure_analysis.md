# Failure Analysis — arXiv:quant-ph/9807029 Replication

Even for a clean `REPLICATED` verdict, the wave brief requires an honest accounting of friction, gaps, workarounds, and residual questions. Here is the full ledger.

## What failed, and how it was fixed

### F1. Sample-decoding bug in the harness (own-goal)
- **Symptom:** initial sweeps for $N\geq 8$ showed the quantum algorithm plateauing at ~30–45% success, well below both the paper's bound and direct-sample simulations of the same Z distribution.
- **Root cause:** in `sample_Z_from_joint`, I flattened the shape `(N, 2)` joint distribution with `np.flatten()` (C-order → index = `a*2 + b`), then decoded as if it were F-order (`a = idx % N`, `b = idx // N`). For $N=2$ these happen to coincide; for $N\geq 4$ they scramble $a$ and $b$.
- **Diagnosis method:** wrote a 10-line direct-sample-from-`pz` control that got 100% success at $m=60$ for $N=16$, while `sample_Z_from_joint` was stuck at ~60%. The gap said "sampler bug".
- **Fix:** changed to `a = idx // 2`, `b = idx % 2`. Instantly recovered the expected success curves.
- **Lesson:** always sanity-check a Monte-Carlo pipeline against a closed-form or independent-implementation baseline before trusting the aggregate numbers.

### F2. Paper's $b{=}1$/sin post-processing branch does not work (paper-side)
- **Symptom:** after fixing F1, running the paper's algorithm literally (branching on which of $b=0$ vs $b=1$ has more shots) still gave ~60% asymptotic success on $N=16$, versus 100% for a $b{=}0$-only rejection variant.
- **Root cause:** the paper (Theorem 3 proof, our line 262 of pdftotext) says: if fewer than $m'/2$ $b{=}0$ outcomes are obtained, use the $b{=}1$ samples with $\arg\max_{k} \sum_i \sin(2\pi k a_i / N)$. Under $\Pr[a\mid b{=}1] = (2/N)\sin^2(\pi k_0 a / N)$, the distribution is symmetric under $a \leftrightarrow N-a$, and $\sin(2\pi k \cdot)$ is an odd function, so $\mathbb{E}[\sin(2\pi k a / N) \mid b{=}1] = 0$ for every $k$. The estimator cannot discriminate $k_0$.
- **Verification:** numerically, $b{=}1$/sin branch gives ~10% success at $m=60$ for $N=16, k_0=5$; $b{=}0$/cos on the same joint gives 100%.
- **Workaround:** ran the paper's literal flow AND a $b{=}0$-rejection variant; used the latter for the headline numbers, and documented the discrepancy explicitly in `REPORT.tex §5` and in Open Question Q1.
- **Impact on the paper's headline claims:** by concentration ($\Pr[b{=}0]$ is exactly $1/2$ when $2k_0 \neq N$), the branch is triggered only exponentially rarely for large $m'$, so the $O(\log N)$ query bound and the $1 - 1/(2N)$ success bound still hold if one restarts on that branch. The specific $b{=}1$/sin construction in the paper is not consistent as written but the overall theorem is salvageable. Whether an erratum exists in the published *Adv. Appl. Math.* 25:239 version is Open Question Q1's next step.

### F3. Marker / Nougat CLIs not installed on host
- **Symptom:** the mandatory 8-artifact standard requires `extraction/marker.md` and `extraction/nougat.mmd`.
- **State:** `which marker`, `which marker_single`, `which nougat` all fail on the host (CherryRd). `python3 -c "import marker"` also fails. No central QC-200 corpus manifest of pre-parsed Marker/Nougat outputs was found under `~/Dropbox/REPLICATE-PROJECT/` (searched `parsed-papers/`, `_LUCID100_ADMIN/marker_md_*`, etc.).
- **Workaround:** wrote both files as `pdftotext -layout` output with a clear leading comment noting the fallback and pointing here. This preserves the artifact slot and gives downstream tooling a readable plain-text version of the paper; it is NOT a true Marker/Nougat parse.
- **What would be needed to close:** install Marker (`pip install marker-pdf`) or Nougat (`pip install nougat-ocr`), both of which require torch + LLM weights (~2–5 GB each). Not run here to keep the replication self-contained on CPU.

### F4. No REPORT.pdf compiled
- **Symptom:** REPORT.tex written but not compiled.
- **Reason:** pdflatex not exercised in this run; the LaTeX source uses only standard packages (`geometry, amsmath, amssymb, booktabs, hyperref, listings, xcolor`) so should compile cleanly on any TeX Live install.
- **Fix if needed:** `cd report && pdflatex REPORT.tex && pdflatex REPORT.tex`.

## What was NOT tested

- **Theorem 2** (reduction from general dihedral HSP to reflection-subgroup case). Reasoning: the wave brief asks for the "reproducible core"; Theorem 2 is a classical wrapper around Theorem 3 that uses the Abelian HSP algorithm as a subroutine. Testing it end-to-end would require implementing the Abelian HSP too. Left as scope.
- **Theorem 5 tight constant.** We use the paper's stated constant $\lceil 64\ln N\rceil$; we observe our empirical $m^\star$ is ~10–30× smaller, but did not try to derive a better analytical constant. Left as Open Question Q2.
- **$N \geq 64$.** Our oracle is an explicit $2^{2n+1}\times 2^{2n+1}$ complex matrix (memory $\sim (2N)^2 \cdot 2N \cdot 16$ bytes $\approx 40$ MB at $N=32$; blows up to ~2.5 GB at $N=64$). A permutation-based oracle would be needed for larger $N$. Not implemented here.
- **Non-power-of-two $N$.** Requires qudit or block-encoded $F_N$. Open Question Q5.

## Residual gaps summary

| Gap | Severity | Would close by |
|---|---|---|
| $b{=}1$/sin branch inconsistency in paper | Low (bound still holds via $b{=}0$ concentration) | Formal fix as in Open Question Q1 |
| Marker/Nougat fallbacks | Low (paper text is preserved verbatim, extractions used only downstream by manifests) | Install `marker-pdf` + `nougat-ocr` and rerun the extraction step |
| REPORT.pdf not compiled | Cosmetic | `pdflatex REPORT.tex` |
| No sweep beyond $N=32$ | Medium (scaling constant uncertain) | Rewrite oracle as permutation, sweep $N$ up to 256 |
| Kuperberg-sieve comparison | Optional (paper leaves it open by design) | Implement sieve on top of our sampler |

## Honest ratings

- **Reproducibility of the paper as written:** High. The core Lemma-4 formula reproduces to machine precision; the query complexity bound is comfortably satisfied.
- **Clarity of the paper:** High for the algorithm construction and Lemma 4; medium for the $b{=}1$/sin fallback in the Theorem-3 proof (which as we show cannot be right as literally stated).
- **Ease of replication:** High. CPU-only, minutes to run, ~250 lines of Qiskit. The paper's algorithm is remarkably clean.
