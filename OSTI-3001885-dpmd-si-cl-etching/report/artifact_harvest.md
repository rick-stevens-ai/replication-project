# Artifact Harvest — OSTI 3001885

## Primary paper PDF
- **URL:** https://www.osti.gov/servlets/purl/3001885
- **Fetched:** 2026-07-02 via uicgpu (behind Argonne proxy, OSTI direct 403's some clients)
- **Local:** `work/osti_3001885.pdf` (6,621,375 B / ~6.3 MB, PDF 1.5)
- **Text extract:** `work/paper.txt` (pdftotext -layout, 1329 lines)

## Data deposit (referenced by paper, publicly available)
- **DOI:** https://doi.org/10.34770/zqj0-3z73
- **Landing:** https://datacommons.princeton.edu/discovery/catalog/doi-10-34770-zqj0-3z73
- **Bulk transfer:** Globus endpoint `bb151d8e-ea3f-4612-b357-94d07f538f0c`
  path `/10.34770/zqj0-3z73/590/`
- **Total size:** 590 MB
- **Contents (per Data Availability Statement in paper):**
  - Final DeepMD model file (.pb)
  - 58,536-frame training data set (energies, forces, coordinates, box)
  - LAMMPS input decks for impact simulations
  - Data tables summarizing results
- **Fetched to local?** No — landing page uses Cloudflare Turnstile + Globus interactive auth.
  Not attempted from a headless subagent context (would require interactive OAuth).
- **Consistency check:** landing-page HTML enumerates a manifest identifier `590`, matches the
  size stated on the landing page, matches paper's DAS.

## Software / toolchain
- **DeePMD-kit source:** https://github.com/deepmodeling/deepmd-kit tag `v2.1.5`
  cloned to `uicgpu:/data/stevens/osti-3001885-repl/deepmd-kit/` (public FOSS, MIT+LGPL).
- **DeePMD-kit v2.1.5 pip wheel:** `pip install deepmd-kit==2.1.5` installed cleanly into
  `uicgpu:/data/stevens/envs/dpmd-repl` (python 3.10, tensorflow-cpu==2.10.0, numpy 1.23.5).
- **LAMMPS 29 Aug 2024** available at `uicgpu:/data/stevens/envs/lammps-cuda/bin/lmp`
  (WITHOUT `deepmd` pair style — requires rebuild against libtensorflow_cc).
- **Water example dataset** (used for pipeline verification): shipped with the deepmd-kit
  v2.1.5 tag, `examples/water/data/data_{0..3}` (192-atom H2O box, 320 training frames
  and 80 validation frames).

## Reference literature (cross-checked, not fetched)
Referenced by paper for comparison + used by LLM judge for external plausibility:
- Chang et al. 1997 JVST A 15, 1853 (exp. Cl/Ar+ yields vs energy)
- Vella & Graves 2020s REBO MD Cl/Ar+ etching of Si
- Brichon et al. 2015 J. Appl. Phys. (REBO Cl+ etching, mixed layer)
- Layadi et al. 1997 (XPS Cl coverage of Si)
- Vitale & Smith 2003 (exp. Cl+ etch yields)
- Coburn-Winters 1979 J. Appl. Phys. (ion-neutral synergy foundational work)
- Weakliem & Carter (Cl-Si potentials)

## Compute inventory
- Host: uicgpu (8×NVIDIA A100 80GB, 255 cores, 2 TB RAM, /data 14 TB nvme)
- Env: `/data/stevens/envs/dpmd-repl` (~2.5 GB)
- Water demo training checkpoints: `uicgpu:/data/stevens/osti-3001885-repl/deepmd-kit/examples/water/se_e2_a/`
- Frozen model: `graph.pb` (500-step) and pending `graph_20k.pb` (20000-step) demonstrations.

## Added 2026-07-04 (physics-anchor promotion)

- Chang & Sawin 1997 experimental Cl/Ar+ Si-yields at 35/60/100 eV — transcribed
  from paper's own Table I (paper.txt lines 887-921): 0.3 / 1.3 / 2.4 Si/Ar+.
  Original source: Chang J.P., Coburn J.W., "Feature-scale simulation of Si etching
  in Cl-based plasmas," J. Vac. Sci. Technol. B 15, 1853 (1997).
- Brichon 2015 REBO comparator Cl+ Si-yields — transcribed from Table I same
  paper: 0.03/0.10/0.25/0.35/0.45 at 5/10/25/50/100 eV. Original: Brichon et al.
  J. Appl. Phys. 118, 053303 (2015).
- NIST WebBook / JANAF / Luo "Comprehensive Handbook of Chemical Bond Energies"
  (public reference values): Si-Cl BDE 380 kJ/mol; SiCl4 atomization 1568 kJ/mol;
  Si-Si diamond cohesion 4.63 eV; Cl-Cl BDE 242 kJ/mol; Si-H BDE 318 kJ/mol.
- Sigmund/Steinbrüchel threshold sputter law Y(E) = A(√E − √Eth), from Steinbrüchel
  Appl. Phys. Lett. 55, 1960 (1989); canonical form used throughout Chang 1997,
  Vitale 2003, Vella 2019.
- DataCite record for Princeton Data Commons doi:10.34770/zqj0-3z73 — pulled via
  https://api.datacite.org/dois/10.34770/zqj0-3z73 — confirms deposit is
  "findable", CC-BY-4.0, DE-AC02-09CH11466-funded; contentUrl null (Globus-hosted).
