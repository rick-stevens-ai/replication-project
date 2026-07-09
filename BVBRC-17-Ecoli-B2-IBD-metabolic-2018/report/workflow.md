# Workflow — Fang et al. (2018) replication

**Paper:** Fang X et al., *BMC Systems Biology* 12:66 (2018). DOI 10.1186/s12918-018-0587-5.
**Verdict:** PARTIAL REPLICATION (strong).
**Effort:** ~3 min laptop wall-clock end-to-end; ~1–2 weeks analyst time cumulative across three passes (2026-06-17 spot-check, 2026-06-25 FBA upgrade, 2026-06-27 genomic upgrade).

---

## 0. Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install cobra biopython
# BLAST+ 2.x from Homebrew / apt / bioconda: makeblastdb, tblastn, blastn
```

Python 3.14, COBRApy 0.31.1, Biopython 1.87, GLPK solver (COBRApy default), BLAST+ 2.x.

---

## 1. Corpus availability check (C1, C2)

- Europe PMC REST API for bibliographic + abstract.
- BV-BRC public API confirmed 5,737 complete E. coli genomes indexed (vastly exceeds paper's 110-strain corpus).

---

## 2. Download reference genomes (C2, C5, C6)

Four canonical strains via NCBI Datasets v2alpha REST (free, no auth):

```bash
for acc in GCA_000284495.1 GCA_000013265.1 GCA_000183345.1 GCF_000005845.2; do
  curl -sS -o "${acc}.zip" \
    "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/${acc}/download\
?include_annotation_type=PROT_FASTA&include_annotation_type=GENOME_FASTA"
  unzip -q "${acc}.zip" -d "${acc}"
done
```

- `GCA_000284495.1` — LF82 (AIEC, Crohn's reference, B2)
- `GCA_000013265.1` — UTI89 (UPEC reference, B2)
- `GCA_000183345.1` — NRG857c (AIEC, B2)
- `GCF_000005845.2` — K-12 MG1655 (A, positive control)

Then `python3 genome_stats.py` → `genome_stats.json` (Biopython 1.87 parses `.fna` + `protein.faa`).

---

## 3. Direct genomic verification of C5 (central B2 loss-of-function claim)

```bash
# Extract K-12 frl operon proteins by accession (frlA/B/C/D/R) → frl_query.faa
# Build BLAST dbs
for g in GCA_000284495.1 GCA_000013265.1 GCA_000183345.1 GCF_000005845.2; do
  makeblastdb -in genomes/$g/*.fna -dbtype nucl -out blast/${g}_db
done
# tblastn frl proteins vs. each genome
python3 frl_blast.py     # → blast/*_frl.tsv + blast/frl_presence.json
```

**Presence rule:** pident ≥ 70%, coverage ≥ 70% of query, e-value ≤ 1e-30.

Result: **frl operon ABSENT (0/5 genes) in all 3 B2 strains, PRESENT (5/5) in K-12.**

---

## 4. 17-gene sanity panel (C3)

`python3 metabolic_survey.py` → `metabolic_survey.json`.

Panel: nagA/B/K, galE/K/T, fucA/I/K/P, nanA/K/E, agaA/S/Y, frlA/B/C/D/R.

Result: **16 shared genes conserved ≥96% in all 3 B2 strains; only the 5-gene frl operon uniformly absent.** Clean single-operon loss signature.

---

## 5. Independent phylogroup assignment (C6)

`python3 clermont.py` → `clermont_results.json`.

- Encode 4 Clermont (2013) quadruplex primers (chuA, yjaA, TspE4.C2, arpA).
- `blastn -task blastn-short -word_size 7 -dust no`, ≥85% identity, ≥85% length coverage.
- Require forward + reverse hits on same contig, opposite strands, at expected amplicon distance.
- Map (chuA, yjaA, TspE4.C2, arpA) presence vector through Clermont 2013 decision table.

Result: LF82 = B2, UTI89 = B2, NRG857c = B2, K-12 = A. **4/4 agreement with paper.**

---

## 6. FBA on reference GEMs (C4a–d)

Download BiGG models:
- `iML1515.json` (2,712 rxns, 1,877 mets, 1,516 genes) — K-12 reference
- `iJO1366.json` — earlier K-12 reference

Defined M9 minimal medium:
- NH4, Pi, SO4, K, Na, Mg, Ca, Fe2/3, Cl, CO2, H, H2O, O2, trace metals
- All carbon exchanges closed
- Open one test carbon at 10 mmol·gDW⁻¹·h⁻¹
- Aerobic, `cobra.Model.optimize()` (GLPK)

```bash
python3 fba_table1.py    # Table 1 substrates
python3 fba_mucus.py     # Fig. 3b mucus glycans
```

Outputs: `table1_results.json`, `fba_results.json`.

Result: 6/8 Table-1 substrates match paper qualitative growth call; xanthosine + XMP within paper's within-phylogroup variance; GalNAc alone gives μ = 0 (K-12 fails), consistent with B2 TBP-aldolase advantage thesis.

---

## 7. GPR-level mechanism cross-check

Walk GPRs of FRULYSt2pp, FRULYSDG, FRULYSK, FRULYSE, PSCLYSt2pp in iML1515; confirm they map to frlA/B/C/D. Combined with §3, closes the mechanism chain: **B2 loss of frlA/B/C/D ⇒ FBA infeasibility on fructoselysine/psicoselysine**.

---

## 8. Not done (PARTIAL → REPLICATED gap)

1. 110-strain pan-genome (Roary / PanX / CD-HIT 80%).
2. Per-strain GEM reconstruction for all 110 strains via CarveMe or KBase.
3. 649-substrate FBA panel per strain (Fig. 3a).
4. Fig. 1a / 3a heatmaps.
5. IBD-53-isolate strain-to-BV-BRC accession mapping.

Estimated remaining work: ~1–2 weeks analyst time on a single 16–32 GB workstation. No commercial software, GPUs, or restricted data required.

---

## 9. Reproducibility one-liner

Full pipeline (post-env setup):

```bash
python3 genome_stats.py && \
python3 frl_blast.py && \
python3 metabolic_survey.py && \
python3 clermont.py && \
python3 fba_table1.py && \
python3 fba_mucus.py
```
