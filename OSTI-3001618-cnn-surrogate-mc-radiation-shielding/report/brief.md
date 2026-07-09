# Brief

Independent-replication attempt of Pal Chowdhury et al. (FRIB, 2025),
"Surrogate Modeling of Monte Carlo Radiation Transport with Convolutional
Neural Networks for Shielding Optimization" (Nucl. Instrum. Methods B,
DOI 10.1016/j.nimb.2025.165909, OSTI 3001618).

The paper trains a 1D CNN (TensorFlow) to emulate PHITS Monte-Carlo neutron
transport through BPE, concrete and steel shields (1–250 MeV pencil beams,
10–150 cm thicknesses), then uses the ~20-ms/inference surrogate to sweep
shielding-material combinations for FRIB. Reported: CNN vs PHITS single-layer
dose agreement within ~7 % (Table 2), multi-layer within factor of 2
(Tables 3–4), 4-hour PHITS run vs <1 s CNN inference.

Why this is hard to reproduce exactly: PHITS is a **closed, license-controlled
code** (RIST/JAEA distribution — not free/open), and the paper releases
**no code, no data, no trained weights**. Strict bit-for-bit replication is
infeasible. Replication plan (documented, non-fabricated substitution):
use **OpenMC** (open-source, ENDF/B-VII.1 or JEFF library) on uicgpu as an
independent MC ground-truth, rebuild the same 1D CNN architecture in
TensorFlow/Keras, generate the training dataset, train, and verify the
qualitative claims (single-material %-level agreement, ms-scale inference,
brute-force sweep feasibility). LLM-judge scoring completes the verdict.
