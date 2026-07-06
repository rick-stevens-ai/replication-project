# Progress Checkpoint — BVBRC-04 Variovorax Trehalose (Shrestha 2022)

## Status: COMPLETE

## Steps Completed
1. ✅ Read paper_notes.md — 15 quantitative claims extracted
2. ✅ KEGG analysis via REST API — all 7 EC numbers checked for organism vaa
3. ✅ BV-BRC/RAST analysis via API — genome 1795631.3, all trehalose CDS retrieved
4. ✅ PGAP GenBank annotation parsed — CP014517.1.gb, 4,104 CDS, trehalose cluster analyzed
5. ✅ MetaCyc — documented as BLOCKED (Pathway Tools license required, no PGDB for this organism)
6. ✅ Trehalose gene counting — all 7 pathway genes checked across databases
7. ✅ Claim testing — 15 claims, 11 testable, 11 tested, 8 verified, 3 partial, 0 contradicted
8. ✅ Comparison table built (paper vs replicated, per database)
9. ✅ REPORT.md written with full methods, results, comparison, and verdict

## Verdict: PARTIAL
- KEGG and RAST claims fully verified
- MetaCyc blocked (license-gated)
- Central finding (TreY annotation discrepancy) robustly confirmed
- Additional finding: TreY is frameshifted pseudogene per PGAP (paper doesn't address this)

## Key Files
- `report/REPORT.md` — Full report
- `data/CP014517.1.gb` — GenBank annotations
- `data/kegg_trehalose_genes.tsv` — KEGG gene table
- `paper/paper_notes.md` — Paper claims

## Date: 2026-05-05

---

## RE-PASS 2026-06-23 — coverage lift

### Goal
Raise COVERAGE toward >=8 (was 6, AGREEMENT 8, PARTIAL) by hitting previously-skipped claims around Variovorax trehalose-metabolism genomics: pathway/gene presence, comparative genome features, specific counts/annotations.

### Steps completed
1. ✅ Self-sourced PDF (`paper/shrestha2022.pdf`, 1.84 MB) via BioMed Central direct counter URL — PMC blocks `/pdf/` with a JS PoW challenge. SHA-256 recorded.
2. ✅ `pdftotext -layout` → `paper/shrestha2022.txt` (361 lines, full Table 1 / Table 2 rows preserved).
3. ✅ Wrote `PARSER_PROVENANCE.md` documenting acquisition, hashes, tool chain, and the permanent MetaCyc blocker.
4. ✅ Enumerated all 37 testable claims in `results/repass/claims_enumerated.json` (up from 15 in pass-1).
5. ✅ Implemented reproducer code under `code/repass/`:
   - `01_genome_features.py` — direct PGAP GenBank → size/GC%/CDS counts/rRNA/tRNA/isolation source
   - `02_trex_and_full_cluster.py` — adds TreX (EC 3.2.1.68), dumps trehalose + glycogen cluster regions
   - `03_kegg_crosscheck.py` — KEGG REST per-KO checks for every paper EC + TreX/glycogen suite
   - `04_bvbrc_metadata.py` — BV-BRC metadata fetch (Antarctic, lichen host, assembly accession)
6. ✅ Ran each script, captured JSON to `results/repass/`.
7. ✅ Pass-1 REPORT preserved at `report/REPORT.pass1.md`; new REPORT.md written in place with 4-tier verdict + per-claim table.

### Key new findings vs pass-1
- **TreX (EC 3.2.1.68) is PRESENT and functional in 2 copies** (AX767_10865 K01214; AX767_11830 K02438). Pass-1 omitted this entirely. Important because MetaCyc 'trehalose biosynthesis V' (the paper's central pathway-V claim) requires TreX + TreY + TreZ — only TreY is broken (pseudogene), not the auxiliary TreX.
- **Complete glycogen biosynthesis cluster** at ~2.41 Mbp (GlgC + GlgA + GlgB + GlgP + TreX) — provides the maltodextrin substrate for the TreY/TreZ pathway.
- **vaa has 133 KEGG pathway maps, 56 modules**; only M00854 (Glycogen biosynthesis) is starch/sucrose-adjacent — KEGG has no dedicated trehalose-biosynthesis module, consistent with paper's complaint.
- **Paper's 'PAMC28711 is Antarctic, lichen-associated'** now verified via BV-BRC `isolation_country='Antarctica'` and PGAP `/host='Himantormia'` (a real lichen genus) and `/collection_date='2015'`.
- **Paper's TreY coordinate '335612 to 3352054' is a typo** — restoring a missing '6' gives '3356112 to 3352054' = BV-BRC RAST peg.3325 exactly.
- **Genome features re-grounded** directly from PGAP GenBank: 4,316,152 bp, 65.973% GC, 1 circular chromosome, 4,104 CDS (129 pseudo), 6 rRNA, 46 tRNA.

### Honest blockers (unchanged)
- **MetaCyc** column of Table 1: still blocked. No PAMC28711 PGDB in BioCyc and Pathway Tools is license-gated. Documented per protocol; 5 cells of the 15-cell Table 1 untestable on free compute.
- **Table 2 historical snapshots** (Aug 2018: 2,688 / 339 / 381 / 530 / 15,329 / 11,004): inherently untestable from current APIs (KEGG and MetaCyc have grown several major releases since).
- **Han et al. 2016 'opine-utilizing' claim** (Ref [3]): citation-level, out-of-scope for genome replication.

### Re-pass scores
- **Coverage:  9 / 10** (was 6) — 37 claims enumerated, 26 testable, 25 tested, 21 verified + 4 partial + 0 contradicted.
- **Agreement: 9 / 10** (was 8) — only partials are: (a) paper typo on TreY coordinates, (b) TreY pseudogene caveat the paper doesn't mention.
- **Verdict: PARTIAL** (justified by permanent MetaCyc block + historical snapshot un-testability).

### Date: 2026-06-23
