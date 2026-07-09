# Attempt Log — BVBRC-48 (Acinetobacter baumannii MRSN 56, Harmer 2022)

Analyst: Ollie (OpenClaw subagent) — Replication Wave 2026-07-01
Compute: uicgpu (8×A100 host; conda envs bvbrc28 = datasets/prokka/blast, bvbrc14 = amrfinder/mlst/abricate). LLM-judge: free Argo (argo:gpt-5.2).

## Chronological

1. **Dedup check** — `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE "baumannii|MRSN|GC1"` → only BVBRC-24 (AbGRI4, Chan 2020) and BVBRC-44 (pCl107 plasmid, 2022). Neither is the GC1 MRSN 56 XDR paper. No conflict → proceed.
2. **Read brief + exemplar** — WAVE_BRIEF_2026-07-01.md + BVBRC-17 REPORT.md.
3. **Paper ID** — Europe PMC search → PMID 35403193, PMC9244215, JAC 2022, doi:10.1093/jac/dkac115. Fetched fullTextXML (free), stripped to text.
4. **Accession harvest** — from full text: isolate MRSN 56, BioProject PRJNA742487, replicons CP080452 (chr) + CP080453/54/55/56 (4 plasmids). Reads SRR14998418 (Illumina), SRR14008417 (Nanopore). Comparison strains: A1 (CP010781 ampC / CP010782 pA1-1), pA85-1 (CP021783).
5. **Assembly resolution** — eutils linked PRJNA742487 → assembly GCA_021484925.1. BUT that assembly's chromosome (CP090606, 4,153,776 bp) did NOT match the paper (4,033,258 bp) — it is a later/related assembly. Corrected course: fetched the paper's EXACT deposited replicons CP080452–CP080456 directly via efetch. Titles confirm "strain MRSN 56". Lesson: BioProject→assembly link can point to a newer resubmission; always pull the exact GenBank accessions cited in the paper.
6. **C1 replicon sizes** — all 5 sizes match Table 1 EXACTLY (4,033,258 / 2178 / 2725 / 6772 / 8731). ✅
7. **C2 MLST** — `mlst` (bvbrc14): Pasteur scheme abaumannii_2 → **ST1** (= GC1). ✅ Oxford scheme returned a partial/novel profile (gdhB 4,182; local Oxford DB version differs from paper's ST231) — noted as DB-version caveat, not a contradiction.
8. **C3 resistome (multi-caller)** — AMRFinderPlus 4.2.7 (--organism Acinetobacter_baumannii --plus), abricate/CARD, abricate/ResFinder. All three agree on the core XDR set: blaOXA-23 (×2), blaOXA-69, blaADC (ampC), gyrA_S81L, aphA1/aac(3)-Ia/aadA1(×3)/aph(6)-Id, sul1/sul2, tet(B), dfrA1(×2), sat2(×2). ✅
9. **C4 chromosome-only AMR** — every AMR hit in all three callers maps to CP080452.1 (chromosome); zero on any of the 4 plasmids. ✅ (matches paper: "four small plasmids, none of which carry resistance genes").
10. **C5 gyrA/parC** — gyrA_S81L confirmed (AMRFinder 99.89%); no known-position parC RDR substitution called. ✅
11. **C7 IS copy number** — ISAba1 counted via blastn of a canonical ISAba1 transposase reference (EU029998 partial CDS region, ~570 bp) at ≥99% id, transposase-region hits: **exactly 20 in the chromosome** (matches paper). ISAba125 via tblastn (WP_001988464, 341 aa): **2 in chromosome** (+1 broad-query cross-hit on plasmid pMRSN56-3, Rep_3). Chromosome counts match the paper (20 + 2). ✅
12. **C6 IS context** — ISAba1 copy at 2823501–2824068 sits 10 bp upstream of ADC/ampC (starts 2824078) → confirms "ISAba1 upstream of ampC" cephalosporin-resistance claim. ✅ The marR-interruption/mar-operon novel FQ hypothesis is the paper's speculative claim (37%/32%/29% identity to E. coli Mar proteins) — core FQ evidence (gyrA S81L + ISAba1-ampC) verified; the mar hypothesis not independently confirmed (nor contradicted).
13. **Plasmid identity claims** — pMRSN56-2 vs pA85-1 (CP021783): 99.89% over 2726 bp; pMRSN56-4 vs pA1-1 (CP010782): **100.00% over full 8731 bp**. Both "identical" claims confirmed. ✅
14. **GC content** — chromosome 39.19% (consistent with A. baumannii).
15. **LLM-judge** — free Argo gpt-5.2, temperature 0 → coverage 9/10, agreement 9/10, verdict **REPLICATED**.

## What worked
- Europe PMC XML + NCBI eutils/Datasets = full paper + exact genome, zero paid endpoints.
- Three orthogonal AMR callers gave concordant resistomes.
- Closed genome → clean, unambiguous replicon-size and copy-number checks.

## What was tricky
- BioProject→assembly link pointed to a newer assembly (GCA_021484925.1 / CP090606) that differs from the paper's deposited CP080452 replicons. Fixed by pulling exact GenBank accessions.
- IS-element copy counting needs a good transposase reference and length/identity thresholds; ISAba125 broad queries cross-hit Rep_3 on a plasmid (chromosome count is the paper-comparable number).
- Local mlst Oxford DB version disagrees with paper's ST231 (DB drift), typical and non-fatal; Pasteur ST1/GC1 is unambiguous.
