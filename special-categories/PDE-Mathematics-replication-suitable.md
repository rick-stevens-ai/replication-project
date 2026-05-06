# Replication Corpus — PDE / Mathematical Physics (v4 strict)

*Top 100 papers solving novel scientific problems (v4: drops tool/database/method-announcement papers)*

Generated 2026-05-05 from `~/Dropbox/PIPELINE/PDE/papers/`.

## v4 Filter (over v3)

Drop a paper if any of:
1. publication type is Book / Review / Editorial / etc.
2. year < 2000
3. referenceCount > 200
4. abstract missing or < 200 chars
5. title matches textbook patterns
6. title matches system/tool patterns (X Server, Toolkit, Pipeline, etc.)
7. title matches database-intro patterns
8. **NEW v4: title contains tool keywords ("annotation tool", "genome browser", "R package", etc.)**
9. **NEW v4: title is `<short_name>: <tool descriptor>` (e.g., "eggNOG: orthology annotation tool")**
10. **abstract reads like a tool/method-announcement paper ("we developed X, a [tool/method]", "available at https", "open-source", etc.)**
11. abstract lacks problem-solving language AND lacks workflow hints

## Filter Summary

- **Input:** 8638 papers
- **Output:** 100 replication-tractable
- **Removed:** 8087

Top skip reasons:

- `no-problem/workflow-language` × 5161
- `no-abstract` × 1590
- `abstract:system-paper-v4` × 237
- `type:Review` × 235
- `type:JournalArticle,Review` × 79
- `year:1998<2000` × 61
- `year:1999<2000` × 51
- `year:1997<2000` × 49
- `year:1996<2000` × 39
- `year:1995<2000` × 30
- `year:1993<2000` × 30
- `year:1994<2000` × 28
- `year:1992<2000` × 26
- `title:system/tool` × 25
- `year:1990<2000` × 24

## Stats on Filtered Top-100

- Total citations: 6,547
- Mean citations: 65
- Year range: 2001 – 2023

## Top 100 Replication-Suitable Papers

