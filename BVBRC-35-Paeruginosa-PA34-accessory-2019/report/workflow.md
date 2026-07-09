# Workflow — BVBRC-35 (Subedi et al. 2019, *P. aeruginosa* PA34)

## Replication workflow (as executed)

1. **Claim extraction** — parsed Subedi 2019 into 14 testable claims (C1–C14): 8 computational pangenome/Venn, 3 genomic (MLST, virulence, AMR), 1 manual-comparative (GI count), 2 wet-lab (MIC, cytotoxicity).
2. **Genome acquisition** (NCBI Datasets v2 REST + nuccore efetch, free, no auth):
   - PA34: GCF_003332705.2 (chromosome CP032552); plasmids by GenBank accession MH547560.1, MH547561.1
   - PAO1: GCF_000006765.1; PA14: GCF_000014625.1; VRFPA04: GCF_000473745.2
   - Assembly IDs resolved from paper accessions via NCBI esearch (naive Datasets guess returned unrelated *Staphylococcus* — corrected in `attempt_log.md`).
3. **Genome statistics** — local FASTA parser (`work/genome_stats.py`).
4. **Uniform annotation** — Prokka 1.12 (Bacteria, genus *Pseudomonas*) on all four `.fna`; matches paper's "annotate all four with Prokka" method to avoid annotation bias.
5. **Pangenome** — Roary v3.12.0 at 95% BLASTP identity (default), core-alignment on, on the four Prokka GFFs → `summary_statistics.txt` + `gene_presence_absence.csv`.
6. **Venn decomposition** — `work/analyze_roary.py` parses presence/absence to reproduce Fig-1 (per-strain accessory, unique, PA34 no-ortholog vs each reference, PA34∩VRFPA04 exclusive).
7. **AMR / virulence** — abricate against ResFinder + CARD + VFDB on PA34 chromosome + both plasmids.
8. **MLST** — `mlst` (paeruginosa scheme).
9. **Verdict scoring** — LLM-judge via free Argo (`argo:gpt-5.2`) with claim-by-claim evidence; no regex.

## Tools / codes used

| Tool | Role |
|---|---|
| NCBI Datasets v2 REST / efetch | Genome retrieval (free) |
| Prokka 1.12 (conda env `bvbrc28`) | Uniform annotation |
| Roary 3.12.0 (conda env `bvbrc28`) | Pangenome / accessory decomposition |
| abricate + ResFinder + CARD + VFDB (env `bvbrc14`) | AMR + virulence screen |
| mlst (paeruginosa scheme) | Sequence typing |
| Custom `analyze_roary.py`, `genome_stats.py`, `judge.py` | Venn parsing + stats + LLM judging |
| Argo `argo:gpt-5.2` (free proxy) | LLM-as-judge scoring |

## Compute footprint

- Host: **uicgpu** (255 cores, conda envs bvbrc28 + bvbrc14)
- Prokka on 4 genomes: ~15-25 min
- Roary at 95% ID on 4 genomes: ~10-20 min
- abricate screens: ~2-5 min per DB
- LLM judge: 1 Argo call
- **Total effective effort: ~2-3 hours** (analyst + compute) for the computational-claim replication; extensions (parameter sweep in Q1, GI re-derivation in Q2, plasmid mobility in Q3) would each add 4-8 hours materially.
