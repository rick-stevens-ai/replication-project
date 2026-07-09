# Replication Workflow — BVBRC-57 (Kang et al. 2020, *P. psychrotolerans* CS51)

**Analyst:** Ollie (OpenClaw AI subagent)
**Date:** 2026-07-02
**Verdict:** REPLICATED
**Free-endpoint compliance:** ✅ (NCBI, Europe PMC, Argo — no paid tools)

---

## 0. Compute environment

| Component | Host | Env | Notes |
|---|---|---|---|
| Paper retrieval, JSON parsing, LLM judge | local (m1 / CherryRd) | shell + Python 3 + Biopython | Europe PMC + NCBI eutils + Argo gpt-5.2 (`localhost:44497`, free) |
| Genome stats (length/GC/feature counts) | local | Biopython | parses FASTA + RefSeq PGAP GFF |
| AMRFinderPlus 4.2.7, abricate, mlst 2.33.1 | uicgpu (8×A100) | conda env **bvbrc14** | `amrfinder -n CS51.fna --plus`; abricate DBs: card, resfinder, vfdb, plasmidfinder, ncbi, bacmet2 |
| fastANI (species boundary) | uicgpu | conda env **bvbrc28** | CS51 vs 8 public *P. oryzihabitans* complete genomes |
| Prokka + Roary (pan-genome) | uicgpu | conda env **bvbrc28** | Prokka `--genus Pseudomonas`; Roary `-p 32 -e -n -i 90 -cd 99` on 9 conspecific genomes |

All GPU-adjacent tooling runs on uicgpu; no phenotypic (wet-lab) work.

---

## 1. Numbered workflow

### Step 1 — Paper + accession retrieval
- Europe PMC core search on PMID 32182882 (S2 API key) → PMC7142416 (CC-BY).
- Pull full-text XML from `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7142416/fullTextXML`.
- Extract GenBank accession **CP021645** from the Data Availability statement.
- Extract every reported numeric value (genome length, GC, rRNA/tRNA/CDS counts, core-gene count 2122).

### Step 2 — Accession → assembly resolution
- NCBI eutils `esearch` / `esummary` on CP021645 → assembly **GCF_006384975.1** (GCA_006384975.1).
- Note: NCBI organism = ***P. oryzihabitans*** strain CS51 (taxid 47885) — flag as post-publication reclassification.

### Step 3 — Genome download
- NCBI Datasets REST v2alpha (no auth):
  `genome/accession/GCF_006384975.1/download` with `GENOME_FASTA, PROT_FASTA, GENOME_GFF, CDS_FASTA`.
- md5s recorded in `report/artifact_harvest.md`.

### Step 4 — Genome statistics (local)
- Biopython parse of FASTA → length, contig count, GC%.
- RefSeq PGAP GFF parse → feature-type counts (CDS / gene / rRNA / tRNA / pseudogene).
- Protein FASTA count.
- Emit `report/evidence/genome_stats.json`.

### Step 5 — Functional gene detection (uicgpu, bvbrc14)
- (a) Grep RefSeq PGAP GFF product fields for each claimed category (Cu, Co-Zn-Cd, Ni, IAA/Trp, nitrate/nitrite, Pst, sulfate). → `report/evidence/pgp_metal_genes.txt`.
- (b) `amrfinder -n CS51.fna --plus` → check for acquired AMR.
- (c) `abricate` against **CARD, ResFinder, VFDB, PlasmidFinder, NCBI, BacMet2** for orthogonal cross-check (esp. BacMet2 for metal resistance).
- (d) `mlst 2.33.1` — no scheme (species has none).

### Step 6 — fastANI (uicgpu, bvbrc28)
- CS51 vs 8 public *P. oryzihabitans* complete genomes (accessions in `artifact_harvest.md`).
- Output: ANI matrix + closest neighbor.

