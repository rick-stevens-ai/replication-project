# Brief

Gao et al. (Sandia, ACM TODAES vol 31, art 76, March 2026, DOI 10.1145/3766551, SAND2026-19093J,
OSTI 3024853) present a Charon(TCAD) + Dakota(UQ) + random-forest surrogate + DRAM–Bayesian
calibration pipeline that fits the Kimpton hole-trap TID model to threshold-voltage shifts
measured in a 3.3 kV COTS SiC power MOSFET (GeneSiC) irradiated at three Sandia facilities
(IBL 100-keV electron gun, ACRR pulsed gamma reactor, LMTF-LINAC 20–30 MeV electron beam),
then reduces the calibrated TCAD to a 3-parameter sigmoid compact model
ΔV_th(d) = A/(1+exp(-B(d-C))) suitable for circuit-level UQ.

This replication is a **SPOT-CHECK**: full re-execution requires (i) Sandia's internal
experimental dataset SAND2023-00940 (not published), (ii) proprietary GeneSiC device
geometry/doping from SEM, and (iii) ~2.2 M CPU-hours of Charon TCAD simulations on Sandia's
1496-node HPC cluster. Charon and Dakota are open source but their input decks for this study
are not released. We verify (a) that Charon (github.com/tcadsoftware/charon) and Dakota
(dakota.sandia.gov) are indeed public, (b) the sigmoid compact-model math and the paper's
reported MAP parameters Φ_opt={A=−0.92 V, B=3.58, C=0.8} produce curves consistent with the
paper's Figure 15 LINAC prediction (saturation near −0.9 V, transition near d≈0.8, matching
the 5th/95th percentile shape), and (c) reimplement the paper's Bayesian inverse-problem
formulation (Eqs. 6–8) on a synthetic dataset drawn from the paper's own Kimpton equations
(Eqs. 3–5) with the reported LINAC MAP parameters, to confirm the method is mathematically
self-consistent and would recover the reported parameter ranges.
