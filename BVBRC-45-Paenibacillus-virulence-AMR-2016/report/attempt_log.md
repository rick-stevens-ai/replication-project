# Attempt Log — BVBRC-45 (2026-07-01)

1. **Dedup** — `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -iE paenibacillus` → no existing dir. Proceeded.
2. **Read brief + BVBRC-17 exemplar** to match structure/verdict vocabulary.
3. **Located paper** via Europe PMC (`JOURNAL:"Gut Pathogens"` + Paenibacillus): PMID 26900405, PMC4761199, DOI 10.1186/s13099-016-0089-1. Title confirms strain **VT-400**.
4. **Fetched full-text XML** (free, Europe PMC). Extracted: abstract, genome stats (116 contigs / 6,986,122 bp / GC 45.8%), WGS accession **LELF01000000**, DSM 100755, virulence Table (hemolysin D, CD4+ superantigen, peptidases, flagella…), AMR Table (96 MFS + 18 ABC transporters, SMR, beta-lactamases, catA, DHFR…), susceptibility Table 5 (R: erythromycin, azithromycin, chloramphenicol, TMP-SMX; S: rest).
5. **Resolved assembly accession** — eutils esearch on `LELF01`/`VT-400` → assembly UID 350701 → **GCF_001029205.1** (Paenibacillus sp. VT-400, Contig level).
6. **Set up uicgpu** — bvbrc28 env at `/data/stevens/envs/bvbrc28` (datasets 18.32.0, fastANI 1.34, blast, prokka); AMRFinderPlus 3.12.8 in `~/micromamba/envs/amr`.
   - Snag: `conda activate bvbrc28` failed (env is path-based, not named). Fixed by `conda activate /data/stevens/envs/bvbrc28`.
   - Snag: no Biopython in env + pip blocked by proxy. Worked around with pure-Python FASTA parser for genome stats.
   - Snag: `amrfinder -u` failed (baked-in build-path). Worked around by pointing `-d` at the existing DB `share/amrfinderplus/data/latest` (2024-07-22.1).
7. **Downloaded genomes** via `datasets download` — VT-400 (genome+protein+gff3) + 5 relatives (genome).
8. **Genome stats** → 115 contigs, 6,985,624 bp, GC 45.8%, N50 4.44 Mb, 5,936 proteins. Matches paper C2 essentially exactly.
9. **Novel-species test** — fastANI VT-400 vs 5 relatives: **P. amylolyticus 97.13%, P. xylanexedens 96.24%**, others 81–84%. Both top hits > 95% species boundary → **novel-species claim CONTRADICTED**.
10. **AMR** — AMRFinderPlus protein mode → 4 curated acquired genes: **catA** (chloramphenicol), **msr** (macrolide), vat (streptogramin A), arr (rifampin). catA+msr corroborate paper phenotype.
11. **Annotation-drift check** — paper-cited WP accessions still exist but several are now generic: "Hemolysin D"→TrhA membrane protein; "CD4+ superantigen"→BMP lipoprotein; "Vancomycin resistance protein"→VanW family (consistent with vanc-S phenotype). Confirms over-interpretation of 2016 RAST calls.
12. **LLM judge** (free Argo gpt-5.2, temp 0) → verdict **CONTRADICTED**, coverage 7/10, agreement 4/10.
13. **Wrote report/, copied evidence.**
