# Artifact Harvest — OSTI 3363025

| # | Artifact | URL / Source | Size | Notes |
|---|---|---|---|---|
| 1 | Paper PDF | https://www.osti.gov/servlets/purl/3363025 | 771,957 B | Fetched via uicgpu (proxy required). Saved as `paper.pdf`. |
| 2 | GitHub repo | https://github.com/miscquanta/HMRRL-tersoff-silica.git | 4 files | Cloned to `/tmp/HMRRL-tersoff-silica/` on uicgpu; copied to `work/HMRRL-tersoff-silica/`. |
| 3 | `ML-Tersoff.tersoff` | (from repo) | 1543 B | LAMMPS Tersoff format, 8 element-triplet blocks. |
| 4 | `Q-Tersoff.tersoff` | (from repo) | 1547 B | LAMMPS Tersoff format, 8 element-triplet blocks. Si-Si block identical to ML-Tersoff. |
| 5 | `in.relax` | (from repo) | 1079 B | LAMMPS input: 5x5x5 replicate, iso box/relax + NVE 10 ps at 298 K. |
| 6 | `quartz.data` | (from repo) | 598 B | 9-atom α-quartz unit cell (P3_121 hex, a=4.916, c=5.405, ρ=2.648 g/cm³). |
| 7 | IZA database | http://www.iza-structure.org/databases/ | not downloaded | Paper claims data comes from here. NOT needed for α-quartz; needed for the other 20 polymorphs (not tested this run). |
| 8 | Navrotsky thermochemistry | Navrotsky et al. Chem. Rev. 2009, 109, 3885 (ref 36) | not downloaded | Source of reference cohesive energies for the paper's 21 polymorphs. |
| 9 | LAMMPS 29Aug2024 | Pre-installed on uicgpu at `/data/stevens/envs/lammps-cuda/bin/lmp` | — | Kokkos-CUDA build; ran on CPU here. |
| 10 | This report + evidence dir | Local | 26 files in `report/evidence/` | All log files, input scripts, final geometries, angle-analysis code, and LLM judge JSON responses. |

**Publicly-available artifacts that were NOT retrieved and would be needed for a full 21-polymorph replication**:
- 20 IZA polymorph structure files (CIF or LAMMPS data format) matching the paper's benchmark set (FER, AFI, MFI, MEL, MTW, CFI, STT, BEA, MWW, IFR, ITE, EMT, AST, CHA, FAU, MEI, ISV, Cristobalite, Tridymite, Moganite).
- Navrotsky reference energetics for each of the 21 polymorphs relative to α-quartz.
- A GAP silica potential file (paper's baseline) if we wanted to independently confirm the 100× speedup claim.
- The BLAST framework code containing the c-MCTS + hierarchical-reward pipeline (paper says available only via CNM user program).
- Elastic constant computation script (paper's Fig 5).
- Amorphous S(q) melt-quench script (paper's Fig 6).

**Judge outputs saved as**: `report/evidence/judge_response_gpt51.json`, `report/evidence/judge_response_gemini25.json` (see below step).
