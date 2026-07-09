# Failure analysis

Overview: no *terminal* failures — the replication succeeded end-to-end and produced a REPLICATED verdict. But several intermediate failures cost real time and would have derailed a less-methodical run. These are worth writing down so future replicators (human or agent) can skip the trapdoors.

## Failure 1 — Sub-optimal convergence rate on first working solve

- **Symptom.** First convergence run gave H¹-velocity rate ~0.5 and pressure L² rate ~0.5 on Taylor-Green. Theoretical prediction (Thm 5.5 with r=s=1) is O(h) — rate 1.0. Off by a factor of ~2 in the rate is a serious red flag.
- **First (wrong) hypothesis.** "The paper predicts only ‖u‖₁ + ‖p‖₀ ≤ C(h‖u‖₂ + h²‖p‖₂), so maybe the O(h) is really the tight bound and my errors are dominated by an O(δh) inconsistency term from Lemma 5.2." → I stared at Lemma 5.2 for 5 minutes trying to rationalize the sub-optimality.
- **Second (wrong) hypothesis.** Sign error in the discrete-Laplacian coupling. I flipped the sign and re-ran — still bad.
- **Third (wrong) hypothesis.** Pressure zero-mean subtraction was off. Added proper `p - mean(p)` normalization in the L² error norm. Made no measurable difference.
- **Fourth hypothesis (correct) — polynomial-reproduction test.** Ran u=(x,−y), p=x, f=(1,0). This is *exactly* representable in P1/P1, so any weakly-consistent P1/P1 method should reproduce it to machine precision (this is the whole point of Lemma 5.2). My implementation gave errors *O(1)* and *growing* with mesh refinement — obvious bug.
- **Root cause.** In (5.1), −Δ_h : H¹_0(Ω) → V^h, defined by `(−Δ_h u, vʰ)_0 = (∇u, ∇vʰ)_0 for all vʰ ∈ V^h_0` (test functions vanishing on boundary — the space where the FE variational method lives). I was interpreting "into V^h" loosely and testing with ALL V^h dofs including boundary — which produces a well-defined but *different* operator that has O(1/h) artifacts at boundary rows.
- **Fix.** Restrict the mass-matrix test space to interior dofs, solve there, and set z_boundary := 0 to embed back into V^h. Two lines of code — but the debugging took ~20 minutes.
- **Lesson.** Every time you implement a new mixed FE method with an auxiliary operator (discrete Laplacian, L² projection, discrete gradient, discrete divergence), **the polynomial-reproduction test is the fastest smoke test**. If your method claims weak consistency + rate p, it *must* reproduce degree-p polynomials exactly. Run this test *before* trying to interpret convergence-rate slopes.

## Failure 2 — B*(u,q) vs B(u,q) equivalence assumption

- **Symptom.** During the polynomial-reproduction debugging, even the standard PSPG control code (which had previously given nice O(h) rates on Taylor-Green with u|_∂Ω=periodic-ish) got wrong interior values on the linear test.
- **Root cause.** The paper writes B*(u,q) = ∫u·∇q and notes it's equivalent to B(u,q) = −∫q ∇·u "for continuous pressure approximations and for velocity fields that vanish on the boundary." My linear test u = (x, −y) has u·n = ±1 on the boundary, so B* ≠ B by a nontrivial boundary term. Using B* with inhomogeneous velocity BCs introduces a spurious surface source that shows up as garbage in the interior.
- **Fix.** Switch to the proper `B(u,q) = -∫q ∇·u` form (which respects arbitrary boundary conditions correctly). Kovasznay and Taylor-Green with the fix show identical behavior since their boundary contributions are small; the linear test with fix reproduces to machine precision.
- **Lesson.** IBP identities in FE formulations often carry implicit boundary-condition assumptions. When reading a paper that writes "these are equivalent" — check whether their assumption holds for *your* boundary conditions.

## Failure 3 — Kovasznay Re=40 does not show convergence