| # | Cites | Year | Title | Authors | Venue | PMID/DOI |
|---|---:|---|---|---|---|---|
| 1 | 243 | 2013 | Coexistence of synchrony and incoherence in oscillatory media under nonlinear gl | L. Schmidt; Konrad Schönleber + 2 | Chaos | PMID:24697364 |
| 2 | 190 | 2007 | Asymptotic behavior of smooth solutions for partially dissipative hyperbolic sys | S. Bianchini; B. Hanouzet + 1 | ? | DOI:10.1002/CPA.20195 |
| 3 | 189 | 2002 | Wannier functions analysis of the nonlinear Schrödinger equation with a periodic | G. Alfimov; P. Kevrekidis + 2 | Physical review. E, Statistica | PMID:12443350 |
| 4 | 171 | 2022 | Data-driven modeling and prediction of non-linearizable dynamics via spectral su | Mattia Cenedese; Joar Axås + 3 | Nature Communications | PMID:35169152 |
| 5 | 148 | 2010 | The noisy edge of traveling waves | O. Hallatschek | Proceedings of the National Ac | PMID:21187435 |
| 6 | 144 | 2020 | Population modeling of tumor growth curves and the reduced Gompertz model improv | C. Vaghi; A. Rodallec + 3 | PLoS Comput. Biol. | PMID:32097421 |
| 7 | 143 | 2007 | Nonlinear mean field Fokker-Planck equations. Application to the chemotaxis of b | P. Chavanis | ? | DOI:10.1140/epjb/e2008-00142-9 |
| 8 | 133 | 2017 | Large-Scale Description of Interacting One-Dimensional Bose Gases: Generalized H | B. Doyon; J. Dubail + 2 | Physical Review Letters | PMID:29219524 |
| 9 | 131 | 2014 | Stochasticity, periodicity and localized light structures in partially mode-lock | D. Churkin; S. Sugavanam + 3 | Nature Communications | PMID:25947951 |
| 10 | 123 | 2010 | KAM for the Quantum Harmonic Oscillator | B. Grébert; Laurent Thomann | ? | DOI:10.1007/s00220-011-1327-5 |
| 11 | 122 | 2017 | Polynomial Approximation of High-Dimensional Hamilton-Jacobi-Bellman Equations a | D. Kalise; K. Kunisch | SIAM Journal on Scientific Com | DOI:10.1137/17M1116635 |
| 12 | 116 | 2013 | Green-Hyperbolic Operators on Globally Hyperbolic Spacetimes | Christian Bär | ? | DOI:10.1007/s00220-014-2097-7 |
| 13 | 112 | 2017 | A nonlinear, three-dimensional model for ocean flows, motivated by some observat | A. Constantin; R. Johnson | ? | DOI:10.1063/1.4984001 |
| 14 | 111 | 2023 | The emergence of clusters in self-attention dynamics | Borjan Geshkovski; Cyril Letrouit + 2 | Neural Information Processing  | DOI:10.48550/arXiv.2305.05465 |
| 15 | 107 | 2020 | Nonlinear delay differential equations and their application to modeling biologi | David S. Glass; Xiaofan Jin + 1 | Nature Communications | PMID:33741909 |
| 16 | 107 | 2003 | Cracking chaos-based encryption systems ruled by nonlinear time delay differenti | V. Udaltsov; V. Udaltsov + 3 | ? | DOI:10.1016/S0375-9601(02)01776-0 |
| 17 | 96 | 2008 | Single mode heat rectifier: controlling energy flow between electronic conductor | D. Segal | Physical Review Letters | PMID:18352208 |
| 18 | 94 | 2018 | Anisotropic stars as ultracompact objects in general relativity | G. Raposo; P. Pani + 3 | Physical Review D | DOI:10.1103/PhysRevD.99.104072 |
| 19 | 89 | 2011 | Discreteness of Transmission Eigenvalues via Upper Triangular Compact Operators | J. Sylvester | SIAM Journal on Mathematical A | DOI:10.1137/110836420 |
| 20 | 87 | 2009 | On dispersion of small energy solutions of the nonlinear Klein Gordon equation w | D. Bambusi; Scipio Cuccagna | ? | DOI:10.1353/AJM.2011.0034 |
| 21 | 85 | 2009 | Asymptotic behaviour of global solutions to a model of cell invasion | Gabriela Liţcanu; C. Morales-Rodrigo | ? | DOI:10.1142/S0218202510004775 |
| 22 | 84 | 2008 | Growth of Sobolev Norms and Controllability of the Schrödinger Equation | V. Nersesyan | ? | DOI:10.1007/s00220-009-0842-0 |
| 23 | 84 | 2016 | Bio-inspired computational heuristics to study Lane–Emden systems arising in ast | Iftikhar Ahmad; M. Raja + 2 | SpringerPlus | PMID:27822440 |
| 24 | 83 | 2008 | Condensation in disordered lasers: theory, 3D+1 simulations, and experiments. | C. Conti; M. Leonetti + 3 | Physical Review Letters | PMID:18851528 |
| 25 | 82 | 2018 | A class of differential hemivariational inequalities in Banach spaces | S. Migórski; Shengda Zeng | Journal of Global Optimization | DOI:10.1007/s10898-018-0667-5 |
| 26 | 78 | 2004 | PROLONGATIONS OF GEOMETRIC OVERDETERMINED SYSTEMS | T. Branson; A. Čap + 2 | ? | DOI:10.1142/S0129167X06003655 |
| 27 | 78 | 2017 | Confined Rayleigh-Bénard, Rotating Rayleigh-Bénard, and Double Diffusive Convect | K. Chong; Yantao Yang + 3 | Physical Review Letters | PMID:28949632 |
| 28 | 76 | 2018 | Massive Vector Fields in Rotating Black-Hole Spacetimes: Separability and Quasin | V. Frolov; P. Krtouš + 2 | Physical Review Letters | PMID:29932711 |
| 29 | 74 | 2008 | Are there waves in elastic wave turbulence? | N. Mordant | Physical Review Letters | PMID:18643509 |
| 30 | 73 | 2003 | Dynamical structure of irregular constrained systems | O. Mišković; J. Zanelli | ? | DOI:10.1063/1.1601299 |
| 31 | 70 | 2013 | Integration over Multiple Timescales in Primary Auditory Cortex | S. David; S. Shamma | Journal of Neuroscience | PMID:24305812 |
| 32 | 69 | 2019 | Extracting Interpretable Physical Parameters from Spatiotemporal Systems using U | Peter Y. Lu; Samuel Kim + 1 | Physical Review X | DOI:10.1103/PHYSREVX.10.031056 |
| 33 | 68 | 2020 | MHV gluon scattering amplitudes from celestial current algebras | Shamik Banerjee; Sudip Ghosh | Journal of High Energy Physics | DOI:10.1007/JHEP10(2021)111 |
| 34 | 67 | 2015 | Dual solutions of radiative MHD nanofluid flow over an exponentially stretching  | Sandeep Naramgari; C. Sulochana | Applied Nanoscience | DOI:10.1007/s13204-015-0420-z |
| 35 | 66 | 2019 | Large deviations and dynamical phase transitions in stochastic chemical networks | A. Lazarescu; Tommaso Cossetto + 2 | Journal of Chemical Physics | DOI:10.1063/1.5111110 |
| 36 | 65 | 2018 | Optimization of non-linear conductance modulation based on metal oxide memristor | Huan Liu; Mingrui Wei + 1 | Nanotechnology Reviews | DOI:10.1515/NTREV-2018-0045 |
| 37 | 63 | 2004 | THE BOUSSINESQ INTEGRABLE SYSTEM: COMPATIBLE LATTICE AND CONTINUUM STRUCTURES | A. Tongas; F. Nijhoff | Glasgow Mathematical Journal | DOI:10.1017/S0017089505002417 |
| 38 | 62 | 2014 | Data fusion via intrinsic dynamic variables: An application of data-driven Koopm | Matthew O. Williams; Clarence W. Rowley + 2 | ? | DOI:10.1209/0295-5075/109/40007 |
| 39 | 62 | 2013 | Traveling Wave Solutions in a Reaction-Diffusion Model for Criminal Activity | H. Berestycki; N. Rodríguez + 1 | Multiscale Modeling & simulati | DOI:10.1137/12089884X |
| 40 | 60 | 2012 | Numerical approximation of one model of bacterial self-organization | R. Čiegis; Andrej Bugajev | ? | DOI:10.15388/na.17.3.14054 |
| 41 | 59 | 2007 | Quenched CLT for random toral automorphism | Arvind Ayyer; C. Liverani + 1 | ? | DOI:10.3934/dcds.2009.24.331 |
| 42 | 55 | 2014 | Conservation-dissipation formalism of irreversible thermodynamics | Yi Zhu; L. Hong + 2 | ? | DOI:10.1515/jnet-2014-0037 |
| 43 | 54 | 2015 | Catastrophic Regime Shift in Water Reservoirs and São Paulo Water Supply Crisis | R. Coutinho; R. Kraenkel + 1 | PLoS ONE | PMID:26372224 |
| 44 | 54 | 2012 | On the Inviscid Limit for the Compressible Navier–Stokes System in an Impermeabl | Franck Sueur | Journal of Mathematical Fluid  | DOI:10.1007/s00021-013-0145-2 |
| 45 | 53 | 2014 | Effects of heat and mass transfer on peristaltic flow of a nanofluid between ecc | S Nadeem; A. Riaz + 2 | Applied Nanoscience | DOI:10.1007/s13204-013-0225-x |
| 46 | 52 | 2021 | Convergence to nonlinear diffusion waves for a hyperbolic-parabolic chemotaxis s | Qingqing Liu; Hongyun Peng + 1 | Journal of Differential Equati | DOI:10.1016/j.jde.2022.01.021 |
| 47 | 51 | 2012 | Nonlinear time reversal in a wave chaotic system. | M. Frazier; B. Taddese + 2 | Physical Review Letters | PMID:23432243 |
| 48 | 51 | 2010 | Convergence of frozen Gaussian approximation for high‐frequency wave propagation | Jianfeng Lu; Xu Yang | ? | DOI:10.1002/CPA.21384 |
| 49 | 50 | 2023 | A Denoising Diffusion Model for Fluid Field Prediction | Gefan Yang; S. Sommer | arXiv.org | DOI:10.48550/arXiv.2301.11661 |
| 50 | 50 | 2018 | Long time existence for fully nonlinear NLS with small Cauchy data on the circle | R. Feola; Felice Iandoli | ? | DOI:10.2422/2036-2145.201811_003 |
| 51 | 48 | 2020 | Octagon at finite coupling | A. Belitsky; A. Belitsky + 1 | Journal of High Energy Physics | DOI:10.1007/JHEP07(2020)219 |
| 52 | 47 | 2014 | Dark solitons, breathers, and rogue wave solutions of the coupled generalized no | N. V. Priya; M. Senthilvelan + 1 | Physical review. E, Statistica | PMID:25019845 |
| 53 | 46 | 2005 | Dynamics and thermodynamics of axisymmetric flows: Theory. | N. Leprovost; B. Dubrulle + 1 | Physical review. E, Statistica | PMID:16711930 |
| 54 | 46 | 2020 | An Efficient Analytical Approach for the Solution of Certain Fractional-Order Dy | Yamei Qin; Adnan Khan + 3 | ? | DOI:10.3390/en13112725 |
| 55 | 46 | 2022 | EMHD Nanofluid Flow with Radiation and Variable Heat Flux Effects along a Slande | Aamir Ali; Hajra Khan + 2 | Nanomaterials | PMID:36364648 |
| 56 | 45 | 2021 | An assessment of the mathematical model for estimating of entropy optimized visc | Yong-Min Li; M. Khan + 3 | Scientific Reports | PMID:33986435 |
| 57 | 45 | 2019 | Learning Deep Stochastic Optimal Control Policies Using Forward-Backward SDEs | Ziyi Wang; M. Pereira + 1 | Robotics: Science and Systems | DOI:10.15607/RSS.2019.XV.070 |
| 58 | 44 | 2015 | Exact Solutions to the (2+1)-Dimensional Boussinesq Equation via exp(Φ(η))-Expan | M. Alam; M. Hafez + 2 | ? | DOI:10.3329/JSR.V7I3.17954 |
| 59 | 43 | 2007 | How state preparation can affect a quantum experiment: Quantum process tomograph | Aik-meng Kuah; K. Modi + 2 | ? | DOI:10.1103/PhysRevA.76.042113 |
| 60 | 43 | 2015 | Multiscale Metabolic Modeling of C4 Plants: Connecting Nonlinear Genome-Scale Mo | Elijah Bogart; C. Myers | PLoS ONE | PMID:26990967 |
| 61 | 43 | 2006 | Metastability in interacting nonlinear stochastic differential equations: I. Fro | N. Berglund; B. Fernandez + 1 | ? | DOI:10.1088/0951-7715/20/11/006 |
| 62 | 43 | 2014 | Turing Instability and Pattern Formation for the Lengyel–Epstein System with Non | G. Gambino; M. Lombardo + 1 | Acta Applicandae Mathematicae  | DOI:10.1007/s10440-014-9903-2 |
| 63 | 42 | 2017 | Viscous displacement in porous media: the Muskat problem in 2D | Bogdan–Vasile Matioc | Transactions of the American M | DOI:10.1090/TRAN/7287 |
| 64 | 42 | 2015 | Fluctuating hydrodynamics for a discrete Gross-Pitaevskii equation: Mapping onto | M. Kulkarni; D. Huse + 1 | ? | DOI:10.1103/PhysRevA.92.043612 |
| 65 | 42 | 2006 | Sufficient Set of Integrability Conditions of an Orthonomic System | M. Marvan | Foundations of Computational M | DOI:10.1007/s10208-008-9039-8 |
| 66 | 41 | 2018 | Multiscale formulation for coupled flow-heat equations arising from single-phase | T. Praditia; R. Helmig + 1 | Computational Geosciences | DOI:10.1007/s10596-018-9754-4 |
| 67 | 41 | 2019 | Port-Hamiltonian Modeling of District Heating Networks | S. Hauschild; N. Marheineke + 3 | Progress in Differential-Algeb | DOI:10.1007/978-3-030-53905-4_11 |
| 68 | 40 | 2022 | Hall effect on MHD Jeffrey fluid flow with Cattaneo–Christov heat flux model: an | M. Awais; H. Rehman + 3 | Complex & Intelligent Systems | DOI:10.1007/s40747-022-00754-1 |
| 69 | 40 | 2003 | Quaternionic factorization of the Schrödinger operator and its applications to s | V. Kravchenko; V. Kravchenko | ? | DOI:10.1088/0305-4470/36/44/008 |
| 70 | 39 | 2017 | Convergence to equilibrium of renormalised solutions to nonlinear chemical react | K. Fellner; B. Tang | ? | DOI:10.1007/s00033-018-0948-3 |
| 71 | 39 | 2002 | Form factor for a family of quantum graphs: an expansion to third order | G. Berkolaiko; H. Schanz + 1 | ? | DOI:10.1088/0305-4470/36/31/303 |
| 72 | 38 | 2022 | Variational quantum evolution equation solver | F. Y. Leong; W. Ewe + 1 | Scientific Reports | PMID:35752702 |
| 73 | 38 | 2017 | V-cycle Multigrid Algorithms for Discontinuous Galerkin Methods on Non-nested Po | P. Antonietti; G. Pennesi | Journal of Scientific Computin | DOI:10.1007/s10915-018-0783-x |
| 74 | 38 | 2019 | Impact of ohmic heating on MHD mixed convection flow of Casson fluid by consider | B. J. Gireesha; K. Ganesh Kumar + 3 | Nonlinear Engineering | DOI:10.1515/nleng-2017-0144 |
| 75 | 38 | 2015 | Lane Formation by Side-Stepping | M. Burger; S. Hittmeir + 2 | SIAM Journal on Mathematical A | DOI:10.1137/15M1033174 |
| 76 | 37 | 2020 | Finite Element Study of MHD Impacts on the Rotating Flow of Casson Nanofluid wit | Bagh Ali; R. A. Naqvi + 3 | Mathematics | DOI:10.3390/math8091555 |
| 77 | 37 | 2002 | Chiral dynamics of the p wave in K − p and coupled states | D. Jido; E. Oset + 2 | ? | DOI:10.1103/PhysRevC.66.055203 |
| 78 | 37 | 2017 | Generation of Caustics and Rogue Waves from Nonlinear Instability. | A. Safari; R. Fickler + 2 | Physical Review Letters | PMID:29219350 |
| 79 | 36 | 2006 | Remarks on nonlinear relation among phases and frequencies in modulational insta | Y. Nariyuki; T. Hada | ? | DOI:10.5194/npg-13-425-2006 |
| 80 | 36 | 2016 | Global Existence Results for Viscoplasticity at Finite Strain | A. Mielke; Riccarda Rossi + 1 | ? | DOI:10.1007/s00205-017-1164-6 |
| 81 | 36 | 2001 | Linear superposition in nonlinear equations. | A. Khare; U. Sukhatme | Physical Review Letters | PMID:12059300 |
| 82 | 36 | 2021 | Physics-based neural networks for simulation and synthesis of cyclic adsorption  | Sai Gokul Subraveti; Zukui Li + 2 | Industrial &amp; Engineering C | DOI:10.26434/chemrxiv-2021-lm2sl |
| 83 | 36 | 2017 | Enhanced nonlinear frequency conversion and Purcell enhancement at exceptional p | A. Pick; Zin Lin + 2 | ? | DOI:10.1103/PhysRevB.96.224303 |
| 84 | 35 | 2008 | Universality of Crystallographic Pinning | A. Hoffman; J. Mallet-Paret | ? | DOI:10.1007/S10884-010-9157-2 |
| 85 | 35 | 2013 | Coupled backward- and forward-propagating solitons in a composite right- and lef | G. P. Veldes; J. Cuevas + 2 | Physical review. E, Statistica | PMID:23944572 |
| 86 | 35 | 2011 | ON THE EXPONENTIAL STABILITY OF SWITCHING-DIFFUSION PROCESSES WITH JUMPS | C. Yuan; J. Bao | ? | DOI:10.1090/S0033-569X-2012-01292- |
| 87 | 35 | 2017 | Stability of correction procedure via reconstruction with summation-by-parts ope | Philipp Offner; Jan Glaubitz + 1 | ESAIM: Mathematical Modelling  | DOI:10.1051/m2an/2018072 |
| 88 | 35 | 2014 | Singular Limits for Reaction-Diffusion Equations with Fractional Laplacian and L | S. M'el'eard; S. Mirrahimi | ? | DOI:10.1080/03605302.2014.963606 |
| 89 | 35 | 2013 | Cohomology of fiber bunched cocycles over hyperbolic systems | V. Sadovskaya | Ergodic Theory and Dynamical S | DOI:10.1017/etds.2014.43 |
| 90 | 34 | 2017 | Fourth order superintegrable systems separating in Cartesian coordinates I. Exot | I. Marquette; M. Sajedi + 1 | ? | DOI:10.1088/1751-8121/aa7a67 |
| 91 | 33 | 2016 | Kagome lattice from an exciton-polariton perspective | D. Gulevich; D. Yudin + 3 | ? | DOI:10.1103/PhysRevB.94.115437 |
| 92 | 32 | 2008 | Generalized quantum potentials | L. Nottale | ? | DOI:10.1088/1751-8113/42/27/275306 |
| 93 | 32 | 2016 | Chaotic universe model | E. Aydiner | Scientific Reports | PMID:29335452 |
| 94 | 32 | 2012 | Epidemiology of the Emergent Disease Paridae pox in an Intensively Studied Wild  | S. Lachish; B. Lawson + 2 | PLoS ONE | PMID:23185230 |
| 95 | 32 | 2014 | Global well-posedness for the massless cubic Dirac equation | N. Bournaveas; Timothy Candy | ? | DOI:10.1093/IMRN/RNV361 |
| 96 | 32 | 2012 | Finding Eigenvalues of Holomorphic Fredholm Operator Pencils Using Boundary Valu | W. Beyn; Y. Latushkin + 1 | ? | DOI:10.1007/S00020-013-2117-6 |
| 97 | 32 | 2013 | Transformation of Adaptation and Gain Rescaling along the Whisker Sensory Pathwa | M. Maravall; A. Alenda + 2 | PLoS ONE | PMID:24349279 |
| 98 | 32 | 2018 | Adomian Decomposition Method with Modified Bernstein Polynomials for Solving Ord | A. F. Qasim; Ekhlass S. Al-Rawi | Journal of Applied Mathematics | DOI:10.1155/2018/1803107 |
| 99 | 32 | 2017 | Global linearization and fiber bundle structure of invariant manifolds | J. Eldering; Matthew D. Kvalheim + 1 | Nonlinearity | DOI:10.1088/1361-6544/aaca8d |
| 100 | 32 | 2017 | Scalar-Fluid interacting dark energy: cosmological dynamics beyond the exponenti | J. Dutta; Wompherdeiki Khyllep + 1 | ? | DOI:10.1103/PhysRevD.95.023515 |
