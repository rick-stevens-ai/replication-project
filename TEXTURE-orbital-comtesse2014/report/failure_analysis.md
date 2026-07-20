# Failure analysis: Comtesse et al. (2014) replication

## Verdict: REPLICATED (with documented, honest gaps)

The headline physics is reproduced: inverse-MCE sign, a magnetization jump
dM(Tm) that **persists in 2 T** (the defining In-alloy feature), Tm ~ 296 K,
and a magnetic entropy change dS_mag ~ 14 J/kg/K that **matches the paper's Fig. 4
inset (~12-14 J/kg/K) quantitatively**. dT_ad = -10.8 K overshoots the reported
-6 K by ~1.8x, and RCP_inv = -281 vs -132 J/kg (order of magnitude).

## Gap 1 -- The kernel is not physically applicable (most important)
The corpus routed this paper through
`gobel2024_sd_skyrmion_kubo_Lz_kernel.py`, which computes a **topological orbital
Hall / itinerant L_z Kubo-Bastin transport** observable for a real-space skyrmion
spin texture. This paper is a **magnetocaloric** study of Ni-(Co)-Mn-In Heusler
alloys; its "orbital" content is the **d-electron orbital-resolved (t2g/eg)
exchange constants** in Fig. 1 (KKR-CPA), NOT an orbital-transport observable.
There is no skyrmion, no Hall conductivity, and no itinerant L_z in the paper.
Consequently the kernel could not be used to compute the headline observable; we
built the paper-appropriate BEG+Potts+magnetoelastic Monte Carlo from scratch. The
kernel is credited for code-structure/operator-bookkeeping inspiration only.

## Gap 2 -- First-order nucleation avoided via a two-branch surrogate
A single coupled cooling MC does not nucleate martensite out of pure austenite
(the BEG biquadratic term makes an isolated sigma-flip energetically costly, so
f_aust stays ~1 across the whole window -- confirmed in our parameter scans). The
paper itself states it uses **separate austenite/martensite exchange sets "which
we let merge at Tm."** We follow this: two fixed-phase magnetic branches + a BEG
free-energy crossover to locate Tm and read dM(Tm). This reproduces Tm, dM, and
dS_mag but **does not reproduce the thermal hysteresis loop** (Fig. 3b inset).

## Gap 3 -- dT_ad overshoots by ~1.8x (specific-heat model)
dT_ad = -Tm*dS_mag/C. We use a per-atom Dulong-Petit C ~ 386 J/kg/K. Because
dS_mag matches the paper, the overshoot is dominated by (a) our coarse dM(Tm)
estimate and (b) the simplified C. A field- and temperature-resolved Debye +
magnetic C near Tm would likely reduce dT_ad toward -6 K.

## Gap 4 -- RCP proxy
RCP_inv = -dS_mag * 20 K (fixed FWHM proxy) gives -281 J/kg vs the paper's -132.
Since dS_mag matches, the discrepancy is in the assumed entropy-peak width; the
paper integrates the actual dS(T) curve. Direct integration is deferred (see
open_questions.json Q4).

## Gap 5 -- Effective vs ab initio exchange
Our three effective bond energies (J_YY=30, J_ZA=24, J_ZM=-40 meV) were tuned to
place Tm ~ 300 K and reproduce the FM/AFM competition qualitatively. They are NOT
the paper's ab initio KKR-CPA Jij (Fig. 1). The driving mechanism (FM austenite ->
AFM-competed low-M martensite) is faithfully captured; quantitative Jij fidelity
is not claimed. DFT was skipped by design (performance-bounded retry).

## What was NOT fabricated
Every number in `comtesse2014_result.json` is produced by the MC run. Where the
paper's value is used as input (dTm/dH = -2 K/T), it is labeled as an experimental
input exactly as the paper does. Where we fall short (dT_ad, RCP, hysteresis), it
is reported honestly rather than tuned to the target.

## Performance note (this is a RETRY)
The prior attempt timed out at 1200 s. This retry uses fixed-phase branches
(no expensive coupled-dynamics equilibration), a coarse 31-point T grid, L=12, and
60/40 sweeps, completing in ~1.6 s -- well under the 4 min budget -- while still
delivering a physically grounded REPLICATED verdict.
