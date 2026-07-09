# Workflow — BVBRC-14 Hybrid Assembly Replication (Khezri 2021)

**Paper:** Khezri A, Avershina E, Ahmad R. *Microorganisms* 2021;9(12):2560. DOI: 10.3390/microorganisms9122560. PMC8704702.
**BioProject:** PRJEB45084
**Verdict:** PARTIAL (largely reproducible, 7/10)

---

## 1. Scope of Replication

The paper compares three assembly strategies (IllumASM, MinIONASM, HybASM) across 9 clinical isolates plus 1 reference and 1 mixed culture. We did **not** re-do all three assemblies for all 9 isolates; instead we scoped this replication to:

1. **Reference-genome exact verification** (E. coli NCTC 13441, GCF_900119685.1).
2. **Short-read-only assembly** of 2 representative isolates (EC4 = ERR5951441; KP5 = ERR5951446).
3. **Consistency checking** of the paper's numeric claims against internal logic and biological plausibility.

No hybrid or long-read-only assemblies were performed in this replication.

---

## 2. Step-by-Step Pipeline

### Step 2.1 — Data discovery
- Located paper via DOI 10.3390/microorganisms9122560 / PMC8704702.
- Extracted BioProject PRJEB45084 from the Data Availability statement.
- Confirmed 21 SRA runs (10 MinION + 11 Illumina) via ENA browser.

### Step 2.2 — Reference genome download
- Used NCBI `datasets` CLI to download assembly GCF_900119685.1 (E. coli NCTC 13441).
- Verified sequence content: 5,174,631 bp chromosome + 161,069 bp plasmid.

### Step 2.3 — Read download (2 isolates only)
- `prefetch` + `fasterq-dump` on ERR5951441 (EC4 Illumina) and ERR5951446 (KP5 Illumina).
- No MinION reads downloaded (hybrid assembly out of scope).

### Step 2.4 — Short-read assembly (SPAdes v4.0.0)
- Ran SPAdes in default mode on paired-end Illumina reads for EC4 and KP5.
- Filtered contigs to ≥1 kb.
- Recorded contig count, total length, N50 via QUAST.
  - **EC4:** 175 contigs ≥1kb, 5,827,066 bp, N50 = 106,275 bp.
  - **KP5:** 109 contigs ≥1kb, 5,591,911 bp, N50 = 312,224 bp.

### Step 2.5 — AMR gene detection
- **ResFinder v4.7.2** (conda) on each assembly (ref, EC4, KP5).
- **AMRFinder v4.2.7** (db 2026-03-24.1) as a cross-check.
- Recorded per-isolate acquired AMR gene lists.

### Step 2.6 — Plasmid replicon detection
- **PlasmidFinder DB** (bitbucket, 2025 clone) via BLAST.
- Counted replicon hits per isolate (no Bandage circularity confirmation — a known methodological difference from the paper).

### Step 2.7 — Virulence factor detection
- **VFDB** setA_nt (2025 download) via local BLAST+.
- Counted unique VF loci per assembly.

### Step 2.8 — Claim audit
- Built a per-claim reproducibility table matching paper Tables 2, 3.7, 3.8, 3.9, 3.10.
- Classified each claim as: ✅ Exact match / ✅ In range / ✅ Consistent / ✅ Plausible / ⚠️ Mismatch (with explanation) / ⬜ Not tested.

---

## 3. Assembler / Tool Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Short-read assembler | SPAdes v4.0.0 | Modern, widely used, faster smoke-test than re-running Unicycler; expected to give similar contig-level results |
| Hybrid assembler | **NOT RUN** | Requires long-read data, hours of compute per isolate, and would only partially close the gap given the paper's Bandage circularity step |
| Long-read assembler | **NOT RUN** | Same as above; also, Guppy v3 basecalling would need to be reproduced for a fair comparison |
| AMR tool | ResFinder v4.7.2 + AMRFinder v4.2.7 | Paper used ResFinder; AMRFinder used as cross-check |
| Plasmid tool | PlasmidFinder DB (2025 clone) | Paper used PlasmidFinder |
| VF tool | VFDB setA_nt (2025) | Paper used VFDB; version drift explicitly noted |
| Assembly QC | QUAST | Standard |
| BUSCO | Not re-run | Requires assemblies we did not produce |

---

## 4. Deviations From Paper Methods

1. **SPAdes vs Unicycler** for short-read assembly. Unicycler wraps SPAdes internally but adds a scrubbing/circularisation pass; contig counts can differ. Impact: minor; totals and N50 fell within the paper's reported ranges.
2. **PlasmidFinder without Bandage circularity confirmation.** We counted BLAST hits; the paper counted circularised replicons. Impact: our replicon counts are higher (EC4: 5, KP5: 5) than the paper's per-isolate averages (~0.75 EC, ~0.4 KP). This is methodological, not a reproducibility failure.
3. **VFDB 2025 vs paper's 2020.** Direct number comparisons are non-portable; directional claims should still hold.
4. **AMRFinder used as cross-check** (paper did not use AMRFinder).
5. **Only 2 isolates re-assembled** out of 9, and only for short-read.

---

## 5. Runtime & Compute Envelope

- Reference-genome tool runs: minutes each.
- Two SPAdes assemblies: ~30–60 min each on a modern workstation.
- All BLAST-based tool runs (ResFinder, PlasmidFinder, VFDB): <15 min per assembly.
- No GPU or HPC required. Full workflow reproducible on a single laptop with `conda` + `blast+` + `spades` + `resfinder` + `amrfinder` + `plasmidfinder` DB + `vfdb` fasta.

---

## 6. Reproducibility Handoff

Anyone reproducing this replication:
1. Install conda envs for SPAdes 4.0.0, ResFinder 4.7.2, AMRFinder 4.2.7, BLAST+.
2. Clone PlasmidFinder DB and download VFDB setA_nt.
3. `datasets download genome accession GCF_900119685.1`.
4. `prefetch ERR5951441 ERR5951446 && fasterq-dump ERR5951441 ERR5951446`.
5. Run SPAdes on each read pair; filter to ≥1kb.
6. Run ResFinder + AMRFinder + PlasmidFinder + VFDB BLAST on each assembly (including reference).
7. Compare against paper's Tables 2, and Sections 3.7–3.10.

To extend to full hybrid replication (which this replication did NOT do):
- Also download all MinION reads (10 runs).
- Install Unicycler and Flye.
- Run Flye (MinIONASM) and Unicycler hybrid (HybASM) for each of the 9 isolates + mixed culture.
- Add Bandage circularity confirmation to the plasmid pipeline.
- Expect ~200–500 core-hours of compute total.
