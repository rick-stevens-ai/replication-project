# On-lattice kinetic Monte Carlo approaches for modeling molecular anisotropy in resveratrol crystallization

Tesia D Janicki, Tyler R Kennelly, Jonathan Leonard, Christine Roberts, Rekha R Rao, and Theron M Rodgers

Sandia National Laboratories, Albuquerque, NM 87185, United States of America

Corresponding author: tdjanic@sandia.gov

Received 27 February 2025; revised 12 May 2025; Accepted 5 June 2025; Published 18 June 2025

*Modelling and Simulation in Materials Science and Engineering* **33** (2025) 055010 (11 pp)

DOI: https://doi.org/10.1088/1361-651X/ade176

## Abstract

Stilbenes are a class of organic compounds with broad-ranging pharmaceutical and agricultural applications, which are typically isolated and purified through recrystallization. We are motivated by reducing experimental waste and optimizing yield via developing predictive simulations for processing-dependent crystal morphologies. Using resveratrol as a model stilbene system, we have developed an approach for simulating crystallization with molecular resolution using on-lattice kinetic Monte Carlo. In this work, we highlight modifications to the Stochastic Parallel PARticle Kinetic Simulator (SPPARKS) software package, which were essential to this application. Key enhancements include the incorporation of non-orthogonal cell shapes and monomer anisotropy approximations using bound hard spheres. This new SPPARKS application has been applied to resveratrol with attachment energy libraries obtained from density functional theory, resulting in excellent agreement with experimental morphology prediction.

Keywords: kinetic Monte Carlo, crystallization, resveratrol, stilbene

## 1. Introduction

Stilbenes are a class of molecules with a (1,2)-diphenylethylene base structure. Stilbenes are pervasive in a variety of application domains, including pharmacy, agriculture, and chemical sensing. trans-resveratrol is a stilbene possessing three hydroxyl functional groups. As an antioxidant naturally occurring in agricultural products (e.g. grapes, peanuts), resveratrol has gained popularity as a dietary supplement and has even been incorporated into cancer prevention and treatment. Typical for pharmaceutical compounds, resveratrol isomers can be isolated and purified through recrystallization. Processing conditions impact final crystal morphology, which is directly correlated with product properties, such as protein adsorption. In order to test possible recrystallization conditions (e.g. solvent, temperature) comprehensively, this work aims to develop a workflow for characterizing crystallization in stilbenes with resveratrol as a specific example.

Crystal structure prediction methods have been used to identify energetically favorable crystals and cocrystals in resveratrol and other stilbenes. These simulation methods are valuable for identifying anticipated product structures but lack the resolution to identify mechanisms driving early stages of crystal growth. Therefore, the incorporation of molecular-scale crystal growth simulations, such as molecular dynamics (MD) or Monte Carlo (MC), is required to fully characterize crystallization.

Kinetic Monte Carlo (kMC) uses binding energies derived from higher accuracy methods (e.g. quantum mechanics) to determine the probability of a monomer attaching to any site on the growing crystallite. The Stochastic Parallel PARticle Kinetic Simulator (SPPARKS) is an open-source software package which has been invoked for a variety of materials kMC applications. SPPARKS is an advantageous choice due to its modularity and parallelization.

To simulate surface attachment using kMC, SPPARKS randomly distributes deposition attempts uniformly over an assigned surface. The probability (Γ) of a monomer binding to the designated site (i) determines whether the deposition is accepted (sticks) or is rejected, according to the Arrhenius relation, equation (1):

Γ(i) = v · exp[E_bind(i) / (k_B T)]    (1)

where T is the temperature and k_B is the Boltzmann constant. E_bind(i) is the binding energy tabulated by the coordination number of the monomer on site i. v is a parameter with units of inverse time and is chosen based on experimental precursor flow rate (gas) or concentration (liquid).

On-lattice models enable growth characterization for specific crystal polymorphs but typically assume that all particles (monomers) are isotropic. Prior to this work, molecular anisotropy had not been implemented in SPPARKS but was deemed essential for accurate representation of resveratrol. Rather than changing the shape of the monomer to a spherocylinder, we took inspiration from linear tangent hard sphere (LTHS) representations of molecule chains, which have been applied successfully to larger molecules in liquid crystal and polymer ordering. We thus maximized the existing framework of on-lattice SPPARKS by representing each resveratrol unit with two bound hard spheres. Deviating from LTHS models, binding was geometrically enforced by the lattice positions rather than applying an additional intra-site force. By reducing each 28-atom molecule down to two sites, this approximation makes on-lattice crystal growth tractable for resveratrol while retaining relevant physics within molecular geometry.

