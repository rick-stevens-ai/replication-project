# Attempt Log — OSTI 3007459 (Kolmogorov-Arnold Wavefunctions)

Chronological, 2026-07-02.

1. **Target selection.** Ranks 1–2 already done. Went down the OSTI-100 topup list;
   ranks 3–28 are mostly heavy multiphysics/PIC/DFT codes, benchmark sets, or reviews.
   Picked **rank 29, OSTI 3007459** — a self-contained VMC + KAN-ansatz paper with an
   *exactly solvable* validation target and analytic references (Busch N=2, TG limit):
   ideal for a rigorous, GPU-friendly, from-equations reimplementation. Verified no
   colliding `OSTI-3007459-*` dir.

2. **PDF fetch.** Direct `curl` from CherryRd times out (known). Fetched via `ssh uicgpu`
   with its Squid proxy (`~/env.sh`); 523 KB PDF. `pdftotext -layout` → paper.txt.
   Extracted architecture (Eq. 2 tanh-composed splines; Eq. 3 MLP), the two model
   Hamiltonians (Eq. 6 solvable, Eq. 12 delta+harmonic), exact energy (Eq. 7), cusp
   term (Eq. 10–11), and the headline ~10× efficiency claim.

3. **Reimplementation v1** (`kan_vmc.py`): bosonic KAN (piecewise-quadratic splines),
   bosonic MLP (sorted-coordinate symmetrization), Metropolis VMC, ADAM, VMC gradient
   estimator, autodiff local energy.

4. **Sanity check FIRST** (`check_exact.py`): computed the smooth local energy of the
   EXACT wavefunction (Eq. 8) for the solvable model → **= E₀ (Eq.7) to machine
   precision with ZERO variance** for N=2,4,8. This validated the local-energy estimator
   and the exact-energy formula before any training. (Evidence: check_exact_output.txt.)

5. **First VMC runs collapsed** (solvable model): energy diverged to −∞. Diagnosis: I
   had dropped the repulsive `g·δ(xi−xj)` term; the attractive `σ|dx|` (σ<0) then makes
   the truncated Hamiltonian unbounded below. On the *exact* wf the δ is cancelled by the
   cusp, but a general trial wf needs it explicitly.

6. **Pivot to the delta+harmonic model (Eq. 12)** — bounded, well-posed for VMC, with
   the Busch N=2 analytic + TG references the paper itself uses. Reintroduced the δ via a
   **Gaussian-regulated delta** (width ε) in the local energy. Verified the Busch
   transcendental solver reproduces the known E(g) curve (g=0.5:1.307 … g→∞:2.0).

7. **Still collapsing** — but the **MLP ansatz trained fine** on the same model
   (N=2 g=1 → E=1.435 vs Busch 1.487). => the bug was **KAN-specific**: my
   piecewise-quadratic spline produced derivative spikes the optimizer exploited
   (a classic flexible-ansatz VMC collapse).

8. **Fix: smooth Gaussian-RBF line-functions** for the KAN (a faithful "smooth
   line-function" choice; the paper explicitly requires smoothness). **KAN then trained
   stably** (N=2 g=1 climbing 0.94→1.476, ~0.7% of Busch) — and faster than the MLP in
   that run, consistent with the paper's efficiency thesis.

9. **GPU port** (device fixes in metropolis/refine). ~12× speedup (200 steps: 150s CPU →
   12s A100).

10. **Systematic validation** (`final_experiments.py`, no import side-effects):
    - **E1 g=0 non-interacting**: E = 1.0/1.5/2.0 for N=2/3/4, relerr ~1e-6, zero
      variance. Exact. PASS.
    - **E2 ε→0 extrapolation (N=2 g=1)**: non-monotonic in ε, large seed scatter →
      no clean extrapolation (extrap 2.19 vs Busch 1.487). The regulated-δ + KAN-cusp
      interplay is not clean enough for quantitative ε→0.
    - **E3 KAN vs MLP efficiency (N=2 g=1)**: KAN 408 params vs MLP 1186 (**2.9× fewer**,
      confirming the parameter-frugality claim) — BUT our KAN was slower (51s vs 18s) and
      less accurate (relerr 21% vs 3.3%). The headline ~10× walltime/FLOP advantage was
      **NOT** confirmed in our reimplementation.
    - **E4 E(g) shape (N=2)**: g=0→1.0 (exact); g=2.0→1.682 vs Busch 1.674 (**0.5%**,
      excellent); but g=0.5→1.79 and g=4.0→2.49 (above TG=2.0, unphysical) — **seed/run
      dependent**, not robust.

11. **LLM-judge** (free Argo gpt-5.2): coverage 1.0, agreement 0.55, **PARTIAL**.

12. Collected evidence JSON/logs, code, and judge verdict into `report/evidence/`.
    Verdict: **PARTIAL**.
