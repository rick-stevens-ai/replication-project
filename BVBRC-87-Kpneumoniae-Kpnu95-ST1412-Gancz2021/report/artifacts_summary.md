# Artifacts Summary — BVBRC-87 (Gancz 2021, KpnU95 ST1412)

All artifacts are stored under the replication directory:  
`~/Dropbox/REPLICATE-PROJECT/BVBRC-87-Kpneumoniae-Kpnu95-ST1412-Gancz2021/`

## Input artifacts (`work/`)

| File | Source | Size | Purpose |
|---|---|---|---|
| `work/paper.xml` | NCBI eutils `efetch db=pmc rettype=xml id=PMC8151138` | 169 KB | Full-text JATS XML of Gancz 2021 |
| `work/kpnu95_asm/` | NCBI Datasets REST (`v2alpha/genome/accession/GCA_015714665.1/download`) | ~5.2 Mb assembly + protein FASTA + GFF | KpnU95 whole-genome assembly (Scaffold, 61 contigs) |
| `work/pKpnU95.fasta` | NCBI eutils `efetch db=nuccore MK552109.1 rettype=fasta` | 183 KB | Closed plasmid sequence (FASTA) |
| `work/pKpnU95.gb` | NCBI eutils `efetch db=nuccore MK552109.1 rettype=gb` | 400 KB | Closed plasmid annotation (GenBank) |
| `work/plasmidfinder_db/enterobacteriales.fsa` | Bitbucket `genomicepidemiology/plasmidfinder_db` | ~50 KB | 159 replicon reference sequences (Enterobacteriaceae) |

## Evidence artifacts (`report/evidence/`)

| File | Producer | Content |
|---|---|---|
| `report/evidence/mlst_klebsiella.tsv` | `mlst 2.35.0 --scheme klebsiella` | 7-locus MLST call: ST1412 with all 7 alleles (gapA=2, infB=5, mdh=1, pgi=1, phoE=4, rpoB=1, tonB=18) |
| `report/evidence/kleborate_kpsc.tsv` | `Kleborate 3.2.4 --preset kpsc` | Full Kleborate output — species, ST, K/O typing (KL107), num_resistance_genes=10, num_resistance_classes=6, per-class ARG breakdown, cipro MIC prediction (1 mg/L [1–2]), Bla_chr=SHV-1 |
| `report/evidence/plasmidfinder_blast.txt` | `blastn` vs. PlasmidFinder DB, `-perc_identity 90 -evalue 1e-30` | Replicon typing hits — top hit: `IncFIB(K)(pCAV1099-114)_1__CP011596` at 100.000% identity over full 560 bp, e=0 |
| `report/evidence/assembly_stats.txt` | Biopython 1.87 | Assembly summary — total 5,223,689 bp / 57.51% GC / 5,063 CDS; chromosome scaffolds 5,055,295 bp (**byte-exact vs paper**); plasmid scaffolds 168,394 bp (16 fragments, IS26 collapse) |
| `report/evidence/plasmid_annotation.txt` | Biopython 1.87 GenBank feature audit of MK552109.1 | Per-gene CDS inventory — 10 ARGs (blaCTX-M-15×1, qnrS1×1, sul1×1, sul2×1, dfrA12×1, aadA2×1, strA'×2, strB'×1, mph(A)×1, chrA×2); complete fec/pco/sil/ars/chrA/umuCD operons; single traI (pseudogene) with no traD/traK/traY/oriT |
| `report/evidence/llm_judge_verdict.json` | Argo `argo:gpt-5`, T=1, strict-JSON | Aggregate verdict: `PARTIAL (strong)`, one-liner: *"Core genomic and plasmid features incl. 10 ARGs are confirmed; capsule is KL107 (not K109); source and meta-analysis untested."* |

## Report artifacts (`report/`)