## 2. Additions to the SPPARKS package

### 2.1. Non-orthogonal lattice construction

The first addition to SPPARKS was enabling non-orthogonal simulation boxes. This feature permits a <90° angle between a- and b- lattice vectors, with the third dimension orthogonal to the plane. For general use cases, specific lattice sites for a hexagonal-close-packed (HCP) unit cell were incorporated into this modification and are enabled via user command **lattice HCP a**, where a is the a-lattice parameter. Remaining box vectors are defined as |a| = |b| = sqrt(3/8) |c| and θ_ab = 60°. This lattice style must be used in conjunction with the new **hex region** style, which accounts for unit cell replication and periodicity.

For parallel computations, hex subdomains are assigned on a cubic grid prior to shifting the atoms by the x-component of the y-lattice vector, xylattice.

This new branch also permits 3D deposition. Instead of defining an incident vector for particle deposition, the user may define the vector as (0 0 0), for which trial sites are generated randomly over all available surfaces. Candidate sites within the capture distance are only considered if their nearest-neighbor coordination is within a user-defined range (e.g. 2–6).

Specific lattice sites for resveratrol are enabled in a second branch and are invoked as **lattice resv 1.0**. Since the unit cell geometry is incorporated in this lattice type, the lattice parameter was set to unity.

### 2.2. Implementation for resveratrol

The second, more extensive addition to SPPARKS addressed the inherent anisotropy in stilbene geometry; this branch addition was specific to P21/c resveratrol. Rather than use a single sphere to represent each resveratrol monomer, we approximated that each monomer can be represented by two bound spheres. Each sphere is centered on the half-monomer center-of-mass and are not permitted to dissociate from each other. Accounting for the different functional groups on each half of the monomer, each sphere is permitted to bind only to specific sites within the lattice assigned to its specific number of OH substituents. Lattice style **resv** in this branch designates the resveratrol bound-sphere lattice configuration and must be used with **region hex**.

A new **diffusion/disphere** app style was created in the SPPARKS code to address bound-sphere motion (Table 1). The binding energy table for the bound sphere approach uses 2D indexing for the coordination on each sphere in the bound pair. By consequence of being bound to a nearest neighbor, individual spheres must have a minimum coordination of unity. This app style currently can only support the resveratrol lattice but could be extended to other systems by adding a new lattice style.

Table 1. Schematic of on-lattice kMC algorithm and modifications made for bound sphere kMC.
| Traditional kMC | Bound sphere kMC |
|---|---|
| 1. Generate random event for i → j | 1a. Generate random event as if moving a single site i1 → j1 |
| | 1b. Identify sites coupled to i1 and j1 |
| 2. Determine initial and final coordination of site for random event | 2. Determine the initial and final coordination of each site in the disphere pair |
| 3. Look up associated energies for coordination assignments. | 3. Look up associated energies for coordination assignments. |
| 4. Compute probability of this move, equation (1). | 4. Compute probability of this move, equation (1). |
| 5. Accept or reject | 5. Accept or reject |

## 3. Resveratrol simulation and experimental comparison

### 3.1. Energy library generation

Each binding energy was computed from the energy of a surface with a deposited monomer, less the energy of the pre-deposited surface and free monomer. A total of 74 surface depositions were incorporated.

All energies were computed using all-atom density functional theory (DFT) with the Fritz Haber Institute ab initio materials simulation package (FHI-aims) with 'light' numerical settings and tier 1 basis functions. Exchange-correlation interactions used PBE generalized gradient approximation with the Tkatchenko-Scheffler Hirschfeld-partitioning van der Waals correction and a Pulay direct inversion in the iterative space (DIIS) mixing algorithm with 0.1 eV Gaussian broadening width.

The periodic P21/c resveratrol unit cell positions and box size were optimized with fixed box shape. Parameters included a 3×3×1 kpoint mesh using a Broyden–Fletcher–Goldfarb–Shannon algorithm with a 0.01 eV Å^-1 trust radius and SCF convergence within 10^-4 eV. A single gas-phase monomer was cleaved out of the unit cell and relaxed with identical settings.

Surface calculations were performed along each of the three facet planes of the unit cell. The unit cell was replicated for each direction with a >20 Å vacuum gap.