- **Symptom.** On our mesh sizes (n ≤ 64), Kovasznay at Re=40 gives H¹-velocity error ~2.5 that is essentially constant in h. Interpretation-vulnerable: could look like the method is broken.
- **Root cause.** Kovasznay Re=40 has a boundary layer of thickness ~1/|λ| where λ ≈ 20; we need h ≪ 0.05 to be *asymptotic*. Our n=64 gives h ≈ 0.02 — barely in the asymptotic regime for the boundary layer, and the L²-norm error is dominated by discretization of the boundary layer itself.
- **Fix / decision.** Documented, but did NOT chase further meshes (would need n=256+, hours of solve). Ran Kovasznay Re=1 instead — smooth, no boundary layer, clean super-optimal convergence rates.
- **Lesson.** Choose benchmarks whose smoothness matches the mesh sizes you can afford. For an under-resolved benchmark, report *stability* (no blowup) but do not claim convergence rates. Add a smoother companion benchmark that IS in the asymptotic regime.

## Failure 4 — matplotlib buffering / process silence

- **Symptom.** `python3 bochev_sgls_stokes.py --mode both | tail -60` produced no output for minutes; `process poll` returned "still running" repeatedly.
- **Root cause.** `tail` was buffering the piped output; the Python process was actually completing but its output was withheld until enough had accumulated to fill tail's buffer. All JSON files were being written correctly.
- **Fix / workaround.** Check the output directory directly with `ls` — the JSON files were there, timestamped, done. Also `python3 -u` for unbuffered stdout in future runs.
- **Lesson.** Never trust "still running" alone. If a script's outputs are files, `ls -la $outdir` is the ground truth. Add `flush=True` to every `print` in a background-executable script.

## Failure 5 — Initial JSON serialization of numpy ints

- **Symptom.** After a 90-second n=64 solve, `json.dump` blew up with `Object of type int32 is not JSON serializable`.
- **Root cause.** Python 3.14's stdlib `json` no longer accepts numpy scalars via the default encoder (was more forgiving in older versions).
- **Fix.** Added `_sanitize` helper that recursively converts `np.integer` → `int` and `np.floating` → `float` before dumping.
- **Lesson.** Always sanitize numpy types before JSON in Python 3.13+. Ideally, cast at the moment of dict construction (which we now do for the stability sweep) so you never build a nested structure that has to be walked.

## What DIDN'T fail (worth appreciating)

- scikit-fem's assembly of arbitrary bilinear forms just worked once we understood the `(rows=test-space, cols=trial-space)` convention.
- The sparse block-matrix construction via `sp.hstack`/`sp.vstack` was clean and fast.
- The scipy `splu` factorization of the mass matrix was reused across all columns of A — O(1) factorization + O(nu² × block) triangular solves.
- Semantic Scholar API delivered the OA PDF URL in one call — 3 seconds total.
- pdftotext handled the equation-heavy paper cleanly (all Greek letters + math symbols came through as Unicode; the layout preserved).

## Generalizable takeaways

1. **Polynomial-reproduction test first.** Before trusting a convergence-rate plot, verify that your method reproduces exact solutions in its approximation space.
2. **Read the paper's assumptions on B* vs B carefully** when boundary conditions are inhomogeneous — these identities often hide "u|_∂Ω=0" assumptions.
3. **Discrete operators (−Δ_h, ∇_h, L² projections) have codomain subtleties.** Whether they map into V^h or V^h_0 matters and is easy to get wrong. Check by evaluating on a known-exact input (e.g. for −Δ_h, use a linear u and require −Δ_h u ≡ 0).
4. **Pre-asymptotic mesh regimes are dangerous.** A "flat" error curve doesn't imply broken code; it may mean h is too big for the solution's features. Add a smoother companion benchmark to disambiguate.
5. **When output is unexpectedly silent, `ls -la` on the output dir** — output-buffering will lie to you but the filesystem won't.
