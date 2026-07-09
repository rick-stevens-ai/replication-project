# Workflow — BVBRC-62 Independent Replication
## *Providencia hangzhouensis* HL_Adamas-11 (Adhikary et al. 2026, MRA)

**Replicator:** OpenClaw subagent (CherryRd)
**Date:** 2026-07-02
**Tooling constraint:** free / open-source only; no paid PDF tools; free LLM endpoints (Argo).

---

## Stage 0 — Paper acquisition

1. Resolved DOI `10.1128/mra.01372-25` → PMID 42059626 → PMCID PMC13248694 (Open Access, CC-BY 4.0).
2. Pulled full text via Europe PMC REST endpoint (`.../PMC13248694/fullTextXML`) → `work/paper_fulltext.xml`.
3. Extracted paper's reported metrics, accessions, and named genes from the XML for later automated comparison.

---

## Stage 1 — Accession → deposited artifact resolution

1. Paper accessions: BioProject **PRJNA1314473**, BioSample **SAMN51056432**, WGS **SGQL00000000**, SRA **SRR35282168**.
2. Two candidate NCBI assemblies pointed at BioSample SAMN51056432:
   - **GCA_053592895.1 / GCF_053592895.1** (ASM5359289v1)
   - GCF_056140255.1 (identical duplicate deposit)
3. Disambiguation: matched the paper's exact reported `Coverage = 91.664×` and `ContigN50 = 16,147 bp` to the NCBI assembly record → picked **GCA_053592895.1** as the target artifact.

---

## Stage 2 — Download

Using NCBI `datasets` CLI:

```
datasets download genome accession GCA_053592895.1 \
  --include genome,protein,gff3,seq-report
```

Artifacts obtained:
- Genome FASTA (`*_genomic.fna`)
- Protein FASTA (`protein.faa`)
- GFF3 annotation
- Assembly / sequence report (structural + GC + coverage fields)

---

## Stage 3 — Genome architecture (paper §3.1 claims)

1. **Contigs / N50 / coverage / length / GC** → parsed NCBI assembly report + Biopython recompute of GC from the FASTA.
2. **Feature counts** (CDS, tRNA, rRNA, ncRNA) → GFF3 parse + cross-check against NCBI annotation stats.
3. **Plasmid count** → contig-level `plasmid` labels in the assembly report (4 distinct plasmid names: pAA860, pAB133, pAC129, pnovel_c01a4b).

**Outcome:** All architecture claims match exactly except GC%; length shows expected –0.20% shrink from GenBank low-quality contig filtering.

---

## Stage 4 — Species / ANI

1. Reference: `GCF_029193595.2` = *P. hangzhouensis* strain PR-310 (type-adjacent).
2. **fastANI** v1.x → `work/fastani_ref.txt` → 98.46%.
3. **skani** (independent method) → 98.62%.
4. Both above the 95% ANI species threshold → confirms *P. hangzhouensis*.

---

## Stage 5 — MLST

1. Tool: `mlst` v2.33.1 (Torsten Seemann) with bundled PubMLST schemes.
2. Ran against the assembly FASTA with scheme auto-detect → `providencia` scheme selected.
3. Result: `ST = "-"` (unassigned), alleles fusA(17) gyrB(105) ileS(29) lepA(~49) leuS(49).
4. **Not reproduced** — scheme/DB-version mismatch. Bundled scheme is the classic *P. stuartii*-dominant 5-locus PubMLST profile; paper used the live PubMLST *Providencia* DB (which has since added *P. hangzhouensis* profiles).
5. Logs: `work/mlst_out.txt`, `work/mlst.log`.

---

## Stage 6 — AMR genotype (paper §3.4 — the central functional claim)

1. Tool: **AMRFinderPlus v4.2.7**, database version **2026-05-15.1**.
2. Mode: nucleotide (`--nucleotide`), `--plus` for stress/virulence context.
3. Input: `*_genomic.fna`.
4. Output: `work/amrfinder_nuc.tsv` (27 AMR rows), log `work/amrfinder_nuc.log`.
5. Cross-checked each paper-named gene against the AMRFinderPlus hit table across 4 classes:
   - β-lactam (5 genes claimed; all 5 recovered; 3 extra hits)
   - Aminoglycoside (3 genes claimed; class fully recovered; 1 nomenclature typo, 1 real-name correction)
   - Macrolide (3 genes claimed; all recovered; 3 extra)
   - Phenicol (2 genes claimed; all 2 recovered)
6. Metal-resistance mer operon incidentally recovered.

---

## Stage 7 — LLM judge

1. Prepared `work/judge_input.md` (paper claims table + replication result table + free-text discrepancies).
2. Judge model: Argo `gpt-5.2`, temperature 0 (deterministic, free-tier via Argo proxy).
3. Prompt requested: verdict ∈ {FULL, PARTIAL, FAIL}, `coverage/10`, `agreement/10`, rationale.
4. Output: `work/judge_output.md`.
5. Judgment: **PARTIAL**, Coverage 8/10, Agreement 7/10.

---

## Stage 8 — Report assembly

1. Human-readable synthesis → `report/REPORT.md`.
2. LaTeX detailed report + genuine-critique section → `report/REPORT.tex`.
3. Open-questions ledger → `report/open_questions.json` (5 grounded open questions).
4. Artifacts summary → `report/artifacts_summary.md`.
5. Failure analysis → `report/failure_analysis.md`.
6. This document (`report/workflow.md`).

---

## Explicit non-steps (out of scope for this replication)

- **CheckM completeness/contamination** — heavy lineage DB, not re-run. Paper values (93.78% / 5.14%) accepted as-is.
- **Virulence screen (VFDB/Victors)** — not performed; paper does not claim virulence content.
- **Plasmid typing (PlasmidFinder / MOB-suite)** — plasmid count accepted from NCBI contig labels; Inc/MOB not re-derived.
- **CARD / ResFinder cross-tool AMR comparison** — AMRFinderPlus alone was used; the paper's exact CARD v6.0.5 + ResFinder v4.7.2 outputs were not reproduced.
- **Raw-read reassembly from SRR35282168** — not performed; started from the deposited assembly.

---

## Reproducibility notes

- All tool versions pinned in this workflow doc.
- All input artifacts recoverable from public NCBI + Europe PMC.
- Only non-public inputs are the LLM judge model (Argo `gpt-5.2`) and its output — a reader with a different judge would need to re-run stage 7.
- Full command lines are captured in the per-stage log files under `work/`.
