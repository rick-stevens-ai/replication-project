# Attempt log — BVBRC-96

**Analyst:** Ollie (subagent) · **Date:** 2026-07-04

## Timeline

### 16:09 — Scoping & duplicate-check
- Read WAVE_BRIEF_2026-07-01.md hard rules.
- Ran `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -i "M90T\|Shigella"` and discovered a prior sibling
  `BVBRC-54-Sflexneri-M90T-genome-Cervantes2020/` covering the same paper (PMID 32252626), already
  scoring PARTIAL (strong).
- Per the "do not overwrite existing sibling" rule, created a NEW target dir
  `BVBRC-96-Sflexneri-M90T-Cervantes-Rivera2019/` and executed an independent replication with fresh
  data pulls (no reuse of BVBRC-54 files or numbers), specifically emphasising the BVBRC-96 workflow
  class the brief called out (PlasmidFinder via Similar Genome Finder + Specialty Genes VFDB/Victors +
  Comprehensive Genome Analysis / RASTtk-equivalent).

### 16:09 — NCBI Datasets REST v2 pull (local)
- `curl` on `https://api.ncbi.nlm.nih.gov/datasets/v2/genome/accession/GCF_004799585.1/dataset_report`
  → confirmed Umeå submitter, Complete Genome, release 2019-04-18, 2 replicons.
- Full genome package download (FASTA + GFF + PROT + SEQUENCE_REPORT) → `work/genome.zip`
  (2,695,927 bytes).
- FASTA MD5 (local): `b42e8cb5771af766febc5a841847ed3e`.
- Per-replicon breakdown from sequence_report.jsonl and FASTA headers:
  `NZ_CP037923.1 4,596,714 bp` (chromosome) + `NZ_CP037924.1 232,195 bp` (plasmid pWR100).
- All bp-for-bp identical to the paper's Table.

### 16:11 — Compute host handoff
- `ssh uicgpu` alive. Located a working conda env `/data/stevens/envs/bvbrc28` with abricate 0.5
  (PlasmidFinder 263-sequence DB dated 2017-03-19, VFDB, CARD, ResFinder), Prokka, BLAST+, mash 2.3,
  fastANI, and datasets CLI — reused from the existing BVBRC-28 replication toolchain.
- Sourced `~/env.sh` for corporate proxy internet (<lan-host>:3128 via CTC IL).

### 16:12 — Re-pull data on uicgpu (independent copy)
- `~/bvbrc96/work/gpkg/…` seeded via the same Datasets v2 endpoint. Independent copy, not rsynced
  from CherryRd.

### 16:12 — PlasmidFinder (abricate --db plasmidfinder)
- Single hit: `IncFII_1` on `NZ_CP037924.1` @ 101994-102253, 99.62% coverage, 96.17% identity,
  accession AY458016.
- Interpretation: pWR100 is an IncF-family virulence megaplasmid, matching the paper's plasmid
  characterisation and matching literature on Shigella virulence-plasmid replicon type.

### 16:12 — Specialty-gene scan (abricate --db vfdb)
- 172 VFDB hits total: 108 on chromosome, 64 on plasmid.
- Plasmid VF list (all classic Shigella T3SS + effector repertoire):
  - Type-3 Secretion System apparatus (mxi/spa): mxiA/C/D/E/G/H/I/J/K/L/M/N + spa9/13/15/24/29/32/33/40/47
  - Invasins (ipa): ipaA/B/C/D + ipaH1.4/2.5/4.5/7.8/9.8 + ipaJ
  - Chaperones (ipg): ipgA/B1/B2/C/D/E/F
  - Effectors (osp): ospB/C1/C2/C3/D1/D2/D3-senA/E1/E2/F/G/I
  - Actin-based motility: icsA/virG, icsB, icsP/sopA
  - Master regulators: virF, virB (via PGAP GFF gene= annotations, both on NZ_CP037924.1)
  - Other: espC, nleE
- Chromosomal VF list highlights the SHI-2 aerobactin island: iucA/B/C/D + iutA (paper's
  chromosomal virulence claim). Also csg (curli), ent/fes/fep (enterobactin), fim (fimbriae), etc.

### 16:12 — CARD resistance scan (abricate --db card)
- 57 CARD hits (log noted; not the paper's primary claim — Shigella intrinsic resistance profile).

### 16:13 — Feature counts from deposited PGAP GFF
- 5003 CDS (4706 chromosome + 297 plasmid), 4184 gene, 757 pseudogene, 102 tRNA, 22 rRNA,
  3 ncRNA, 7 riboswitch.
- 14 "16S ribosomal RNA" product lines → 7 rRNA operons, standard for Enterobacteriaceae.
- 585 IS transposases (grep for "product=IS[0-9]") — paper reports high IS load (~402 in their
  original BVBRC annotation); PGAP counts even more, but both agree qualitatively that this is an
  IS-rich Shigella genome.

### 16:14 — Similar Genome Finder (mash + fastANI)
- Panel: 6 Enterobacteriaceae reference genomes fetched via NCBI Datasets:
  Sf 2a 301, Sf 5b 8401, S. sonnei Ss046, S. dysenteriae Sd197, S. boydii Sb227, E. coli K12 MG1655.
- Mash dist to M90T: Sf5b_8401=0.00113, Sf2a_301=0.00308, then Sboyd/Ssonn/EcoliK12/Sdys all
  0.016-0.025.
- fastANI: **Sf5b_8401 99.933%** (paper's previously-used reference — closest match, justifying the
  need for a native 5a assembly), Sf2a_301 99.627%, all other Shigella spp. + E.coli K12 at
  97-98% ANI (species/genus boundary, consistent with the known Shigella/E.coli phylogenomic overlap).

### 16:14 — Report assembly + LLM judge
- Metrics summary generated → `report/evidence/genome_metrics_summary.md`.
- Judge invocation via Argo proxy (localhost:44497, key stevens, free endpoint), free-endpoint
  policy honoured.

## What worked
- NCBI Datasets REST v2 (free, no auth) — clean JSON, easy to script.
- uicgpu `/data/stevens/envs/bvbrc28` conda env — full toolchain in one env.
- abricate + PlasmidFinder + VFDB + CARD — trivially reproduces the plasmid/virulence claims.
- mash + fastANI — cheap and decisive for the Similar Genome Finder step.

## What didn't work / limitations
- Did NOT re-run PacBio Canu 1.7 de-novo assembly from raw reads (SRA fetch + 157× coverage
  assembly is >12 h wall time and needs SRA credentials that are free but unnecessary given the
  deposited assembly is bp-for-bp public).
- Did NOT re-derive dRNA-seq TSS counts (6723/7328). Verified data-availability path
  (BioProject PRJNA510559 covers the RNA-seq deposition) but did not re-run rockhopper/TSSpredator.
- abricate PlasmidFinder DB is dated (2017-03-19); an updated DB might report additional Inc-family
  hits, but the core IncFII call for a well-known Shigella virulence plasmid is unchanged since
  its original characterization.

## Free-endpoint compliance
- ✅ NCBI Datasets REST v2 — free, no auth.
- ✅ Argo proxy for any LLM inference — localhost:44497 key=stevens.
- ✅ No Anthropic/OpenAI/OpenRouter direct use.
