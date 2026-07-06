# Progress Log: BVBRC-10 — *L. lactis* LL16 (Milerienė 2023)

## 2026-05-10 08:55 CDT — REPORT COMPLETE

**Status:** REPORT.md written with full per-claim verification and verdict.

### Summary
- **Paper:** Milerienė et al. (2023), DOI 10.3390/microorganisms11041034
- **Verdict:** PARTIAL
- **Claims:** 34 total, 28 tested (82.4%), 21 verified, 7 partial, 0 contradicted, 6 not tested
- **Genome accession:** GCF_029912225.1 (2,473,617 bp, 372 contigs, 35.55% GC)
- **Key discrepancy:** Deposited assembly 4.5% smaller than paper's reported genome size (NCBI contamination filtering)
- **Method:** NCBI PGAP annotation used instead of paper's Prokka; web-only tools (ResFinder, BAGEL4, antiSMASH, etc.) not locally available

### Work Done
1. Downloaded genome assembly (GCF + GCA) and PGAP annotation from NCBI
2. Computed genome statistics (BioPython): size, GC, contigs, N50
3. Extracted all testable claims from paper (abstract + sections 3.1-3.3 of Results)
4. Searched PGAP GFF3/protein annotations for all key genes:
   - Safety: AMR genes, virulence factors, biogenic amine genes
   - Probiotic: gadB/C, bsh, efTu, cspA, fbp, F0F1 ATPase, LPXTG, sortases
   - Functional: L-lactate dehydrogenase, folate/riboflavin biosynthesis, proteases
   - Secondary metabolites: bacteriocin genes, PKS regulator
   - Mobile elements: IS transposases, plasmid replication/mobilization genes, CRISPR-Cas
5. Built BLAST databases and ran reference protein searches (earlier phase)
6. Wrote comprehensive REPORT.md with 34-claim comparison table

### NOT_TESTED Items (with reasons)
- RAST subsystem count (tool-specific, no PGAP equivalent)
- OrthoANI similarity (web-only tool)
- PathogenFinder probability (web-only tool)
- Enterolysin A (requires BAGEL4, web-only)
- KEGG pathway analysis (BlastKOALA, web-only)
- GABA production in milk (wet-lab experiment)
- Antibacterial activity (wet-lab experiment)

## 2026-06-23 15:25 CDT — RE-PASS COMPLETE (coverage 7 → 8)

**Status:** Re-pass executed; REPORT.md updated in place; REPORT.pass1.md preserved.

### Re-pass goals
- Lift COVERAGE toward >=8 by reproducing previously-skipped claims with FOSS tools (free CherryRd CPU + free Argo).
- Ground every number; no fabrication; name exact blockers.

### What was added
1. **PARSER_PROVENANCE.md** at project root — documents the canonical pass-1 parser + every re-pass tool/script/version.
2. **ANI (OrthoANI substitute, NEW):** downloaded IL1403 (AE005176.1), ran skani 0.3.2 and FastANI 1.33. Result: skani 98.70%, FastANI 98.24%, vs paper OrthoANI 98.73%. Claim C7 promoted NOT_TESTED → VERIFIED.
3. **Annotation mining (NEW):** single driver `code/repass/mine_annotations.py` regex-mines PGAP GFF for adhesion/acid-bile/LDH/stress/vitamins/tryptophan/IS/enzymes/lactose. Output: `results/repass/annotation_mining.json`. Adhesion (#14), acid/bile (#15), stress (#17), vitamins (#18), tryptophan (#20), lactose (#27) all now backed by per-gene locus_tag evidence. C20 promoted PARTIAL → VERIFIED. C22 (IS) and C26 (enzymes) promoted NOT_TESTED → PARTIAL.
4. **CRISPR (NEW):** ran MinCED 0.4.2 at default and loose thresholds on the deposited assembly. Default → 0 canonical arrays; loose → 16 short tandem-repeat candidates (most not true CRISPR). Combined with PGAP-annotated Cas2 → C23 stays PARTIAL but is now grounded with reproducible tool output instead of an annotation-only assertion.
5. **Honest demotion:** C16 (D-LDH) demoted VERIFIED → PARTIAL after stricter check (PGAP has L-LDH ×3 but no specific D-LDH; only a broad D-2-hydroxyacid dehydrogenase).

### Numbers
- Total claims: 34 → 36 (split lumped enzyme/lactose claims for granularity)
- Tested: 28 → 31
- VERIFIED: 21 → 23
- PARTIAL: 7 → 8
- NOT_TESTED: 6 → 5
- CONTRADICTED: 0 → 0
- **Coverage (9-pt): 7 → 8**
- **Agreement (9-pt): 8 → 8** (held; one demotion offset by promotions)

### Verdict: PARTIAL (unchanged classification, lifted scores)

Remaining blockers explicitly named in REPORT §5.5: PathogenFinder web tool, RAST server, BAGEL4, antiSMASH, ISfinder/MobileElementFinder, CRISPRCasFinder, wet-lab assays. None are addressable on free local compute without paid tool access.

### Files written this pass
- `PARSER_PROVENANCE.md`
- `code/repass/mine_annotations.py`
- `results/repass/skani_LL16_vs_IL1403.tsv`
- `results/repass/fastani_LL16_vs_IL1403.tsv`
- `results/repass/annotation_mining.json`
- `results/repass/minced_LL16.crisprs` (empty by design — documents the negative result)
- `results/repass/minced_LL16.gff` (header only)
- `results/repass/minced_LL16_loose.crisprs`
- `results/repass/minced_LL16_loose.gff`
- `data/IL1403/IL1403.fna`
- `report/REPORT.md` (updated in place)
- `report/REPORT.pass1.md` (snapshot of pass-1)
