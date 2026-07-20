# Failure analysis — Das (2014) SODW replication

## 1. The interrupting failure (why this is a RETRY)
The prior attempt hit an **HTTP 502 mid-run**. The Python physics itself had
completed and written `work/das2014_result.json` (SAVE-EARLY worked), so no
compute was lost — but the *physics in that saved file was wrong* (see below), so
the run needed to be redone regardless of the 502.

## 2. The real bug: collapsed self-consistent gap
The prior `sodw_meanfield.py` built the full 4x4 SODW Nambu Hamiltonian and
computed the mean field as `Delta = (V/N) sum_k <M>_k` with `M = dH/dDelta` via a
batched-eigh trace `Tr[rho M]`. Symptoms in the saved JSON:
- `working_point.gap_Delta0_meV = 1.45e-5` meV (essentially zero)
- `gap_vs_T.Th_model_K = 0.0`
- `gap_vs_V.gap_meV` all ~1e-6 to 1e-5 meV
- it had to push V up to ~1041 meV and still got no gap.

**Root cause.** In the 4x4 basis the SODW couples *two* pair channels
(0-3 and 1-2) with opposite-sign coherence factors from the `+i*lambda` /
`-i*lambda` SOC entries. The `Tr[rho M]` accumulation summed contributions that
nearly cancel, so the self-consistent map `Delta -> V/N * <M>` had only the
trivial fixed point Delta=0 for all reachable V. The gap never bootstrapped.

## 3. The fix
Reduced the problem to the **nested particle-hole 2x2 block** that actually carries
the SODW instability (Das Eq. 2 restricted to the nested pair k, k+Q):
```
H_k = [[eps1(k), Delta],[Delta*, eps2(k+Q)]]
E_pm = eps_+ +/- sqrt(eps_-^2 + Delta^2)
```
and solved the standard density-wave gap equation
```
1 = (V/N) sum_k [f(E_-) - f(E_+)] / (2 sqrt(eps_-^2 + Delta^2))
```
with proper particle-hole nesting (eps2(k+Q) mirrors eps1(k) about E_F at
Q=(pi,pi)). This has a nontrivial fixed point above a critical V and converges
smoothly with mixing. Result: Delta0 = 6.15 meV, Th = 17.9 K — physical.

## 4. Remaining (honest) physics gaps -> why PARTIAL not REPLICATED
- **FS spectral-weight loss ~6% vs paper ~40%.** The toy band gaps only a thin
  nested strip; the real DFT FS has extended nesting sheets that remove far more
  weight.
- **Entropy release ~0.006 kB ln2 vs paper ~24% R ln2.** Same cause: too little
  phase space is gapped, so the entropy discontinuity is tiny.
- **Zeeman Bc ~106 T vs ~35 T.** A static `2 Delta0 = g muB Bc` estimate ignores
  the field dependence of Delta and the anisotropic (momentum-dependent) g-factor
  the paper uses; it overshoots ~3x.
- **2 Delta0 / kB Th ~ 8 vs BCS 3.53.** The flat-nested model band is strongly
  non-BCS; not necessarily wrong but not benchmarked against the paper's Delta(T).

## 5. What was deliberately not attempted
- WIEN2k DFT bands (scoped out per task).
- RPA spin-excitation spectrum / the in-gap collective mode.
- The two-order-parameter Ginzburg-Landau SODW/SDW competition (Eqs. 11-12).
These are enumerated as next steps in `open_questions.json`.

## 6. Environment / operational notes
- Runner: `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5, scipy 1.17.0). OK.
- `marker` and `nougat` not available -> extraction artifacts use a `pdftotext`
  fallback, clearly headed `INTERIM: pdftotext fallback`.
- SAVE-EARLY preserved: JSON is written by the solver itself; a 502 at the agent
  layer cannot lose the numerical result.
