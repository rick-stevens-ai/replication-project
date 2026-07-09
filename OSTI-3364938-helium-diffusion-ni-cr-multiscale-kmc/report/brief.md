# Brief — OSTI-3364938

Wang, Yu, Wang & Zhang (INL/U. Wisconsin, 2026, JNM 156551) combine
DFT (VASP-PAW-PBE) with atomic Kinetic Monte Carlo (residence-time
algorithm) to study He interstitial diffusion in Ni–Cr alloys at 600–1000 K.
They report a **non-monotonic** dependence of He diffusivity on Cr
concentration (0–12 at%): D drops from 5.52×10⁻⁵ cm²/s at 0 at% Cr to a
minimum ~6×10⁻⁶ cm²/s at 5 at% Cr, then **rises back to 1.67×10⁻⁵ cm²/s
at 12 at% Cr**, overturning the conventional wisdom that adding Cr
monotonically slows He. The mechanism is a competition between isolated
3NN-T "trapping" sites and 1NN energy basins that **percolate into
channels at high Cr**, becoming fast-diffusion pathways. This
independent replication (a) implements both compared analytical models
(simplified-McNabb-Foster, modified-Oriani) with the paper's DFT
inputs, (b) builds a KMC lattice simulator using the residence-time
algorithm and the paper's DFT-NEB barriers, and (c) reproduces the
paper's non-monotonic D(c_Cr) trend and the ~7/8 correlation factor limit.
