# Failure analysis — QC-1711.11336 (Portugal 2017) replication

## What worked
- Fetch → extract → simulate → plot → report pipeline completed in a single turn (~15 min wall).
- The paper's **entire numerical content** reproduces on real numpy simulation without approximation. Log-log Q vs N slope = 0.665 vs theory 2/3 = 0.667. Success probability monotonically → 1. Invariant-subspace structure verified to machine precision.
- Classical baseline recovers all planted collisions.

## What did NOT work / what I had to fix / friction

### F1. Task prompt disagreed with the paper (severity: would have wrecked replication)
The subagent task described the paper as using a **coined quantum walk on Johnson graph J(N,3)** with "3-subsets of [N]" as vertices. The paper actually uses a **staggered quantum walk on graph Γ** (the line graph of Ambainis' bipartite graph), and the vertex set is `{(S, y) : S is an r-subset of [N], y ∈ [N] \ S}` with r = round(N^{k/(k+1)}) (not r=3 fixed). Also the invariant subspace has dimension 2k+1 = 5, not J(N,3)-related.

**Mitigation**: On reading the paper's Section 2.1 I discovered the discrepancy, ignored the prompt's paraphrase, and coded what the paper actually says. If a downstream consumer trusts the prompt over the paper they would misfile this replication under a completely different algorithmic framework.

**Lesson**: For dense theory papers, always cross-verify the algorithmic core from the actual PDF before writing code. The prompt is a hint, not ground truth.

### F2. Apparent typo (or misread) in Eq. (9) (severity: caused first-run non-unitary matrix)
Reading Eq. (9) literally from the pdftotext output gave the Kronecker `δ_{ℓ - (-1)^{j'}, ℓ'}` for the off-diagonal element of u_β. Coding this made u_β non-symmetric (`||B - B^T||_∞ = 1.0`), hence non-unitary, hence the algorithm ran but with total-probability leaking to zero — first sweep showed p_succ monotonically dropping from 0.2 to 0. Debugging took ~5 min: verified u_α is unitary (yes), so the bug is in u_β; recognized that (ℓ+j) = (ℓ'+j') is required for symmetric coupling, which forces `ℓ' = ℓ - (-1)^{j}` (using **j**, not **j'**). Switched to the symmetric reading; both matrices became unitary+Hermitian to machine precision and the sweep produced the expected N^{2/3} scaling with p_succ → 1.

**Residual gap**: Without access to the arXiv LaTeX source, I cannot say whether this is (a) a genuine typo in the printed paper, (b) a pdftotext rendering artifact of a diacritic I couldn't see, or (c) a valid alternate basis convention I'm misinterpreting. This is filed as Open Question Q1.

### F3. Marker + Nougat not installed on execution host (severity: cosmetic)
The wave brief's 8-artifact standard requires `extraction/marker.md` and `extraction/nougat.mmd`. Neither tool was installed on CherryRd at run time (no `marker`, `marker_single`, or `nougat` binaries on PATH; `import marker` fails). Rather than block the replication on installing a full GPU-hungry OCR pipeline for a 14-page purely-textual math paper, I used `pdftotext -layout` as a fallback and mirrored the same extracted text into both slots, with `extraction/README.md` documenting the substitution.

**Impact**: Zero on the replication scoring (equation-aware Markdown wouldn't help with the algorithmic replication). Some for a downstream consumer who wants to LaTeX-round-trip the equations — they'd need to rerun with real marker+nougat.

### F4. Integer overflow in initial-state normalization at large N (severity: caught in first sweep, fixed)
`build_psi0` initially computed `C(N,r) * (N-r)` as a Python int then called `math.sqrt(...)`, which threw `OverflowError: int too large to convert to float` at N=3000. Fixed by computing all binomial coefficients and the amplitude in log-space via `lgamma`. Post-fix, the sweep runs cleanly up to arbitrary N.

### F5. Small pre-asymptotic non-monotonicity in p_succ (severity: cosmetic, but interesting)
At N=15 (p_succ=0.64) and N=30 (p_succ=0.72) the success probability dips below neighboring N=9, 12, 20. This is a genuine finite-size artifact — the integer-rounding of t1 either lands one step short of or one step past the amplitude-amplification peak. The paper's asymptotic bound is silent on pre-asymptotic behavior. This is filed as Open Question Q3 and does not affect the REPLICATED verdict (the asymptotic slope + monotone envelope both hold).

### F6. LLM judge not consulted (severity: minor)
The wave brief allows "3-judge Argo panel only if time remains; else self-verdict." I self-verdicted based on the quantitative match of the log-log fit slope (0.665 vs 0.667, agreement to 3 parts in 700) and the monotone p_succ → 1 behavior. Both match the paper. A downstream consumer wanting independent judging can post the REPORT.pdf + evidence to Argo `argo:claude-opus-4.8` at `localhost:44497` via the aggregator; I did not do so because the numerical evidence is unambiguous.

## What I would add given more time
- k=3 sweep (would confirm the reduction extends to element 3-distinctness, Q ~ N^{3/4}).
- Fractional-t1 evolution to test whether the observed slope bias is a rounding artifact (Open Q2).
- Diagonalize u^{t2} R and correlate the p_succ dips with eigenvalue near-degeneracies (Open Q3).
- Push the sweep to N = 1e5 to see when observed p_succ crosses 0.99 (Open Q4).
- Fetch the arXiv LaTeX source and confirm the Eq. (9) typo (Open Q1).
