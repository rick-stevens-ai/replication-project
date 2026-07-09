# BVBRC-94 — Attempt Log

## 2026-07-04 (single session, subagent bvbrc-94, ~40 min wall clock)

1. **Brief + exemplar**: read `WAVE_BRIEF_2026-07-01.md`; reviewed `BVBRC-17-Ecoli-B2-IBD-metabolic-2018/` layout as template.
2. **Paper metadata**: Europe PMC search `EXT_ID:37110457 AND SRC:MED` → hit; captured title, authors, DOI 10.3390/microorganisms11041034, PMCID PMC10145936, CC-BY open access.
3. **Paper PDF**: `curl` from `europepmc.org/articles/PMC10145936?pdf=render` → 2.0 MB PDF, `pdftotext` → 1350-line text; grep’d accessions.
4. **Assembly discovery**:
   - Paper reports WGS deposit `JARHUB000000000` (GenBank WGS master).
   - `esearch` on assembly with term `Lactococcus lactis LL16` → 1 record, id 16519601.
   - `esummary` → **GCF_029912225.1 / GCA_029912225.1** (`ASM2991222v1`), submitted 2023-05-01 by Lithuanian University of Health Sciences (matches paper authors). BioSample SAMN33682203.
5. **Assembly download**: NCBI Datasets v2alpha REST → `GCA_029912225.1_ASM2991222v1_genomic.fna` + `cds_from_genomic.fna` + `genomic.gff` + `protein.faa`.
6. **First reality-check on assembly stats (Biopython + GFF parse)**:
   - Total length = 2,473,617 bp vs paper 2,589,406 (**delta −4.5%**).
   - n_contigs = 372, N50 = 10,345 bp (paper does not disclose).
   - GC = 35.55% vs paper 35.4% (match).
   - GFF: 2531 gene, 2507 CDS, 2469 proteins.faa (paper: 2878 CDS via RAST).
   - GFF: 51 tRNA (paper: 63), 7 rRNA features, 1 tmRNA, 36 pseudogenes.
   - **Interpretation**: length/CDS/tRNA deltas are consistent with a RAST-vs-NCBI-PGAP annotation gap and possibly a slightly different assembly deposited to GenBank vs the internal draft the paper analyzed. GC matches.
7. **Heavy analyses on uicgpu** (`/data/stevens/BVBRC-94-LL16/`), envs: `kleborate` (BLAST, mash), `bvbrc28` (barrnap, abricate).
8. **Reference downloads**:
   - UC06 chromosome `NZ_CP015902.1` via GCF_002078975.1 FTP (2.7 MB fna).
   - `AF178424` pCI2000 plasmid via efetch.
   - UniProt: LcnB (P35518), LciB (P35517), Q4FD00 enterolysin-A-like, GadB Q9CG20, GadC Q9CG19, GadR O30416.
9. **mash**: LL16 vs UC06 → distance 0.00399629 (ANI≈99.6%), MinHash 851/1000. Paper’s k-SNP 91.64% is a different k-mer metric — both indicate the same subspecies.
10. **BLAST**:
    - `makeblastdb` on LL16 assembly.
    - tblastn LcnB: 38.1% id / 63 aa hit + tblastn LciB adjacent on `JARHUB010000163.1` → predicted lactococcin cluster present.
    - tblastn EnlA-like Q4FD00: **58.4% id / 149 aa, bit=177, e=3.9e-51** → strong enterolysin-A homolog.
    - tblastn GadB / GadC / GadR: **99.06 / 99.21 / 95.29% identity**, all on same contig `JARHUB010000048.1` → GAD operon intact.
    - blastn pCI2000 (AF178424) vs LL16: multiple 90–99.7% id hits, longest 1865 bp / 96.1% id → **repUS4/pCI2000 plasmid confirmed**.
11. **barrnap**: 1×16S, 1×23S, 5×5S rRNA regions detected (mostly fragmented across contigs — expected for a 372-contig draft).
12. **ABRicate** (all thresholds ≥90% id, ≥60% cov):
    - ResFinder: **0 hits** (matches paper "no acquired AMR").
    - CARD: 2 hits (`lmrD` 99.80% + `lmrC` 99.59%, both intrinsic Lactococcus efflux — not acquired transferable AMR).
    - NCBI-betalactamase: 0. ARG-ANNOT: 0. VFDB: **0** (matches "no virulence factors").
    - PlasmidFinder: 0 replicon hits at ≥90% — CGE PlasmidFinder DB is Gram-negative-biased and lacks repUS4, so BLAST-against-AF178424 is the correct call for the lactococcal replicon (and IT hit).
13. **Biogenic amines**: keyword grep of `protein.faa` for lysine/ornithine/histidine/tyrosine/arginine decarboxylase → **0 hits** (matches paper).
14. **IS6 family**: 4 PGAP-annotated `IS6 family transposase` proteins (paper reports 3 IS6 elements — close, differences attributable to contig fragmentation).
15. **CRISPR**: 1 `CRISPR-associated protein Cas2` PGAP annotation → consistent with paper's 1 CRISPR-Cas system claim.
16. **Adhesion / probiotic scaffold**: 4 LPXTG anchor proteins + 2 sortases + 1 collagen-binding-domain protein + DnaK + GroEL + full F0F1 ATPase operon present.
17. **T3PKS BGC**: antiSMASH 8.0.4 available in `envs/antismash/` but `/data/stevens/antismash_db/` is empty (would need ~20 GB download); direct antiSMASH run failed at `check_prerequisites`. Fell back to keyword grep of `protein.faa` — found `polyketide synthase regulator (partial)` MDH8063741.1 and `ketoacyl-ACP synthase III` MDH8064341.1 → consistent with the T3PKS claim but not a full independent BGC re-detection. Marked SPOT-CHECK for this specific claim.
18. **LLM judge** (Argo `argo:gpt-5.2`, temp=0.0, prompt in `work/judge_prompt.txt`, output in `evidence/judge_verdict.txt`) → **PARTIAL / 80% coverage / MODERATE agreement**.

## What worked
- NCBI Datasets REST for the assembly.
- Europe PMC + pdftotext for paper metadata.
- kleborate env's BLAST tools + bvbrc28's abricate suite.
- Direct BLAST against AF178424 for the plasmid (bypassing PlasmidFinder DB limitation).
- Multi-DB abricate cross-check to strengthen the safety claim.

## What didn’t work / limitations
- **antiSMASH DB missing** on uicgpu → T3PKS BGC could not be independently re-detected end-to-end (only supported by direct-annotation grep).
- Assembly length discrepancy of −4.5% between paper text and the deposited assembly is not resolvable from public data alone; could reflect a different assembler config, contamination filter, or the RAST vs PGAP annotation window.
- **In vitro GABA in fermented milk** is a wet-lab claim — not reproducible from a subagent workstation.
- Full 110-strain-style pan-genome is out of scope for this paper (they didn't do one either).
- Paper's mangled OCR string "CDA and RNRs were 2878 and 63" almost certainly means "CDSs and tRNAs" — treating it as such.
