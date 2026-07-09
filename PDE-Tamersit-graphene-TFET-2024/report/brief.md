# Brief — Tamersit et al. 2024 (JLGNR TFET multi-gas nanosensor)

**Paper.** Tamersit, K.; Kouzou, A.; Rodriguez, J.; Abdelrahem, M. *Electrostatically Doped Junctionless Graphene Nanoribbon Tunnel Field-Effect Transistor for High-Performance Gas Sensing Applications: Leveraging Doping Gates for Multi-Gas Detection.* Nanomaterials **14**, 220 (2024). DOI: 10.3390/nano14020220 (OA CC-BY, MDPI; PMC10821285).

**What.** The authors propose a junctionless armchair-graphene-nanoribbon tunnel FET (N=13 dimer, W=1.47 nm, E_g=0.86 eV) with two electrostatic doping gates (which double as gas-sensing gates) and a bottom control gate. They compute I_DS-V_GS transfer characteristics with a self-consistent mode-space NEGF + 2D Poisson solver (ballistic, T=300 K, HfO2 t_ox=1.5 nm, V_DS=0.4 V, V_SG=-0.7 V, V_DG=+1 V) and report an ambipolar transfer with a subthermionic subthreshold swing ≈7 mV/dec and gas-sensitivity of 10^3–10^6 in the steep-slope regime under ΔΦ = ±0.05 eV.

**Why.** MDPI paper, cited 13×, code is described as a homebrew MATLAB simulator (data available "on reasonable request", not published). Real replication requires re-implementing (or invoking) mode-space NEGF for an A-GNR under electrostatic doping and comparing at least the baseline transfer characteristic (SS, ambipolarity, ON/OFF ratio) against Figure 3b.
