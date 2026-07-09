# Marker parse — FALLBACK from OA twin papers

**Target paper:** Liew et al. 2022 IJROBP 112(3):802–817. DOI 10.1016/j.ijrobp.2021.09.048. **CLOSED-ACCESS.** No `paper.pdf` in this slot dir.

This `marker.md` is a **fallback**, not a Marker parse of the target paper. It concatenates OA text
extracts of the twin/companion papers that fully specify the UNIVERSE + DDRi mechanistic model
reproduced by this slot. When the target paper.pdf becomes available, replace this file with a
real Marker parse.

Sources (all in `../source/`, all OA CC-BY unless noted):
- `liew2019_ddr_hypoxia_photon.pdf` (photon UNIVERSE + DDRi; Eqs 1–7; Table 1 K; Table 3 RSF)
- `mein2019_universe_rbe.pdf` (ion-beam Kiefer–Chatterjee + UNIVERSE-RBE)
- `liew2020_hypoxia_direct_indirect.pdf` (hypoxia HRF)
- `liew2022_universe_repair.pdf` (de-masks the model as UNIVERSE)
- `liew2022_universe_flash.pdf` (UNIVERSE FLASH companion)

The target paper's abstract is available in `../source/semantic_scholar_metadata.json`. Sizes below
are pointers to the pre-extracted `.txt` files in `../source/` (already produced with pdftotext at
slot creation time on 2026-06-09).

## 1. Target paper abstract (from Semantic Scholar)

See `../source/semantic_scholar_metadata.json`. Full abstract, authors, DOI, PMID captured there.

## 2. Liew 2019 IJMS (photon UNIVERSE + DDRi) — text extract

See `../source/liew2019_ddr_hypoxia_photon.txt` (63 KB). Contains all model equations, K values
(Table 1), and RSF values (Table 3) used by this replication.

## 3. Mein 2019 Radiat Oncol (ion-beam UNIVERSE-RBE) — text extract

See `../source/mein2019_universe_rbe.txt` (82 KB). Contains the Kiefer–Chatterjee radial dose
distribution and per-ion RBE-LET curves anchoring the LET surrogate.

## 4. Liew 2020 Cancers (hypoxia HRF) — text extract

See `../source/liew2020_hypoxia_direct_indirect.txt` (52 KB). HRF parameterisation m = 2.94,
K = 0.129 %.

## 5. Liew 2022 IJMS repair companion — text extract

See `../source/liew2022_universe_repair.txt` (103 KB). Names UNIVERSE explicitly.

## 6. Liew 2022 IJMS FLASH companion — text extract

See `../source/liew2022_universe_flash.txt` (119 KB).

## 7. Scholz 2020 LEM-IV part 1 — text extract

See `../source/scholz2020_lemiv_part1.txt` (90 KB). LEM-IV cluster-complexity reference.

## Notes

- Full-text extracts are kept as separate files (not concatenated into this marker.md) to keep this
  file's on-disk size small and avoid multi-hundred-KB token spend on downstream sweeps.
- Downstream tools that need model equations should read the specific `.txt` file for the specific
  question (e.g., DDRi equations → `liew2019_ddr_hypoxia_photon.txt`).
