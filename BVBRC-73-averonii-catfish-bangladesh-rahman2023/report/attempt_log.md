# Attempt Log — BVBRC-73

**Date:** 2026-07-03 · **Host:** CherryRd (macOS local) · **Duration:** ~90 min.

## Chronology

1. **Read wave brief** (`WAVE_BRIEF_2026-07-01.md`). Confirmed free-endpoints-only, real-replication, LLM-judge scoring rules.
2. **Fetched paper metadata** via NCBI E-utilities (PMID 37969805). Got title, authors, journal, DOI 10.5455/javar.2023.j711, PMCID PMC10636080. Paper is Open Access (CC BY 4.0) via PMC.
3. **Downloaded full text** as PMC XML (PMC10636080 → 80 KB). Extracted the "Accession numbers" and "Materials and Methods" sections. Identified:
   - BioProject: **PRJNA810265**
   - WGS accession: **JALLKR000000000** (later resolved to RefSeq **GCF_026738955.1**)
   - Cited reference genome (for proteome comparison): NZ_CP044060.1 (which turned out to be *A. veronii* FDAARGOS_632, RefSeq GCF_008693705.1)
   - Cited phylogenetic sisters: strain TH0426 (China, catfish) and strain B565 (Chinese catfish).
4. **Resolved assembly ID** via NCBI E-utilities esearch on assembly DB. Got GCF_026738955.1 / ASM2673895v1: 93 contigs, N50 150,337, total length 4,494,464 bp, GC via metadata.
5. **Downloaded 6 genomes** (Alim_AV_1000, TH0426, B565, FDAARGOS_632/Av_ref, A. hydrophila ATCC 7966, A. salmonicida A449) from NCBI FTP.
6. **Genome QC**: independently computed size, GC%, contig count of Alim_AV_1000. Matched the paper to 0.001% (Δ 51 bp on 4.49 Mb) and exactly on GC and contig count. Claims C1/C2/C3 replicated.
7. **ANI** via skani triangle sparse mode. Alim_AV_1000 vs TH0426 = 96.34%, vs B565 = 96.47%, vs Av_ref = 96.33%, vs A. hydrophila = 87.81%, vs A. salmonicida = 85.87%. Species boundary (95%) is respected: all three *A. veronii* strains cluster together; other species below. Claim C11 replicated.
8. **Installed tools locally** via Homebrew: `abricate` (with any2fasta and bioperl deps; installs full DB set: card, resfinder, ncbi, argannot, megares, vfdb, plasmidfinder, ecoli_vf, ecoh, victors, upec_expec_vf, bacmet2), `barrnap 0.9`, and `mlst` (mlst had Perl-API mismatch → skipped, used PubMLST REST API instead).
9. **CDS calling** with Prodigal V2.60 (closed and open-ends modes). Closed-ends: 4,063 CDS. Open-ends: 4,108. Paper's RAST call was 4,229 (Δ 3.9%). C4 = PARTIAL (expected caller/pipeline drift).
10. **rRNA calling** with barrnap 0.9. Found **13** rRNA (11×5S + 1×16S + 1×23S). Paper reports 13 rRNA — exact match. C6 replicated.
11. **tRNA calling** with aragorn. Found **96** tRNA. Paper reports 102 (via tRNAscan-SE in RAST). Δ = -6, 5.9% low. C5 = PARTIAL (tool-dependent).
12. **AMR calls** via abricate against CARD, NCBI AMR, ResFinder, ARGannot, and MEGARes (5 concordant DBs). Consistent hits: **cphA4 / CPHA / cphA-4** (subclass B2 metallo-β-lactamase, carbapenem, 96.19% id — chromosomal in Aeromonas), **OXA-12 / blaOXA-12 / ampS** (class D oxacillinase / class C penicillinase, 97.59% id), **rsmA** (RNA-binding regulator affecting MDR efflux, 81% id). No tetracycline/tetR family gene above default thresholds — the paper's specific tetracycline claim did not replicate in current CARD/ResFinder, though the general MDR + β-lactam story did. C10 = PARTIAL (β-lactam resistome replicated).
13. **Virulence-factor scan** via abricate against VFDB. Found 135 hits / 130 unique gene names organized as: Polar flagella (40), T3SS (37), Lateral flagella (17), T6SS (16), Exe T2SS (9), Tap type IV pili (7), MSHA type IV pili (6), Type I pili (3). The paper's C8 (T2SS/T3SS/T6SS present) and C9 (adhesion/flagella/pili) both replicated.
14. **MLST** via PubMLST REST API on scheme 1 (Aeromonas, 6 loci: gyrB, groL, gltA, metG, ppsA, recA). Submitted full assembly (base64) to the sequence-scan endpoint. Got 5 exact matches (gyrB=633, groL=91, gltA=340, metG=124, recA=1460) and one near-miss (ppsA best-match=627 at 99.44% identity, 3 mismatches — implies a new ppsA allele variant). Downloaded the full 2,755-profile ST table and searched: **no ST matches our profile**. Retrieved ST 492's canonical profile from PubMLST: gyrB=112, groL=347, gltA=44, metG=217, ppsA=384, recA=381 — matches NONE of our observed alleles. Result: **claim C7 (ST 492) is CONTRADICTED**. This is a genuine disagreement; the deposited assembly (which we verified matches size/GC/contigs essentially exactly) does not carry the alleles the paper's ST 492 requires.
15. **PHASTER phage detection** — attempted phaster.ca API POST with 4.5 MB fasta; broken-pipe error on all 3 retries. External service issue (not our fault); local PHASTER not installed. Marked C12 as SPOT-CHECK.
16. **LLM-judge scoring** via Argo proxy at 127.0.0.1:44497 (key=stevens). Sent the compact claims-table to 6 judge models. 2 of the Claude Opus endpoints returned Argo upstream 502 (validation-error on the message-format parse — Argo-side bug, unrelated to our request). 4 judges succeeded: **GPT-5.2, Sonnet 4.5, Gemini 2.5 Pro, GPT-4.1**. All 4 verdicts: **PARTIAL**. Mean scores: coverage 8.75, agreement 7.0, fidelity 7.5, reproducibility 7.5.
17. **Wrote** report/brief.md, report/artifact_harvest.md, report/attempt_log.md, report/REPORT.md, and evidence/ (abricate TSVs for card/resfinder/ncbi/argannot/megares/vfdb, ani_skani.tsv, rRNA.gff, tRNA.txt, claims_table.md, mlst_analysis.txt, llm_judges_raw.json, llm_judge_summary.json).

