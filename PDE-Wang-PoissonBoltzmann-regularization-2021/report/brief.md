# Brief

**Paper:** Siwen Wang, Emil Alexov, Shan Zhao (2021), "On regularization of charge
singularities in solving the Poisson-Boltzmann equation with a smooth solute-solvent
boundary", *Mathematical Biosciences and Engineering* 18(2):1370–1405.
DOI:10.3934/mbe.2021072. Open access (AIMS Press, CC-BY).

**What:** The paper introduces the first *regularization* scheme for charge
singularities in the **diffuse-interface** (smooth dielectric) Poisson-Boltzmann (PB)
model. Its "dual decomposition" splits the potential `u = u_C + u_RF` (Coulomb +
reaction field) AND the dielectric `ε = ε_i + ε̂` (constant base + space-varying part).
The singular Coulomb part is captured analytically as a Green's function with the
*constant* base dielectric `ε_i`; the reaction-field part then satisfies a
**regularized (linearized) PB equation with a smooth source** `∇ε·∇G` (Eq. 2.16),
which is solved by 2nd-order central finite differences + a biconjugate-gradient solver.
A Gaussian-Convolution-Surface (GCS, FFT-based) generates the diffuse interface for
real molecules. It is compared against the traditional trilinear point-charge method.

**Why replicate:** The headline correctness claim is a clean, fully-specified,
*analytic* test — the one-atom system (§4.1, Table 1) with the analytic `tanh`-like
diffuse interface — where the regularization free energy converges to a grid-independent
limit (≈ −65.66 kcal/mol for the 1-charge case) while the trilinear method does not.
This is an ideal independent numerical-PDE replication: no proprietary data, a
self-contained boundary-value problem with a known convergent answer, plus a
`σ→0` sharp-interface analytic check (SAS Born energy = −46.8447 kcal/mol).

**Result (this replication):** Implemented the regularized LPB solver from scratch
(Python/NumPy/SciPy, `scipy.sparse` + BiCGSTAB) exactly per Eqs. (2.16)–(2.19),
(2.4), (2.6), (2.13), (4.1). Reproduced Table 1's regularization free-energy column
to within ~0.1–0.5 kcal/mol across all mesh sizes N=11…401 (limit ≈ −65.66 kcal/mol),
reproduced the two-charge column (limit ≈ −303.8 kcal/mol), reproduced the trilinear
column's non-convergent behavior, and independently confirmed the analytic Born/SAS
limit −46.8447 kcal/mol. **Verdict: REPLICATED** (core analytic claim independently
reproduced from first principles).
