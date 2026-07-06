# Workflow — BVBRC-02-Ralstonia-Fluit2021

Reconstructed from REPORT.md (pass-1 + pass-2). Two passes; pass-2 is a strict superset of pass-1.

## Pass-1 pipeline (pre-existing artefacts)

1. **Input acquisition**
   - 18 clinical *Ralstonia* SRA read pairs → `data/sra/`.
   - Strain metadata table → `data/strain_info.tsv`.
   - ResFinder database snapshot → `data/resfinder_db/`.

2. **Assembly**
   - SPAdes v4.2.0 (`--only-assembler`, contig ≥500 bp).
   - Output: 18 assembled genomes → `data/genomes/*.fna`.
   - (Paper used SPAdes v3.11.1 `--careful`, contig ≥1000 bp — see method-audit drift.)

3. **Average Nucleotide Identity (ANIb)**
   - `pyani` BLAST-based ANIb over all-vs-all pairs of the 18 assemblies.
   - Output: `analysis/ani/` (BLAST files + matrix).

4. **Acquired AMR gene calls**
   - ResFinder BLAST per genome against `data/resfinder_db/`.
   - Output: `analysis/resfinder/` (per-strain BLAST results).

5. **Report-1 assembly**
   - Cross-check of the paper's abstract + hand-typed table 1 vs pass-1 numbers.
   - Output: `paper/paper_notes.md` (hand-curated), `report/REPORT.pass1.md`.
   - Pass-1 verdict: PARTIAL, coverage 6/10, agreement 8/10.

## Pass-2 pipeline (new work; supplements pass-1)

6. **Full-text PDF self-sourcing**
   - `paper/paper.pdf` fetched from `https://europepmc.org/articles/PMC8448721?pdf=render`
     (native PMC PDF was proof-of-work challenged).
   - `pdftotext -layout` → `paper/paper.txt`.
   - Trail: `PARSER_PROVENANCE.md`.

7. **Reference sequence pulls**
   - 16S: *R. pickettii* ATCC 27511 (`NR_043152.1`, 1491 bp) → `data/refs/Rpickettii_16S.fna`.
   - 16S: *R. mannitolilytica* → `data/refs/Rmannitolilytica_16S.fna`.
   - OXA-22 protein (`AAD12233.1`, 326 aa) → `data/refs/OXA-22.faa`.
   - OXA-60 protein (`YFD08942.1`, 271 aa) → `data/refs/OXA-60.faa`.

8. **Per-strain gene extraction**
   - Script: `code/repass/extract_and_tree.py`.
   - 16S: `blastn` ≥90% pid, ≥1000 bp. 14/18 clean hits; 4 R. pickettii strains (551631,
     551634, 551636, 551637) had 16S split across contigs → rescued by
     `code/repass/rescue_16S.py` (fragment stitch, 935–1464 bp consensus).
   - OXA-22 / OXA-60: `tblastn` ≥70% pid, ≥150 aa; best-bitscore hit; nucleotide region
     translated. 18/18 hits for each family.
   - Output: `results/repass/{16S,OXA22,OXA60}.fasta`, `results/repass/extract_summary.json`.

9. **Alignment**
   - `mafft --auto` (MAFFT 7.526) on each set.
   - Output columns: 1491 (16S) · 278 (OXA-22) · 271 (OXA-60).
   - Output: `results/repass/{16S,OXA22,OXA60}.aln.fasta`.

10. **ML phylogeny**
    - Nucleotide (16S): `FastTree -nt -gtr`.
    - Protein (OXA-22, OXA-60): `FastTree` JTT default.
    - Driver: `code/repass/build_trees.sh`.
    - Output: `results/repass/{16S,OXA22,OXA60}.nwk` + `.fasttree.log` (model + log-lik).

11. **Group-monophyly validation**
    - Script: `code/repass/validate_trees.py` (custom Newick parser).
    - For each paper-defined group (D1, D2, E1, E2, F, G) it checks whether the group's
      strains form a monophyletic clade in the ML tree; if not, reports the smallest
      containing clade + foreign tips inside it.
    - Output: `results/repass/tree_validation.json`.

12. **Report-2 assembly**
    - Cross-check pass-1 numbers + pass-2 new evidence vs the full-text PDF.
    - Discovered 3 additional testable claims (13 = 16S tree, 14 = OXA-22 tree,
      15 = OXA-60 tree) that pass-1 missed.
    - Promoted them from NOT_TESTED → PARTIAL.
    - Output: `report/REPORT.md` (pass-2 main), `report/REPORT.pass1.md` (pass-1 preserved
      verbatim), `PARSER_PROVENANCE.md`.
    - Pass-2 verdict: PARTIAL, coverage 8/10, agreement 8/10, zero contradictions.

## Deliberately NOT attempted (with reason)

- **MICs (Claims 11, 12)** — wet lab; no free in-silico substitute.
- **cgMLST 517-gene topology (Claim 16, Fig. 1)** — Ridom SeqSphere v5.0.0 is
  commercial. chewBBACA/PIRATE workaround is bounded (~1 analyst-day) but not done.
- **Full 78-tip 16S / 29-tip OXA-22 / 27-tip OXA-60 trees** — need to harvest 60
  reference 16S + 11 reference OXA-22 + 9 reference OXA-60 accessions from
  Supplementary Table 2. Bounded, not fundamental.
- **R. pickettii FDAARGOS-410 clustering with R. mannitolilytica D2** — need to add
  FDAARGOS-410 assembly. Bounded.
- **Full 8-group A–H ANIb** — need 57 GenBank genomes + 4 type-strain assemblies.
  Bounded.

## Compute constraints honoured throughout

- Free compute only. No Argo charges. No commercial tools.
- Tool set: BLAST+ 2.x, MAFFT 7.526, FastTree 2.1.11, Python 3 stdlib, Biopython 1.87.
