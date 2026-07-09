# Artifacts Summary — BVBRC-73

Every output produced during the replication of Rahman et al. 2023 (MDR *A. veronii* Alim_AV_1000 from Bangladeshi stinging catfish, GCF_026738955.1).

## Report-level artifacts (`report/`)

| File | Purpose |
|------|---------|
| `REPORT.md`             | Canonical narrative replication report (13 claims, verdict PARTIAL). |
| `REPORT.tex`            | LaTeX version + dedicated Genuine Critique section. |
| `brief.md`              | Short summary of the replication. |
| `attempt_log.md`        | Running log of what was tried and when. |
| `artifact_harvest.md`   | Landing map for downloaded / generated files. |
| `open_questions.json`   | 5 truly open follow-up questions grounded in the paper's biology. |
| `workflow.md`           | End-to-end reproducible workflow. |
| `artifacts_summary.md`  | This file. |
| `failure_analysis.md`   | Detailed breakdown of what did not replicate + why. |

## Evidence artifacts (`report/evidence/`)

| File | Content | Verdict backed |
|------|---------|----------------|
| `claims_table.md`         | 13 falsifiable paper claims + per-claim verdict | ALL |
| `ani_skani.tsv`           | skani ANI matrix, 6 genomes (learned-ANI) | C11 (Replicated; target vs. B565 96.47%, vs. TH0426 96.34%, vs. FDAARGOS_632 96.33%; outgroups 87.81% / 85.87%) |
| `rRNA.gff`                | barrnap 0.9 output; 13 loci (11×5S + 1×16S + 1×23S) | C6 (Replicated exact) |
| `tRNA.txt`                | aragorn output; 96 tRNA | C5 (Partial; paper 102 RAST) |
| `card.tsv`                | abricate vs. CARD | C10 (β-lactam Replicated; tet ✗) |
| `ncbi.tsv`                | abricate vs. NCBI-AMR | C10 |
| `resfinder.tsv`           | abricate vs. ResFinder | C10 |
| `argannot.tsv`            | abricate vs. ARGannot | C10 |
| `megares.tsv`             | abricate vs. MEGARes | C10 |
| `vfdb.tsv`                | abricate vs. VFDB; 135 hits / 130 unique genes | C8, C9 (Replicated) |
| `mlst_analysis.txt`       | PubMLST REST scan; alleles gyrB=633, groL=91, gltA=340, metG=124, ppsA≈627 (new), recA=1460; ST 492's canonical alleles absent at every locus | C7 (CONTRADICTED) |
| `llm_judges_raw.json`     | Full JSON returns from 4 free judges (gpt-5.2, sonnet-4.5, gemini-2.5-pro, gpt-4.1) | Judge stage |
| `llm_judge_summary.json`  | Parsed scores + majority: 4/4 PARTIAL, mean Cov 8.75 / Agr 7.00 / Fid 7.50 / Rep 7.50 | Judge stage |

## Working artifacts (`work/`)

| Path | Content |
|------|---------|
| `work/paper.xml`               | PMC10636080 full text (parsed for claim extraction). |
| `work/genomes/*.fna`           | 6 downloaded assemblies (target + 3 A. veronii refs + 2 outgroups). |
| `work/annot/`                  | Prodigal (closed + open) + barrnap + aragorn intermediates for target. |
| `work/amr/`                    | Per-DB abricate outputs (5 AMR DBs). |
| `work/vf/`                     | abricate VFDB + PlasmidFinder outputs. |
| `work/ani_skani.tsv`           | Raw skani triangle (later copied to `report/evidence/`). |

## Key headline numbers (all from REPORT.md, not fabricated)

- Assembly: 4,494,464 bp / 58.87% GC / 93 contigs / longest 296,612 bp / N50 150,337 bp — matches paper's 4,494,515 / 58.87 / 93 essentially to the base.
- Annotation: 4,063 CDS (Prodigal closed) / 4,108 CDS (Prodigal open); 96 tRNA; **13 rRNA (exact match)**.
- Phylogeny: ANI to B565 96.47%, TH0426 96.34%, FDAARGOS_632 96.33%; *A. hydrophila* 87.81%, *A. salmonicida* 85.87%.
- Virulence: 135 VFDB hits (130 unique genes) covering T2SS (9), T3SS (37), T6SS (16), polar flagella (40), lateral flagella (17), MSHA/Tap/type-I pili.
- AMR: OXA-12 97.59% id, cphA4 96.19% id, rsmA 81.06% partial — five-way concordant.
- MLST: PubMLST alleles gyrB=633, groL=91, gltA=340, metG=124, ppsA best-match 627 at 99.44% (new), recA=1460 — no ST match across 2,755 STs; ST 492's canonical profile (112/347/44/217/384/381) absent at every locus.
- Judges: 4/4 PARTIAL (gpt-5.2, sonnet-4.5, gemini-2.5-pro, gpt-4.1). Mean scores C 8.75 / A 7.00 / F 7.50 / R 7.50.
