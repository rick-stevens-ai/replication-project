# Failure analysis — Tazai2022 loop-current replication

Honest accounting of what did NOT work first-try, what remains out of scope, and
where the replication is qualitative rather than quantitative.

## Fixed during the run
### F1. Momentum-space Berry/Chern AHE gave nonsense (fixed -> real-space Kubo)
- **Symptom:** first C3 implementation summed the Berry curvature (Fukui method)
  of the single lowest kagome band. It returned Chern = 1.0 at `dt^c = 0` and
  ~0 (1e-16) when cLC was turned on — the exact OPPOSITE of the physics.
- **Root cause:** bare kagome has a quadratic band touching (flat band) at Gamma.
  The "lowest band" is degenerate there, so a single-band Chern number is
  ill-defined; the link-variable product picked up a spurious 2*pi winding
  independent of TRS. Also the imaginary structure factor I used (sin at
  half-angle) was not cleanly k-odd, so it failed to break TRS in the intended way.
- **Fix:** switched to a real-space Kubo-Greenwood Hall conductivity on the SAME
  6x6 kagome torus used for C1/C2, with velocity operators v_mu = i[H, R_mu].
  This is TRS-exact: sigma_xy is identically 0 when H is real (dt^c = 0), so the
  vanishing-without-cLC signature is guaranteed by construction, and a nonzero,
  sign-definite, TRS-odd value appears only with the imaginary cLC hopping.
- **Outcome:** C3 now passes on the two robust signatures (see caveats below).

## Known limitations / partial (NOT failures, but honest scope)
### L1. C3 magnitude and damping crossover not quantitative
- We reproduce the QUALITATIVE claims: sigma_xy = 0 without cLC (TRS), nonzero with
  cLC, and sign-flip under dt^c -> -dt^c. We do NOT reproduce (a) the absolute
  magnitude sigma_H ~ 1 (e^2/h) -> ~10^2 Ohm^-1 cm^-1, nor (b) the Fig-6a
  intrinsic-Hall crossover sigma_H ~ const (gamma << Delta) to sigma_H ~ gamma^-2
  (gamma >> Delta). Our finite-cluster Kubo uses a fixed broadening eta as a proxy,
  not the gamma-dependent two-Green-function form, and the staggered 3Q texture
  partially cancels on a small torus. The sigma_xy vs |dt^c| curve is therefore
  non-monotonic across the full range, and the small-|dt^c| linearity fit is weak
  (r^2 negative). This is the biggest gap between our replication and the paper's
  transport section. See open_questions.json Q2.

### L2. cLC is IMPOSED, not self-generated
- The paper's core mechanistic result — that BO fluctuations, via the linearized
  Maki-Thompson DW equation (lambda_q f = (T/N) sum I_q {-GG} f, I ~ -chi_g), drive
  the odd-parity cLC with max_q lambda_q -> 1 at q = q_n — is NOT solved here. We
  impose an imaginary odd-parity dt^c and verify its downstream consequences. So we
  confirm the cLC ORDER PARAMETER's properties, not its self-consistent emergence
  or the T_cLC/T_BO phase diagram (Fig 4). See open_questions.json Q1, Q5.

### L3. Z3 nematicity / GL free energy not evaluated
- The C6 -> C2 nematic selection from the 3rd-order GL coefficients
  (b1 b2 < 0; Supp Eqs. 35-38) is entirely out of scope of the current checks.
  See open_questions.json Q3.

### L4. chi0(q) is a Lindhard proxy, not the paper's full multi-index chi0_g
- C4 uses a bare inter-band/inter-sublattice Lindhard susceptibility summed over
  band pairs, evaluated near van-Hove filling with a small t' warp. This correctly
  reproduces the peak-at-M-vs-Gamma nesting signature but is not the exact
  form-factor-weighted chi0_g^{lmm'l'}(q) of Eq. (5). Filling/t' sensitivity not
  scanned (open_questions.json Q4).

## Not attempted (explicitly out of scope for an overnight kernel replication)
- Self-consistent chi_g(q) + self-energy Sigma_m(eps_n) loop (Methods Eq. 8).
- 60x60 k-mesh production numerics; multi-orbital extension; SC / PDW discussion.
- Aslamazov-Larkin vs Maki-Thompson diagram weighting; Ward-identity coefficient y.

## No fabrication statement
All numbers in REPORT/results.json are produced by running
`work/tazai2022_loop_current_checks.py`. Failed/partial items are labeled as such;
none were back-filled with invented values.
