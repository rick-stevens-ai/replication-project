# Attempt Log — BVBRC-85 · Ali et al. 2019 MRSA SO-1977

**Analyst:** Ollie (OpenClaw subagent, model argo/argo:claude-opus-4.7 driving; LLM-judge = gpt-5.2 + claude-sonnet-4.6 + gemini-2.5-pro via Argo :44497).
**Session:** BVBRC-85 (wave 2026-07-01-night, X-100 target #85).
**Duration:** ~40 min end-to-end, all light-compute local (no `ssh uicgpu` needed — one 2.8 Mb assembly).

## Chronological log

**T+0min — Setup.** Created `~/Dropbox/REPLICATE-PROJECT/BVBRC-85-Saureus-SO1977-Sudan-Ali2019/{report/evidence,work}`. Read wave brief; noted BMC OA so PMC XML would be the paper source (no OSTI PDF fetch needed).

**T+2min — Paper fetch.** Europe PMC REST → resolved PMID 31185900 → PMC6558803, DOI 10.1186/s12866-019-1470-2. Pulled `fullTextXML` (79 KB). Parsed tables from the XML. Recovered all four crucial accessions from paper Table 1: `NFZY00000000` (WGS), `PRJNA385553` (BioProject), `SAMN06894057` (BioSample), plus locus tag `CA803`.

**T+4min — Accession resolution.** `esearch db=assembly term=NFZY00000000` → UID 1156631 → `esummary` returned `GCF_002224825.1 / GCA_002224825.1 (ASM222482v1)` with matching N50=62,783 and coverage=122.26× (both identical to paper). Downloaded genomic FASTA, protein FASTA, feature table, GFF from the NCBI FTP root. Also grabbed the authoritative `md5checksums.txt`.

**T+6min — Independent genome statistics.** Wrote a small Python script over the downloaded FASTA to recompute contigs / total length / largest / N50 / GC%. Result: 151 contigs, 2,827,644 bp, 146,886 bp largest, N50=62,783, GC=32.79%. **All five paper stats match exactly** (paper reports 32.8% GC, which rounds correctly from 32.79%).

**T+9min — Tool inventory.** Confirmed local install of `abricate 1.4.0` (12 DBs fresh 2026-Jul-03: card, ncbi, resfinder, vfdb, plasmidfinder, argannot, megares, victors, ecoli_vf, ecoh, upec_expec_vf, bacmet2), plus `blastn/tblastn/makeblastdb`. `mlst` binary present but broken by Homebrew Perl 5.34-vs-5.32 XS mismatch (`XS.c: loadable library and perl binaries are mismatched`). Decided to bypass — the MLST scheme allele files (`*.tfa` + `saureus.txt` profile) are just data, so we ran blastn manually.

**T+12min — Bulk AMR / VF calls on SO-1977.** `abricate --db {card,ncbi,resfinder,vfdb,victors,argannot,megares,plasmidfinder}` on the assembly. Rate-of-return: card 16, ncbi 5, resfinder 4, vfdb 73, victors 33, argannot 9, megares 19, plasmidfinder 3. All calls at 100% ID / >98% coverage for the core AMR genes. mecA and blaZ both at 100/100; tet(K) and tet(M) both at 100/>99.

**T+15min — MLST.** Ran manual blastn of each pubMLST S. aureus scheme allele (`arcC/aroE/glpF/gmk/pta/tpi/yqiL.tfa`) against a makeblastdb-built SO-1977 db. Required 100% identity + full-length match to call an allele. Result: `arcC-43, aroE-37, glpF-48, gmk-19, pta-49, tpi-26, yqiL-39` → exact profile match in `saureus.txt` → **ST140**. (Paper did NOT report an ST — this is genuinely new evidence.)

**T+18min — Comparator genomes.** Downloaded MRSA252 (`GCF_000011505.1`) and MSSA476 (`GCF_000011525.1`) from RefSeq — same two strains the paper compares SO-1977 against in Table 4. **PATH hiccup**: `for` loop in the exec shell mysteriously lost PATH mid-iteration; retried inside a fresh `bash -c` and it worked cleanly.

**T+22min — Comparative AMR panel.** Ran abricate against card/ncbi/resfinder/vfdb on both comparators. Built a joint presence/absence table over all AMR genes seen in any of the three strains → `AMR_comparison_table.tsv`.

**T+25min — Paper claim verification (against real data).**
- Central claim: "two genes were only found in SO-1977 strain conferring resistance against Tetracycline" → **`tet(K)` and `tet(M)` present in SO-1977 only; absent in MRSA252 and MSSA476 by both CARD and ResFinder.** ✅ Directly reproduced.
- `mecA` + `mecR1` in SO-1977 and MRSA252; `mecI` only in MRSA252 → all confirmed. `mecR1` was initially not called by abricate for SO-1977 (assembly break at contig 34 edge truncates it to 310 aa / 585); a manual `tblastn(MecR1)` against the SO-1977 db recovered the 100%-ID 310-aa segment on `NFZY01000034.1` — consistent with the paper.
- Secondary claim: "SO-1977 was the only one having the norA gene providing resistance against Quinolone" → **CONTRADICTED**: CARD detects `norA` in all three strains at similar identity/coverage. `norA` is a well-known S. aureus core-genome gene; paper's uniqueness call is a comparator-annotation artifact.

**T+30min — Taxonomy.** Extracted the single 16S rRNA locus (`CA803_14545`, 1,557 bp, contig NFZY01000100.1) from the assembly via GFF coords + strand-aware slicing; remote BLASTN against NCBI `nt` returned top-6 hits all *Staphylococcus aureus*, top hit 100% identity — confirms the paper's 16S-based species assignment.

**T+35min — LLM-judge (3 models, cross-validated).** Built compact evidence pack (`evidence_summary.md`) with every gene call, comparator table, and stats table. Argo proxy verified live (`/v1/models` returned 40+ models, `argo:gpt-5.2` smoke-tested with a 5-token reply). Tried `argo:claude-opus-4.7` first — HTTP 502 (transient) — fell back to `argo:gpt-5.2`, then cross-validated with `argo:claude-sonnet-4.6` and `argo:gemini-2.5-pro`. All three judges converged on **overall_verdict = PARTIAL, coverage_fraction 0.75-0.82**, with the norA contradiction explicitly flagged by all three.

**T+40min — Report write-up + wave-line emission.**

## What worked cleanly
- NCBI Datasets / eutils / FTP for accession → assembly → files.
- abricate 1.4.0 against all 8 relevant DBs.
- Manual pubMLST call via direct blastn (30 lines of Python) as a full workaround for the mlst-Perl-XS breakage.
- Comparator download + comparative panel.
- 3-model LLM-judge on Argo (free) — GPT-5.2 first-pass, Claude-Sonnet-4.6 + Gemini-2.5-Pro cross-check.

## What broke (and how it was routed around)
- **Homebrew `mlst` Perl-XS handshake mismatch** (Perl 5.32-built XS module against system Perl 5.34). Not fixable in a subagent; replaced with 30 lines of Python calling blastn on the pubMLST `*.tfa` files.
- **Argo Opus 4.7 HTTP 502** on one call — transient. Retried with GPT-5.2 and it worked; kept Opus off the critical path for this run.
- **Zsh loop PATH regression** during download of comparators — invisible cause, fixed by wrapping in `bash -c`.

## What was NOT done (limits of scope)
- No live antibiotic MIC testing (paper's disc-diffusion data on oxacillin/cefoxitin is a wet-lab claim; not replicable in silico).
- No full re-annotation with RAST — RAST-server subsystem counts (26, 1970 genes, 83 in "Virulence/Disease/Defense") are compared against VFDB/CARD counts, which use different (more curated) gene sets — comparison is shape-only, not gene-for-gene. Full RAST rerun would need a RAST-server account and would add zero rigor to the "does the assembly exist and does it look right" question this replication is really answering.
- No cephamycin/carbapenem/teicoplanin resistance gene deep-dive beyond what the AMR databases automatically flag; the paper's claims for those classes look weak (they're inferred from downstream RAST subsystem membership, not from validated resistance-gene detections), but I left that flag in the "PARTIAL" bucket rather than escalating to CONTRADICTED without a fuller manual check.