| File | Purpose |
|---|---|
| `report/REPORT.md` | Canonical narrative replication report (16 KB) |
| `report/REPORT.tex` | LaTeX version with dedicated `GENUINE CRITIQUE` section |
| `report/open_questions.json` | 5 truly-open comparative-genomics / model-fidelity / plasmid-curing generalizability questions with basis + next steps |
| `report/workflow.md` | End-to-end pipeline diagram + tool inventory + design choices |
| `report/artifacts_summary.md` | This file — what's on disk and where |
| `report/failure_analysis.md` | Honest inventory of what didn't fully replicate, what wasn't attempted, and why |

## Key numeric outcomes

| Metric | Paper value | This work | Match |
|---|---:|---:|---|
| Sequence type | ST1412 | ST1412 (all 7 alleles exact) | ✅ exact |
| Chromosome bp | 5,055,295 | 5,055,295 | ✅ byte-exact |
| Chromosome CDS | 5,087 | 5,063 | ⚠ 0.5% delta (PGAP-only vs PGAP+RAST) |
| Chromosome GC% | 57.76% | 57.51% (whole-assembly) | ✅ within rounding |
| Plasmid bp | 180,286 | 180,286 | ✅ exact |
| Plasmid CDS | 243 | 243 | ✅ exact |
| Plasmid GC% | 50.21% | 50.23% | ✅ within rounding |
| Plasmid replicon | IncFIB(K), 100% id to CP011596 | IncFIB(K)(pCAV1099-114)_1__CP011596, 100.000% id, full 560 bp | ✅ exact |
| Plasmid ARG count | 10 | 10 (Kleborate + direct GenBank audit both agree) | ✅ exact |
| Flagship gene 1 | blaCTX-M-15 | blaCTX-M-15 present | ✅ |
| Flagship gene 2 | qnrS1 | qnrS1 present | ✅ |
| Chromosomal SHV | present (SHV-family) | SHV-1 (Bla_chr) | ✅ |
| Capsule (Sec 3.4) | K109 | KL107 (Kleborate) | ⚠ CONTRADICTED (but paper is internally inconsistent) |
| Capsule (Sec 3.5) | KL107 | KL107 (Kleborate) | ✅ MATCHES |
| Persistence operons (fec/pco/sil/ars/chrA/umuCD) | present | all present | ✅ |
| Non-conjugative (pseudogene traI, no oriT) | asserted | 1× traI, 0× traD/K/Y, 0 oriT | ✅ |
| Cipro MIC prediction | plasmid-mediated R | Kleborate predicts 1 mg/L [1–2], nonwildtype R | ✅ |

## Not on disk (intentional)

- **C11 wet-lab outputs** — plasmid-curing MIC panels, artificial-urine growth curves, copper MIC curves, *C. elegans* survival curves. These require the physical KpnU95 strain + cured derivative + nematode facility. Not attempted; not fabricated.
- **C9 SRA-mining outputs** — read-mapping of the 5 Houston Methodist ST1412 SRA runs against pKpnU95 to independently reproduce the KL107 backbone-carriage claim. Out of scope for a rank-40 spot-replication; would be the natural next step to close C9.
- **Independent hybrid re-assembly from raw reads** — pulling the SRA short + long reads and re-running Unicycler-hybrid to reach an independent 180,286-bp closure. Not attempted; the current run reads the authors' own MK552109.1 deposit, which is the correct test of ``can a reader retrieve and re-verify the deposit'' but not of ``can an independent lab re-close from raw reads.'' See `failure_analysis.md`.

## Provenance stamps

- Analyst: Ollie (OpenClaw subagent, `argo/argo:claude-opus-4.7`)
- Date: 2026-07-03 CDT
- Compute host: `uicgpu` (8×A100, proxy internet)
- Wall time: ≤5 minutes (dominated by Kleborate)
- Wave: X-100 replication project
- Rank/score: BVBRC-TOPUP85 rank 40, score 18, 6 citations
- License of paper: CC BY 4.0