Table 2. Geometric parameters for facet-dependent deposition.
| Direction | Replication (a × b × c) | Monomer layers frozen |
|---|---|---|
| (1 0 0) | 4 × 3 × 2 | 2 |
| (0 1 0) | 6 × 2 × 2 | 2 |
| (0 0 1) | 6 × 4 × 1.5 (bottom monomer deleted) | 1 |

DFT-generated energies were each input as ecoord binding energies for each deposition, indexed by local coordination of the two half-molecule center-of-masses. Where multiple depositions shared the same coordination indexing, energies were averaged. Coordinations not explicitly set from a DFT binding calculation were given an arbitrarily large barrier.

### 3.2. Simulating resveratrol crystal attachment in SPPARKS

Initial resveratrol lattices were generated using the new **resv** lattice type. The periodic simulation box was tuned during trial runs to accommodate variation in growth velocity for each facet. Unique crystal nuclei sizes and shapes listed in Table 3 were invoked for each of 5 simulations. Unless otherwise noted, the total boxsize for each production run encompassed a 48 × 16 × 24 periodic unit cell volume (~200 nm × 250 nm × 210 nm).

Table 3. Initial crystal nuclei geometries for each run.
| RunID | Description | Replication (a × b × c) |
|---|---|---|
| 1 | Cube (box b=12) | 4 × 1 × 2 |
| 2 | Bigger cube | 8 × 2 × 4 |
| 3 | Short in a | 4 × 2 × 4 |
| 4 | Short in b | 8 × 1 × 4 |
| 5 | Short in c | 8 × 2 × 2 |

The temperature was set at 20 °C in energy units as 0.0270 eV/k_B. The **event** deposition style was invoked with a 0.1 s^-1 prefactor, 5.0 Å incident capture distance, with depositions only permitted on sites with coordinations between 1–9. The **tree** solve style was used for 5×10^6 trial steps with statistics saved every 10^5 steps.

In these trajectories, we identified a strong degree of anisotropy, with growth proceeding most rapidly along a single direction, which agrees qualitatively with experimental observation.

### 3.3. Experimental validation

For experimental comparison, 2 g resveratrol were dissolved in 20 g of 2:1 ethanol–water solution. The mixture was heated in an oven at 70 °C for 24 h. The solution was transferred to a chamber maintained at 20 °C and left undisturbed for 5 days.

To observe the crystal structures, we employed Micro-CT with a Bruker SKYSCAN 1272 microcomputed tomography (microCT or μCT) scanner with 0.45 μm resolution. The reconstructed crystal population model was analyzed in Dragonfly v2024.1, where individual crystals were segmented from the population via a watershed transform. 1207 crystals were segmented and exported as mesh files, with length L defined as longest axis, W as shortest, H as middle.

Figure 7 includes the H:L and W:L aspect ratio distributions of experimental crystals and simulated results. Distributions for experiment come from independent crystallites within the solution, while simulation distributions come from 560 independent simulation replicants using different random number seeds. Simulated distributions are much narrower than experiment, but the distribution peaks overlap well.

## 4. Conclusions

To probe crystal growth mechanisms in resveratrol, we have introduced several modifications to the SPPARKS simulation package. Non-orthogonal (i.e. hexagonal) simulation boxes have been enabled for the general HCP unit cell for a wider range of materials. Specifically for resveratrol, the addition of bound-sphere motion enables non-spherical particles in on-lattice kMC models for crystal attachment. This new infrastructure was implemented for crystal attachment in resveratrol using DFT-based event libraries. We have shown excellent agreement with experiment for qualitative crystal morphologies.

## Data availability statement

The data that support the findings of this study will be openly available following an embargo at the following URL/DOI: https://spparks.github.io/ and https://github.com/tdjanic-snl/spparks.

## Acknowledgments

This work was supported by the Laboratory Directed Research and Development program at Sandia National Laboratories, a multimission laboratory managed and operated by NTESS for the U.S. DOE/NNSA under contract DE-NA0003525.

---
*Extraction note (2026-07-06):* Neither `marker` nor `nougat` was available on uicgpu at replication time. This file is a clean text extraction produced from `pdftotext -layout` output (see `work/paper_layout.txt`) plus HTML-scraped table structure from IOPscience, hand-cleaned by the replication agent to preserve the paper structure. The nougat.mmd sibling is produced by the same pipeline. Character-for-character fidelity is limited to what pdftotext + IOPscience HTML could recover; math is transcribed in ASCII.
