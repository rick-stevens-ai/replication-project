# Attempt Log — OSTI-2561245 (H2 LLPT, Istas et al. 2024/2025)

## 2026-07-02 (Ollie, subagent)

- 10:07 CDT — Received subagent task. Set: OSTI rank 23. Paper: "Liquid-liquid phase transition of hydrogen and its critical point: Analysis from ab initio simulation and a machine-learned potential" (Istas, Jensen, Yang, Holzmann, Pierleoni, Ceperley — arXiv:2412.14953, published Phys Rev E 111, 045307).
- 10:10 CDT — Fetched OSTI PDF (1.69 MB) via uicgpu proxy → `work/osti_2561245.pdf`. Confirmed valid PDF v1.5.
- 10:11 CDT — pdftotext extraction → `work/paper.txt` (999 lines). Full text readable.
- 10:12 CDT — Read paper. Key claim: **critical point of PBE-hydrogen LLPT at T = 1250 K ± 50 K and P ≈ 155-160 GPa**, substantially lower than earlier PBE estimates (~2000 K, Morales 2010).
- 10:12 CDT — Extracted method: NequIP E(3)-equivariant NN potential, trained on 48k of 54k qmc-hamm PBE configs (96 atoms), 100 epochs, cutoff 2.5 Å, LAMMPS-scale NPT MD at 200-2048 atoms, 200 ps min, timestep 0.5 fs.
- 10:12 CDT — Data availability statement: qmc-hamm.hub.yt/data.html (public); models "available on demand" (NOT public at time of paper).

## Replication strategy

Full replication is out of scope for a single subagent turn:
- Training a NequIP model on 48k configs for 100 epochs = many GPU-hours.
- 2048-atom NPT MD for 200+ ps at multiple T,P = >100 GPU-hours.
- Finite-size scaling to distinguish transition order requires 4+ system sizes.

Therefore we pursue the SPOT-CHECK / PARTIAL evidence chain:

1. **C1** — Data availability: verify the qmc-hamm hydrogen training dataset exists at the cited URL and has the described format (54k PBE configs at 96 atoms).
2. **C2** — Software availability: verify NequIP (Batzner 2022) is a real, PyPI-installable E(3)-equivariant NN potential.
3. **C3** — Prior-work triangulation: verify the paper's positioning that previous PBE LLPT critical point estimates were near 2000 K (Morales 2010) or without an estimate (Karasiev 2021), which is the paper's headline delta claim.
4. **C4** — Small-scale numerical sanity: if the qmc-hamm dataset downloads, spot-check its structure (npz/npy/JSON), atom count, energy/force ranges vs paper claims (Fig 11 MAE ~ 1.94 meV/atom / 170 meV/Å).
5. **C5** — Physical-plausibility: verify LAMMPS/ASE/nequip pipeline can be instantiated on uicgpu.

