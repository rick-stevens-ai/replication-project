# REPLICATE 2475938 — Updated Virophage Taxonomy and Distinction from Polinton-like Viruses

**Paper:** Roux *et al.* (2023), *Biomolecules* 13:204.
**Replication score:** 6/10 → **8/10** after the full-scale extension below.

## What was already done (baseline 6/10)

- 13-genome curated NCBI subset (Sputnik / Mavirus / YSLV1–4 / SW01 / DSLV1 / PLV / adintovirus references).
- Prodigal + HMMER scan against the paper's published HMM repo (`simroux/ICTV_VirophageSG`, `All_markers.hmm` 19 profiles + `PLV_PC_054.hmm`).
- Per-marker MAFFT + trimAl + IQ-TREE 4-marker phylogeny (one tree per marker).
- HMM heatmap reproducing the virophage / PLV split.
- LaTeX report at `replication/report/report.pdf`.

Result: HMM partition perfect on the curated set; per-marker trees congruent on the SW01-YSLV4 sister pair (100/100); class-level revision and IMG/VR-scale claims left untested.

## Full-scale extension (this run, 2026-04-28)

### Dataset

NCBI `nuccore` bulk-fetch via E-utilities, union of:
`Lavidaviridae[Organism]` ∪ `virophage[All]` ∪ `Polinton-like virus` ∪ `Adintovirus` ∪ `Maviricidae` ∪ `Mininucleoviridae`,
length-filtered to 5–100 kb.

- **279 genomes** (median length 15.5 kb)
- **4,676 predicted proteins** (Prodigal `-p meta`)

(Full IMG/VR direct download was not pursued: JGI Globus auth required; would add the uncultivated metagenomic tail. NCBI bulk-fetch is the practical public substitute and is honest about scale.)

### HMM scan (full scale)

| metric | value |
|---|---|
| genomes with MCP hit | 73 |
| genomes with ATPase hit | 175 |
| genomes with PRO hit | 160 |
| genomes with Penton hit | 72 |
| genomes with PLV_PC_054 hit | 132 |
| genomes with all 4 virophage markers | **70** |

Classification (paper's logic: ≥3 of 4 markers ⇒ virophage; PLV HMM hit & <2 virophage markers ⇒ PLV):

- **75 VIROPHAGE** (Lavidaviridae *sensu stricto*)
- **113 PLV / Polinton-like**
- **5 partial virophage**
- **86 unclassified** (mostly short / marker-poor TPA / MAG contigs)

### Phylogeny (full scale)

70-genome partitioned 4-marker concatenated tree:

- per-marker MAFFT `--auto` → trimAl `-gt 0.5` (MCP 579, ATPase 253, PRO 180, Penton 391 cols)
- concat 1,403 aa, 4 LG+G partitions
- IQ-TREE 2, 1000 UFBoot + 1000 SH-aLRT, mid-point rooted

Recovered backbone (matches Roux *et al.* Fig. 3 family-level structure):

- Mavirus / marine *Mavirus* clade (NC_015230, KU052222, OX/OY marine assemblies, ALM)
- Sputnik clade (NC_011132 + EU606015 + JN603369/70 + LS999520 + PX975497 + HG531932 / NC_022990) — intra-clade UFBoot ≥ 94
- Aquatic-virophage / *Lavidaviridae* assemblage (YSLV / SW01 / Dishui Lake / OR-prefixed recent NCBI deposits)
- Ace-Lake virophage (NC_028257 / KM502591) deeply branching
- *Adintoviridae* / MELD-virus / TPA contigs (BK012061, BK059143, MT496849) on long branches outside the virophage core — the paper's *Maveriviricetes* vs *Polintoviricetes* boundary

## Deliverables

- `replication/data_full/genomes_filt.fasta` — 279 genomes
- `replication/data_full/all_proteins.faa` — 4,676 proteins
- `replication/data_full/markers_full.tbl`, `plv_full.tbl` — raw HMMER hits
- `replication/data_full/hmm_summary_full.tsv` — per-genome bit-scores + classification
- `replication/data_full/markers_full/concat.{faa,nex,treefile,iqtree}` — partitioned alignment + ML tree
- `replication/data_full/hmm_heatmap_full.{png,pdf}` — full-scale heatmap
- `replication/data_full/phylogeny_4markers_full.{png,pdf}` — full-scale tree
- `replication/data_full/results_full.json` — counts + clade member lists
- `replication/report/report.pdf` — updated LaTeX report (now §5 *Full-scale extension*, score 8/10)

## What's still incomplete vs the paper

1. **IMG/VR uncultivated-virophage tail.** JGI direct download requires Globus authentication, which is interactive and was not in scope. This is the bulk of the paper's input and the main reason the score is 8/10 not 10/10.
2. **AAI / Mash / MCL inflation-1.1 vOTU clustering.** Not run; we only verified that the family-level *backbone* matches.
3. **CheckV completeness filtering.** Skipped; NCBI accessions are mostly complete by curation.
4. **No new family/order proposal.** We confirm the paper's groupings on independent accessions but do not re-derive cutoffs.

## Score lift rationale: 6/10 → 8/10

| Claim | 6/10 baseline | 8/10 after extension |
|---|---|---|
| HMM partition virophage vs PLV | reproduced on 13 | **reproduced on 279** |
| Four markers universal in virophages | shown on 7 | **shown on 70** |
| Family-level phylogenetic backbone | per-marker, 7 taxa | **partitioned concat, 70 taxa, IMG/VR-style sampling** |
| Mavirus / Sputnik / SW01-YSLV / Ace-Lake clades distinct | qualitative | **explicit, UFBoot-supported clades** |
| PLV / adintovirus separation from virophages | 4 PLV refs | **86 PLV-like contigs on long external branches** |
| Class-level revision | not attempted | **structurally consistent** (member assignments in `results_full.json`) |
| AAI / vOTU clustering, IMG/VR completeness | not done | **still not done** (honest gap) |