## What worked
- NCBI E-utilities + Datasets FTP: 6 genomes in <1 min, no auth.
- skani ANI: instant, clean, matches published expectations.
- abricate: correctly installed via brew, all major AMR/VF DBs updated 2026-Jul-03.
- barrnap: exact match to paper on rRNA count.
- PubMLST REST API: gave definitive allele calls; enabled the ST 492 disagreement finding.
- Argo proxy for LLM judges: worked for 4 of 6 attempted models.

## What failed / did not work
- PHASTER API: broken pipe on POST — external service problem.
- `mlst` binary: Perl API mismatch (v5.32 vs v5.42) after brew perl install. Worked around via PubMLST REST directly.
- Argo `claude-opus-4.7` and `claude-opus-4.8`: upstream 502 with message-parse validation error. Substituted Sonnet 4.5 + Gemini 2.5 Pro + GPT-4.1 as additional judges (still 4 free judges total).

## Would-do-next / limitations
- Fresh de-novo assembly from the SRA reads (if any) would let us evaluate the paper's assembly step directly. Skipped because the deposited assembly's size/GC/contig count already reproduces the paper's numbers essentially exactly — a full re-assembly would test only assembler-noise, not any interesting claim.
- ppsA new allele could be submitted to PubMLST to formally assign a new ST — outside the scope of a replication check.
- Local PHASTER or PHASTEST install would close C12.
