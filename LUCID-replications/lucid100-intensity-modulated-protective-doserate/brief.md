# Brief — Matsuya et al. 2019 (IMK, modulated radiation fields)

**Paper:** Matsuya Y, McMahon SJ, Ghita M, Yoshii Y, Sato T, Date H, Prise KM. *Intensity Modulated Radiation Fields Induce Protective Effects and Reduce Importance of Dose-Rate Effects.* Scientific Reports 9:9533 (2019). DOI: 10.1038/s41598-019-45960-z.

**Topic:** Half-field vs uniform-field irradiation of AGO1522 (normal human skin fibroblasts) and DU145 (human prostate cancer). The authors fit an Integrated Microdosimetric-Kinetic (IMK) model to single-dose, split-dose and fractionated survival data, with an intercellular-communication branch. Headline conclusions:

- (i) In-field survival is **higher** under half-field (MF) than uniform-field (UF) for the same delivered dose (AGO1522).
- (ii) The importance of sub-lethal damage repair (SLDR) for AGO1522 is **reduced** under half-field exposure.
- (iii) Half-field exposure produces fewer initial DNA lesions (protective, not rescue).

**Replication strategy:** SPOT-CHECK only. The full IMK has many coupled parameters (DNA-TE term, sublesion repair, intercellular communication, dose-rate convolution); the paper's Table 1 gives `alpha_0`, `beta_0`, `a+c` for both cell lines under both fields. In the acute single-dose limit (N=1, T→0) the IMK DNA-TE branch reduces to standard LQ form, so we can directly evaluate `S(D) = exp(-(α_0 D + β_0 D²))` and check whether Table 1 *as published* reproduces the qualitative direction of headline claims (i) and (ii). This does not refit the data; it checks internal consistency of the published parameters with the published headline claims.

**Scope of this report:** SPOT-CHECK — direct evaluation of acute LQ survival from Matsuya 2019 Table 1; qualitative pass/fail of claims (i) and (ii). Full IMK (split-dose, fractionation, intercellular signalling) **not** replicated.
