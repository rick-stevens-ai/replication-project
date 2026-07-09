# Brief — Ma, Xu, Zhang (2020) mPNP with Coulomb and hard-sphere correlations

Ma, Xu & Zhang (SIAM J. Appl. Math. 2020, DOI 10.1137/19M1310098) develop a
modified Poisson–Nernst–Planck (mPNP) model that adds two energetic
corrections to classical PNP: (i) a long-range Coulomb correlation
represented by a generalized Debye–Hückel Green's-function equation solved
under a WKB approximation, and (ii) short-range hard-sphere correlations
represented by the Modified Fundamental Measure Theory (MFMT). We
independently re-derived the MFMT weighted-density integrals in 1D, verified
the paper's claimed **second-order finite-difference convergence** of the
hard-sphere chemical potential (Fig. 4.1), and solved the steady-state
modified Poisson–Boltzmann problem in the two-plate geometry via Newton's
method for the **MF and SC models**. The SC (hard-sphere-only) cation density
peak at the negative electrode is 18.7% larger than the pure mean-field peak
(2.094 vs 1.765) and the SC total diffuse charge is larger than the MF
diffuse charge (0.230 vs 0.224), quantitatively consistent with the paper's
Fig. 4.5 qualitative claims. LLM-judge verdict (Argo Sonnet 4.6):
**REPLICATED**.  Duplicate-work notice: an earlier and more complete
independent replication of the same paper exists at
`~/Dropbox/REPLICATE-PROJECT/PDE-replications/modified-pnp/` (Ollie,
2026-05-28, MF/SC/LC/LS all implemented).  This work independently agrees
on the MFMT + MF + SC subset. The full LC/LS models (which require the WKB Coulomb
self-energy integral, Eq. 3.22) were not implemented in this replication;
those are out of scope but consistent with what the paper published.
