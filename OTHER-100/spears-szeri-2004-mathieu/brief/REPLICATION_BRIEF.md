# Replication Brief — Spears & Szeri (2004), Physica D

**Paper:** B.K. Spears, A.J. Szeri, "Topology and resonances in a quasiperiodically forced oscillator," *Physica D* **197** (2004) 69–85. DOI: 10.1016/j.physd.2004.06.008
**Requested by:** Rick (for Brian Spears) — replicate OUT OF BAND (standalone, not part of PDE/LUCID/BVBRC collections).
**OCR status:** Embedded text + tesseract 300dpi cross-check complete. Sources in `../source/`, OCR in `../ocr/`.

## The model (Eq. 1/2)
Damped, cubic-nonlinear, quasiperiodically (two-frequency) parametrically forced Mathieu equation, modeling axial motion of a charged particle in a quadrupole ion trap:

    z'' + mu*z' + 4*(gamma + alpha*cos(2t) - delta*eps*cos(2*wf*t)) * (-z + chi*z^3) = 0

NOTE on epsilon placement: the secondary-forcing amplitude term reads `- eps*cos(2*wf*t)` in Eq.(1) and `- delta*eps*cos(2*wf*t)` after the rescale in Eq.(2). eps<<1 is the small perturbation parameter; chi, delta, mu are O(1); alpha, gamma are O(1) in the first stable Mathieu region. Implement BOTH readings and confirm which reproduces the figures (delta appears as an O(1) multiplier on the secondary forcing; in most figures delta=1 so they coincide, but Fig.2 has delta=10 and Fig.4 has delta=1 — use Fig.2 to disambiguate).

Suspended 4D autonomous form (R^2 x T^2), Sec 3.2:
    q1' = q2
    q2' = -mu*q2 - 4*(gamma + alpha*cos(theta1) - eps*cos(theta2))*(-q1 + chi*q1^3)   [paper writes beta*q1^3; that is a typo for chi]
    theta1' = 2
    theta2' = 2*wf

## Core claims to reproduce
1. **Resonance criterion:** large-amplitude solutions occur only at secondary frequencies `wf,res = p + beta`, p in Z, where beta(alpha,gamma) is the fundamental Mathieu exponent (Eq. 9, continued fraction). "Central resonance" = p=0, i.e. wf = beta. Far from resonance, solutions decay to 0 exponentially.
2. **Fundamental frequency beta** via continued-fraction Eq.(9) and coefficients D_2n via Eqs.(10,11). Verify the quoted values: for (alpha=0.15, gamma=-0.05) beta=0.5094 (Fig.1); for (alpha=0.25, gamma=0.001) wf=2+beta=2.3674 => beta=0.3674 (Fig.2).
3. **Multiple-scales approximation** matches direct numerical integration of Eq.(2) on both fast and slow time scales (Figs. 4-5, 7-9, 13-14). Slow-amplitude ODEs (Eqs. 16-17) cubic form: A' = g1 B^3 + g2 A^2 B + g3 A + g4 B ; B' = h1 A^3 + h2 A B^2 + h3 B + h4 A.
4. **Slow-time (A,B) dynamics:** spirals into stable focus at resonance (Fig.6). With detuning wf = beta + nu (Eq.19), slow equations become nonautonomous (forcing freq 2*nu); on large-amplitude branch the (A,B) solution becomes a 2-periodic limit cycle (Fig.15, Poincare).
5. **Response diagram** z_inf vs wf (Fig.12): two trivial (decay) branches + one large-amplitude stable branch, unstable branch between; two bifurcations near wf=0.6375 and wf=0.6405 (params alpha=0.05, gamma=-0.1). MS approximation branches match numerics.
6. **Asymptoticity / accuracy controlled by |D_-2|:** small |D_-2| => good approx. Quoted: (alpha=0.05,gamma=-0.1) gives D_-2=-0.07 (good, Figs.4-6); (alpha=-0.04,gamma=0.125) gives D_-2=-0.11 (worse, Figs.7-9).
7. **Topology / TTBs (stretch goal):** Poincare sections Sigma_theta1, Sigma_theta2; nonresonant attractor = 1-strand braid (Fig.16); resonant = 2-strand braid (Fig.17); the two bifurcations are type-II doubling TTBs; appear as period-doubling in slow-time equations (Fig.18). Saddle tori via fixed points of Ps^2.

## Exact figure parameter table (for validation targets)
- Fig.1 (central resonance, knotted torus): alpha=0.15, gamma=-0.05, mu=delta=chi=1, eps=1e-3, wf=beta=0.5094
- Fig.2 (p=2 resonance, small amplitude): alpha=0.25, gamma=0.001, eps=1e-3, mu=0.8, delta=10, chi=5, wf=2+beta=2.3674
- Fig.3 (decay, off-resonance): alpha=0.15, gamma=-0.05, mu=delta=chi=1, eps=1e-3, wf=2*beta=1.0187
- Fig.4/5/6 (good approx, D_-2=-0.07): alpha=0.05, gamma=-0.1, mu=delta=chi=1, eps=1e-3, wf=beta
- Fig.7/8/9 (worse approx, D_-2=-0.11): alpha=-0.04, gamma=0.125, mu=delta=chi=1, eps=1e-3, wf=beta
- Fig.10/11 (detuned, decay): wf = beta - 2.6, other params = Fig.4
- Fig.12 (response diagram): alpha=0.05, gamma=-0.1, mu=delta=chi=1, eps=1e-3
- Fig.13/14 (detuned, still resonant): alpha=0.05, gamma=-0.1, mu=delta=chi=1, eps=1e-3, wf=beta-0.5
- Fig.18 (invariant manifolds): alpha=0.05, gamma=-0.1, mu=delta=chi=1, eps=1e-3, wf=0.637

## Deliverables (out-of-band, standalone)
- `code/` : (1) `mathieu_beta.py` — continued-fraction solver for beta(alpha,gamma) + D_2n (Eqs. 9-11), verify 0.5094 / 0.3674 / D_-2 values. (2) `simulate.py` — direct RK integration of Eq.(2) reproducing Figs. 1,2,3 time series (resonant knotted torus vs decay). (3) `response_diagram.py` — sweep wf, plot z_inf vs wf reproducing Fig.12 shape with bifurcations ~0.6375/0.6405. (4) `slow_amplitudes.py` — derive/integrate (A,B) ODEs, show spiral-to-focus (Fig.6) and detuned 2-periodic limit cycle (Fig.15). (5) optional `topology.py` — Poincare braids Fig.16 vs 17.
- `figures/` : regenerated figure analogs.
- `report/REPORT.md` : four-tier verdict (REPLICATED / PARTIAL / SPOT-CHECK / NO-GO) on Coverage/10 + Agreement/10 per AUDIT_PROTOCOL conventions. Document which claims reproduced, quantitative agreement (beta values, bifurcation locations, branch amplitudes), and any discrepancies.
- `evidence/` : raw numerical outputs, beta/D_2n tables, sweep CSVs.

## Free-endpoint discipline
All compute local (CherryRd Python) — pure numerics, no GPU needed. No paid endpoints. If a subagent is used, model = argo/argo:claude-opus-4.7 (free). NEVER anthropic-direct.
