# paper.pdf MISSING

**Target paper:** Liew H., Meister S., Mein S., Tessonnier T., Kopp B., Held T., Haberer T., Abdollahi A., Debus J., Dokic I., Mairani A. *Combined DNA Damage Repair Interference and Ion Beam Therapy: Development, Benchmark and Clinical Implications of a Mechanistic Biological Model.* **Int J Radiat Oncol Biol Phys** 112(3):802–817 (2022; online 2021-10-25).

- **DOI:** 10.1016/j.ijrobp.2021.09.048
- **PMID:** 34710524
- **Publisher:** Elsevier
- **Access:** **CLOSED** (Unpaywall status `closed`; no PMC record; no arXiv/bioRxiv/medRxiv preprint located as of 2026-06-09 and re-checked 2026-07-06).
- **paper.pdf sha256:** N/A — no PDF present in this replication directory.

## Why no PDF

The target paper is Elsevier closed-access. It is not indexed in PubMed Central. There is no
publisher-hosted OA version. Semantic Scholar / Unpaywall / DataCite searches at replication time
returned no OA copy and no preprint. An institutional Elsevier subscription would be required to
legally obtain the PDF.

## What was done instead

Replication was grounded in the paper's abstract (via Semantic Scholar; see
`source/semantic_scholar_metadata.json`) plus the **five open-access twin/companion papers** that
fully specify the mechanistic model:

- Liew et al. 2019 IJMS (DOI 10.3390/ijms20236054) — photon UNIVERSE + DDRi equations (Eqs 1–7),
  Table 1 K_iDSB/K_cDSB, Table 3 RSF. OA CC-BY. In `source/liew2019_ddr_hypoxia_photon.pdf`.
- Mein et al. 2019 Radiat Oncol (DOI 10.1186/s13014-019-1295-z) — ion-beam Kiefer–Chatterjee
  track structure + UNIVERSE-RBE. OA CC-BY. In `source/mein2019_universe_rbe.pdf`.
- Liew et al. 2020 Cancers — hypoxia HRF. OA. In `source/liew2020_hypoxia_direct_indirect.pdf`.
- Liew et al. 2022 IJMS (DOI 10.3390/ijms23116268) — UNIVERSE repair companion (de-masks the
  model name). OA. In `source/liew2022_universe_repair.pdf`.
- Liew et al. 2022 IJMS — UNIVERSE FLASH companion. OA. In `source/liew2022_universe_flash.pdf`.

## For a future corpus sweep

If the target PDF becomes available (e.g. via an ANL Elsevier subscription or an author-provided
copy), drop it in as:

```
paper.pdf                (at slot dir root)
extraction/marker.md     (Marker parse)
extraction/nougat.mmd    (Nougat parse, GPU)
```

and recompute a sha256 for this file. The current `extraction/nougat.mmd` and `extraction/marker.md`
are stubs / OA-twin-derived; they will need replacement when a real paper.pdf lands.
