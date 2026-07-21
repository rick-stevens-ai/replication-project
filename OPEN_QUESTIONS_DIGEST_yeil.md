# TEXTURES-100 — Yéil Lane: Open-Questions Digest

*Generated 2026-07-20 20:54 · 58 papers · **293 open questions** · 10 REPLICATED / 48 PARTIAL*

Every replication package ships a `report/open_questions.json` with structured research questions (`question` / `why_it_matters` / `next_step`). This digest collates all of them, quick-wins first.

---

## ⭐ Quick-Win Candidates — 21 papers (PARTIAL, Agreement ≥ 8/10)

These reproduced the paper's headline closely (high Agreement) but scored lower Coverage — i.e. the physics is *right*, the gap is scope/resolution/compute. Each is a plausible **PARTIAL → REPLICATED** flip with a bounded push. First open question per paper = the highest-leverage next step.

| Paper | Class | C/A | Highest-leverage next step |
|---|---|---|---|
| `spin-jungwirth2024` | Spin | C3/A9 | Extend the 2-sublattice model to a 4-sublattice (or hexagonal) lattice whose C6/C3 symmetr |
| `orbital-oh2026` | Orbital | C4/A9 | Run FPLO GGA-PBE (12^3 mesh) on the Materials Project relaxed (TaSe4)2I structure for both |
| `polar-morozovska2021` | Polar | C4/A9 | Does the full 3D cylindrical core-shell flexon geometry (two diffuse axial P3-domains near |
| `spin-gurung2023` | Spin | C4/A9 | Run a noncollinear DFT (e.g. VASP/QE + Wannier90) for Gamma_5g Mn3GaN, downfold to a tight |
| `loop-current-christensen2022` | Loop-Current | C5/A9 | Compute the DFT VHS orbital/sublattice content at M and evaluate which iCDW channel has th |
| `loop-current-yang2022` | Loop-Current | C5/A9 | Build the 3Q-iCDW Hamiltonian in a real-space 2x2x(open-y) kagome supercell with per-bond  |
| `polar-tian2026` | Polar | C5/A9 | Run a magnetic (Neel, out-of-plane) DFT+U calculation of monolayer Mg2Mo2(PO5)2 (P4, a=6.5 |
| `spin-lund2021` | Spin | C5/A9 | Extend the LSWT kernel to compute the full k-resolved eigenvectors and project them onto x |
| `spin-wernert2024` | Spin | C6/A9 | Implement the Gaussian-driven a.c. field (Eq.15, sigma=2, omega=1), linearized LLG on the  |
| `polar-brazovskii2003` | Polar | C7/A9 | Compute the quantum breather bound-state spectrum in the spectral window between the colle |
| `orbital-malashevich2012` | Orbital | C3/A8 | Run Quantum ESPRESSO SOC LSDA+U (U=2.0, J=0.8 eV) on the corundum cell: finite-E-field mag |
| `loop-current-kumar2015` | Loop-Current | C4/A8 | Extend loop_current_kagome_kernel with the explicit (2pi, pi/2, pi/2) per-triangle flux (t |
| `multipolar-you2021` | Multipolar | C4/A8 | Rebuild LLG in SI units with Co/Pd Ms~1.4e6 A/m, Hk from the RAHE-H loop, t=3.6 nm, and th |
| `multipolar-banerjee2026` | Multipolar | C5/A8 | Recompute with the paper's exact geometry (psi_0, r_pd/r_dd from Slater-Koster edge-sharin |
| `polar-lohani2019` | Polar | C5/A8 | Does the quantum skyrmion's exponentially small bandwidth, arising from skyrmion<->antisky |
| `polar-verga2014` | Polar | C5/A8 | Implement the coupled stepper (Crank-Nicolson or Chebyshev for Schrodinger; Heun/RK4 for L |
| `spin-fernandes2026` | Spin | C5/A8 | Does the intrinsically-3D hexagonal g-wave altermagnet (D_6h, CrSb/MnTe/Co1/4NbSe2) reprod |
| `spin-jaubert2016` | Spin | C5/A8 | Rerun on L=6-8 with dense q-sampling around (0,0,2) and (1,1,1), fit the transverse S(q) t |
| `polar-berloff2008` | Polar | C6/A8 | Does the macroscopic vortex split require 3D vortex RINGS, or can a 2D straight vortex spl |
| `spin-chen2026` | Spin | C6/A8 | Run rt-TDDFT (or at least a Wannier-interpolated DFT+SOC band structure) on the crux compu |
| `multipolar-chen2022` | Multipolar | C7/A8 | Implement the full self-consistent loop solving chi1=<s~+ s~->, chi2=<s~+ s~x>, I1=I2=<Phi |

---

## Full Question Bank (by texture class)

### Orbital — 13 papers, 65 questions

#### `orbital-choi2021` — PARTIAL (C4/A5)

1. **Why does the surrogate d-orbital TB give sigma_OH ~ 10^2-10^3 (peak ~775) rather than the exact 3800?**
   - *Why:* The factor ~5 gap separates 'correct order of magnitude / correct mechanism' from a quantitative DFT-level match; knowing its origin tells us whether the physics or just the parameters are missing.
   - *Next:* Add s and p orbitals (spd hybridization) and fit Slater-Koster parameters to a real fcc-Ti DFT band structure (e.g. Wannier90), then recompute sigma_OH at the true E_F.
2. **How sensitive is sigma_OH to the exact position of E_F within the Ti d-manifold?**
   - *Why:* The fine E_F sweep shows sigma_OH changing sign and magnitude sharply (peaks near band near-degeneracies), so the reported 3800 may sit on a steep feature; small E_F errors could swing the answer a lot.
   - *Next:* Compute sigma_OH(E_F) on a denser k-grid with adaptive refinement near the orbital-Berry-curvature hot spots and locate Ti's actual E_F from electron count (d^2 s^2).
3. **Does including SOC actually produce the small sigma_SH = -40 observed, alongside the large OHE?**
   - *Why:* The paper's headline is the two-orders-of-magnitude OHE/SHE ratio; our model sets SOC=0 so sigma_SH is identically 0. Adding weak SOC would test whether the ratio ~-95 emerges naturally.
   - *Next:* Add an on-site lambda L.S term (lambda ~ 20-30 meV for Ti), recompute both sigma_OH and sigma_SH via the same Kubo machinery, and compare the ratio to ~-95.
4. **Is the coarse-k convergence trustworthy given the sign flip between nk=12 and nk=16?**
   - *Why:* Orbital Berry curvature has sharp k-space hot spots; a coarse grid can under- or mis-sample them, so the reported converged value carries real grid uncertainty.
   - *Next:* Run nk=24,32 (and a tetrahedron or adaptive integration) to establish a converged sigma_OH and error bar before quantitative comparison.
5. **How does the intrinsic (bulk) sigma_OH connect to the experimentally measured surface orbital accumulation / Kerr signal?**
   - *Why:* The paper measures a MOKE Kerr rotation from surface-accumulated orbital moments, not sigma_OH directly; the link requires orbital drift-diffusion (orbital relaxation length lL ~ 74 nm) and magneto-optics.
   - *Next:* Couple the computed bulk sigma_OH to a 1D orbital drift-diffusion model with the paper's kappa and lL, then to a magneto-optical Kerr model to predict theta_K/j_c.

#### `orbital-comtesse2014` — PARTIAL (C5/A6)

1. **Does an explicitly nucleated, coupled BEG+Potts+magnetoelastic MC (single simulation with dynamic sigma) reproduce Tm and the hysteresis, rather than the two-branch free-energy-crossover surrogate used here?**
   - *Why:* The paper emphasizes a first-order martensitic transition WITH thermal hysteresis (inset of Fig. 3b). Our coarse retry sidesteps the nucleation barrier by running fixed-phase branches and merging at the free-energy crossover; it therefore reproduces Tm and dM but not the hysteresis loop width.
   - *Next:* Run the fully coupled dynamic-sigma MC with cluster/Wolff or parallel-tempering moves and heating+cooling sweeps to recover the hysteresis and confirm Tm is identical to the branch-crossover value.
2. **How sensitive is dT_ad to the specific-heat model? We used a per-atom Dulong-Petit C ~ 386 J/kgK; the paper uses a full Debye lattice term plus the field-dependent magnetic C(T,H).**
   - *Why:* Our dT_ad = -10.8 K overshoots the paper's -6 K by ~1.8x, and dT_ad is inversely proportional to C. A more realistic (temperature- and field-resolved) C near Tm could bring dT_ad into closer agreement.
   - *Next:* Implement a proper Debye C(T) with the alloy's Debye temperature and add the MC-derived magnetic C(T,H) at both fields; recompute dT_ad and RCP with the field-integrated Eq. 5 as a cross-check.
3. **Are the effective lattice exchange constants (J_YY, J_ZA, J_ZM) quantitatively consistent with the paper's KKR-CPA orbital-resolved Jij (Fig. 1), or merely qualitatively FM/AFM-competing?**
   - *Why:* We tuned three effective bond energies to place Tm ~ 300 K and reproduce dM; the paper derives Jij ab initio with t2g (FM) / eg (AFM) decomposition. Quantitative fidelity of the driving mechanism hinges on matching those magnitudes.
   - *Next:* Digitize Fig. 1 (Ni50Mn30Ga20 austenite/martensite Jij vs distance), map the dominant MnY-MnY / MnY-MnZ constants onto nearest-neighbor lattice bonds, and re-run without free tuning.
4. **Does the RCP proxy (dS x 20 K FWHM) explain the 2x overshoot vs the paper's -132 J/kg, or is the entropy-change width itself different?**
   - *Why:* RCP is a key figure of merit. Our -281 J/kg uses a crude fixed 20 K width; the paper integrates the actual dS(T) peak. The dS magnitude matches, so the discrepancy is likely in the assumed peak width.
   - *Next:* Compute the full dS_mag(T) curve at 2 T from MC (Eq. 5 Maxwell relation away from Tm plus Eq. 6 at Tm), integrate RCP = int dS dT over the FWHM directly.
5. **How do finite-size (L=12) and Monte-Carlo-sampling (60/40 sweeps) errors bound the reported dM(Tm) and dS_mag?**
   - *Why:* The coarse, performance-bounded retry uses a small lattice and short sampling for a <4 min budget. Statistical/finite-size drift in dM directly propagates (linearly) into dS_mag, dT_ad and the verdict margin.
   - *Next:* Run an L in {8,12,16,20} finite-size scan with 5 RNG seeds each, extrapolate dM(Tm) to the thermodynamic limit, and report error bars on dS_mag and dT_ad.

#### `orbital-cullen2025` — PARTIAL (C4/A6)

1. **Build the dominant quantum correction Delta j1 (interband-polarization / dipole-rotation term of Eq. 6) and check whether it alone lifts the conventional ~49 toward the ~10^3 headline.**
   - *Why:* The paper's whole thesis is that quantum corrections DOMINATE the OHE; Delta j1 (and Delta j2) are named as the two largest contributions (Fig. 2, lines 590-591). Without them the ~20x gap to the headline cannot close, and 'orbitronic promise of Ge' rests entirely on this unbuilt physics. This is the single most important missing piece.
   - *Next:* Implement the covariant-derivative form of the interband OAM current from the modern theory of orbital magnetisation (Eq. 6 first term, all velocity + off-diagonal OAM elements). Reuse the existing spherical eigenbasis kernel in work/ohe_spherical.py; add the interband-dipole matrix elements. Validate order-of-magnitude against paper Fig. 2 sigma-component curves.
2. **Build Delta j2 (interband OAM matrix elements / time-fluctuating OAM) and Delta j3 ([r,v] non-commutativity, opposite sign) and reconstruct the full signed sum sigma_L + sigma_conv + Delta sigma_1,2,3.**
   - *Why:* Delta j3 has OPPOSITE sign to all other contributions (line 522), so the total is a signed cancellation, not a simple sum. Getting the net ~10^3 requires all terms with correct relative signs; a partial build could give a spuriously wrong magnitude. Tests whether our conventional piece has the right sign relative to the corrections.
   - *Next:* Extend the kernel with the L-operator interband matrix elements and the position-velocity commutator term; assemble the signed total and compare each component's magnitude/sign to Fig. 2 (sigma_L, sigma_conv, Delta sigma_1, Delta sigma_2, Delta sigma_3 curves for Ge).
3. **Does the full (non-spherical) 4x4 and the 6x6 LKBP Hamiltonian change the Ge number materially, and is it required for the other four semiconductors (Si especially)?**
   - *Why:* The paper uses the spherical 4x4 only for analytic insight and switches to full 4x4 / 6x6 for numerical accuracy; Si REQUIRES 6x6 (small delta_so ~40 meV, large gamma2-gamma3 difference). Our spherical Ge number cannot be extended to Si without the 6x6, and cubic anisotropy (gamma2 != gamma3) may shift even the Ge value.
   - *Next:* Implement Eq. (1) full 6x6 with material-specific gamma1,gamma2,gamma3,delta_so from the paper's Table I; rerun the Kubo integration for Ge (check vs spherical) then Si/GaAs/InAs/InSb.
4. **Is the community-standard Go-et-al conventional-Kubo convention we used numerically identical to the paper's 'proper' current (Eq. 7 analogue with the tilde/check non-degenerate/degenerate matrix-element split)?**
   - *Why:* For spin-3/2 holes the OAM is not conserved, so the proper vs conventional current distinction (which the paper stresses for the SHE, lines 555-558) can differ by O(1) factors or more. If our sigma_conv ~49 is computed in a slightly different convention than the paper's sigma_conv curve, even the 'conventional agreement' claim needs a convention audit.
   - *Next:* Derive the proper orbital current from Eq. (7) with L replacing s, implement the degenerate-manifold (check) vs non-degenerate (tilde) Berry-connection split explicitly, and compare to our braced-anticommutator conventional form at identical params.
5. **How do the OHE (and the dominant quantum corrections) scale with Fermi energy / hole density, and does the predicted ~10^3 survive at experimentally accessible densities?**
   - *Why:* Our conventional piece already drops from 49 (EF=10 meV) to 34 (EF=5 meV) -- a strong density dependence. The paper's orbitronic proposal for Ge is only useful if the large OHE persists at realistic p-type doping; the EF-dependence of the DOMINANT quantum-correction terms is the experimentally decisive curve.
   - *Next:* Once Delta j1,2,3 are built, sweep EF (or hole density n) across the paper's stated range (up to ~10 meV) and reproduce the total sigma_OHE(EF) trend; compare to the paper's density-dependence figure and to the YIG/W/Ge, YIG/Pt/Ge experimental order of magnitude (Ref. 62).

#### `orbital-dar2026` — PARTIAL (C5/A5)

1. **Why is the fourfold angular modulation of the triplet intensity essentially identical in the AM (rho_z=0.1) and AFM (rho_z=0) runs, when the paper's Fig. 4(a,b) shows it is unique to the altermagnet and vanishes at rho_z=0?**
   - *Why:* This is the paper's single most falsifiable claim and the physical signature that distinguishes an altermagnet from an antiferromagnet in this setup. If it cannot be resolved, the replication cannot confirm the headline. Our result suggests the emergent SOC alpha ~ r_hat (present in both limits) dominates the on-wall angular structure while the AM-only V_z ~ cos(2*chi) contributes only <=3%.
   - *Next:* Increase rho_z toward the paper's exchange-dominated regime and sweep rho_z in {0, 0.05, 0.1, 0.2, 0.3} to test whether the l=4 FFT power grows monotonically and separates from the AFM baseline; if it does, the null result is a small-rho_z / weak-anisotropy artifact, not a physics disagreement.
2. **Is the triplet-to-singlet ratio of ~0.4% intrinsic, or an artifact of the semiclassical, non-self-consistent fixed Delta_0 and the coarse 1.6 nm grid?**
   - *Why:* At 0.4% the AM-vs-AFM triplet contrast is a difference of small numbers (replication-skill pitfall 8), so no quantitative AM signature can be trusted until the triplet channel is resolved with enough dynamic range.
   - *Next:* Re-run with a self-consistent Delta(r) = V_sc <c_up c_dn> iteration (recipe step 5) and a finer grid (a<=0.8 nm, N>=88), and confirm the singlet suppression near the wall predicted by the altermagnet lifting Kramers degeneracy; compare triplet/singlet ratio vs grid to check convergence.
3. **Does a properly Wigner-transformed, momentum-resolved triplet correlator F_sigma-sigma(R,p) (paper Eq. 15) reproduce the rotating p_R=0 nodes and the spin-dependent elliptical node condition, which our on-site bond-correlator proxy for Eq. 16 cannot directly show?**
   - *Why:* The paper's mechanism for the hotspots is the d-wave form factor deforming a circular node (AFM) into a spin-dependent ellipse (AM). Our real-space bond intensity integrates over p and loses the node structure that actually carries the fourfold pattern.
   - *Next:* Compute F_sigma-sigma(R,p) on a local k-grid at several wall positions R, extract the node loci, and verify the circle->ellipse deformation and the pi/2 rotation of nodes around the wall (paper Fig. 3), then integrate Eq. 16 exactly rather than via the nearest-neighbor bond proxy.
4. **What is the supercurrent-induced quadrupolar torque tau_quad(R) (Sec. VII), and does it inherit the fourfold symmetry of the altermagnetic order parameter?**
   - *Why:* This is the paper's second headline (the reciprocal effect) and was entirely scoped out of the present replication; without it, coverage of the paper's results is capped near half.
   - *Next:* Extend the BdG solver to the finite-Cooper-pair-momentum form (Eq. 17, Delta -> exp(iQ.R)Delta), compute the quasiparticle contribution to the torque via tau = <dH/dn(R)>.J_s, and test the Q-linear quadrupolar (fourfold) angular pattern near the wall.
5. **Do the local BdG spectra exhibit the paper's position-dependent nodal-to-fully-gapped transitions around the wall, and how does the minimum gap vary with chi?**
   - *Why:* The paper claims the local spectrum is fully gapped or point-nodal depending on wall position, tied to both the wall and the altermagnetic order; our single global min|E_BdG|=5.1e-4 does not resolve this angular gap structure.
   - *Next:* Compute the angle-resolved local density of states / minimum quasiparticle gap as a function of chi along the wall annulus, and map where the spectrum closes (nodes) vs stays gapped, comparing to the paper's node conditions (sigma*xi - b_z = 0).

#### `orbital-ding2026` — PARTIAL (C4/A7)

1. **Is the checkerboard altermagnetic order actually the ground state at 0.25 hole/Fe, or merely a low-lying metastable configuration?**
   - *Why:* The paper's own discussion warns that imposing a checkerboard config and observing splitting does NOT prove it is the true ground state. Only a full 8-configuration total-energy comparison (which our TB surrogate cannot do) settles this.
   - *Next:* Run spin-polarized DFT (or a Heisenberg-plus-doping model) enumerating all 8 magnetic configs vs. doping to confirm the dimer->checkerboard transition and its critical doping.
2. **What sets the absolute 620 meV scale microscopically — is delta (ligand hopping anisotropy) really ~0.09 eV for Cl on FeSe?**
   - *Why:* Our surrogate reproduces 620-720 meV only after tuning delta; the value is not derived from first principles. The magnitude claim rests on the true Cl-induced anisotropy.
   - *Next:* Wannier-downfold the DFT bands of Fe2Se2Cl to extract the real Fe-Fe hopping anisotropy and on-site exchange, then feed them into this TB model unmodified.
3. **How does SOC modify the splitting and open the reported anti-crossings (Weyl gapping along X-M vs M-Y)?**
   - *Why:* The paper reports Neel-vector-dependent Weyl gapping ([100] vs [110]) that our spin-conserving no-SOC model cannot capture, but which is central to the spintronic/topological pitch.
   - *Next:* Add a Rashba/atomic SOC term lambda (L.S) to the 4x4 (spinful, 2-sublattice) Hamiltonian and track anti-crossing gaps vs Neel-vector orientation.
4. **Does the altermagnetism truly survive in the 10-layer slab / bulk limit as claimed?**
   - *Why:* The robustness-to-bulk claim is a key novelty (surface-driven, decoupled from nonmagnetic bulk). A 2D monolayer TB cannot test interlayer hybridization.
   - *Next:* Extend the TB model to a multilayer stack with interlayer hopping t_perp and a nonmagnetic underlayer; check whether the top-layer d-wave splitting persists.
5. **Would the lifted spin degeneracy actually bias equal-spin triplet pairing as the paper speculates?**
   - *Why:* The headline application (Majorana / topological quantum computing) hinges on triplet SC emerging from the altermagnetic normal state.
   - *Next:* Add an attractive interaction to the TB model and solve the linearized gap equation to see whether Delta_up-up / Delta_dn-dn channels are favored over singlet.

#### `orbital-durnev2023` — REPLICATED (C7/A9)

1. **Does the full Eq (20)+(22) angular-sum conductivity reproduce the same spectral lineshape off-resonance as the near-resonance closed forms Eq (25)/(26) used here?**
   - *Why:* The closed forms assume Omega*tau0 >> 1 and omega ~ Omega. Off-resonance the full angular-harmonic sum could diverge from the Lorentzian approximation, affecting the wings of the Faraday spectrum in Fig. 2/3.
2. **Do the parabolic-dispersion (bilayer/2DEG) formulas Eq (21)/(23)/(24) yield the same order-of-magnitude 0.1 deg / 0.1 T as the graphene case?**
   - *Why:* The paper claims generality across linear and parabolic spectra; only the linear/graphene branch was coded here, leaving half the paper's headline scope unverified.
3. **Is theta_K approx -theta_F an adequate substitute for the independent Kerr evaluation via Eq (6) at the n1=1, n2=3 dielectric contrast?**
   - *Why:* The Kerr angle carries the reflection Fresnel factors; at finite (not infinite) contrast theta_K may deviate from -theta_F by a non-negligible factor, changing the Kerr headline number.
4. **How sensitive is the peak Faraday angle to the choice tau0/tau1 ratio, and does the paper's Fig. 3 assume tau0 = 5 ps or 10 ps?**
   - *Why:* theta_F and B_syn scale with tau0; the 2x ambiguity (5 vs 10 ps) between Fig. 3 params and the paper's explicit B_syn estimate propagates directly into the headline agreement (0.044 vs 0.1 deg).
5. **Does a pixel-level digitization of Figs. 2-4 confirm the resonance peak position and width predicted by Eq (26)?**
   - *Why:* Cross-checks match the paper's stated scalar numbers, but no figure-level curve comparison was done; the resonance width (set by tau0) is untested against the plotted lineshape.

#### `orbital-göbel2025` — PARTIAL (C4/A6)

1. **Does replacing the itinerant L_z = 0.5(X v_y - Y v_x) operator with the modern-theory-of-orbital-magnetization current operator drive the uniform-FM reference conductivity to ~0, yielding a clean topological residual?**
   - *Why:* The current 275 [e/2pi] residual is a difference of two large numbers (4330 - 4055). A non-zero FM reference proves the operator carries a spurious PBC trivial contribution, so the isolated 'topological' number is not trustworthy quantitatively.
   - *Next:* Implement the k-space modern-theory OAM operator (Wannier/Bloch derivative form) and re-evaluate sigma^Lz_xy for the uniform FM; verify it vanishes by symmetry before trusting the hopfion residual.
2. **How does sigma^Lz_topological converge with reciprocal-space k-mesh density (paper uses ~40x40x40) versus the single Gamma-point real-space supercell used here?**
   - *Why:* The real-space Gamma-only cell samples one k-point; the paper's energy-resolved sigma(E) curves require dense BZ integration. Convergence controls whether the sign and magnitude of the Hall response are physical.
   - *Next:* Port the Hamiltonian to a Bloch/reciprocal-space form and sweep n_k = 4, 8, 16, 32, 40; check sigma^Lz_xy(mu) for a plateau.
3. **Are the in-plane orbital Hall tensor elements (sigma^Lx and sigma^Ly, e.g. sigma^Lz_yz-type) finite and consistent with the paper's Fig. 3, which is the distinguishing 3D signature versus a 2D skyrmionium?**
   - *Why:* The paper's central novelty is that a hopfion produces BOTH out-of-plane and in-plane orbital Hall conductivities; only sigma^Lz_xy was computed here, so the uniquely-3D part of the claim is untested.
   - *Next:* Extend the Kubo kernel to build L_x, L_y operators and compute the full sigma^{L_alpha}_{beta gamma} tensor; compare the in-plane components against the hopfion Hopf-index expectation.
4. **Does the topological orbital Hall residual scale with the Hopf index (e.g. multi-twist or H=2 hopfions) rather than with lattice-specific artifacts?**
   - *Why:* The paper's headline is that the 3D orbital Hall effect is the electronic manifestation of the Hopf index. Demonstrating proportionality to H (and vanishing for a trivial texture) is what separates topology from a numerical accident.
   - *Next:* Construct textures with Hopf index H=0,1,2 (varying the helical z-twist number) and check whether the topological residual scales linearly with H.
5. **How robust is the effect to finite temperature, disorder, and finite quasiparticle lifetime (broadening eta), i.e. is it observable in a real device?**
   - *Why:* The paper motivates hopfion detection in spintronic devices; the T=0, clean, DC calculation says nothing about whether the orbital Hall signal survives room-temperature broadening and impurity scattering.
   - *Next:* Add a Fermi-Dirac occupation factor and a finite eta in the Kubo-Bastin denominator; sweep T and eta and report the degradation of sigma^Lz_xy(mu).

#### `orbital-lux2017` — PARTIAL (C6/A7)

1. **Can the absolute 1/4*chi_LP coefficient (Eq. 12) be recovered by replacing the itinerant 1/2(r x v) operator with the modern-theory-of-orbital-magnetization (Berry-phase) L_z operator?**
   - *Why:* The headline is a quantitative prefactor (1/4 for TOM vs 1/2 for COM). Our lattice itinerant operator confirms linearity in chirality and the sign, but its normalization does not map onto the continuum Landau-Peierls susceptibility, so the absolute 1/4 is untested. This is the same limit that caps gobel2024/2025 to qualitative agreement.
   - *Next:* Implement the Bianco-Resta / modern-theory M_orb = (e/2 hbar c) Im Tr[P r Q H Q r P] (Q=1-P) on the same lattice, extract M_tom/chi in physical units, and compare to (1/4)(-e^2/12 pi m_e)*(hbar/2e).
2. **Does the clean mu-parabola (1 - 3 mu^2/Delta^2) emerge in the near-band-edge continuum limit of the lattice model?**
   - *Why:* H2 only reproduced a qualitative sign change; the paper's clean parabola is a band-edge result. Confirming it would close the second structural claim.
   - *Next:* Restrict the mu-sweep to a narrow window just above the lower band bottom (parabolic regime), increase L to reduce finite-size van Hove structure, and fit M_tom(mu) to a+b*mu^2; check b<0 and the sqrt(3) sign-change location |mu|=Delta/sqrt3.
3. **Is the COM branch (Eq. 8/11), linear in alpha_R and in the 1D spiral gradient, reproducible with a Rashba SOC term added to the lattice s-d model?**
   - *Why:* The paper's second half is the SOC-driven chiral orbital magnetization; the 1/2 prefactor (vs TOM's 1/4) is the companion claim. We only built the zero-SOC TOM branch.
   - *Next:* Add alpha_R (sigma x p)_z hopping phases to build_H_custom, use a 1D Neel spiral n=(sin qx,0,cos qx), and verify M_com ~ alpha_R and M_com vanishes as alpha_R -> 0 (Eq. 8).
4. **Can the full Fig. 2 (alpha_R, Delta_xc) TOM phase diagram, including the |alpha_R|>|Delta_xc| enhancement region, be mapped?**
   - *Why:* The paper's headline figure shows both the stability of Eq. 12 for Delta>>alpha and a strong non-linear enhancement where alpha>Delta. Reproducing the enhancement region tests the physics beyond the perturbative gauge-field picture.
   - *Next:* Sweep (alpha_R, Delta_xc) on a grid at mu=0 for the Neel skyrmion, evaluate TOM at the core, and look for the enhancement lobe where alpha_R exceeds Delta_xc.
5. **How faithfully does the direct lattice diagonalization reproduce the semiclassical Green-function gradient expansion order-by-order (COM=1st, TOM=2nd order in gradients)?**
   - *Why:* The paper's method IS the gradient expansion; a from-scratch replication that instead diagonalizes the model does not directly verify the diagrammatic order counting. Bridging the two would validate the expansion itself.
   - *Next:* Compute M_orb as a function of a texture-gradient scaling parameter lambda^{-1} (skyrmion size) and fit the leading powers; TOM should scale as (gradient)^2 while COM (with SOC) scales linearly.

#### `orbital-malashevich2010` — PARTIAL (C6/A3)

1. **Can the paper-level PBC-vs-bounded agreement (differences ~1e-7 e^2/hc) be reproduced with the full L=4..7 + 1/L,1/L^2,1/L^3 extrapolation?**
   - *Why:* This quantitative cross-method agreement IS the headline validation of the k-space OMP formula; our L<=5 clusters leave alpha at the noise floor.
   - *Next:* Build open clusters L=4,5,6,7 (up to ~2925 sites -> sparse eigensolver), fit M(L) to the cubic-in-1/L form, and compare to the smooth-gauge PBC value at matched phi.
2. **Does the non-Abelian Chern-Simons integral (47a) converge to a gauge-invariant theta_CS on a fine, globally smooth k-mesh?**
   - *Why:* The CS 3-form is only locally gauge-invariant; a one-shot delta-projection on an 8^3 grid can leave large gauge-noise, which we observed (theta_CS ~ 1e-4 scatter).
   - *Next:* Implement a max-localized-Wannier / twisted-parallel-transport smooth gauge on a 40^3+ mesh and check theta_CS convergence vs mesh density.
3. **What are the actual magnitudes and phi-dependence of alpha_zz and alpha_zy reported in the paper's Fig. 1/Fig. 3?**
   - *Why:* The corpus text (pdftotext) did not preserve the numerical y-axis values, so we lack a hard target number for a quantitative agreement score.
   - *Next:* Digitize Fig. 1 (alpha_zz, alpha_zy vs phi) and Fig. 3 (theta_CS, theta_LC, theta_IC vs phi) from the PDF and store as reference curves.
4. **Do the Kubo-like terms alpha_LC (47b) and alpha_IC (47c) contribute significantly to the trace for this ordinary insulator?**
   - *Why:* The paper's key conceptual result is that theta = theta_CS + theta_Kubo (unlike Z2 TIs where only CS survives); we only implemented the CS term.
   - *Next:* Implement eqs (47b)-(47c) using the covariant field-derivative (50) and compare theta_CS/theta_LC/theta_IC decomposition against Fig. 3.
5. **Is the diagonal-r (convention II) Bloch Hamiltonian consistent with the paper's finite-field r.E coupling on the bounded sample?**
   - *Why:* Gauge/convention mismatch between PBC Bloch phases and open-BC position operator can shift alpha; must be pinned before trusting cross-method agreement.
   - *Next:* Cross-check by computing M(E=0) orbital magnetization both ways (k-space eq 6b-6d vs bounded Tr[P rxv]) and confirm they match before differentiating.

#### `orbital-malashevich2012` — PARTIAL (C3/A8)

1. **What are the numerical spin-lattice (0.77 ps/m) and spin-electronic (0.26 ps/m) contributions to alpha_perp when computed from scratch with SOC DFT+U?**
   - *Why:* These two terms are ~98% of the 1.04 ps/m headline; the entire absolute agreement with experiment rests on them, yet they were out of scope for the fast tight-binding run.
   - *Next:* Run Quantum ESPRESSO SOC LSDA+U (U=2.0, J=0.8 eV) on the corundum cell: finite-E-field magnetization for spin-electronic, plus phonons + Born charges for spin-lattice.
2. **Does an explicit ab-initio Z2/parity evaluation of Cr2O3 confirm theta=0 (topologically trivial), justifying the tiny 0.0012 ps/m Chern-Simons term?**
   - *Why:* Our Wilson-Dirac model assumes Cr2O3 is a trivial insulator to get theta=0; verifying this from the real band structure closes the loop between the toy CS calculation and the material.
   - *Next:* Compute inversion parities at the 8 TRIM from the QE Bloch states (Cr2O3 has inversion+TRS center) and evaluate the Chern-Simons theta via the Wannier-based EMV formula.
3. **Why does the calculated longitudinal alpha_parallel (0.002 ps/m) fall two orders of magnitude below the measured 0.2-0.3 ps/m?**
   - *Why:* This is the paper's own acknowledged failure; understanding it tests whether thermal spin fluctuations or beyond-DFT correlation drive the low-T longitudinal response.
   - *Next:* Add finite-temperature spin-fluctuation corrections (e.g. via magnetic susceptibility from spin-dynamics or DMFT) and recompute alpha_parallel.
4. **How sensitive is the orbital ME decomposition (LC vs IC vs CS) to the exchange-correlation functional (LSDA vs GGA)?**
   - *Why:* The paper notes the CS term changed by ~an order of magnitude between LDA and the present work; XC choice may dominate the small orbital terms.
   - *Next:* Repeat the orbital-electronic decomposition with PBE and PBEsol and compare LC/IC/CS subtotals against Table III.
5. **Can the itinerant-circulation orbital ME contribution be reproduced quantitatively (not just qualitatively) from a Wannier-interpolated Cr2O3 model?**
   - *Why:* We showed the IC operator is active (finite Lz) but did not reproduce the -0.0084 ps/m magnitude; a Wannier model would bridge toy operator to material value.
   - *Next:* Build Wannier90 tight-binding Hamiltonian of Cr2O3 with SOC, apply the modern orbital-magnetization + finite-E-field formalism to extract IC and LC contributions.

#### `orbital-oh2026` — PARTIAL (C4/A9)

1. **Does the FULL FPLO DFT + MLWF band structure of (TaSe4)2I reproduce the p-wave Lx texture with the SAME sign convention tied to a fixed structural enantiomer, and does the -0.25 eV constant-energy contour place the OAM nodes at the measured kx = +/-0.2 A^-1?**
   - *Why:* Our model reproduces the SYMMETRY-dictated texture but not the material-specific band energies or node positions. Only a real DFT run pins the texture to the actual (TaSe4)2I bands and validates the quantitative CD-ARPES node locations, closing the gap between 'symmetry-allowed' and 'realized in this material'.
   - *Next:* Run FPLO GGA-PBE (12^3 mesh) on the Materials Project relaxed (TaSe4)2I structure for both enantiomers, Wannierize onto Ta-5d/6s/Se-4p/I-5p, and evaluate <L_x> on the -0.25 eV contour; compare node kx to 0.2 A^-1. Route to the crux compute host (recipe compute_target).
2. **Is the p-wave OAM texture quantitatively captured by the Ta-dx2-ONLY toy Wannier model (the paper's Wannier90 minimal model), where dx2 carries no local OAM and all Lx must come from Se-p tails, or does it require the explicit multi-orbital {py,pz} basis we used?**
   - *Why:* The paper makes a subtle claim: the dx2 Wannier function is OAM-inert but 'inherits substantial p-like contributions from Se' so its TAILS carry the OAM. Whether a single-Wannier model reproduces finite Lx (via off-site/gauge OAM) versus needing an explicit p-doublet is a real conceptual question about where lattice OAM lives (atomic-center vs modern-theory-of-orbital-magnetization).
   - *Next:* Build both: (a) our explicit {px,py,pz} model (done), and (b) a single dx2 Wannier model with Se-p hybridization folded in, computing OAM with the modern itinerant operator L=(1/2)(r x v) as in the gobel2024 kernel; check whether (b) also yields the p-wave texture.
3. **How does the OAM/SAM ratio evolve as SOC strength xi is swept from the weak (TaSe4)2I regime into a strong-SOC regime, and is there a crossover where SAM texture becomes non-negligible (the paper's proposed route to p-wave SAM texture)?**
   - *Why:* The paper proposes that structural chirality + STRONG SOC would convert the p-wave OAM texture into a p-wave SAM texture (the CISS/CIOS connection, analogy to NiI2). Our model has this knob (xi) but we only checked the weak-SOC limit. Mapping the OAM->SAM conversion vs xi would directly test the paper's central mechanistic proposal for engineering p-wave SAM textures.
   - *Next:* Sweep xi in [0, 1] in the 6-band spinful model; track net SAM polarization, band splitting, and whether Sx develops the same odd-parity kx structure; identify the xi at which p-wave SAM emerges.
4. **Can the CD-ARPES intensity (not just the intrinsic Lx) be forward-modeled from the tight-binding wavefunctions including photoemission matrix elements, and does the resulting I_RCP - I_LCP reproduce the observed odd-parity map AND the extrinsic-vs-intrinsic separation (no sign flip across ky, photon-energy dependence)?**
   - *Why:* The experiment measures CD intensity, not Lx directly; the inference Lx <- CD relies on I_CD ~ L.q_photon. Forward-modeling the matrix elements (final-state, interference) would test whether the intrinsic-vs-extrinsic CD argument (the paper's key control experiment) holds, and whether photon-energy sign reversals are reproduced.
   - *Next:* Add a one-step photoemission model (plane-wave or free-electron final state) on top of the TB eigenstates, compute I_RCP/I_LCP at 75 eV, and reproduce Fig. 2(d,e) CD maps including the ky-symmetry test.
5. **Does extending the chiral model to higher angular harmonics (adding sin(2kx)*L or d-wave form factors) predict experimentally accessible d-, f-, g-wave OAM textures, and what lattice/orbital ingredients select the harmonic order?**
   - *Why:* The paper's outlook explicitly targets multipolar OAM textures beyond p-wave (d, f, g, i). Understanding which model terms promote higher harmonics turns the qualitative outlook into a concrete design rule for the next generation of orbitronics materials.
   - *Next:* Add controlled higher-harmonic chiral couplings to H(k), decompose the resulting OAM texture on constant-|k| loops, and map which orbital multiplets + hopping ranges yield m=2,3,4 dominant harmonics.

#### `orbital-urazhdin2024` — REPLICATED (C6/A9)

1. **Does the qualitatively-invoked inter-atomic Berry curvature Omega_xy = 2 Im(<d_Qy psi | d_Qx psi>) actually integrate to a moment consistent with Eq.(18), when computed non-perturbatively over the 2D ionic-displacement manifold Q=(Qx,Qy)?**
2. **Beyond first-order TDPT, does a full time-dependent (non-perturbative) propagation of the 6-state MO wavefunction under Q(t)=Q0(cos wt, c sin wt) reproduce the same transient moment and the Eq.(9) ~6e-5 residual population, and how does it behave as hbar*omega -> Delta (resonance)?**
3. **What is the induced orbital moment when the minimal single-Ti-plaquette MO model is embedded in a periodic k-space band structure of cubic STO (full Ti t2g + O 2p manifold), and does the k-integrated orbital magnetization recover the real-space MO estimate?**
4. **The paper's absolute moment is smaller than the observed MOKE signal and it conjectures additional constructive contributions (plaquette currents through Ti vortices; dxy, px, py orbitals and their bonds). How large are these omitted channels, and do they actually add constructively by the angular-momentum-conservation argument?**
5. **How sensitive are the atomic (Eq.8) and inter-atomic (Eq.18) moments to first-principles-corrected values of a_t, a_l (i.e. replacing the semi-empirical r^{-7/2} Koster-Slater scaling with DFT-derived Ti-O hopping derivatives), and does the ~1.6x atomic:inter-atomic ratio survive?**

#### `orbital-wang2026` — PARTIAL (C6/A6)

1. **What sets the absolute scale of chi_zzyy^(O) = -1.3 (h/e) Ohm^-1 V^-1 beyond the tau*D structure?**
   - *Why:* Our surrogate reproduces the ratio and scaling but only order-of-magnitude in model units; the physical magnitude drives whether the orbital torque is device-relevant (sigma_OH ~ 198 h/e Ohm^-1 cm^-1 estimate).
   - *Next:* Compute D_zzyy from a Wannier-interpolated CuMnAs Hamiltonian with the paper's tau=1.4 ps and 50 K smearing; compare number directly.
2. **How sensitive is the orbital/spin ratio to the definition of the orbital-current operator (itinerant Eq.(3) vs modern orbital-magnetization operator)?**
   - *Why:* Our ratio (~6e3) overshoots the paper's ~150; operator choice and boundary/gauge conventions can shift orbital magnitudes by orders of magnitude.
   - *Next:* Implement both operators on the same model and report the ratio spread; identify which the paper used and match conventions.
3. **Is the non-perturbative 1/gap enhancement quantitatively 1/Delta or a milder power near the nodal line?**
   - *Why:* The paper's central mechanistic claim is that weak SOC (gaps <20 meV) amplifies OBD; the exact scaling law determines how the effect behaves across weak-SOC material families.
   - *Next:* Scan lambda finely near zero on a converged mesh and fit |D^(O)| vs the measured local gap Delta to extract the exponent.
4. **Does the coarse 18^3 grid adequately capture the sharply-peaked Fermi-surface OBD, or is the ratio grid-limited?**
   - *Why:* OBD is a Fermi-surface (df/dk) quantity concentrated on the gapped nodal line; under-sampling can both under- and over-estimate D and inflate ratios.
   - *Next:* Repeat at 24^3, 32^3 and with adaptive refinement; report convergence of D^(O), D^(S) and their ratio.
5. **Does the real CuMnAs magnetic point group m'm'm' enforce exactly the tensor elements (chi_zzyy allowed, others forbidden) that our simplified 4-band model assumes?**
   - *Why:* The paper's symmetry table (Table I / S1) is what guarantees the CPOC selection rules; our surrogate imposes them by construction rather than deriving them from the real crystal symmetry.
   - *Next:* Apply the m'm'm' generators to the DFT Hamiltonian and verify the computed chi tensor has zeros exactly where symmetry requires.

---

### Spin — 11 papers, 56 questions

#### `spin-chakraborty2023` — PARTIAL (C5/A7)

1. **Does the FF superconducting gap survive up to t_am = 0.56 (the paper's upper window edge) on a finer k-grid?**
   - *Why:* Our coarse 24x24 run collapses the gap to zero by t_am=0.50, giving an FF window of only [0.44, ~0.48) instead of the reported [0.44, 0.56]. Confirming the upper edge is needed to move Agreement from 7/10 toward full replication.
   - *Next:* Run the existing script's 'coarse' (N=96) or 'medium' (N=160) mode, which already resolves FF up to 0.55 in prior logs, and cross-check against a converged N=1000 run offline.
2. **Is the finite pair momentum Q* = 0.24 the true energetic minimum, or is it pinned by the 11-point Q-grid spacing (0.06)?**
   - *Why:* The FF diagnostic hinges on argmin_Q e(Q) > 0; a grid-pinned Q* could either fake or hide the FF state. Q* magnitude also encodes the altermagnetic band geometry.
   - *Next:* Add a local parabolic refinement of e(Q) around the discrete minimum, or densify the Q-grid to 21+ points near the winning Q, and verify Q* stability.
3. **Why does the extended-s-wave channel show a spurious FF response at t_am=0.40-0.44 while d-wave does not?**
   - *Why:* The paper argues node-matched d-wave is the favorable FF channel; an s-wave FF artifact suggests coarse-grid noise in the near-degenerate e(Q) landscape rather than real physics.
   - *Next:* Repeat the s-wave scan at higher N and lower Fermi smearing T; confirm the s-wave FF signal disappears or is energetically subdominant to d-wave.
4. **How sensitive is the BCS->FF onset t_am to the density rho and interaction strength V?**
   - *Why:* The paper fixes rho=0.6, V=2; the FF window edges depend on Fermi-surface geometry and pairing scale. Robustness across (rho, V) tests whether the mechanism is generic or fine-tuned.
   - *Next:* Scan rho in {0.5,0.6,0.7} and V in {1.5,2,2.5} at fixed coarse grid; map how the onset t_am shifts.
5. **Does including self-consistent coupling between Delta_d and Delta_s (rather than fixing Delta_s=0) change the FF onset?**
   - *Why:* We minimized over Delta_d with Delta_s~0 for speed. If the two channels mix near the transition, the true ground-state energy and FF window could shift.
   - *Next:* Perform a 2D minimization over (Delta_d, Delta_s) at a few representative t_am values and compare the FF onset to the Delta_s=0 result.

#### `spin-chen2026` — PARTIAL (C6/A8)

1. **What is the absolute anomalous Hall conductivity sigma_xy (paper: ~+/-400 S/cm, Fig 3b), and does its magnitude and +/- oscillation reproduce quantitatively?**
   - *Next:* Run rt-TDDFT (or at least a Wannier-interpolated DFT+SOC band structure) on the crux compute host for the distorted 2x2x2 KNiF3 supercell at 410 fs, then evaluate sigma_xy with the gobel2024 Kubo-Bastin kernel on the real Bloch Hamiltonian.
2. **Does the real fs time trajectory eta_alpha(t) (Fig 4d-f) reproduce the observed sequence: eta_z~1 (a0b0c-, g-wave) at ~400 fs, then eta_y~1 (a0b-c-, d-wave) at ~900 fs?**
   - *Next:* Perform rt-TDDFT with Ehrenfest/nuclear dynamics on crux (laser 4.96 eV, [111] polarization, L||[100]); extract theta_alpha^{u,l}(t), form eta_alpha(t), and correlate with the d/g-wave decomposition of Delta(k,t).
3. **Is the out-of-phase (eta=1) distortion genuinely lower in energy on the EXCITED-state PES than the in-phase (eta=0) mode, as the paper asserts (SM Section IV)?**
   - *Next:* Compute constrained-occupation DFT total energies vs octahedral rotation angle for in-phase and out-of-phase modes on the excited PES (crux), verify the out-of-phase minimum is deeper.
4. **Does the group-theory selection rule (only transverse E_g allowed; light-induced altermagnetism requires laser polarization NOT parallel to L) hold across the proposed family SrMnO3, PbCrO3, RbMnF3, KCoF3?**
   - *Next:* For each material: compute the zone-folded phonon irreps under its magnetic little co-group, decompose Sym2(Gamma_laser), and confirm the out-of-phase rotation lands in the allowed E_g channel; then rt-TDDFT spot-check one.
5. **What is the lifetime/persistence of the nonequilibrium altermagnetic state, and does the spin splitting truly persist for the full ~1 ps photoexcited-carrier lifetime?**
   - *Next:* Extend the rt-TDDFT run to 1 ps with dephasing/relaxation, track the photoexcited population and Delta(k,t) amplitude decay, and estimate the tr-MOKE / THz-emission signal window.

#### `spin-fernandes2026` — PARTIAL (C5/A8)

1. **Does the intrinsically-3D hexagonal g-wave altermagnet (D_6h, CrSb/MnTe/Co1/4NbSe2) reproduce the eta^H_xxxz = -eta^H_yyxz = -eta^H_xyyz tensor structure and the Lifshitz-transition-driven jumps in eta^H(mu) (Fig. 4d/4e)?**
2. **Can the analytic Dirac-theory prefactor C_0 = 8 hbar^2 g^{B2g} g_3^{A1g} / (v_uc t_1 t_d) and the single-Dirac-point mapping eta^H = C_0 sigma_xy^H (Eq. 12) be independently derived and shown to quantitatively track the full tight-binding eta^H(mu) as in Fig. 3b?**
3. **What is the definitive resolution of the shear-coupling factor-of-2 convention (gamma^xy = gamma^{B2g} vs 2*gamma^{B2g}), which changes eta^H by 4x (8.4 vs 16.8 hbar/v_uc)?**
4. **Does the full-frequency (non-quasi-adiabatic) Hall viscosity derived in the SM (Ref. [55]) reduce to the Eq. (6) adiabatic form at low frequency, and how large are the finite-frequency corrections in the magneto-acoustic regime relevant to experiment?**
5. **Is the predicted eta^H ~ 8 uPa*s quantitatively comparable to the alpha-RuCl3 acoustic-Faraday value [Ref. 49] under realistic material parameters, and what SOC strength / gap size is required for a given real altermagnet candidate (R2Mn2Se2O3, AV2Te2O, Fe2X2O)?**

#### `spin-gurung2023` — PARTIAL (C4/A9)

1. **Does the full DFT Fermi surface of antiperovskite Mn3GaN reproduce the nearly-100% p_k|| over a broad 2DBZ area, as opposed to the illustrative 2D kagome surrogate?**
   - *Why:* The headline material claim rests on the real Mn3GaN (001) band structure with 5 Fermi-surface bands; the kagome model only demonstrates the mechanism, not the material-specific breadth.
   - *Next:* Run a noncollinear DFT (e.g. VASP/QE + Wannier90) for Gamma_5g Mn3GaN, downfold to a tight-binding Hamiltonian, and recompute p_k|| on the (001) 2DBZ.
2. **How does the 'broad area' fraction of p>=90% scale with exchange splitting Delta/t and with the chirality/orientation of the 120-degree Neel vector?**
   - *Why:* The paper notes polarization is reduced only at small Delta; quantifying the Delta-dependence tests robustness and the symmetry origin of the effect.
   - *Next:* Sweep Delta/t in [0.3, 3.0] and both chiralities on the kagome model; map frac(p>=0.90) vs Delta and compare to Supplementary Fig. S1.
3. **Does adding spin-orbit coupling (SOC) preserve or degrade the near-100% spin polarization?**
   - *Why:* Real Mn3GaN has finite SOC; the effect is defined without SOC, and SOC can mix spin channels and cap p_k||.
   - *Next:* Add an on-site/bond SOC term to the kagome Hamiltonian and recompute p_k|| vs SOC strength.
4. **Does matching the near-100% conduction channels to SrTiO3 low-decay evanescent states actually yield ETMR ~10^4%?**
   - *Why:* ETMR is the device-level payoff of the spin-polarization claim; spin polarization alone does not prove the transport magnitude.
   - *Next:* Build a ballistic (NEGF or transfer-matrix) AFMTJ model with a SrTiO3-like barrier, compute k||-resolved T_P and T_AP, and evaluate ETMR=(T_P-T_AP)/T_AP.
5. **Is the 'persistent spin texture' region (spins aligned over a broad 2DBZ patch) reproducible in the surrogate, and is it symmetry-enforced or interaction-specific?**
   - *Why:* The paper explicitly flags this as not symmetry-enforced; distinguishing the two matters for generalizing to other Mn3XN antiperovskites.
   - *Next:* Map the spin-direction field s_k|| across the 2DBZ in the kagome model and test for extended constant-direction patches vs symmetry predictions.

#### `spin-jaubert2016` — PARTIAL (C5/A8)

1. **Does the divergence-free residual fragment actually reproduce quantitative pinch points (sharp singular structure at Brillouin-zone centers) rather than merely finite diffuse scattering?**
   - *Why:* The paper's Fig. 10 shows genuine pinch points persisting to the ordering transition; our L=3 lattice is too small to resolve the pinch-point singularity, so we only demonstrated Bragg+diffuse coexistence, not the singular pinch shape.
   - *Next:* Rerun on L=6-8 with dense q-sampling around (0,0,2) and (1,1,1), fit the transverse S(q) to the dipolar Coulomb-phase form 1 - q_perp^2/q^2 to confirm the pinch singularity.
2. **What is the correct bracketed coefficient of Eq. (12) that yields dE_hh = -4.73 D, and can we derive it from first principles instead of trusting garbled OCR?**
   - *Why:* dE_hh is one of the two dumbbell energy-cost predictions; our Madelung construction reproduces dE_mm=19.75 exactly but gives -3.13 for dE_hh, indicating an OCR/sign/factor ambiguity in Eq. (12) we could not resolve from text alone.
   - *Next:* Re-derive dE_hh = -2p_h + V_nn - 2 V_M analytically with V_nn=-(8/3)sqrt(2/3)D and V_M=-(8/3)sqrt(2/3) D * Mzb, checking the Helmholtz half-divergence factor; cross-check against the MC value -4.34 D.
3. **Do dipolar interactions actually order the FCSL into the R-states (quantum-dimer ground state) at very low T, maximizing flippable plaquettes?**
   - *Why:* Section VI's conclusion — the dipolar degeneracy lift selecting R-states — is the paper's low-energy punchline and we did not attempt it (we imposed the FCSL constraint rather than deriving its stability/selection).
   - *Next:* Add the real long-range dipolar energy (Ewald) as a weak perturbation on the FCSL ensemble and measure whether the lowest-energy configs correspond to maximal flippable-plaquette (R-state) order.
4. **Is the monopole-hole / monopole (2-in-2-out vs 4-in/4-out) distinction and their non-confining Coulomb interaction reproducible via direct defect-pair energetics in MC?**
   - *Why:* The semiconductor analogy (valence=order, conduction=Coulomb liquid) rests on the two defect species interacting via a non-confining 1/r potential; we validated the analytic prefactor but not the numerically extracted V(r) curves of Fig. 5.
   - *Next:* Insert defect pairs at controlled separations into FCSL backgrounds, compute averaged dipolar energy vs r with Ewald summation, and fit to V/D = -2.177 (r_d/r) to reproduce Fig. 5.
5. **How robust is the FCSL to thermal/quantum excitation density, i.e. where is the T/D window in which fragmentation (rho~1/2) survives?**
   - *Why:* The paper reports pinch points persisting to T/D~2 and up to the transition; we only sampled ground-state (E=0) FCSL configs, so we have no thermodynamic phase boundary.
   - *Next:* Run finite-T Metropolis with the four-body H = J_sq sum_nu (sum S.S)^2 plus dipolar term, sweep T/D and track rho, defect density, and pinch-point intensity to map the FCSL stability window.

#### `spin-jungwirth2024` — PARTIAL (C3/A9)

1. **Does the g-wave altermagnet realized in the actual materials MnTe and CrSb reproduce the same M=0 + protected-sign-structure claim in a minimal tight-binding model, or does the higher-order (g-wave) form factor introduce qualitatively new nodal geometry?**
   - *Why:* The paper's headline experimental candidates are g-wave, not d-wave. Our replication covers only the d-wave prototype; the central claim is asserted for d/g/i-wave collectively but only demonstrated here for d.
   - *Next:* Extend the 2-sublattice model to a 4-sublattice (or hexagonal) lattice whose C6/C3 symmetry forces a g-wave (cos2k-type) form factor; verify diagonal/axial node count matches the g-wave harmonic.
2. **How large is the non-relativistic altermagnetic spin splitting predicted for real materials by ab-initio DFT, and does the toy-model magnitude (0.56 t_nn) map onto the ~eV-scale splittings reported for MnTe/CrSb?**
   - *Why:* The Perspective cites DFT-predicted splittings; a toy model gives only a dimensionless number. Connecting to a material scale is what makes the claim experimentally falsifiable.
   - *Next:* Run a spin-polarized DFT (VASP/QE) calculation of MnTe or CrSb, extract the momentum-resolved spin splitting along a symmetry line, and compare its k-dependence to the model form factor.
3. **What is the precise symmetry (spin-group) operation that protects the sign structure, and can it be verified as an explicit anti-commutation/commutation relation on the Bloch Hamiltonian rather than only as a numerical antisymmetry residual?**
   - *Why:* The paper's whole framing is spin-group symmetry classification. A machine-checkable spin-group operator would upgrade our numerical C4-antisymmetry residual to a first-principles symmetry proof.
   - *Next:* Construct the spin-group element [C2||C4] (spin C2 combined with real-space C4) as an explicit unitary and assert U H(k) U^dagger = H(C4 k) over the BZ.
4. **How does the altermagnet's momentum-space spin texture relate quantitatively to the superfluid-3He / higher-partial-wave Pomeranchuk order-parameter texture that the Perspective uses as its central analogy?**
   - *Why:* The intellectual contribution of the paper is the analogy/distinction to Fermi-liquid Pomeranchuk instabilities and 3He; our replication captures the crystal altermagnet but not this analogy, which is where the paper's novelty lies.
   - *Next:* Build a continuum Fermi-liquid l=2 spin-channel Pomeranchuk order parameter and compare its M=0 + d-wave spin texture to the lattice altermagnet, identifying which features are lattice-specific.
5. **Under an applied SOC term, does the conserved-S_z picture break down in the way the paper's relativistic-spin-splitting section describes, and does a small net magnetization or anomalous Hall response then appear?**
   - *Why:* The paper distinguishes non-relativistic (S_z-conserving) and relativistic altermagnetic effects; our model is strictly non-relativistic, so the SOC-induced phenomena (weak ferromagnetism, AHE) are untested.
   - *Next:* Add a Rashba/atomic SOC term to the model, recompute the net moment and a Kubo anomalous Hall conductivity, and check whether a symmetry-allowed finite response emerges.

#### `spin-lee2025` — REPLICATED (C7/A10)

1. **The paper states a single-unit-cell (110) film of RuO2 loses altermagnet symmetry yet the microscopic picture still predicts spin-split bands. Does the minimal 4-band model reproduce this residual splitting when translational symmetry between A/B is explicitly broken?**
   - *Why:* Resolves whether spin splitting is fundamentally a local (bond-anisotropy) effect vs a global crystal-symmetry effect - decisive for 2D altermagnet spintronics.
   - *Next:* Add an on-site A/B energy offset (delta_AB * tau_z) breaking PT, re-diagonalize, and check whether momentum-dependent splitting survives with delta_t=0.
2. **How does the d-wave nodal spin structure evolve into Weyl/nodal-loop topology when a small SOC (lambda * L.S) term is added to the minimal model?**
   - *Why:* The intro links altermagnet nodes to Weyl physics and anomalous Hall readout; the SOC-free model cannot show this directly.
   - *Next:* Add Rashba/atomic SOC to the 4-band H, compute Berry curvature via the Kubo-Bastin routine from the gobel2024 kernel, and locate gapped nodes / Chern contributions.
3. **The claimed eV-scale spin splitting assumes h_eff ~ few eV for transition-metal d orbitals. What delta_t magnitude does the actual MnF2 non-magnetic-cage distortion produce?**
   - *Why:* Sets whether the minimal model is quantitatively (not just qualitatively) predictive for real MnF2.
   - *Next:* Fit delta_t and t1,t2,t3 to the DFT-GGA MnF2 bands in Fig 5(a) via Wannier downfolding; compare fitted splitting to measured/DFT values.
4. **Does the anomalous Hall coefficient predicted from the accidental + symmetry nodal degeneracies remain finite in the SOC-free limit, or does it require SOC?**
   - *Why:* AHE is the stated electrical readout mechanism for altermagnetic order; its origin (crystal vs relativistic) is physically important.
   - *Next:* Compute intrinsic sigma_xy via Kubo-Bastin over occupied bands as a function of mu with and without an SOC term.
5. **How robust is the 'both delta_t and h_eff required' result to longer-range or multi-orbital hopping (the paper notes multi-orbital band structure is recoverable by extending the Hilbert space)?**
   - *Why:* Determines whether the two-ingredient rule is a strict theorem of the minimal model or an artifact of the single-orbital truncation.
   - *Next:* Extend to a 2-orbital (X2-Y2 and Z2) 8-band model with orbital-dependent delta_t and re-test the necessity condition.

#### `spin-li2019` — PARTIAL (C7/A6)

1. **Why does the ordinary Berry curvature fail to integrate to the paper's clean Chern numbers (-3, 1, 2) in our from-scratch build?**
   - *Why:* The Chern numbers are the topological fingerprint of the magnon bands and underlie the intrinsic (dissipationless) nature of the spin Nernst response. A wrong Chern count signals either a subtle sign/convention error in the BdG blocks or an ill-conditioned Berry curvature near the AFM Goldstone mode.
   - *Next:* Compute Chern numbers with the gauge-invariant Fukui-Hatsuda-Suzuki plaquette method (link variables) on a dense grid, which is robust to the near-degeneracy, instead of the m-sum curvature formula.
2. **Is the strong grid sensitivity of the alpha^y_yx peak (2.7 at nk=24 vs ~0.4 at nk=36) purely a Goldstone-mode artifact, or a genuine convergence issue in the spin Berry curvature?**
   - *Why:* The paper's headline number is alpha^y_yx/kB ~ 3.5; if our value is not converged we cannot claim quantitative agreement, only sign/order-of-magnitude.
   - *Next:* Introduce a small physical anisotropy gap (or finite magnon mass) as in the paper's material, and perform an adaptive/tetrahedron BZ integration that resolves the hot spots at the avoided crossings without oversampling Gamma.
3. **Does our reconstructed in-plane DMI orientation (radial n_hat plus chirality-staggered Dz) exactly match the paper's Fig. 1 DMI pattern and the Mx mirror plane?**
   - *Why:* The spin Nernst tensor shape (Eq. 18) and the vanishing of the torque/source term follow from the DMI-imposed magnetic space group. A mis-oriented DMI would still give a finite response but with the wrong tensor symmetry.
   - *Next:* Explicitly verify the numerically obtained alpha tensor against the symmetry-allowed form of Eq. (18) (antisymmetric x/y blocks, specific z block) component by component.
4. **How large is the orbital-magnetization / bound-current (M) term that the paper cancels analytically, and is our c1-weighted formula fully equivalent to their Eq. 8 + Eq. 14 combination?**
   - *Why:* The paper's key step is that the nonequilibrium (S) and equilibrium orbital-magnetization (M) parts combine into the compact c1 formula (Eq. 15). If our direct c1 implementation silently drops a piece, the magnitude would be off by a T-dependent factor.
   - *Next:* Independently evaluate the S-term (Eq. 8, with g and energy weighting) and the M-term (Eq. 14, energy integral of g) and confirm their sum reproduces the c1-weighted result numerically.
5. **Does the predicted response survive with J2 = 0 (the alternative fit mentioned in the paper where the flat band is broadened by fluctuations)?**
   - *Why:* The paper notes the dispersion can also be fit with J2 = 0. If the spin Nernst effect is qualitatively unchanged, it strengthens the material prediction; if it collapses, the effect is J2-sensitive and less robust experimentally.
   - *Next:* Re-run the kernel with J2 = 0 and compare the alpha^y_yx(T) curve and band structure to the J2 = 0.11 meV case.

#### `spin-lund2021` — PARTIAL (C5/A9)

1. **Does the k=0 uniform-precession picture survive at finite k, i.e. do the three magnon bands retain distinct, well-separated polarization character across the Brillouin zone?**
   - *Why:* The orthogonal-polarization spin-pumping claim is derived only at k=0. A real driven film excites a finite-k envelope; band mixing away from Gamma could contaminate the pumped-current polarization.
   - *Next:* Extend the LSWT kernel to compute the full k-resolved eigenvectors and project them onto x/y/z; quantify polarization purity vs |k|.
2. **How does the Heisenberg zero-energy flat band (reproduced here) shift once the paper's Kz, K anisotropies and DMI are switched on?**
   - *Why:* The flat band is the hallmark of kagome AFM frustration; anisotropy gaps it and sets the low-frequency pumping response. Its fate controls the density of pumping-active modes.
   - *Next:* Add on-site anisotropy and (if present) DMI terms to the BdG matrix and track the lowest band gap vs Kz/J and K/J on a coarse grid.
3. **What is the quantitative magnitude of the pumped ac spin current (Eq. 17) for a realistic kagome jarosite (e.g. KFe3(OH)6(SO4)2) and drive field?**
   - *Why:* The paper gives functional forms but no absolute numbers; experimental feasibility (ISHE voltage) depends on plugging in real J, K, lambda, spin Hall angle.
   - *Next:* Parameterize a1,a2,K1,K2 from measured J and anisotropy, evaluate g1,g2 at resonance, and estimate the ISHE electric field from Eq. 18.
4. **Is the exact xy-degeneracy / z-splitting of the three resonance modes robust to symmetry-lowering perturbations (strain, interfacial DMI, off-diagonal K)?**
   - *Why:* Mutual orthogonality of polarizations relies on K being diagonal. Off-diagonal anisotropy would rotate/mix the polarization axes and blur the frequency-selective control.
   - *Next:* Introduce off-diagonal K elements and recompute the eigenvectors; measure orthogonality error vs perturbation strength.
5. **How does thermal magnon population (finite T) and Gilbert-like damping alpha_tilde broaden the three resonances and reduce polarization selectivity?**
   - *Why:* Room-temperature operation is the practical target; overlapping damped resonances would prevent clean single-band excitation and mixed polarizations.
   - *Next:* Include the damping term (Delta_omega = 2 a2 alpha_tilde / a1^2) in a Lorentzian lineshape model and compute resonance overlap vs alpha_tilde and T.

#### `spin-mestral2025` — PARTIAL (C5/A7)

1. **Why does the soft-mode frequency omega(disp) collapse far more steeply (2.0->1.0 THz over 0.466%->0.425%) than a simple quartic Landau double-well predicts?**
   - *Why:* r51 ~ 1/omega^2, so the exact omega(off-centering) law controls how sharply r51 can be enhanced and how sensitive it is to structure. Our Landau model missed omega by ~33%.
   - *Next:* Build a real frozen-phonon curvature calculation of the Ti <110> soft mode vs displacement (finite-difference Hessian on a tight-binding or shell-model BTO), or fit a higher-order (6th) Landau expansion to the three paper points.
2. **Why does PBEsol underestimate the ground-state r51 by 46% (391 vs 730 pm/V) while its soft-mode frequency (1.80 THz) is closer to experiment (1.14 THz) than PBEsol+U+V (3.16 THz)?**
   - *Why:* It signals the r51 error is not purely a soft-mode-frequency error but also involves Raman susceptibility / mode-polarity (eigenvector) accuracy.
   - *Next:* Decompose r51 into alpha_m, p_m, and 1/omega^2 factors per mode for PBEsol and check which factor carries the residual error against experiment.
3. **Does the extended Hubbard (U+V) correction genuinely improve the electronic structure while degrading r51 only through the phonon eigenvectors, as the paper claims?**
   - *Why:* Distinguishes an electronic-structure improvement from a vibrational artifact; central to whether functional-independence actually helps EO prediction.
   - *Next:* Reproduce the r_el vs r_ion split (paper Fig. 5) and compare eigenvector 'Slater character' overlaps between PBEsol and PBEsol+U+V.
4. **How does mode 14 produce a positive contribution to nu_max that flips the sign of r13, violating the symmetry expectation that r13, r33, r51 share sign?**
   - *Why:* The anomalous r13 sign suggests a missing physical contribution and undermines confidence in the smallest coefficient.
   - *Next:* Isolate mode 14's alpha/p contribution across the displacement series and test whether including strain/piezo-optic terms restores the correct r13 sign.
5. **Is the r51 enhancement at reduced off-centering a real thin-film-clamping effect or an artifact of choosing a structure off the P4bm ground state?**
   - *Why:* Determines whether 0.45% (near-experimental r51) is physically realizable in clamped BTO films or just a convenient tuning knob.
   - *Next:* Compare against XRD-measured Ti displacements in clamped BTO thin films and compute the clamped ground-state under epitaxial strain boundary conditions.

#### `spin-wernert2024` — PARTIAL (C6/A9)

1. **Can the full linearized-LLG FM/noncollinear-AFM bilayer strip (100x1 kagome, JFM=-1, JAFM=1, compensated interface via Jnnn=JFM) be rebuilt to reproduce the numerical d.c. Hall spin current magnitudes in Fig.2, not just the sign structure?**
   - *Why:* Our replication confirmed the analytic headline exactly and the Fig.2 sign flip, but did not reproduce the absolute magnitudes/profiles that require the interface boundary condition, anisotropies (K=0.01, Kz=0.00125), and boundary damping sinks (alpha=100). Matching magnitudes would upgrade coverage from 8 to ~10.
   - *Next:* Implement the Gaussian-driven a.c. field (Eq.15, sigma=2, omega=1), linearized LLG on the strip with edge damping, and the End-Matter Sec.IV lattice spin-current formulas; compare Jyy(direct) vs Jyy(inverse) profiles to Fig.2 (a)/(b).
2. **Does the exact velocity assignment of Eq.(13) [c_I=sqrt(g0/rho), c_{II,III}=sqrt((g0+gH)/rho)] emerge when the n_alpha x (spin-rotation) projection of the LLG EOM (Eq.4) is retained, rather than the naive elastic dynamical matrix we used?**
   - *Why:* Our T5 verified the splitting magnitude (2 gH/rho) exactly but not the specific branch labeling of Eq.(13); resolving the projection would make T5 a strict rather than qualitative match.
   - *Next:* Linearize Eq.(4) around the isotropic polycrystal ground state with Gamma-bar, keep the cross-product (Berry/gauge) term, and diagonalize the resulting non-symmetric dynamical matrix to recover the exact c_I, c_II, c_III.
3. **How large is gH relative to g0 for real cubic and hexagonal Mn3X computed from Eq.(11) with realistic (beyond nearest-neighbor) exchange couplings from inelastic neutron data?**
   - *Why:* The paper states off-diagonal Gamma components are 'of the same order' as diagonal ones for Mn3X, implying an experimentally observable Hall spin current. Quantifying gH/g0 for specific materials sets detection feasibility.
   - *Next:* Feed measured Heisenberg parameters for Mn3Sn/Mn3Ge/Mn3Ir into Eq.(11), angular-average per Eq.(12) to extract gH, g0, and tabulate gH/g0 and the predicted magnon velocity split.
4. **Is the transverse (Hall) Noether spin current experimentally distinguishable from ordinary spin-Hall / spin-swapping backgrounds via ISHE in a low-symmetry detector, as the Discussion proposes?**
   - *Why:* The Hall mass is claimed to be a generic, symmetry-protected classifier of ALL noncollinear AFMs. Establishing a clean experimental signature (radial Jyy detectable by ISHE) is the path from theory to a measurable classifier.
   - *Next:* Model an ISHE detector stack on the noncollinear AFM, compute the converted charge voltage from the circularly-polarized-magnon-driven radial spin current, and estimate signal vs thermal/spin-pumping background.
5. **Does the itinerant-electron topological Hall response (gobel2024 s-d Kubo/Berry kernel) applied to the SAME kagome noncollinear texture give a consistent, complementary Hall signal to the magnonic Noether current derived here?**
   - *Why:* The two mechanisms (electronic Berry-curvature AHE vs magnonic Noether spin current) share the noncollinear-texture origin. Cross-checking with the sibling gobel2024 kernel would tie the electronic and magnonic Hall responses of the same texture together.
   - *Next:* Adapt gobel2024_sd_skyrmion_kubo_Lz_kernel.py to a kagome lattice with a 120-degree coplanar spin texture (direct/inverse triangular), compute sigma_xy^spin/orbital, and compare its sign/symmetry to the Noether Jyy sign flip found in T4.
6. ****

---

### Polar — 13 papers, 66 questions

#### `polar-berloff2008` — PARTIAL (C6/A8)

1. **Does the macroscopic vortex split require 3D vortex RINGS, or can a 2D straight vortex split macroscopically under the right forcing?**
2. **What is the linear growth rate of the s=2 -> 2x(s=1) instability, and how does it depend on xi relative to xi_crit?**
3. **Can we reproduce the paper's core-energy parameter l(t) (Eq 42) and the vortex-ring energy/impulse/velocity curves quantitatively?**
4. **Under periodic pressure, how many daughter rings form as a function of (eps, eta), and does the count match the paper's elucidated conditions?**
5. **How sensitive are xi_crit and the split dynamics to the nonlinearity exponent gamma (beyond the cubic-quintic gamma=1 case)?**

#### `polar-brazovskii2003` — PARTIAL (C7/A9)

1. **Compute the quantum breather bound-state spectrum in the spectral window between the collective-mode edge omega_t and the photoconductivity gap 2*Delta. The paper states this region is 'filled by a sequence of quantum breathers, bound states of two solitons' but gives NO closed form.**
2. **Derive the quantum renormalization U -> U* microscopically and fix the prefactor C in Delta ~ C*U^{1/(2-2gamma)}. The paper treats gamma as a phenomenological Luttinger parameter and leaves C undetermined.**
3. **Predict the temperature laws omega_t(T) and omega_cr(T) (hence Z(T)) from a Landau-Ginzburg free energy for the CD order parameter, replacing the 'reasonable suggestions' the paper invokes to obtain the Curie singularity at omega=0.**
4. **Resolve the reported factor-of-~3 (triple for TMTTF) divergence in the metallic plasma frequency omega_p by reparametrizing published optical data with the correct dielectric form Eq.(2) at the scale omega_0t, which the paper states 'was never exploited'.**
5. **Model the alpha-soliton (FE domain-wall) dynamics that the paper says produce the observed frequency dispersion of epsilon below T0, including the aggregation of alpha-solitons into walls and their pinned/creep motion.**

#### `polar-hong2025` — PARTIAL (C4/A7)

1. **Why is our stabilized vortex period (~5 nm) smaller than the paper's reported ~14 nm trilayer periodicity?**
   - *Why:* The absolute period is set by the ratio of gradient stiffness to electric/elastic energy and the film thickness; matching it quantitatively is what turns a mechanism-level replication into a full quantitative one and validates the coefficient set.
   - *Next:* Sweep gradient stiffness g and film thickness (film_frac) and calibrate the g/eps ratio against a known PTO domain-wall width (~0.5-1 nm) so the Kittel-like period lands at ~14 nm; compare period-vs-thickness scaling to the paper's trilayer-vs-superlattice (14 vs 10 nm) contrast.
2. **Does adding an explicit anisotropic elastic (strain) energy reproduce the mixed vortex + a1/a2 twin-domain phase of the [PTO16/STO12]10 superlattice?**
   - *Why:* The paper's second half of the claim is that the SAME free-energy functional yields a pure vortex phase in the trilayer but a mixed phase in the superlattice; capturing the switch is the discriminating test of the model.
   - *Next:* Add a Landau-elastic coupling (a1/a2 in-plane tetragonal variants) and a superlattice stacking mask, then check whether twin domains coexist with vortices at superlattice periodicity.
3. **Is the vortex array the true global energy minimum or a long-lived metastable state?**
   - *Why:* TDGL from random noise can trap metastable textures; the paper claims an equilibrium vortex phase, so robustness to initial conditions and annealing matters.
   - *Next:* Run multiple seeds + simulated-annealing (noise ramp) and compare final free energies of vortex vs uniform vs stripe states.
4. **How does the full 3D flux-closure structure (swirling in-plane + out-of-plane rotation) compare to our 2D cross-section?**
   - *Why:* The paper emphasizes a 3D swirling polarization; a 2D (x,z) cross-section captures the winding but not the full toroidal moment / in-plane [100]-[001] orientation reported from DF-TEM.
   - *Next:* Extend to a 3D (x,y,z) grid with 3-component P and measure the toroidal moment G = <r x P> per vortex tube.
5. **Can the model reproduce the paper's dynamical headline - vortex-boundary motion via zigzag-core switching under a trailing bias field?**
   - *Why:* The paper's main experimental result is field-driven, reversible vortex-boundary motion; the phase-field vortex phase is the substrate on which that dynamics is claimed to occur.
   - *Next:* Add a localized/trailing E-field term coupling to Pz and track lateral displacement of the vortex-boundary and the zigzag-pattern switching of cores over time.

#### `polar-hong2026` — PARTIAL (C5/A7)

1. **Does the 2pi-skyrmion's wide stability window survive in a full 3D BFO/STO superlattice with realistic temperature-dependent Landau coefficients, or is the widest-window ordering an artifact of the reduced single-layer model?**
   - *Why:* The paper's central device claim (room-temperature 2pi storage after Sm doping) rests on 2pi being uniquely robust. Our minimal TDGL reproduces the ordering, but only 3D + real coefficients settle whether the margin is physical.
   - *Next:* Port the seed + Langevin machinery to a 3D multilayer grid using published BFO/STO Landau coefficients and depolarization boundary conditions; recompute stability windows.
2. **Is the thermal-hysteresis / path-dependence (at 600 K, cooling bypasses 1pi and jumps solitons->2pi) reproducible as a genuine first-order transition with an energy barrier?**
   - *Why:* Reversibility with hysteresis is the paper's evidence that these are distinct metastable topological phases, not a smooth crossover. Our survival metric does not yet resolve hysteresis.
   - *Next:* Run closed heating-cooling loops (ramp T up then down) tracking Q and ring count, and look for a hysteresis loop / discontinuous order switching.
3. **How does the stability window depend on the gradient stiffness g and easy-axis anisotropy K_z relative to the Landau well depth?**
   - *Why:* The 2pi advantage may come from a specific balance of exchange vs anisotropy; identifying it would give a design rule for which materials host wide 2pi windows.
   - *Next:* Sweep (g, K_z) on a coarse grid and map the region where 2pi remains the widest-window order.
4. **Does 2% Sm doping act, as the paper claims, primarily by lowering transition temperatures (shifting T0 / a(T)), and can a simple T0 shift in our model reproduce room-temperature 2pi stabilization?**
   - *Why:* This is the practical route to device operation; distinguishing a T0 shift from a change in barrier heights matters for materials selection.
   - *Next:* Lower T0 in the Landau term to emulate Sm doping and check whether the 2pi survival window slides down to 300 K.
5. **Is our structural-survival overlap S(T) a faithful proxy for the paper's Pontryagin-density-based identification of skyrmion order, especially near the paraelectric onset?**
   - *Why:* If S(T) and Q(T) diverge near high T, the measured window widths could be biased; the comparison to the paper needs a topological, not just structural, survival criterion.
   - *Next:* Add a Q(T)-based survival criterion (Berg-Luscher per annealed frame) and compare window widths to the S(T)-based ones.

#### `polar-huang2022` — PARTIAL (C7/A7)

1. **What is the paper's actual exchange stiffness A (only shown in Fig.4), and does using it collapse our ~40 nm diameter onto the reported ~12 nm?**
2. **Does rebuilding on the true Fe honeycomb lattice (rather than the square-lattice approximation) change the geometric DMI prefactor enough to shift D_c relative to the paper's D values?**
3. **Can we reproduce the DFT-computed FE-switchable DMI values (0.28 vs 0.06 mJ/m^2 bilayer; 0.22 vs -0.24 trilayer) from first principles, rather than taking them as inputs?**
4. **Are the trilayer skyrmions (D=0.22, |D|=0.24 mJ/m^2), which sit just below our analytic D_c=0.255, thermodynamically stable or merely metastable from the seed?**
5. **Does a full atomistic spin-dynamics run with the paper's true anisotropy caveat (DFT MAE 8.57 MJ/m^3 vs adopted 0.04 MJ/m^3) reproduce the ~0.03 nm 'no skyrmion' regime and the ~100 nm experimental regime as the paper's Eq.6 predicts?**

#### `polar-jankowski2024` — PARTIAL (C4/A7)

1. **Does a full HWCC/SHP tight-binding calculation of the super-Haldane model (N=51, VSL=10) reproduce the exact discontinuous polarization jump in units of the polarization quantum, not just its sign and non-vanishing?**
   - *Why:* Our TDGL surrogate reproduces the QUALITATIVE magnitude drop (~30%) and winding survival, but not the quantized SHP value the paper reports. A direct Wilson-loop implementation would turn a mechanism-level match into a quantitative one.
   - *Next:* Implement the super-Haldane Hamiltonian (Eq. 9) + hybrid Wannier charge centers via Wilson loops, evaluate Eq. 5 for P(r_j) and Eq. 8 for quantized DeltaC on both sides of the TPT.
2. **Is the meron winding Q genuinely +-1/2 over the triangular AA-AB-BA domain, or does the true SHP field give integer skyrmion charge over the full moire cell?**
   - *Why:* The paper claims half-integer merons per triangular domain that sum to integer topology over the cell. Our single-meron relaxation gives |Q|~1/2 but does not tile the moire triangulation.
   - *Next:* Build the full moire supercell polarization field from the twisted-Haldanium continuum model (Eq. 11) and integrate Eq. 12 per triangular domain and over the whole cell.
3. **How robust is winding preservation to thermal/Langevin noise near the TPT critical (metallic) point?**
   - *Why:* The paper notes the TPT crosses an intermediate metallic state; near criticality fluctuations could unwind the texture. We relaxed noise-free.
   - *Next:* Re-run relax_branch with kT_noise>0 sweeping through the effective critical well depth and track Q(t) for unwinding events.
4. **Does the local Chern marker C(r_j) (Fig 2d/e) spatially correlate with the polarization-magnitude drop as the paper reports?**
   - *Why:* The paper links trivialization of SHP (quantized DeltaC) to the magnitude reduction. We did not compute a spatially-resolved Chern marker.
   - *Next:* Add a real-space Chern-marker calculation C(r_j)=-4pi Im<r_j|P x_hat Q y_hat|r_j> to the super-Haldane replication and overlay on |P|(r).
5. **Does the effect generalize beyond Haldane to a generic Chern insulator with a superlattice length scale and local inversion breaking, as the paper conjectures?**
   - *Why:* Generality is a stated conclusion; confirming it in a second model (e.g. QWZ + superlattice) would strengthen the claim's materials relevance.
   - *Next:* Repeat the SHP/winding pipeline on a QWZ Chern model with an added superlattice potential and check for the same discontinuous-but-nonvanishing polar texture.

#### `polar-lohani2019` — PARTIAL (C5/A8)

1. **Does the quantum skyrmion's exponentially small bandwidth, arising from skyrmion<->antiskyrmion tunneling, reproduce in an independent ED build?**
2. **Do the angular-momentum quantum numbers l_z lock to the spin quantum number N_f as the paper claims ('locking of angular momentum and spin quantum numbers characteristic for skyrmions')?**
3. **What is the full J2-B (and J2-K) phase diagram, and where exactly is the skyrmion-stable region boundary (paper Fig. 4, J2 >~ 0.45)?**
4. **Does the winding-number correlation (paper Eq. 12, the arctan of transverse spin-spin correlations) yield the expected quantized-in-the-classical-limit winding for the bound state?**
5. **Do the finite-flake results converge to the thermodynamic-limit skyrmion as flake size grows (7 -> 19 -> 31 -> larger), i.e. is the bound state a genuine localized object rather than a finite-size artifact?**

#### `polar-morozovska2021` — PARTIAL (C4/A9)

1. **Does the full 3D cylindrical core-shell flexon geometry (two diffuse axial P3-domains near the cylinder ends separated by a P3~0 region, with an azimuthal XY vortex/meron core) emerge from the same Lifshitz-invariant coupling, or does it additionally require the depolarizing-field boundary conditions at the cylinder ends?**
2. **What is the topological index of the flexon at the cylinder ends, and is it exactly +/-1/2 (meron) as the paper claims, robust to shell permittivity and cylinder aspect ratio?**
3. **How does the FULL flexoelectric tensor F_ijkl anisotropy (not a single scalar F) reshape the domain morphology? The paper stresses that flexoelectric ANISOTROPY 'critically influences' the texture.**
4. **Can the absolute transverse polarization (in uC/cm^2) be matched to the paper, i.e. does a dimensionalized version with the real BaTiO3 material tensors and self-consistent electrostriction/electrostatics reproduce the paper's quantitative magnitudes, not just the sign/scaling?**
5. **Where exactly is the Bloch-to-Ising wall transition (as a function of K/|a| and F), and does the net chiral moment saturation we observe at |F|~1 map onto a real physical saturation of the flexon chirality, or is it an artifact of the finite anisotropy K?**

#### `polar-sinha2016` — REPLICATED (C7/A9)

1. **What is the correct microscopic value of a = 4*alpha*beta/(hbar^2 omega v), and hence the Fermi velocity v, that the paper implicitly used to obtain a=0.17/0.55 nm?**
   - *Next:* Plug measured Bi2Te3 v and lambda into the microscopic a-formula with the paper's evA0/hbar*omega and compare to the tabulated a; quantify the residual and whether an O(1) convention factor (e.g. factor of 2 in alpha,beta) closes it.
2. **Do the full 2D spin-texture colormaps (Figs. 1, 2, 4) reproduce quantitatively, including the C3v streamline topology and the snowflake Fermi-surface evolution?**
   - *Next:* Generate (Sx,Sy) quiver + Sz colormap on a dense kx-ky grid for both gapless (a=0) and gapped (a=0.55, Dw=0.10) cases; overlay against Figs. 1-2-4 and compare node lines and sign domains pixel-wise.
3. **How large are higher-order Floquet-Magnus / van Vleck corrections at hbar*omega = 8 eV with evA0 up to 0.9 eV, and do they shift the gap or deviation angle measurably?**
   - *Next:* Build the exact Floquet Hamiltonian (Sambe/extended zone, multiple photon sidebands), diagonalize, and compare its low-energy gap and spin texture to the van Vleck 2x2 result as a function of hbar*omega.
4. **Does the higher-order warping perturbation Hhw = i*xi*(k+^5 sigma+ - k-^5 sigma-) leave the light-induced deviation-angle fingerprint (delta=0 only along Gamma-K) unchanged, as the paper claims?**
   - *Next:* Add Hhw to Heff, recompute delta_omega(theta) at fixed k, and check whether the Gamma-K-only node survives across a range of xi.
5. **What is the experimental observability window — light intensity, frequency, and temperature — for the induced gap 2*Dw and the broken locking to be resolvable by spin-ARPES?**
   - *Next:* Invert evA0 and hbar*omega=8 eV to the physical E0 and intensity (W/cm^2) for a Bi2Te3 surface; compare to pump-probe damage limits and spin-ARPES energy resolution to assess detectability.

#### `polar-tian2026` — PARTIAL (C5/A9)

1. **Does the full DFT band structure of monolayer Mg2Mo2(PO5)2 place the {|dxz,up>2, |dyz,down>1} ridge states near the Fermi level with the projected orbital character claimed in Fig. 2(f)/S2?**
   - *Why:* The TB model is a schematic; the paper's material claim rests on DFT showing that the green-box ridge states are genuinely dxz/dyz-derived and dominate transport at E_F. Without it, the material realization (not just the toy model) is unverified.
   - *Next:* Run a magnetic (Neel, out-of-plane) DFT+U calculation of monolayer Mg2Mo2(PO5)2 (P4, a=6.56 A, Mo on 2g), project onto Mo t2g orbitals, and confirm the ridge dispersion + spin/orbital labels along Gamma-X-M and Gamma-Y-M.
2. **Is the layer polarization P(k) of the two ridges genuinely opposite (top vs bottom Mo layer), as required for the 'layer' in RSLC and for electric-field control?**
   - *Why:* Our TB model captures ridge-spin locking but has no explicit layer degree of freedom; the RSLC mechanism and the electric Hall effect depend on opposite layer polarization enabling Ez to split R1/R2.
   - *Next:* Extend the TB basis to include the two Mo sublayers explicitly (4-band model with {C2||S4z} enforced), compute layer projection P(k) of each ridge, and add an on-site Ez potential to verify degeneracy lifting.
3. **How much orthogonal-channel leakage (finite delta) is present in the real material, i.e. what is the effective delta/pi0 that sets the quasi-1D SP ceiling below 100%?**
   - *Why:* The paper claims '100%' but any real ridge has small curvature; our sweep shows SP=0.997 at delta=0.05 and 0.956 at delta=0.2. Quantifying the material's delta sets how close to ideal the experimental SP can be.
   - *Next:* Fit the DFT ridge dispersion along Delta(0,v,0) to pi0 cos + delta cos, extract delta/pi0, and propagate it through the Boltzmann SP formula to predict the achievable spin polarization.
4. **Does the relativistic (spin-orbit) calculation reproduce the electric Hall effect coefficient chi_xy that switches sign under +/-Ez, with S4z*T forbidding sigma_xy at Ez=0?**
   - *Why:* The layer-dependent electric Hall effect is the paper's second headline device concept; it requires SOC and is entirely outside the nonrelativistic TB scope replicated here.
   - *Next:* Add atomic SOC (lambda L.S) to the multi-orbital, multi-layer TB model, compute the Berry-curvature/Kubo anomalous Hall sigma_xy vs Ez, and verify sigma_xy(Ez=0)=0 and sign reversal for +/-Ez.
5. **Are the symmetry criteria (8 SLGs, RSLC only for 2 SSGs with 2e/2f/2g Wyckoff) reproducible from an independent spin-layer-group enumeration, and do they correctly single out the three candidate materials?**
   - *Why:* The materials-discovery claim (Table I) is the paper's route from concept to real compounds; independent symmetry verification would confirm the search is complete and correct, not cherry-picked.
   - *Next:* Use a spin-space-group / spin-layer-group tool (e.g. SpinSpaceGroup, or the FindSym-style analysis) to enumerate 2D square-lattice altermagnetic SLGs, apply the ridge (1D band rep along Delta) + {C2||OL} filters, and check the 8-SLG / 3-material result.
6. ****

#### `polar-verga2014` — PARTIAL (C5/A8)

1. **Does the full coupled Schrodinger (electrons) + Landau-Lifshitz (spins) time integrator reproduce the collapse snapshots of Fig. 2 (t = 5912-5960 t0) and the collapse time t* ~ lambda/(s0 a)?**
   - *Next:* Implement the coupled stepper (Crank-Nicolson or Chebyshev for Schrodinger; Heun/RK4 for LL with the STT torque term), seed with the relaxed BP skyrmion, measure t* vs lambda and compare the ~5900 t0 figure.
2. **Is the topological-charge collapse Q(t): 1 -> 0 correlated with the nucleation of an intense electron b-field vortex carrying its own topological charge, as claimed in Sec. III (lines 304-330, 520)?**
   - *Next:* After Q1, compute Q_S(t) and Q_b(t) = Berg-Luscher charge of s(r,t); test the anti-correlation / conservation-transfer claim at the collapse instant.
3. **How does the exchange-dissipation term d smooth the skyrmion->ferromagnet transition, and what is the quantitative d-dependence of the Q(t) curves in Fig. 3?**
   - *Next:* Add the exchange-dissipation operator to the LL RHS, run a d-scan, reproduce the smoothing trend and the dissipation-dependent transition sharpness of Fig. 3.
4. **Does the exact self-similar solution (Eqs. 24-25) of the driven LL equation quantitatively match the collapsing core profile f(X) from the full numerical run, beyond the exponent (alpha,beta) match?**
   - *Next:* Solve the self-similar ODE (Eq. ~22-23) for f(X) with the stated boundary conditions; overlay rescaled numerical cores from Q1 to test data collapse.
5. **How sensitive is the collapse (existence of a finite-time singularity vs. a smooth crossover) to lattice cutoff a, initial size lambda_0, current polarization Bp, and electron density ne?**
   - *Next:* Grid (lambda_0, Bp, ne) at fixed a, run the Q1 solver at each, fit beta and t*, and map where the self-similar collapse survives vs. where dissipation dominates.

#### `polar-yuan2023` — PARTIAL (C5/A7)

1. **Does a hexagonal close-packed polar SkX emerge SPONTANEOUSLY from a labyrinth/stripe domain state under increasing Ez, without seeding pre-formed skyrmions?**
   - *Why:* The paper's central claim is field-INDUCED emergence (L -> Sk&L -> SkX). Our reduced 2D LGD reproduced SkX stability and its field-driven destruction, but the SkX had to be seeded; spontaneous nucleation is the harder, unproven half of the headline.
   - *Next:* Add the full 3D depolarization field (open-circuit boundary with screening theta) and a Landau expansion with the paper's Haun PbTiO3 coefficients [Ref 56], then quench from a random state at fixed Ez to test whether SkX nucleates without seeds.
2. **Is the simulated SkX genuinely Neel-type with center-convergent/divergent top/bottom planes and a purely out-of-plane middle plane, as the paper reports?**
   - *Why:* The paper distinguishes its Neel-type SkX from the Bloch-walled skyrmion bubbles of PTO/STO superlattices [Ref 33]; the wall type is a physical fingerprint of the strain/electrostatic balance.
   - *Next:* Extend to a 3D slab (Nz ~ 6 cells) and inspect the through-thickness rotation of P at a single core; verify Ising-type (out-of-plane) connecting wall vs Bloch-type.
3. **Does the hexagonal lattice constant w obey Kittel scaling, w^2 proportional to film thickness h, over 5 nm < h < 13 nm?**
   - *Why:* This quantitative scaling law (w=13.6 nm at h=6 nm, w=20.5 nm at h=11.2 nm) is a second, independent testable prediction distinct from the field-collapse headline.
   - *Next:* Run 3D simulations at h = 6, 8, 11 nm, extract nearest-core distance from the SkX autocorrelation, and regress w^2 vs h.
4. **Where exactly do the S->SkX and L->SkX transition boundaries sit in the T-E phase diagram, and is the low-T-L / high-T-S inverse transition reproduced?**
   - *Why:* The paper reports SkX only between 300-500 K and an unusual inverse L->S transition on heating; the phase-boundary topology is a strong test of the free-energy balance.
   - *Next:* Add a temperature-dependent Landau coefficient a(T)=a0(T-T0) and a thermal-noise TDGL sweep to map n_sky and |Q| over a (T, Ez) grid.
5. **How sensitive is the SkX stability window to the screening factor theta and misfit strain, which the paper fixes at theta=0.6 and eps=-1.0%?**
   - *Why:* These two boundary-condition parameters set the depolarization/anisotropy balance; the whole SkX-existence region may shrink or vanish outside a narrow range, affecting experimental realizability.
   - *Next:* Sweep theta in {0.4,0.6,0.8} and eps in {-0.5%,-1.0%,-2.0%} in the depolarization kernel amplitude and anisotropy K_z, and record the Ez-width of the |Q|>0 window.

#### `polar-zhang2012` — REPLICATED (C8/A9)

1. **What is the exact origin of the factor-2 prefactor gap in the total in-plane orbital spin magnitude, and does it disappear when the atom/orbital sum over alpha (the |Phi> expansion cross-terms) is retained rather than collapsed to a single effective orbital?**
2. **Does an independent ab-initio (DFT+SOC) calculation of a Bi2Se3 slab reproduce the same p-orbital-resolved spin-orbital texture (p_z helical, p_x/p_y 2-theta, tangential-upper/radial-lower) that the effective k.p model predicts, and do the fitted u0,v0,u1,v1,w1 come out with the signs the texture requires?**
3. **What spin-resolved, photon-polarization-dependent ARPES intensity would actually be measured for P_{p_x}, once dipole matrix elements and photon-energy/geometry dependence are folded in on top of the bare Eq.10 polarization?**
4. **How does the spin-orbital texture evolve when a hexagonal-warping (Fu C3v k^3) term is ADDED to Eq.1 -- i.e., bridging arXiv:1211.0762 (isotropic) to the warped-Dirac model of the sibling paper the task framing conflated it with?**
5. **Is the right-handed net in-plane orbital spin for BOTH Dirac cones (the paper's headline qualitative surprise) robust to the parameter set, or does it require a specific sign/magnitude ordering of u1 vs w1 -- and where in (u1,w1) space does the tangential-dominant vs radial-dominant character invert?**

---

### Multipolar — 10 papers, 51 questions

#### `multipolar-banerjee2026` — PARTIAL (C5/A8)

1. **Does the induced anisotropy Gamma^(3)/J_eff actually reach order-1 (comparable to J_eff) as Fig.3(a) shows, or does the minimal analytic evaluation cap it at ~10^-3?**
   - *Why:* The paper's central physics (opening the enlarged Kitaev-like multipolar liquid regime) requires the bond anisotropy to become strong enough to compete with the leading exchange. Our evaluation gives Gamma^(3)/J_eff ~ 2.7e-3 at zeta=4, three orders below the ~O(1) suggested by Fig.3(a).
   - *Next:* Recompute with the paper's exact geometry (psi_0, r_pd/r_dd from Slater-Koster edge-sharing geometry) and confirm whether A0=E0*r_dd/Omega vs A=E0*r_pd/Omega ratio and the J^(4) t_pd^4 term amplify anisotropy at large zeta; cross-check Appendix B/C definitions of U-tilde.
2. **What is the precise definition of the effective interaction scale U-tilde in terms of U, J_H, and lambda (Appendix A/C)?**
   - *Why:* U-tilde sets the virtual-denominator resonances (U-tilde - m*Omega) that control the entire Floquet sum magnitude; we used the representative U-tilde=3.0 eV but its microscopic composition changes coupling ratios and resonance placement.
   - *Next:* Extract Appendix A/C from the full PDF (pages beyond the provided excerpt) and substitute the exact U-tilde(U,J_H,lambda) expression, re-evaluating Eqs.6a-6f.
3. **Does the many-body ED phase diagram (AFO, FO, PPFQ, IO, ML) emerge from Heff over the (Gamma^(3)/J_eff, h_m/J_eff) plane?**
   - *Why:* The paper's Fig.8 phase diagram is the physical payoff of the induced couplings; we replicated the couplings but not the phases, so the claim that only AFO survives without CPL is unverified here.
   - *Next:* Build the honeycomb-cluster pseudospin Hamiltonian Eq.(4) and run exact diagonalization (e.g. 24-site cluster) scanning Gamma^(3) and h_m; identify order parameters <sigma^y> (FO/AFO octupole), quadrupolar, and entanglement signatures of the liquid.
4. **Is the h_m proportional-to-Gamma^(3) constraint (ratio 9/8) an exact analytic identity or an artifact of the single-t2 minimal model?**
   - *Why:* The paper states the proportionality is a consequence of the minimal model (single t_2) and can be lifted by an external [111] field; understanding this distinguishes a robust prediction from a model simplification.
   - *Next:* Add a second TM-TM hopping channel or a weak static B[111] to the coupling formulas and verify the ratio h_m/Gamma^(3) departs from 9/8, matching the paper's claim that the constraint relaxes.
5. **How large is the prethermal lifetime tau* in physical units, and does it exceed pump-probe timescales for the stated Omega ~ 100 THz and Lambda ~ meV?**
   - *Why:* The entire effective-Hamiltonian description (Eq.4) is valid only in the prethermal window; if tau* is too short the induced OIFE field is not observable, undermining the experimental proposal.
   - *Next:* Evaluate Eq.(5) tau* ~ (hbar/Lambda) exp(alpha*hbar*Omega/Lambda) with Lambda=max local scale from our computed couplings (~1.5e-2 eV) and alpha~1; confirm the several-picosecond estimate quoted in the paper.

#### `multipolar-chen2022` — PARTIAL (C7/A8)

1. **What are the exact phase boundaries in the (Jperp~/Jx~, J2xz/Jx~) plane from the full self-consistent gMFT (chi1, chi2, I1, I2)?**
   - *Why:* Our replication scans an effective inter-sublattice hop t2 rather than the two microscopic couplings; the true 2D boundary and the location of the U(1)-QSL/AF*/fragmented-AFM triple region cannot be quantitatively pinned without the coupled self-consistency.
   - *Next:* Implement the full self-consistent loop solving chi1=<s~+ s~->, chi2=<s~+ s~x>, I1=I2=<Phi† Phi'> jointly with lambda, then re-scan the true 2D parameter plane.
2. **Is the AF*→fragmented-AFM transition continuous (spinon condensation at Gamma) as claimed, and 3D-Ising at finite T?**
   - *Why:* The paper asserts a continuous Anderson-Higgs boundary and a finite-T 3D Ising transition for the AAO order; our T=0 gap-closure is consistent but does not test the universality class.
   - *Next:* Add the Gamma-point condensate order parameter and a finite-T treatment (or Monte Carlo of the effective Ising AAO field) to check continuity and 3D-Ising exponents.
3. **What is the absolute magnitude of the T^3 specific-heat coefficient in physical units for Nd2Sn2O7?**
   - *Why:* The 'anomalously large' claim is the key experimental fingerprint; a material-specific number would enable direct comparison with heat-capacity data.
   - *Next:* Fit the emergent photon velocity from ring-exchange g ~ 12 Jperp^3/Jx^2 using reported Nd2Sn2O7 exchange scales and convert to J/mol/K^4.
4. **Does the two-spinon continuum (Eq. 16-17) reproduce the paper's Fig. 2 spectral envelope along high-symmetry lines?**
   - *Why:* The broad INS spinon continuum is the dynamical smoking gun distinguishing AF* from a conventional magnon spectrum.
   - *Next:* Compute Omega(q)=w_mu(k1)+w_nu(q-k1) min/max envelopes on a fine grid along Gamma-X-W-L and overlay on the paper's Fig. 2 (t1=0.025, t2=0.02).
5. **How robust is the AF* state to the neglected '...' terms (dipolar S^z-S^z, further-neighbor superexchange)?**
   - *Why:* The minimal model drops terms that could shift or destroy the AF* window; robustness determines material realizability.
   - *Next:* Add a tunable second-neighbor Jzz and dipolar tail, re-solve gMFT, and map the shrink/growth of the AF* region.

#### `multipolar-das2014` — PARTIAL (C4/A6)

1. **Does using the realistic WIEN2k DFT Fermi surface (rather than a single nested tight-binding pocket) recover the ~40% FS spectral-weight loss and ~24% R ln2 entropy release?**
   - *Why:* These integrated quantities are the extensive thermodynamic fingerprints of the HO transition and are the main under-reproduced numbers in this model replication (we get ~6% and ~0.006 k_B ln2). They test whether the gap phenomenology is quantitatively, not just qualitatively, an SODW.
   - *Next:* Downfold DFT bands for URu2Si2 near E_F onto the two spin-orbit-split 5f orbitals, identify the (110)/(100) hot-spot nesting at Q=0.5(pi,pi,0), and re-run the same self-consistent gap equation over the realistic multi-sheet FS.
2. **Why is the model 2*Delta0/k_B*Th ratio (~8) far above the BCS value 3.53, and is the real SODW strong-coupling?**
   - *Why:* The gap-to-Tc ratio diagnoses coupling strength and the shape of Delta(T). A ratio of ~8 signals the self-consistency in this flat-nested band is strongly non-BCS, which affects the predicted specific-heat jump at Th.
   - *Next:* Compute Delta(T) with finer T resolution near Th and fit the mean-field order-parameter exponent; compare the specific-heat jump Delta C/C to the measured 24% entropy discontinuity.
3. **Can the naive Zeeman estimate B_c = 2*Delta0/(g*muB) (~106 T here) be reconciled with the experimental ~35 T once the field dependence of Delta and the anisotropic g-factor are included?**
   - *Why:* The predicted quantum critical field near 35 T is a headline falsifiable prediction of the SODW theory; our static gap-closing estimate overshoots by ~3x.
   - *Next:* Add a Zeeman term to H_k, recompute the self-consistent Delta(B) until it vanishes, and use the momentum-dependent g-factor from quantum-oscillation data rather than g=2.
4. **How does the competition/coexistence with the LMAF (SDW) order parameter (Das Eqs. 11-12, GL functional) shift the SODW gap and Th?**
   - *Why:* The HO->LMAF first-order transition under pressure/field is a defining feature of URu2Si2; the pure-SODW mean field here ignores the gamma|Delta_sodw|^2|Delta_sdw|^2 cross-coupling.
   - *Next:* Implement the two-field Ginzburg-Landau free energy F[Delta_sodw, Delta_sdw] with the alpha, beta, gamma coefficients of Eq. 12 and map the phase boundary in the (U/V, lambda/W) plane of Fig. 4.
5. **Is the SODW gap really time-reversal invariant (zero net moment) in the model, as Das proves analytically (Eq. 9)?**
   - *Why:* The absence of an ordered magnetic moment is what makes the order 'hidden'; verifying it numerically in the model validates that our construction is a genuine SODW and not a disguised SDW.
   - *Next:* Evaluate the spin expectation S = (1/N) sum_k <c^dag_{k+Q} sigma c_k> in the self-consistent SODW ground state and confirm it vanishes for all V, as Eq. 9 predicts.

#### `multipolar-konakanchi2025` — REPLICATED (C7/A8)

1. **What is the exact origin of the ~2x dimensionless prefactor difference between our self-consistent low-barrier 1/e time (sqrt(2)/omega_J with omega_J=gamma*sqrt(H_J*H_th/3)) and the paper's published Eq. 10 constant (sqrt(2*ln2)/(gamma*sqrt(H_J*H_th)))?**
   - *Why:* It determines whether the replication is quantitatively exact or only scale-accurate. The physical picosecond scale and all qualitative conclusions are unaffected, but a factor ~2 matters for device retention-time engineering.
   - *Next:* Rederive the mz-mode normalization from the full three-sublattice free energy (the factor-3 in stiffness 3/2 Ms H_J V) and confirm whether the paper defines tau at C=1/e or C=1/2; check the SI Eq. 9->10 reduction line-by-line against a symbolic (sympy) Gaussian-integral derivation.
2. **Does the full six-spin (or three-magnetization) stochastic-LLG simulation with explicit J, D, K, nu reproduce the same tau as the reduced (mz, phi_oct) effective theory across the crossover region Delta ~ kT?**
   - *Why:* The paper's headline rests on the reduced effective theory; the crossover (Delta ~ kT), where neither Langer nor pure dephasing is exact, is the least-validated regime and is exactly the device operating point for probabilistic computing.
   - *Next:* Implement the full 3-vector s-LLG (Eq. 3) with Heun/Stratonovich integration and FDT thermal fields, sweep V so Delta/kT spans 0.05-8, and overlay measured C(t) tau against both analytic asymptotes.
3. **What Mn3Sn material parameters (J, D, K, Ms, nu, V) reproduce BOTH the ~100 T exchange field AND the specific ~10 ps quoted for the lowest barrier simultaneously and self-consistently?**
   - *Why:* We adopted H_J=100 T and literature Ms directly; a first-principles-consistent parameter set would turn a scale-match into a parameter-free quantitative match and enable predictive material design.
   - *Next:* Extract J, D, K for Mn3Sn from Refs. [27,35,44] cited in the paper, compute H_J=(9J+3sqrt3 D)/3Ms and Delta=2nuKJV/(J+sqrt3 D) from those, and verify the ps scale emerges without free tuning.
4. **How accurately does the depopulation factor A(V*deltaF/kT) stay at unity for the very-low-damping (alpha ~ 1e-3) chiral AFMs now being reported, where the paper warns A may deviate significantly?**
   - *Why:* In the VLD limit the IHD Langer escape time is an underestimate; if A deviates from 1 the high-barrier retention times (and thus memory viability) change substantially.
   - *Next:* Numerically evaluate the depopulation integral A(x) (paper Eq. D18) for the actual V*deltaF/kT = 6*alpha*sqrt(J K nu V)/kT at alpha=1e-3 and confirm/correct the A~1 assumption.
5. **Can the proposed spin-orbit-torque (Josephson-junction analogy) electrical tuning of tau by 'orders of magnitude' be reproduced quantitatively, including the tilted-washboard critical current I_c?**
   - *Why:* The electrical-tunability claim is the applied payoff of the paper (probabilistic computing, tunable RNG); it was not exercised in this replication and is central to device relevance.
   - *Next:* Add the spin-current term H_S=(hbar/2e)(theta_sh I_b)/(3 Ms V) to the effective free energy (Eq. E5), recompute asymmetric barriers Delta_up-down/Delta_down-up (Eqs. F11-F12) and the two-path relaxation rate (Eq. F13) vs I_b/I_c, and verify orders-of-magnitude tuning.

#### `multipolar-kotetes2010` — PARTIAL (C5/A6)

1. **Does the strict field-induced character of the dxy component (Delta1=0 at B=0) survive in a microscopic multi-Fermi-line model, rather than only in the Landau reduction?**
   - *Why:* The paper's central claim of a *field-induced* chirality rests on alpha1 > 0 so that dxy only appears through the orbital coupling g*Delta1*Delta2*B. Our simplified single-band model has V''>V', which lets dxy condense on its own at B=0 — the opposite of the paper. Whether the field-only behavior is generic or an artifact of the reduced model bears directly on the falsifiability of the chiral-HO proposal.
   - *Next:* Implement the four-Fermi-line nesting geometry at Q1=(1+/-0.4,0,0) (paper Appendix A footnote) and re-solve C2; check the sign of the bare dxy quadratic coefficient.
2. **Can the double-step metamagnetism (first-order jumps at Bc1=33.5 T and Bc2=41 T) be reproduced from the band-crossing mechanism (Eq. B3) with the stated parameters?**
   - *Why:* The metamagnetic double-step is one of the two headline experimental puzzles the paper claims to unify. It is a first-order (band-crossing) effect not captured by our smooth free-energy topology, so its absolute field scale is an independent, strong test of the model.
   - *Next:* Compute M_z(B) = -dF/dB from the 4-band spectrum including the orbital term (Eqs. E1-E2) on a fine k-grid and locate the field values where an energy branch crosses E_F.
3. **What sets the absolute field scale Bc1 ~ 33.5 T — is it the Zeeman energy muB*Bc1 ~ 1.94 meV matching Delta2(0), or the orbital coupling?**
   - *Why:* muB*33.5 T = 1.94 meV is remarkably close to Delta2(0)=1.55-1.87 meV, suggesting the gap-closing (Pauli-limit-like) scale controls the MCEP. Distinguishing Zeeman vs orbital origin determines which experimental knob (field angle, g-factor) would shift Bc1.
   - *Next:* Run the microscopic solver over B with orbital coupling ORB set to 0 vs finite, and track where Delta2 collapses; compare the collapse field to muB-only prediction.
4. **Does the model reproduce the quadratic field-suppression law Delta2(B)/Delta2(0) ~ 1-(B/Bc1)^2 above the MCEP?**
   - *Why:* This specific law is claimed to be verified in magnetoresistance experiments [47] and is a clean, parameter-light prediction. Our low-T field sweep currently shows Delta2 *rising* with B (single-band artifact), so this is an open discrepancy to resolve.
   - *Next:* In the corrected multi-band model, restrict to T just above the MCEP temperature (~3-5 K) and fit Delta2(B)/Delta2(0) to a + b*(B/Bc)^2.
5. **Is the giant 'tilted-hill' Nernst signal (~30 uV/K near 12 T, 3-4 K) a genuine topological (Berry-curvature) effect of magnitude set by the chiral gap, or dominated by quasiparticle contributions?**
   - *Why:* The paper attributes the giant Nernst to the topological robustness of the chiral condensate (Ref. [46]), computing it ~1 order larger than experiment. Separating topological vs quasiparticle alpha_xy tests the chiral interpretation against conventional semimetal explanations.
   - *Next:* Implement alpha_xy^top from Berry curvature (Eqs. E, sum of nF*Omega) and alpha_xy^qp from the quasiparticle expressions, then form nu=N/Bz and reproduce the T-peak at 3-4 K.
6. ****

#### `multipolar-li2016` — REPLICATED (C8/A9)

1. **Do the exact Supplementary-Information definitions of the rotated couplings (Jx,Jy,Jz) in Eq. 4 modify the FO transition temperature away from the clean 1.5|Jx|?**
   - *Why:* Our exact match To=1.5|Jx| relies on interpreting the reduced-model Jx as the bare octupolar coupling. If the SI rotation mixes Jyz into the effective couplings, To could shift, changing the quantitative (not qualitative) agreement.
   - *Next:* Obtain the SI, implement the full theta-rotation from Eq. 3 including Jyz, and re-derive the effective Jx,Jy,Jz as functions of (bare couplings, theta).
2. **Does a fully self-consistent 3-sublattice mean-field solver reproduce the complete Ox-surface phase diagram (Fig. 2) with correct first- vs continuous-order boundaries?**
   - *Why:* We reconstructed only a coarse Ix-surface slice via classical minimization. The rich AFO-FDy/AFO-FDz/supersolid structure on the Ox surface is the paper's other major result and is untested here.
   - *Next:* Implement HMF (Eq. 6) with iterative self-consistency for mA,mB,mC on a (Jy/Jx, Jz/Jx) grid at Jx=+1 and classify phases and transition orders.
3. **Is chi_zz non-divergence robust to a quantum (rather than single-site mean-field) treatment near To?**
   - *Why:* The 'hidden order invisible to magnetization' claim is the paper's headline experimental prediction. Single-site MF gaps the transverse channel by construction; a fluctuation-corrected treatment could reveal a subleading anomaly.
   - *Next:* Compute chi_zz(T) via linear spin-wave / RPA on top of the FO mean field and check for any cusp or shoulder at To.
4. **What is the full octupolar-wave dispersion along the complete BZ path, and does its gap scale as predicted with Jy, Jz?**
   - *Why:* The gapped octupolar wave is the proposed inelastic-neutron signature of hidden FO order; the gap magnitude and dispersion shape are what an experiment would compare against.
   - *Next:* Sweep Jy, Jz and record the minimum gap min_k omega_k from Eq. 5; verify gap -> 0 only in the isotropic Jy=Jz=Jx limit.
5. **Does the quantum mutual modulation between ferro-dipolar and antiferro-octupolar orders (a stated quantum effect absent classically) appear in exact diagonalization of a small triangular cluster?**
   - *Why:* The paper explicitly states this modulation cannot occur in a classical spin system; our classical minimizer therefore cannot capture it, bounding the scope of a purely classical replication.
   - *Next:* Run ED on a 12- or 18-site triangular cluster in the AFO-FDy regime and measure the 3-sublattice modulation of <T^y> induced by octupolar order.

#### `multipolar-patri2018` — REPLICATED (C7/A10)

1. **What microscopic value of the octupole-strain coupling g_O follows from second/third-order perturbation theory in h.J for PrV2Al20's actual CEF gaps Delta(Gamma4), Delta(Gamma5)?**
   - *Why:* The linear-in-h magnetostriction coefficient equals (1/sqrt3)(g_O/c44)m; only g_O carries the material-specific magnitude. Without it the replication confirms scaling but not absolute size.
   - *Next:* Diagonalize the full J=4 CEF Hamiltonian with published PrV2Al20 B_lm parameters, project h.J onto the Gamma3 doublet at 2nd/3rd order, and read off g_O and gamma_0.
2. **Does the fully coupled minimization of F[phi,phi-tilde,m] reproduce the renormalized octupolar transition T_O ~ 0.65 K and the kink in AFQ at T_O?**
   - *Why:* The paper's phase diagram (Fig.1) hinges on the uphi-m and uphi-tilde-m couplings shifting T_O from its bare value; our part-C uses an isolated FO potential and cannot verify T_O.
   - *Next:* Implement the full free energy Eqs.7-11 with the clock terms (w_phi-tilde, v_phi) and minimize over |phi|,|phi-tilde|,m,alpha,alpha-tilde vs T to trace the coupled phase diagram.
3. **What is the true shape and width of the field-hysteresis loop in m(h) once the cubic-in-h drive competes with the quadrupolar background, rather than in an isolated double well?**
   - *Why:* Our loop width (=1 in units of spontaneous m) is a demonstrator; the experimentally relevant coercive field and loop area depend on the full landscape and on b's microscopic value.
   - *Next:* Add the AFQ/FQ sectors and the h^2 mass renormalizations (s_H, s-tilde_H) to the octupole potential and recompute the loop at finite T just below T_O.
4. **Do the [100] and [110] field-direction predictions in Table 2 (quadrupolar-order signatures) reproduce with the same from-scratch machinery?**
   - *Why:* The paper claims magnetostriction along other directions probes quadrupolar (not octupolar) order; replicating those cross-checks that [111] uniquely isolates the octupole.
   - *Next:* Repeat the strain minimization with psi_H couplings for n=[100] (theta_H=-pi/6) and [110] (theta_H=-pi/2) and extract the field-scaling of each (dL/L) component.
5. **How robust is the linear-in-h octupole result to a small residual dipolar admixture (finite Gamma3-Gamma4 mixing) that would add a competing linear magnetic response?**
   - *Why:* The paper's clean probe relies on the doublet carrying NO dipole moment; real materials have finite CEF gaps, so a subleading dipole channel could contaminate the magnetostriction.
   - *Next:* Introduce a controlled dipole leakage via finite Delta(Gamma4) in the projected model and quantify the h-power and amplitude of the spurious contribution relative to the octupolar term.

#### `multipolar-sim2019` — PARTIAL (C6/A6)

1. **What is the sign of the Ginzburg-Landau quartic invariant q2 for the eg doublet in the exact one-loop / two-band-projected-gap treatment, and why does a single-gap BdG condensation-energy proxy give the opposite sign?**
   - *Why:* q2>0 is the entire content of the headline claim (TR-breaking (1,i) selected). Our proxy gives q2<0. Nailing the sign from the correct microscopic quartic coefficient is the difference between confirming and contradicting the paper's central result.
   - *Next:* Derive q2 analytically via the one-loop particle-particle bubble with the eg vertices M1,M2 projected onto the two active Luttinger bands at E_F (Boettcher-Herbut PRL 120,057002 SI method), and compare to a fully self-consistent multi-gap BdG free-energy minimization rather than a fixed-Delta condensation energy.
2. **Does the self-consistently determined gap magnitude Delta_a(k) (solving the full nonlinear gap equation) change the state ordering relative to the fixed-Delta condensation-energy comparison used here?**
   - *Why:* The TR-breaking state may have a larger self-consistent Delta (it fully gaps most of the FS) that overcompensates the pocket cost. A fixed-Delta comparison cannot see this; only a self-consistent solve can.
   - *Next:* Implement the coupled self-consistency Delta_a = g <psi^T gamma45 gamma_a psi> at each temperature, iterate to convergence per candidate state, and compare converged free energies F[Delta_a*].
3. **Do the 16 Bogoliubov Fermi-surface pockets of the (1,i) state carry Chern numbers +/-2 as claimed (Class D + inversion, 2Z classification)?**
   - *Why:* This is the topological headline that makes the state a topological superconductor; it is an independent, falsifiable prediction not touched by the energetics.
   - *Next:* For the (1,i) BdG Hamiltonian, locate the gapless pockets, wrap a small BZ sphere around each, and compute the Chern number by the standard Fukui-Hatsugai-Suzuki lattice-plaquette Berry-flux method.
4. **How does the ferro-quadrupolar order <O20> reshape the phase diagram (Fig.1) — specifically the transition from eg (1,i) to the t2g dyz+idzx (1,i) state via Fermi-surface distortion c3=c4=(-1-J_K<O20>)?**
   - *Why:* The paper's central novelty is that multipolar order tunes the SC channel and thus the topology. Reproducing the phase boundary would validate the quadrupolar-Kondo mechanism, not just the cubic column.
   - *Next:* Scan J_K<O20> in [0,1.5] and g, recomputing Part A/B with the distorted c_eta, and map which channel (eg vs eta=(d3,d4)) has the leading instability at each point.
5. **Is the microscopic projected Kondo coupling (Eq.7) correctly derived from the orbital form factors Gamma^a_{1,ij}, Gamma^a_{2,ij}, and does it reproduce the stated c3=c4!=c5 anisotropy quantitatively?**
   - *Why:* Eq.7 is the bridge from the localized Pr quadrupoles to the itinerant Fermi-surface distortion; the whole quadrupolar-Kondo story rests on it. We assumed the renormalized c-coefficients rather than deriving them.
   - *Next:* Reconstruct the two-FCC-sublattice tight-binding form factors from SI Sec.II, apply the j=3/2 projector P, and verify the resulting H_K(k) matches Eq.7 term-by-term.

#### `multipolar-vedmedenko2008` — PARTIAL (C6/A7)

1. **Does true long-range orientational order remain absent at the full paper scale (up to 1000 sites, square/rectangular AND circular patches)?**
   - *Why:* Our 151-site circular patch already shows decaying correlations, but finite-size effects can mask weak LRO; the paper's key claim is scale-robust absence of LRO.
   - *Next:* Regenerate patches of N=300,600,1000 in multiple shapes and check that C(r) and the orientation structure factor do not sharpen with N.
2. **Do the odd-parity ground states quantitatively reproduce the decagonal HBS tiling geometry (hexagon+boat+star decomposition), not just its statistical fingerprints?**
   - *Why:* The paper's central visual is the HBS superstructure outlined by thin-rhombus short-diagonal pairs/triplets; matching it geometrically is stronger evidence than histograms.
   - *Next:* Identify thin-rhombus short diagonals from the pentagrid tiles, tag pair/triplet chains, and overlay the HBS decomposition on the relaxed configuration.
3. **Is the observed lack of LRO purely a frustration effect of the interaction Hamiltonian, or partly geometric to the tiling?**
   - *Why:* The paper notes an ordered arrow arrangement DOES exist geometrically (Lifshitz; Cockayne-Widom edge model); disentangling energetic vs geometric frustration guides Hamiltonian design for order.
   - *Next:* Compare our vertex-based rotor ground state against the Cockayne-Widom edge-arrow model energy on the same tiling to see which Hamiltonian admits LRO.
4. **How does the critical interparticle separation R_c (maximal short-range order) emerge when dipolar and octopolar contributions are combined with realistic 1s-2s ratios?**
   - *Why:* The paper predicts an optimal R_c ~ 1s-2s where SRO is maximal; this controls real nanomagnet/adsorbate design.
   - *Next:* Add mixed l=1+l=3 couplings with a tunable size parameter s and scan R_c by locating the peak of the nearest-neighbour correlation.
5. **Do the even-parity multipoles (l=2 quadrupole, l=4 hexadecapole) show the predicted 90-degree / 72-degree local alignment and weaker, harder-to-quantify SRO?**
   - *Why:* Completes the parity dichotomy that is the paper's organizing theme; even-parity is the harder analysis case.
   - *Next:* Extend the rotor kernel with even-parity angular potentials (double-headed arrows, head-to-center attraction) and measure nearest-neighbour angle histograms.

#### `multipolar-you2021` — PARTIAL (C4/A8)

1. **What is the absolute critical current density J_crit in physical (A/cm^2) units, and does a parameterized LLG with real Ms, Hk, thickness reproduce the reported ~9e6 A/cm^2?**
   - *Why:* The headline device metric is J_crit; a reduced-unit macrospin shows a threshold exists but cannot confirm the magnitude, which determines device viability.
   - *Next:* Rebuild LLG in SI units with Co/Pd Ms~1.4e6 A/m, Hk from the RAHE-H loop, t=3.6 nm, and theta_AD,z=0.003 to convert current density to torque amplitude and locate J_crit.
2. **The paper measures theta_FL,z (0.053) >> theta_AD,z (0.003). Does the large field-like sigma_z term help, hinder, or not affect deterministic switching?**
   - *Why:* Determinism is usually attributed to antidamping; a dominant field-like term is unusual and may modify the switching phase diagram / incubation.
   - *Next:* Sweep tau_FL/tau_DL ratio in the macrospin model and map switching probability & threshold vs ratio.
3. **How does the 35-degree angle between J and T (for J along [001]) quantitatively set the sigma_z magnitude via sigma_z ~ Hso x T?**
   - *Why:* The symmetry rule is binary in the paper (present/absent) but sigma_z should scale continuously with the J-T angle; this governs orientation engineering.
   - *Next:* Add explicit angle dependence p_z = sin(angle) to the polarization vector and compute threshold current vs J-T angle from 0 to 90 deg.
4. **Does thermal (Langevin) noise at 300 K preserve the deterministic switching, or does it introduce stochasticity near threshold?**
   - *Why:* Real devices operate at finite T; determinism claims must survive thermal fluctuations to be technologically meaningful.
   - *Next:* Add a stochastic thermal field term to the LLG and compute switching probability vs current over many realizations at 300 K.
5. **Is the ~60% switched volume (RAHE-I vs RAHE-H) consistent with a macrospin, or does it require domain/multidomain (micromagnetic) modeling?**
   - *Why:* Macrospin assumes coherent rotation; partial switching suggests domain nucleation in the current channel, changing the physics of J_crit.
   - *Next:* Run a 1D/2D micromagnetic (e.g. mumax3-style) chain with the sigma_z torque to test domain-wall vs coherent switching.

---

### Loop-Current — 11 papers, 55 questions

#### `loop-current-christensen2022` — PARTIAL (C5/A9)

1. **Which of the seven symmetry-distinct iCDW orders (mM2+, mM3+, mM4+ across occupied/unoccupied vHs) is actually realized in CsV3Sb5?**
   - *Why:* The subsidiary uniform magnetic order (ferro vs octupolar vs toroidal vs monopolar) and the observable magneto-electric/striction signatures depend entirely on which iCDW irrep condenses.
   - *Next:* Compute the DFT VHS orbital/sublattice content at M and evaluate which iCDW channel has the most attractive interaction; cross-check against measured Kerr/muSR TRS-breaking onset.
2. **Does the coupled theory select 3Q-3Q or 2Q-1Q for realistic AV3Sb5 coefficient values?**
   - *Why:* 3Q-3Q preserves C3 (magnetic orders) while 2Q-1Q is orthorhombic; experiments report nematicity, so the sign/magnitude of the biquadratic and quadrilinear coefficients is decisive.
   - *Next:* Fit lambda_ir(1), kappa_ir, u_i, u_r from a microscopic mean-field VHS model rather than treating them as free, then locate the physical point on our phase diagram.
3. **How does the arbitrary-sign trilinear gamma_ir (origin-dependent) affect the physical distinction between star-of-David and tri-hexagonal bond order?**
   - *Why:* The sign of N1 N2 N3 distinguishes SoD vs tri-hexagonal (Ref. 54); the theory says loop-current config is insensitive to sign(Phi1 Phi2 Phi3) but the rCDW config is not.
   - *Next:* Extend the minimizer to track sign(N1 N2 N3) and map which bond-order pattern accompanies each mixed phase across the diagram.
4. **What is the effect of the out-of-plane (kz) modulation and interlayer coupling on the mixed phase selection?**
   - *Why:* The paper notes 2x2x2 vs 2x2x4 stacking; interlayer terms could stabilize different mixed states than the single-layer analysis.
   - *Next:* Add a bilayer order-parameter doubling (above/below plane fields) and the symmetry-allowed interlayer couplings to the free energy and re-minimize.
5. **Does the SOC-induced SDW that necessarily accompanies iCDW change the energetics enough to shift the 3Q-3Q vs 2Q-1Q boundary?**
   - *Why:* The paper states iCDW triggers an SDW at the same wavevector under SOC; back-reaction of the SDW free energy could move the phase boundary.
   - *Next:* Add an SDW order parameter M_i coupled biquadratically to Phi_i and quantify the shift of the phase boundary.

#### `loop-current-chung2009` — REPLICATED (C7/A9)

1. **Can the projection operator P = prod_i (1+D_i)/2 be applied directly to re-derive that the (-1,-1) global-flux sector carries ODD fermion parity in the non-Abelian phase (g<sqrt3), rather than importing that parity result from the paper/Yao-Kivelson?**
   - *Why:* The <Phi_x>=1/3 headline hinges entirely on exactly ONE of the four sectors being projected out. Our replication reproduces the counting GIVEN that parity fact but takes it from the paper. A first-principles re-derivation of the sector parity from P would make the replication fully self-contained and would test the claim's most subtle step.
   - *Next:* Compute the many-body fermion parity Pf = prod_{x',y',z'-links} i c_i c_j of the free-fermion ground state in each of the four (Phi_x,Phi_y) sectors on a finite torus, as a function of g, and confirm it flips to odd only for (-1,-1) at g<sqrt3.
2. **What is the exact Chern number / chiral central charge of the occupied Majorana bands in the Yao-Kivelson convention, and why does our FHS calculation report C=+3 deep in the nA phase instead of |C|=1?**
   - *Why:* The non-Abelian phase is characterized by a single chiral Majorana edge mode (c=1/2). Our raw 3-occupied-band FHS sum gives +3, which is convention/gauge dependent (multi-band, doubled-Majorana counting). Pinning the physical invariant confirms the non-Abelian TQFT class (Ising anyons).
   - *Next:* Compute the Chern number band-by-band with a fixed smooth gauge, and cross-check against an open-cylinder edge-spectrum calculation counting chiral Majorana branches crossing zero energy.
3. **Does the crossover temperature T*(g) obey T* ~ Delta(g)/ln N (Eq.9), and is it non-vanishing at g_c while the fermion gap vanishes?**
   - *Why:* This is the paper's second, more subtle claim: a finite-T signature of topological order whose size scaling is logarithmically slow. It is the bridge from the T=0 degeneracy to a finite-T observable and the paper's main conceptual contribution.
   - *Next:* Evaluate <Phi_x>(T) from Eq.13 for a sequence of torus sizes N (e.g. 20x20, 40x40, 60x40), extract T*(g) from Z^{(-1,-1)}/Z^{(1,1)}=e^{-1}, and fit T* vs Delta(g)/ln N across g including g=g_c.
4. **Can the log-2 excess entanglement entropy from a vortex pair (Fig.5, the non-Abelian Majorana zero-mode signature) be reproduced on a finite Kagome/star torus?**
   - *Why:* This is the third independent diagnostic in the paper and directly probes the non-Abelian statistics (Majorana core states). It is qualitatively distinct from the flux/degeneracy counting and would strengthen the replication from 'degeneracy' to 'anyonic content'.
   - *Next:* Build the free-fermion correlation matrix in a two-vortex background, compute the entanglement entropy across a bipartition via the correlation-matrix eigenvalue formula, and track the delta-S vs g toward the ln2 nA-phase value.
5. **Is the residual ~0.03 minimum bulk gap at g=1.725 purely a finite-k-grid artifact, or does the simplified single-unit-cell gauge shift the true critical point away from exactly sqrt3?**
   - *Why:* We locate g_c to 0.4%, but the gap does not fully close on our grid. Distinguishing grid discretization from a genuine model-convention shift determines whether the replication of g_c is exact or approximate.
   - *Next:* Locate the critical BZ momentum analytically (where det h(k;g)=0), then evaluate the gap on a k-grid refined around that point and confirm Delta->0 exactly at g=sqrt3 in the continuum limit.

#### `loop-current-feng2021` — PARTIAL (C6/A6)

1. **Why are our CFP-vs-CBO/vCDW energy splittings (~0.013 t, 0.007 t) ~15x smaller than the paper's (0.195 t, 0.435 t)?**
   - *Why:* The magnitude of the energy gain is what makes CFP a robust ground state rather than a marginal winner; a 15x discrepancy means we reproduce the ordering but not the energetics, so the strength of the claim is only partially validated.
   - *Next:* Re-derive the exact CFP construction including the current-conservation-restoring diagonal/second-neighbor terms the paper adds, and match the chemical-potential normalization at 5/4 filling; recompute splittings and compare.
2. **Why does our vCDW come out slightly below CBO, opposite to the paper's ordering (CBO below vCDW)?**
   - *Why:* The paper's headline states E_CFP is 0.195 t below CBO and 0.435 t below vCDW, implying CBO < vCDW. Our sub-ordering is reversed, indicating our vCDW or CBO amplitude convention differs from theirs.
   - *Next:* Verify the relative normalization of the onsite vCDW modulation (Eq.4) vs the bond CBO modulation (Eq.7); the paper may scale bond vs onsite lambda differently, or fold the M-point degeneracy differently.
3. **Does the CFP occupied-band Chern number equal C=1 per spin (sigma_xy = 2 e^2/h) in our from-scratch supercell?**
   - *Why:* The anomalous Hall / QAH signature is the second half of the paper's claim; energy-ordering alone does not establish the topological character.
   - *Next:* Fold the 2x2 CFP order into a k-space 12x12 Bloch Hamiltonian and apply the Fukui-Hatsugai-Suzuki Chern routine from loop_current_kagome_kernel.py to the occupied bands.
4. **Is the winning phase stable to the exact placement of the 2x2 modulation origin (gauge/phase convention of cos(Q.R))?**
   - *Why:* The bond-midpoint reference we use to evaluate cos(Q.r_ij) is a modeling choice; a different origin could shift the CBO/CFP balance and even the winner near lambda~0.1.
   - *Next:* Sweep the phase origin of each Q-component and confirm the CFP energy (and winner) is invariant, as it must be for a physical order parameter.
5. **How large does lambda need to be for CFP to overtake vCDW, and does a self-consistent U-V Hubbard treatment select lambda~0.3?**
   - *Why:* The paper imposes lambda by hand and defers the microscopic (extended-Hubbard) stabilization to future work; the physical relevance of lambda=0.3 is unestablished within this model.
   - *Next:* Add on-site U and NN V, decouple in the three channels self-consistently, and check whether the CFP saddle-point amplitude lands near lambda=0.3 at 5/4 filling.

#### `loop-current-gerguri2026` — PARTIAL (C5/A7)

1. **Why does the surrogate crossover occur at U~5 (t units) while the paper reports U*=6 eV, and can the mapping eps_f = eps_f0 + kU*U be calibrated to real eV?**
   - *Why:* The headline is a quantitative U>6 eV threshold; a surrogate that only matches the trend qualitatively cannot validate the specific critical correlation strength.
   - *Next:* Wannierize DFT bands to fix t in eV and determine the true eps_f(U) dependence from constrained-RPA or LDA+U eigenvalues.
2. **Is the q=1/2 selection driven by Ru M-point van Hove nesting, by Ce-4f flat-band shifts, or by their interplay?**
   - *Why:* The paper's novelty is the interaction of d-electron and heavy-fermion flat bands; disentangling the driver tests that central claim.
   - *Next:* Decompose chi_q into Ru-only, f-only, and hybridization contributions by selectively zeroing tf and the f-band shift.
3. **Does a self-consistent (rather than Landau-curvature) treatment preserve the U-driven q=1/3 -> q=1/2 crossover, or does first-order competition change the winner?**
   - *Why:* CDW transitions are often first order; the sign of chi_q alone may not predict the true ground state.
   - *Next:* Implement self-consistent mean-field with free-energy comparison at finite order-parameter amplitude for each q.
4. **Why does removing Ce-4f valence states produce a q=1/4 (CO*) winner in the surrogate, matching the paper's f-as-core DFT observation?**
   - *Why:* Reproducing the correct FAILURE mode (q=1/4 CO* when f is core) is strong evidence the surrogate captures the right electronic mechanism.
   - *Next:* Map the surrogate q=1/4 instability to a specific Fermi-surface nesting vector and compare with the DFT f-as-core Fermi surface.
5. **How does the phonon instability in the qz=1/2 plane combine with the electronic CDW susceptibility to select the observed Pmma structure?**
   - *Why:* The paper cites imaginary phonon modes as the structural driver; a purely electronic surrogate cannot rule in/out the lattice channel.
   - *Next:* Compute DFT phonons for the parent P6/mmm cell and correlate soft-mode wavevectors with the electronic chi_q peaks.

#### `loop-current-kumar2015` — PARTIAL (C4/A8)

1. **Does the C=+1 / sigma_xy^s=1/2 chiral band survive in the paper's specific (2pi, pi/2, pi/2) staggered flux assignment rather than the simple uniform-flux parametrization used here?**
   - *Why:* Our uniform-flux kernel reproduces the C=+1 gap for small chirality flux, but the paper's XY limit is a specific staggered flux pattern. Confirming C=+1 for that exact pattern removes the parametrization ambiguity seen at larger phi.
   - *Next:* Extend loop_current_kagome_kernel with the explicit (2pi, pi/2, pi/2) per-triangle flux (tuple flux_pattern) and recompute the Chern number and gap at half filling.
2. **How does the chiral gap and Chern number evolve across the XY-to-Ising crossover (anisotropy lambda) at fixed chirality h?**
   - *Why:* The paper claims the CSL is an XY-regime phenomenon and that in the Ising regime a strong chirality is needed to close the anisotropy gap first. A lambda sweep would test that competition quantitatively.
   - *Next:* Add an XXZ anisotropy term (sublattice-dependent onsite / bond anisotropy) to the mean-field hopping and sweep lambda while monitoring gap closure and Chern jumps.
3. **Is the self-consistent chirality-induced flux (via phi=arctan[(h/J)(1/2-n)]) actually realized, i.e. does a self-consistent mean-field loop determine n^(a) rather than us imposing the flux by hand?**
   - *Why:* We imposed the Peierls flux; the paper derives it self-consistently from the flux-attachment constraint n=theta*B. A self-consistent solution would confirm the flux is spontaneously selected, not assumed.
   - *Next:* Iterate density n^(a) <-> flux phi^(a) to self-consistency at fixed h/J and check the fixed point lands on the (2pi, pi/2, pi/2) state.
4. **Does the additional plateau structure (m=1/3, 2/3, 5/9) appear at finite external field with the same chiral signature?**
   - *Why:* The paper connects the zero-field CSL to the finite-field magnetization plateaus (Jain/Laughlin states). Reproducing sigma_xy^s at those fillings would validate the broader claim beyond h_ext=0.
   - *Next:* Rerun the Chern computation at fillings 1/3 and 2/3 (fillings=(1,) vs partial band fillings) under the appropriate flux and compare sigma_xy^s to 1/2 and 2/3.
5. **How robust is the C=+1 assignment to finite-size / k-grid convergence and to the DM-term variant?**
   - *Why:* FHS Chern numbers can be grid-sensitive near gap-closing points, and the paper also claims a DM-driven CSL. Convergence and a DM cross-check would strengthen the verdict.
   - *Next:* Converge chern_number over nk in {24,42,64,96} and add a DM Peierls-phase channel to test the 'not too strong DM' CSL window.

#### `loop-current-li2023` — PARTIAL (C6/A7)

1. **Does the absolute magnitude of the full-diagonalization free-energy difference converge to the closed-form Eq.(4) once the exact SM patch measure and band-projection normalization are used?**
   - *Why:* Our replication matches Eq.(4) in sign, lambda^2 scaling, and the instability boundary, but not in absolute prefactor. Closing this gap would upgrade the verdict from PARTIAL to fully quantitative and validate the degenerate-perturbation-theory derivation, not just its qualitative structure.
   - *Next:* Reconstruct SM Sec.II-IV: implement the explicit degenerate perturbation theory on E1..E3 with the paper's k-cutoff regularization and 1/A normalization, then compare prefactors term-by-term at fixed |Delta|, lambda, delta_eps.
2. **How robust is the LCBO ground state when the additional band eps3 below vH1 and the full 9-band tight-binding model are included (Fig.5a,b), rather than the 6x6 patch truncation?**
   - *Why:* The paper claims LCBO survives near vH2 with all bands and the cutoff removed. Independent confirmation would rule out that LCBO is an artifact of the two-vHS patch truncation.
   - *Next:* Extend the model to the 9x9 patch (add eps3 block) and then build the full 9-band H_TB(k) from the DFT-fitted hoppings of Ref.[68]; minimize free energy over Delta on a BZ grid and map the LCBO region.
3. **What are the actual DFT-fitted 9-band tight-binding hopping parameters (Ref.[68]) that yield vH1, vH2 with the stated b=0.52, b'=0.96 weights and lambda=0.35 eV*a?**
   - *Why:* The quantitative application to AV3Sb5 (Fig.3, Fig.4 parameters) depends on these; without them the material-specific phase diagram cannot be independently regenerated, only the effective-model mechanism.
   - *Next:* Obtain/fit the 9-band Wannier model to the DFT bands (or retrieve Ref.[68] supplementary tables), verify the vHS energies and mirror eigenvalues, and derive b, b', lambda from wavefunction overlaps.
4. **Is the LCBO state genuinely inaccessible to a Ginzburg-Landau expansion of Delta at all finite orders, as the paper asserts?**
   - *Why:* This is a strong non-perturbative claim distinguishing this mechanism from conventional GL-based CDW selection. If false, the mechanism could be captured by simpler order-parameter theory.
   - *Next:* Expand f(Delta) computed here in powers of |Delta| and the phase arg(Delta), fit GL coefficients up to 6th order, and test whether the LCBO minimum at pi/3 can ever be produced by any truncation.
5. **How does finite temperature and the position of mu between eps1 and eps2 shape the CBO+/CBO-/LCBO phase boundaries (full Fig.4a phase diagram)?**
   - *Why:* We fixed mu=eps2 and T=90K and self-consistently chose |Delta|; reproducing the full (V, mu) phase diagram would test the mechanism's parameter sensitivity and the claim that LCBO is 'more pronounced near vH2'.
   - *Next:* Add a self-consistent gap equation dF/dDelta=0 solver, sweep (V, mu) on a grid at T=90K, classify each minimum (PM/CBO+/CBO-/LCBO), and compare the boundary shapes to Fig.4a.

#### `loop-current-nakazawa2024` — PARTIAL (C5/A6)

1. **Why is R qualitatively insensitive to eta in the paper, while our open-flake itinerant-Lz model shows R decreasing strongly with eta?**
   - *Why:* The eta-insensitivity is the paper's key surprise (it defeats the naive R ~ pi*xi_J^2 picture and is the evidence for a nonlocal itinerant origin). Failing to reproduce it means our model is missing the nonlocal channel that dominates the paper's supercell BZ calculation.
   - *Next:* Move from an open real-space flake to the paper's periodic 12-site 2x2 supercell with a folded-BZ k-mesh (>=64x64) and the full k-space bulk+edge M_orb formula (Eq. 4), which retains the long-range circulation the finite flake truncates.
2. **Does the clean-limit M_orb ~ eta^3 scaling emerge only with the correct third-nearest t' and precise VHS filling n=2.55, mu=0?**
   - *Why:* We got an exponent ~0.3, not 3. The eta^3 law is a symmetry statement (b100=b010=b001=0 by momentum conservation) that only holds with the exact triple-Q pattern and filling; getting it wrong signals the cLC bond-sign pattern or filling is not faithful.
   - *Next:* Explicitly build the paper's Fig-2 triple-Q sign pattern on the 12-site cell (geometric up/down-triangle discrimination) and pin filling by a finite-T Fermi function at T=0.01 eV, mu=0, then refit log M0 vs log eta.
3. **How much does the two-impurity (Imp1 triangular vs Imp2 hexagonal) averaging change R, and is the 50%-per-1% number an average or an Imp1-only value?**
   - *Why:* The paper says a random impurity is 50/50 Imp1/Imp2; our averaged R and per-site R differ substantially (e.g. size scan shows sign flips). The headline number's definition affects the pass/fail threshold.
   - *Next:* Report R separately for Imp1 and Imp2 across sizes and take the paper's stated 50/50 average; verify against Fig. 5(c) values at n_eff=2.48,2.52,2.56.
4. **Is linear extrapolation from a single impurity (nimp = 1/N) to 1% valid, or does R saturate/curve at finite density?**
   - *Why:* We rescale single-impurity R by 0.01/nimp assuming dM ~ nimp linearity. The paper itself linearly extrapolates 0->0.33%->1%, but if multi-impurity interference matters the extrapolation over/under-states R.
   - *Next:* Place 2-3 impurities in a larger supercell (N~300) and check whether the total suppression is additive (linear) before trusting the 1% number.
5. **Does including the b2g (mixed-type) orbital sector, neglected here and in the paper, change R materially?**
   - *Why:* The paper explicitly defers b2g and notes it is 'qualitatively important for understanding large M_orb'. R could be quantitatively different in the real material.
   - *Next:* Add the b2g orbital manifold as a second kagome layer with its own t,t' and inter-orbital coupling; recompute M_orb and R (a genuine extension beyond both this replication and the paper).

#### `loop-current-tazai2023` — PARTIAL (C7/A5)

1. **Why does our band-theory M_orb(eta) scale as ~eta^1.3 rather than the paper's clean eta^3 for the current-only 3Q state?**
   - *Why:* The eta^3 law is the paper's proof that M_orb arises purely from the fully-symmetric b111 anharmonic invariant (q1+q2+q3=0). A slope near 1 suggests a spurious lower-order contribution is leaking in (e.g. residual net flux from an imperfect 1Q/2Q cancellation in our form factors, or coarse-grid k-noise) rather than the genuine trilinear term.
   - *Next:* Refine on a denser (>=48x48) mesh AND verify the exact TYK form factors f_ij (signs on sites 1,2,4,5 vs 7,8,10,11) so that 1Q/2Q M_orb vanish to machine precision; re-fit the slope over a wider, better-resolved eta range.
2. **Why does the coexisting 3Q bond order SUPPRESS M_orb (x0.5) in our calculation instead of strongly ENHANCING it (linear, GL coefficient m1) as in TYK Fig. 2(d)?**
   - *Why:* The m1*phi*eta trilinear enhancement is the paper's central novelty and the origin of the -3 m1 hz eta.phi field coupling; getting the sign/magnitude of m1 wrong undermines the quantitative field-switching story.
   - *Next:* Implement the exact even-parity bond form factors g_ij from Fig. 1(a) (star-of-David pattern) with correct relative phase to the current form factors, evaluate at n=2.47 (the paper's value for Fig 2d, not 2.55), and extract m1 by fitting M_orb = m1 phi eta + m2 eta^3.
3. **Is the single-orbital effective model sufficient, or do the GL coefficients m_n require the realistic multi-orbital (dXZ,dYZ,dX2-Y2,d3Z2) first-principles kagome model?**
   - *Why:* TYK compute m_n from realistic multiorbital models and note m_n is large only when FS reconstruction happens near the vHS points; the single-b3g-orbital toy may systematically under- or mis-estimate the magnitudes that make ~1 T sufficient.
   - *Next:* Extend the kernel to a multi-orbital vHS-nested FS or, minimally, sweep filling across 2.47-2.63 to confirm the vHS resonance enhancement of M_orb reported in Fig. 2(a) before trusting absolute magnitudes.
4. **What is the actual domain-wall / condensation energy scale that h_z must overcome, so we can quantitatively confirm '~1 T is enough' rather than only matching the paper's dimensionless h_z=1e-4?**
   - *Why:* Our C4 check confirms the -3 hz M_orb coupling form and the 1e-4<->1T identification, but 'a tiny field switches the domain' is only physically demonstrated if the field energy gain exceeds the current-order domain pinning/anisotropy energy.
   - *Next:* Compute the free-energy difference between + and - chirality domains as a function of hz and locate the switching field where dF_switch equals a realistic domain-pinning barrier; compare that field (in Tesla) to the ~1 T claim.
5. **How sensitive is M_orb to the modern-theory formula variant (TYK Eq. 3 finite-T vs Eq. 6 T=0 interband) and to the mu-dependent (e_a+e_b-2mu) weighting on a coarse mesh?**
   - *Why:* M_orb here is ~1e-4 and the odd-in-eta residual is ~1e-4 (same order), i.e. numerical noise is comparable to signal; the choice of formula and chemical-potential accuracy could flip conclusions about small quantitative claims.
   - *Next:* Cross-check M_orb from Eq. 6 against a direct finite-T Eq. 3 evaluation and against a Berry-curvature circular-integral method; converge mu to <1e-6 and quantify the mesh-convergence error bar on M_orb.

#### `loop-current-tazai2025` — PARTIAL (C7/A6)

1. **Does chiral d-wave truly overtake s-wave as the global leading SC instability under pure LC at eta=0.014, or only within a restricted low-T / small-g window?**
   - *Why:* The paper's central claim is that LC order makes chiral d-wave THE instability. Our minimal kernel keeps lam_s > lam_d, so the crossover is not fully reproduced; this is the make-or-break physics.
   - *Next:* Implement the exact LC/BO form factors f_ij, g_ij on the 12-site cell (paper Fig.1b,c) and enforce the sublattice-interference hierarchy Gamma_mm >> |Gamma_ml|; rescan lam_d vs lam_s vs T,g.
2. **What is the precise real-space chiral pattern Delta_mu, and does the mu-dependence produce the ~5% 2x2 PDW component reported?**
   - *Why:* The PDW component (~5%) is a key experimentally-comparable prediction distinguishing chiral d-wave from plain s-wave in kagome SC.
   - *Next:* Resolve the full 12-component eigenvector on a fine k-mesh, decompose into uniform + 2x2 (M-point) Fourier components, and quantify the PDW fraction.
3. **How sensitive is the eta=0.014 resonant peak in lam_d to the chemical potential / filling n=11 and the shallow LC-induced Fermi pocket?**
   - *Why:* The paper attributes the enhancement to a shallow high-DOS Fermi pocket formed by LC-induced vHS hybridization at Gamma; if the peak is filling-fragile the mechanism claim weakens.
   - *Next:* Sweep filling n in [10.5,11.5] and track the DOS at mu and the lam_d peak location vs eta; verify the pocket forms at Gamma.
4. **Is the winding number w=2 of the chiral d-wave gap on each Fermi pocket reproducible from the computed Delta_k?**
   - *Why:* Winding number is the topological fingerprint of the chiral d-wave state (Fig.2d); it determines edge modes and the thermal/SC-diode Hall responses the paper highlights.
   - *Next:* Construct Delta_k = sum_m w_km Delta_m on the Fermi surface, form n=(Re,Im,mu-eps)/|.|, and compute w = (1/4pi) integral of the skyrmion density.
5. **How does adding finite BO (phi != 0) alter the balance, producing the nematic chiral SC (mixed s + chiral-d) state the paper predicts?**
   - *Why:* The full paper prediction is a nematic chiral SC in the coexisting LC+BO phase; the pure-LC case is the base limit. Confirming the BO-driven nematic mixing tests the broader mechanism.
   - *Next:* Turn on phi with the staggered g_ij form factor out-of-phase with f_ij (C6-breaking), and track the s/chiral-d admixture and nematic director vs phi.

#### `loop-current-xie2025` — REPLICATED (C7/A10)

1. **What sets the magnitude of the NV-detectable stray field and the resulting T1 relaxation time (Eqs. 13-15), which we did not attempt?**
   - *Why:* The whole experimental proposal hinges on whether the phason-driven dynamic flux produces magnetic noise above the NV sensitivity floor; the theory paper gives only a qualitative Fermi-golden-rule estimate.
   - *Next:* Compute delta-Phi from the excited A1 phason amplitude, propagate the Biot-Savart stray field to a realistic NV standoff (10-100 nm), and evaluate S_B(omega0) and T1 for AV3Sb5 loop-current magnitudes from DFT/experiment.
2. **How does the mode-mixing signature evolve at finite q (dispersion), beyond the q=0 M-point result we reproduced?**
   - *Why:* Real spectroscopy (IXS, Raman, pump-probe) probes finite-q; the kappa1 q^2 gradient terms shift the mixed-mode dispersions and could change the mode ordering shown schematically in Fig. 3(b).
   - *Next:* Diagonalize the full q-dependent Eq.(10) matrix over the folded BZ using a fitted kappa1, and map the avoided-crossing / mixing strength as a function of q.
3. **Does the mode mixing survive coupling to itinerant electrons (Landau damping) near the Van Hove filling?**
   - *Why:* The paper's modes are from a phenomenological Lagrangian; at the VHS the CDW couples strongly to particle-hole continua, which can damp/broaden the Higgs and shift the phason gap.
   - *Next:* Compute the electronic polarization bubble Pi(q,omega) at 5/12 filling on the kagome lattice and dress the fluctuation propagator (RPA) to check whether the A-channel mixing peak remains a sharp resonance.
4. **How robust is the iCDW-vs-rCDW selection (sign of b) to the third-order lambda3 term we set to zero (following ref. 13)?**
   - *Why:* The lambda3 cos(theta1)cos(theta2)cos(theta3) term, dropped by convention, can compete with lambda2 and alter the phase selection and hence whether sin(3 theta0) is nonzero.
   - *Next:* Reintroduce lambda3 and re-minimize F over the full (theta1,theta2,theta3) space (no C3 assumption) to map the phase boundary and confirm iCDW stability window.
5. **Can the microscopic kernel be made self-consistent so the loop-current order emerges spontaneously rather than as a linear response to an imposed flux?**
   - *Why:* Our cross-check imposes an external Peierls flux; a genuine iCDW requires the loop current to be self-generated by interactions, tying the phenomenological |Delta_Q| to a microscopic order parameter.
   - *Next:* Add a mean-field imaginary bond order decoupling (V * <i c_i^dag c_j>) to the kagome kernel and iterate to self-consistency at VHS filling to obtain a spontaneous loop-current solution.

#### `loop-current-yang2022` — PARTIAL (C5/A9)

1. **Does the full 2x2-folded (12-band-per-spin) chiral flux band structure reproduce the same total Chern numbers and edge-mode counts as the single-M closed-form kernel used here?**
   - *Why:* The paper's Table 1 and Fig. 3 edge spectra are computed in the extended 2x2 unit cell; the single-cell kernel confirms |C|=1 and the TRS-breaking gap but cannot directly render the folded bands or the zero-energy edge modes that physically manifest the Chern number.
   - *Next:* Build the 3Q-iCDW Hamiltonian in a real-space 2x2x(open-y) kagome supercell with per-bond Peierls phases matching Fig. 2, diagonalize, and count chiral edge modes per spin for all 4 cases.
2. **Do the LG quartic coefficients u1 ~= (0.003/tT^2) log(t Lambda^2/T) and u2 ~= 0.006/(tT^2) with u1 >> u2 actually select the 3Q-iCDW over 1Q/2Q as claimed?**
   - *Why:* The paper's assertion that 3Q order minimizes the free energy rests on the sign and hierarchy of u1, u2 from integrating out the patch fermions; this is the quantitative backbone of the whole classification but was not recomputed here.
   - *Next:* Evaluate the one-loop particle-hole bubbles at the three vHS patches numerically, extract u1(T), u2(T), and verify u1 > u2 > 0 across the low-T regime T << t Lambda^2.
3. **How does each of the 4 iCDW patterns select its partner superconducting order parameter through the u4 CDW&SC coupling (Fig. 4)?**
   - *Why:* The paper's headline application is inferring the SC order from the identified orbital-current order (and vice versa); the topological classification is only half the story.
   - *Next:* Derive the bilinear iCDW-SC coupling term in the LG functional and enumerate which singlet SC channel (s, d+-id, etc.) is favored for each of cases (i)-(iv).
4. **Is the sign of C_down at the balanced (2-of-3, e.g. (-i,i,i)) configuration robustly resolvable by a gauge-fixed numerical Chern calculation rather than by symmetry alone?**
   - *Why:* Our direct FHS index was ambiguous at the gapless balanced staggered config, forcing reliance on Eq. (4); an independent numerical sign would upgrade the agreement from symmetry-derived to fully numerical.
   - *Next:* Add a small symmetry-allowed gap-opening perturbation (or use the extended cell) so the balanced configs are gapped, then compute the FHS Chern sign directly and compare to the symmetry prediction.
5. **How stable is the classification against deviations from equal iCDW amplitudes |Phi_1|=|Phi_2|=|Phi_3| and from mu=0?**
   - *Why:* Real AV3Sb5 need not sit exactly at the vHS filling or have perfectly equal 3Q amplitudes; the topological labels could change if bands cross the Fermi level.
   - *Next:* Sweep unequal amplitudes and mu in the tight-binding model, tracking gap closings and Chern-number jumps to map the stability region of each pattern.

---
