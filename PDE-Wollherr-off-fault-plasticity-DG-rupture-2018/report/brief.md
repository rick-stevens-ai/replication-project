# Brief

Wollherr, Gabriel & Uphoff (2018, GJI, doi:10.1093/gji/ggy213) present the
first implementation of off-fault non-associated Drucker–Prager
visco-plasticity inside the ADER-DG SeisSol solver, in two flavours —
sub-elemental integration points (IP) and nodal basis (NB) — and verify it on
SCEC dynamic-rupture benchmarks TPV12/TPV13. This replication (i) locates the
public reference implementation in the SeisSol master branch (coauthored by
Wollherr and Uphoff themselves), (ii) confirms both IP and NB matrix sets
(orders 2–8) are shipped with the code, (iii) re-derives the Drucker–Prager
return-mapping kernel from scratch in NumPy and verifies its four core
mathematical properties (elastic pass-through, exact radial return, exact
first-order-in-dt viscoplastic relaxation, and 500/500 admissibility on random
trial states), and (iv) reproduces the TPV13 initial-stress and yield-surface
values at five depths on the exact material parameters shipped in the
`SeisSol/Examples` `tpv12_13` package. Full 3-D SeisSol rupture runs (the
paper's actual figures) were not attempted — that requires an MPI build of
SeisSol plus a meshed h5 file — so the LLM judge (Argo gpt-5.2) issued a
**SPOT-CHECK** verdict (coverage ≈ 20%, agreement=none): mathematical
machinery + code availability + benchmark inputs all verified, end-to-end
wavefield rerun deferred.
