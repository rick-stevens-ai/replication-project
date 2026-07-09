# Brief — Nicoud (2000), *Conservative High-Order Finite-Difference Schemes for Low-Mach Number Flows*

**Paper.** F. Nicoud, *J. Comput. Phys.* **158**(1), 71–97 (2000). DOI 10.1006/jcph.1999.6408. Proposes three finite-difference algorithms for the low-Mach-number approximation of the Navier–Stokes equations that are (a) **discretely conservative** for mass, momentum, and scalar transport on a staggered mesh and (b) **fourth-order accurate in space** (second-order in time).

**Why replicate.** The two headline claims — *4th-order spatial convergence* and *discrete conservation* — are numerical, self-contained, and reproducible with a modest 1-D solver in numpy. A real replication is a working staggered-grid 4th-order scheme whose (i) truncation error decays as h^4 on manufactured solutions and (ii) whose discrete conservation errors are at machine precision, independent of h.

**What we did.** Built a staggered-grid 4th-order conservative FD scheme for the low-Mach density/momentum/scalar equations in 1-D; ran a manufactured-solution grid-convergence study (N = 32,64,128,256,512) and a periodic-advection conservation test; scored the observed order of accuracy and drift in total mass/momentum/scalar with an Argo-hosted LLM judge (claude-opus-4.7).
