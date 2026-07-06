# Email Draft — Code Request for Zhang et al. 2019

**Status:** DRAFT — Do NOT send without Rick's review

---

**To:** Dongkun Zhang (dongkun_zhang@brown.edu), George Em Karniadakis (george_karniadakis@brown.edu)  
**CC:** Lu Lu (lu.lu@yale.edu)  
**Subject:** Code request — "Learning in Modal Space" (Zhang et al., SIAM J. Sci. Comput. 2020)

---

Dear Dr. Zhang and Prof. Karniadakis,

We are conducting a systematic replication study of computational PDE methods as part of a scientific reproducibility initiative at Argonne National Laboratory. Your paper "Learning in Modal Space: Solving Time-Dependent Stochastic PDEs Using Physics-Informed Neural Networks" is among the papers we are attempting to replicate.

We have reimplemented the NN-DO and NN-BO methods from the paper description and confirmed the qualitative correctness of the approach (eigenvalue crossing handling, variance approximation). However, we are experiencing quantitative gaps that we believe stem from PINN training sensitivity (loss balancing, gauge choice in the modal decomposition) rather than any methodological issue.

Specifically, we've found that:
- The DO/BO modal decomposition has gauge freedom that makes component-level comparison challenging
- PINN convergence for the coupled system (mean + modes + stochastic coefficients) is sensitive to loss weighting schemes not fully specified in the paper
- Our variance estimates are within the right order of magnitude but don't match the sub-1% errors reported

Would you be willing to share the original code used to produce the results in the paper? Access to the implementation would greatly help us achieve a faithful replication and properly credit your work in our study.

We are also exploring a parametric PINN approach (treating ξ as an extra input dimension) as an alternative pathway to verify the statistical results, which has been showing promising convergence.

Thank you for your time.

Best regards,  
Rick Stevens  
Associate Laboratory Director  
Argonne National Laboratory
