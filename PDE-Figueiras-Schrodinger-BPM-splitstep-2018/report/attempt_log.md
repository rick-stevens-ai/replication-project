# Attempt Log

**Environment:** CherryRd (local, Darwin). Python 3.14.6; numpy 2.4.3, scipy 1.18.0, matplotlib 3.10.8. No GPU needed (all runs sub-minute → few minutes on CPU).

Paper PDF sha256: `034a26a1f606e6b1f5c5a0135a89d45c0ef137b5e763cabb10a190d67e933486`.

## Chronology
1. Selected target from PDE_NEXT50 list: rank 181 (Figueiras 2018, Schrödinger BPM). Rationale: Schrödinger/NLSE family uncovered in the set; clean analytic tests available; concrete verifiable numbers (reflectionless T=1, soliton shape preservation, O(dt) order). Dedup: no `*schrod*`/`*schrodinger*` dir existed. Verified target dir non-colliding.
2. Fetched OA PDF from IOP (Unpaywall-confirmed OA). `pdftotext -layout`. Extracted eq. 1 (dimensionless TDSE), eq. 2 (split-step algorithm steps I–V), eq. 3 (Pöschl-Teller), eq. 4/5 (cubic NLSE + bright soliton), eq. 6 (2D vortex).
3. Implemented `work/bpm.py` from scratch: `BPM1D`/`BPM2D` first-order Lie split-step Fourier, numpy FFT only. Kinetic factor exp(-i/2 dt k²) with angular-wavenumber grid; sign convention pinned by the analytic free-propagation test.
4. **Test 1 (analytic-first): free Gaussian wavepacket.** First pass showed constant L2=1.83 vs my analytic reference → my *reference formula* had a prefactor/phase bug (IC mismatch at t=0). Physics was already perfect (norm=1, COM=x0+k0T exactly, σ(T) matched spreading law to 12 digits). Fixed the closed-form propagator (standard Sakurai form) → IC vs analytic t0 = 8e-17, L2 vs exact at T=8 = ~1e-14 (split-step is *exact* for V=0, as expected). PASS.
5. **Test 2 (harmonic oscillator coherent state).** COM returns to displacement d=3.0 after one period; norm conserved. (Field self-conv metric here was noisy because ref used a fixed small dt and the coherent state nearly returns; superseded by Test 5 for the order claim.)
6. **Test 3 (reflectionless wavepacket).** Pöschl-Teller V=-s(s+1)/cosh²x, fast broad packet. R~1e-8 (machine noise), T=1.000000 for s=10,1,2,3 → reflectionless, matching paper Fig 1 (s=10). At this high energy R is tiny for non-integer s too (expected: exponential suppression), so this run alone does not discriminate the quantization.
7. **Test 3b (slow-packet discriminator).** Attempted to reveal reflection for non-integer s with a slow packet — inconclusive (deep-well/periodic-box regime; my inline analytic formula was also wrong). Abandoned as a discriminator.
8. **Test 3c (stationary-Schrödinger ODE scattering, independent method).** scipy solve_ivp. Correctly gave R≈0 for even integer s (1e-23–1e-27) but a spurious R≈0.44 for **odd** integer s (1,3). Diagnosed as a forward-integration instability for the reflectionless odd-parity case (the exponentially growing homogeneous mode must be exactly cancelled; roundoff breaks this). Not trusted for integer s.
9. **Test 3d (exact closed-form + derivation).** Derived R(k,s)=sin²(πs)/(sinh²(πk)+sin²(πs)) from √(1+4s(s+1))=2s+1. This gives R=0 **exactly iff s is an integer** — the paper's claim, proven and numerically 1e-32 for integer s. This closed form is the ground truth; the split-step (Test 3) is consistent with it for integer s.
10. **Test 4 (bright soliton, cubic NLSE κ=-1).** Single soliton: peak 1.00007 (exact 1), COM 7.4999999 (exact 7.5=x0+vT), field L2 vs exact eq-5 = 7e-4 over T=15, norm=2.0000. Two-soliton collision: peaks 1.0→0.99989 (preserved to 1e-4), norm=4.0000. Matches paper Fig 2 (solitons emerge unchanged). PASS.
11. **Test 5 (first-order accuracy).** Self-convergence on the nonlinear soliton (non-commuting operators → genuine Lie-splitting error). Successive-halving diffs ratio ≈2 → observed order **1.0005, 1.0002, 1.0001 = first order O(dt)**, exactly the paper's stated accuracy. PASS.
12. Generated figures: `fig1_reflectionless_s10.png` (repro Fig 1), `fig2_soliton_collision.png` (repro Fig 2).
13. Multi-judge assessment via free Argo endpoints (gpt-5.2, gemini-2.5-pro, gpt-4.1) — see `evidence/judge_*.json` and REPORT verdict.

## What worked / failed
- **Worked:** split-step implementation (exact for free case, first-order for nonlinear), all analytic validations, both paper phenomena (reflectionless integer-s, soliton propagation+collision), O(dt) order.
- **Failed/limited:** ODE-based scattering integrator unstable for odd integer s (documented; not used for the verdict). Non-integer-s reflection best shown by the exact closed form, not by wavepackets in this energy/box regime.
