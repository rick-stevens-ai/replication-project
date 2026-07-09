# Artifacts Summary — BVBRC-57 (Kang et al. 2020, *P. psychrotolerans* CS51)

**Set:** BVBRC-57
**Verdict:** REPLICATED
**Compute:** local (m1 / CherryRd) + uicgpu 8×A100 (bvbrc14 + bvbrc28)
**LLM:** Argo gpt-5.2 (free, localhost:44497)

---

## 1. Report artifacts (this directory)

| File | Purpose | Bytes (approx) |
|---|---|---|
| `REPORT.md` | Canonical human-readable replication report + verdict | 10.6 KB |
| `REPORT.tex` | LaTeX rendering of the same report with dedicated Genuine Critique | ~16 KB |
| `open_questions.json` | 5 structured open questions grounded in CS51 biology | ~7 KB |
| `workflow.md` | Numbered workflow + tools + versions + work estimate | ~6 KB |
| `artifacts_summary.md` | This file — inventory of everything produced | ~5 KB |
| `failure_analysis.md` | Honest failure analysis (shortcuts, misses, unverified) | ~7 KB |
| `artifact_harvest.md` | Accessions, md5s, download provenance for every input genome | (existing) |

---

## 2. Input artifacts (from public archives)

| Artifact | Source | Provenance | Notes |
|---|---|---|---|
| Paper full-text XML | Europe PMC `PMC7142416` | REST `fullTextXML` | CC BY 4.0 (MDPI) |
| GenBank record `CP021645` | NCBI GenBank | eutils esearch/esummary | Referenced in Data Availability |
| Assembly `GCF_006384975.1` | NCBI Datasets REST v2alpha | `genome/accession/…/download` | GENOME_FASTA, PROT_FASTA, GENOME_GFF, CDS_FASTA |
| 8 comparator genomes (*P. oryzihabitans*) | NCBI Datasets | REST | GCF_001913135.1 (PRS08-11306), GCF_050155825.1 (R1), GCF_008693825.1 (FDAARGOS_657), GCF_014522265.1 (KNF2016), GCF_024652905.1 (YY7), GCF_003293465.1 (MS8), GCF_051136255.1 (Lu_Sq_012), GCF_001518815.1 (USDA-ARS-56511) |

All exact accessions + md5s captured in `report/artifact_harvest.md`.

---

## 3. Evidence artifacts (`report/evidence/`)

| File (or family) | Producer | Content |
|---|---|---|
| `genome_stats.json` | Biopython (local) | length, contig count, GC%, feature counts (CDS/gene/rRNA/tRNA/pseudogene), protein count |
| `pgp_metal_genes.txt` | grep on RefSeq PGAP GFF product fields | per-category hit lists for C7–C13 (Cu, Co-Zn-Cd, Ni, IAA/Trp, nitrate/nitrite, Pst, sulfate) |
| AMRFinderPlus output | uicgpu bvbrc14, `amrfinder -n CS51.fna --plus` | acquired-AMR check — negative (expected) |
| abricate outputs (×6 DBs) | uicgpu bvbrc14 | CARD, ResFinder, VFDB, PlasmidFinder, NCBI, **BacMet2** — BacMet2 is the orthogonal metal-resistance cross-check |
| mlst output | uicgpu bvbrc14 | no scheme available for species |
| fastANI matrix | uicgpu bvbrc28 | CS51 vs 8 conspecific comparators (see §5.4 for values) |
| Roary `number_of_conserved_genes.Rtab`, `number_of_genes_in_pan_genome.Rtab` | uicgpu bvbrc28 | pan/core accumulation curves |
| Roary accessory-genome newick tree | uicgpu bvbrc28 | phylogenetic placement — CS51 sister to PRS08-11306 |
| Prokka GFF × 9 | uicgpu bvbrc28 | uniform annotations feeding Roary |
| `llm_judge_gpt52.txt` | Argo gpt-5.2 @ temp 0 | per-claim strength + verdict recommendation |

---

## 4. Trace of key numeric results

| Metric | Paper | Replication | Delta | Verdict |
|---|---|---|---|---|
| Genome length (bp) | 5,364,174 | 5,364,174 | 0 | ✅ EXACT |
| GC content | 64.71% | 64.71% | 0 | ✅ EXACT |
| rRNA | 15 | 15 | 0 | ✅ EXACT |
| tRNA | 67 | 67 | 0 | ✅ EXACT |
| CDS | ~4774 | 4846 | +72 (+1.5%) | ✅ CLOSE (pipeline drift) |
| Genes | ~4859 | 4837 | −22 | ✅ CLOSE |
| Proteins | (implicit) | 4714 | — | (+90 pseudogenes) |
| Core genes | ~2122 (cross-species BPGA) | 2790 (conspecific Roary) | +668 | ⚠️ PARTIAL (different experiment) |
| Closest ANI | PRS08 (relationship stated) | PRS08-11306 @ 94.09% | — | ✅ REPRODUCES |

---

## 5. LLM-judge trace summary

Argo gpt-5.2 (free), temperature 0:
- **STRONG:** C1, C2, C3, C4, C5, C7, C8, C9, C10, C11, C12, C13, C15
- **MODERATE:** C6 (pipeline-dependent counts)
- **WEAK:** C14 (shape yes, count no — different genome set + tool)
- **Overall coverage:** 100%
- **Overall agreement:** 93%
- **Recommended verdict:** REPLICATED

Full text: `report/evidence/llm_judge_gpt52.txt`.

---

## 6. Provenance / free-endpoint compliance

| Endpoint | Used for | Cost |
|---|---|---|
| NCBI eutils | accession resolution | free |
| NCBI Datasets REST v2alpha | genome downloads | free |
| Europe PMC | paper XML | free (S2 API key for search) |
| Argo proxy `localhost:44497` | gpt-5.2 LLM judge | free (Argonne) |
| uicgpu 8×A100 | AMRFinder/abricate/mlst/fastANI/prokka/roary | free (institutional) |

No paid `pdf` tool. No paywalled sources. No paid LLM calls.

---

## 7. What is NOT in the artifact set (intentional)

- No PacBio raw reads or reassembly (we used the deposited assembly).
- No antiSMASH BGC output (deferred; called out as an open question).
- No dDDH / GGDC taxonomic output (deferred; open question).
- No wet-lab MIC / IAA / gibberellin / cucumber-growth data (out of scope — no wet lab).
- No BPGA output (we used Roary; the paper's exact BPGA output was deliberately not reproduced).
