# Workflow — ding2021 (arXiv:2105.04495, PRL 128 2022)

## Narrative
1. Fetched PDF; pdftotext (~4.8k words); Nougat stub (GPU, sha256). Identified the paper = "Observation of the Orbital Rashba-Edelstein Magnetoresistance" (experimental, Py/oxidized-Cu).
2. Extracted the discriminating physics: three field-rotation-plane angular MR (alpha/beta/gamma); AMR flat in beta but OREMR ~cos^2(beta); interfacial thickness saturation (Fig 1-2).
3. Implemented the SMR/OREMR resistivity model rho_xx = rho0 + D_AMR m_x^2 + D_SMR(1-m_y^2).
4. C1: AMR-only beta scan flat (p2p=0), OREMR beta scan cos^2 (p2p=0.015) => discriminator.
5. C2: cos^2 fits R2=1 for all three planes.
6. C3: interface+shunt thickness model => flat MR ratio for t<=5nm, decay beyond (interfacial signature).
7. LLM-judge (free Argo sonnet-4.6): PARTIAL, coverage 7, agreement 6 (theory framework, not experimental data).

## Tools & codes
Python 3.13, NumPy, Matplotlib; pdftotext. code/ding2021_replication.py (~150 LOC). LLM-judge -> argo:claude-sonnet-4.6 (free).

## Effort estimate
CPU-only, ~1s. Wall clock ~15 min incl. identifying the paper + extraction. ~150 LOC, 1 iteration.
