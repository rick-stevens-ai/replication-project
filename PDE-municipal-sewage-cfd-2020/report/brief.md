# Brief — Esemu et al. 2020 (PDE-municipal-sewage-cfd-2020)

Independent replication of Esemu, Masanja, Nampala, Lwanyaga, Awichi & Semwogerere (2020),
"An Application of Computational Fluid Dynamics to Optimize Municipal Sewage Networks; A
Case of Tororo Municipality, Eastern Uganda," *Journal of Advances in Mathematics* 18, 18–29,
doi:10.24297/jam.v18i.8345. The paper couples (a) an analytical set of minimum-slope /
pipe-diameter design rules (Manning-equation self-cleansing, Table 1) with (b) an OpenFOAM
`interFoam` two-phase (water/air) VOF + k-ε simulation of a 20 m × 0.5 m 2-D pipe. This
replication verifies claim (a) by back-solving Manning's `n` from Table 1 (recovers
n ≈ 0.0129 ± 0.0009, i.e. standard concrete-sewer roughness — clean C1-REPLICATED), and
verifies (b) by actually running interFoam v1906 on uicgpu with the paper's geometry and
turbulence model. The CFD reproduces the paper's qualitative Fig. 9 flow-development
behaviour (entrance overshoot then relaxation) at real-CFD cost. Note: the wave-brief
metadata labelled this DOI as "Al Manazlah, Saudi Arabia"; the DOI actually resolves to the
Tororo (Uganda) paper — Crossref confirmed. Replication proceeded against the true paper.