### Step 7 — Pan-genome (uicgpu, bvbrc28)
- Prokka on all 9 genomes: `--genus Pseudomonas`, GFF output.
- Roary: `roary -p 32 -e -n -i 90 -cd 99 *.gff`.
- Read `number_of_conserved_genes.Rtab` and `number_of_genes_in_pan_genome.Rtab` for accumulation curves.
- Extract accessory-genome newick tree for phylogenetic placement of CS51.

### Step 8 — LLM judge
- Full claims table + results POSTed to Argo gpt-5.2 (`localhost:44497`) at temperature 0.
- Prompt asks for per-claim STRONG/MODERATE/WEAK + overall coverage %, agreement %, verdict recommendation.
- Store raw output in `report/evidence/llm_judge_gpt52.txt`.

### Step 9 — Verdict synthesis
- Aggregate per-claim tests → REPLICATED (with PARTIAL on C14 core-count).
- Draft `report/REPORT.md` and `report/REPORT.tex`.
- Draft honest critique section (no wet-lab, no antiSMASH, annotation label drift, pan-genome inputs are our choice).

---

## 2. Tools + versions

| Tool | Version | Provenance | Use |
|---|---|---|---|
| Biopython | current (conda) | local | FASTA/GFF parsing |
| AMRFinderPlus | 4.2.7 | bvbrc14 | acquired AMR check |
| abricate | current | bvbrc14 | 6 DB cross-check |
| BacMet2 | current | bvbrc14 (abricate DB) | metal-resistance orthogonal call |
| mlst | 2.33.1 | bvbrc14 | scheme check |
| fastANI | current | bvbrc28 | species-boundary |
| Prokka | current | bvbrc28 | uniform annotation |
| Roary | current | bvbrc28 | pan-genome |
| NCBI Datasets REST | v2alpha | public, no auth | genome download |
| Europe PMC REST | current | public + S2 API key | paper text |
| Argo proxy | localhost:44497 | free tunnel from studio-ts | gpt-5.2 LLM judge |

---

## 3. Work estimate

| Phase | Wall-clock | Notes |
|---|---|---|
| Paper + accession retrieval | ~15 min | Europe PMC + NCBI eutils, mostly network |
| Genome download + local stats | ~10 min | small (5.4 Mb) genome |
| Comparator downloads (8 genomes) | ~15 min | NCBI Datasets |
| AMRFinderPlus + abricate (6 DBs) + mlst | ~20 min | uicgpu, single genome |
| Prokka × 9 | ~25 min | uicgpu, parallel per-genome |
| Roary (9 genomes, -p 32, -i 90) | ~30 min | uicgpu |
| fastANI (1×8) | <5 min | trivial |
| LLM judge (Argo gpt-5.2, temp 0) | <2 min | single call |
| Report writing (REPORT.md + LaTeX) | ~60 min | manual synthesis |
| **Total** | **~3 hours** | end-to-end, one analyst |

Repeatable in <2 h if all comparator genomes and conda envs are pre-cached.

---

## 4. What was deliberately NOT done

- No wet-lab work (no MIC assays, no IAA quantification, no cucumber growth assay).
- No antiSMASH secondary-metabolite mining (flagged as an open question).
- No dDDH / GGDC taxonomic refinement (flagged as an open question).
- No re-execution of the paper's specific BPGA + cross-species pan-genome workflow (we deliberately chose Roary + conspecific comparison; the shape match still confirms the paper's qualitative pan-genome claim).

---

## 5. Reproducibility summary

Every artifact required to re-run this replication is captured under `report/`:
- Accessions + md5s → `artifact_harvest.md`
- Commands + tool versions → this file + REPORT.md §3
- Raw outputs (json/tsv/Rtab/newick/logs) → `report/evidence/`
- LLM-judge full output → `report/evidence/llm_judge_gpt52.txt`
- Human-readable report → `REPORT.md` and `REPORT.tex`

All external endpoints are free (NCBI, Europe PMC, Argo). No paywalled tools, no paid LLM calls.
