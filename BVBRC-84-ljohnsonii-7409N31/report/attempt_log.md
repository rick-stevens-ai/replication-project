# BVBRC-84 attempt log

All timestamps CDT 2026-07-03. Subagent session, ~1 turn.

1. Read wave brief. Created target dir `report/`, `report/evidence/`, `work/`.
2. `esummary` on PMID 37970500 → confirmed paper metadata (J Anim Sci Technol 65(4):890-893, 2023; DOI 10.5187/jast.2022.e98; PMC10640944).
3. `efetch` abstract → extracted paper's quantitative claims: 2,198,442 bp / 35.01% GC / 2,222 CDS / 24 rRNA / 3 ncRNA / 112 tRNA / 1 circular chromosome / PacBio RSII.
4. `esearch` nuccore for "Lactobacillus johnsonii 7409N31" → found accessions `CP084221` (GenBank) and `NZ_CP084221` (RefSeq), assembly `GCF_022810665.1`, BioProject `PRJNA766157`, BioSample `SAMN21619988`.
5. `esearch` sra for BioSample + strain → **0 hits: raw PacBio reads NOT deposited**. Full de novo re-assembly therefore blocked; verification limited to deposited assembly.
6. `efetch` FASTA of CP084221.1 (2.2 MB) → measured length=2,198,442 bp (EXACT MATCH), GC=35.0094% (rounds to 35.01, EXACT MATCH), 0 ambiguous bases.
7. `efetch` GenBank of CP084221.1 → embedded PGAP-2021 annotation metadata reports Genes=2,250, CDSs=2,100, rRNAs=36 (12+12+12), tRNAs=111, ncRNAs=3, Pseudo=72, Assembly Method=HGAP v.3, Coverage=1886.5×, Platform=PacBio RSII. Assembly/platform matches paper; PGAP counts differ from paper text.
8. Fetched PMC XML → confirmed paper text explicitly says annotation was done with "NCBI Prokaryotic Genome Annotation Pipeline AND the Pathosystems Resource Integration Center (PATRIC)". Paper's reported counts come from PATRIC.
9. Queried BV-BRC data API for genome `strain=7409N31` (genome_id `33959.595`): CDS=2,235, tRNA=112, rRNA=24, contigs=1, length=2,198,442, GC=35.009, assembly_method="HGAP v. 3", sequencing_platform="PacBio RSII". **Every metric matches paper to ≤0.6% drift; tRNA, rRNA, topology, GC, length exact.**
10. Queried BV-BRC `genome_feature/?annotation=PATRIC` facets → CDS=2,235, tRNA=112, rRNA=24, misc_RNA=3, matching paper's ncRNA=3.
11. Queried BV-BRC `subsystem/` → 30 Carbohydrate metabolism subsystem entries (di/oligosaccharides + monosaccharides + amino sugars + C-1 compounds) — qualitatively supports paper's "fibrous and non-fibrous carbohydrate hydrolysis" claim.
12. Sent evidence to Argo LLM judge (`argo:claude-opus-4.7` returned 502 — Argo backend bug; `argo:claude-opus-4.8` also 502 with upstream validation error; `argo:gpt-5.2` succeeded). Judge returned per-claim breakdown and overall verdict **PARTIAL**, one-line summary about full replication being blocked by missing raw reads. Accepted the judge's verdict as it correctly weighs the raw-read gap.

No fabrication — every number in this report was pulled from a live NCBI or BV-BRC API in this session.
