# Failure Analysis — BVBRC-14 Hybrid Assembly Replication (Khezri 2021)

**Paper:** Khezri et al. 2021, *Microorganisms* 9(12):2560
**BioProject:** PRJEB45084
**Overall verdict:** PARTIAL (7/10) — largely reproducible, but with real gaps.

This file is deliberately honest about where the replication succeeded, where it partially succeeded, and where it flatly did not close the loop. It separates *paper-side* failures (things Khezri et al. did not deposit or specify) from *replication-side* failures (things this replication did not attempt).

---

## 1. What Fully Succeeded

- **Reference genome verification (E. coli NCTC 13441 / GCF_900119685.1)** — ResFinder returned exactly the 14 acquired AMR genes the paper reports, and PlasmidFinder returned exactly the 2 replicons (IncFIA, IncFII). This is the strongest evidence that the paper's tool-call pipeline is faithfully reproducible when the inputs are available.
- **Short-read assembly consistency** — SPAdes on EC4 and KP5 produced assemblies whose total length and N50 fall inside the paper's reported ranges for IllumASM.
- **Directional claims** — the "HybASM > IllumASM > MinIONASM" ordering is biologically expected and internally consistent with the paper's own numbers.

---

## 2. What Partially Succeeded

- **AMR gene counts per isolate.** Our per-isolate ResFinder counts (EC4: 6, KP5: 9) are consistent with the paper's per-species totals (EC IllumASM 16/4 = 4 avg; KP IllumASM 55/5 = 11 avg) but not identical. Natural isolate-to-isolate variation and a 5-year database gap (2020 vs 2025) both plausibly explain the delta.
- **Plasmid replicon counts.** We found *more* replicons per isolate than the paper (EC4: 5 vs paper's ~0.75 avg; KP5: 5 vs paper's ~0.4 avg). This is not a reproducibility failure per se — it is because we counted PlasmidFinder BLAST hits directly while the paper required Bandage circularity confirmation. But it does mean the paper's plasmid counts are only comparable to another Bandage-confirmed pipeline.
- **β-lactamase profile.** The all-assembly β-lactamases (blaTEM-1B, blaCTX-M-14/15, blaSHV, blaOXA family) were confirmed in EC4, KP5, and the reference. The paper's 19 "HybASM-unique" blaTEM/blaSHV variants could not be verified.

---

## 3. What Did Not Succeed (Real Failures)

### 3.1 Paper-side: no assembled genomes deposited
The biggest single obstacle to full replication is that Khezri et al. deposited raw reads but **no assemblies**. To exactly reproduce Table 2 (assembly quality), Section 3.7 (plasmid counts), Section 3.8 (AMR counts and β-lactamase variants), or Section 3.9 (VF counts) at the exact numeric level, one must independently re-assemble all 9 isolates plus the mixed culture across all three strategies. That is not something a light-weight replication can do; it requires ~200–500 core-hours of Unicycler hybrid + Flye compute.

**Impact:** the paper's headline claim (three-way assembler comparison) is *not* independently verifiable at the numeric level from what was deposited. Only the reference-genome sub-claims are fully reproducible.

**Fix (paper side):** deposit `.fasta` files for all assemblies (IllumASM, MinIONASM, HybASM) in Zenodo or FigShare, keyed to the SRA/ENA accessions.

### 3.2 Replication-side: hybrid and long-read assemblies not attempted
This replication chose *not* to run Unicycler hybrid or Flye on the paper's isolates. That choice was driven by compute budget and by the observation that reference-genome verification would already validate the tool-call pipeline. But it means:

- The core three-way comparison (HybASM vs IllumASM vs MinIONASM) is **not tested** in this replication.
- The paper's BUSCO scores (99.3% HybASM, 27.7% MinIONASM) are **not tested**.
- The paper's mixed-culture claims are **not tested**.
- The paper's 19 "HybASM-unique" β-lactamase variants are **not tested**.

**Impact:** roughly 18 of 34 audited claims are marked "not tested" — a genuinely large gap.

**Fix (replication side):** allocate ~2–3 days of compute on a modest cluster to run Unicycler hybrid + Flye on all 9 isolates plus the mixed culture. Add Bandage circularity confirmation to the plasmid pipeline. Re-basecall with modern Dorado SUP if signal data becomes available.

### 3.3 Paper-side: β-lactamase "unique variant" list is over-precise
The reported 8 HybASM-unique blaTEM variants and 11 HybASM-unique blaSHV variants are best understood as ResFinder closest-match assignments, not 19 distinct genes. The paper does not sharply distinguish "distinct gene loci" from "closest-reference-allele assignments"; a reader could easily misinterpret this as evidence of much greater β-lactamase diversity than is actually present.

**Impact:** a headline-friendly number that overstates biological novelty.

**Fix (paper side):** report distinct gene loci and their closest ResFinder variant match separately, with sequence-identity thresholds specified.

### 3.4 Paper-side: MinIONASM verdict is chemistry-locked
The paper's MinIONASM BUSCO (~27.7%) is based on R9.4.1 + Guppy v3, which is 2020-vintage. On R10.4.1 + Dorado SUP, nanopore-only bacterial assemblies routinely exceed 95% BUSCO complete. The paper's framing "MinIONASM is worst" is defensible for its own time but should not be read as a durable technology verdict.

**Impact:** future readers may under-value long-read-only assembly based on stale chemistry.

**Fix (paper side):** future work should explicitly caveat basecaller/chemistry version and, where possible, re-basecall archived data with modern basecallers.

### 3.5 Paper-side: VFDB version drift
Our VFDB (2025) returned 109 VF loci for the reference genome vs the paper's 85 with 2020 VFDB — a 28% jump attributable purely to database growth. Any paper reporting absolute VF counts without pinning the VFDB build cannot be numerically reproduced years later.

**Impact:** the paper's VF numbers are not portable across time.

**Fix (paper side & community-wide):** always pin database version + snapshot the database file used, with a checksum.

### 3.6 Replication-side: mixed-culture claim under-tested
The paper's mixed-culture claims (Section 3.10) rest on a single co-culture (EC4+KP5). We did not re-assemble the mixed culture at all. One observation of tangential interest: our single-isolate SPAdes assembly of EC4 *did* recover sul1 (2 copies), which the paper says was missed in the mixed-culture IllumASM. This could indicate the paper's miss is specific to Unicycler on mixed input — but with an N of 1 for the mixed culture, no confident conclusion is possible.

**Impact:** the mixed-culture claim is essentially untested here.

**Fix (replication side):** re-assemble the mixed culture with Unicycler (both IllumASM and HybASM) and check whether sul1 recovery is Unicycler-specific.

---

## 4. Summary of Failure Modes

| Category | Failure mode | Owner | Fixable? |
|---|---|---|---|
| Data deposit | Assemblies not deposited alongside reads | Paper | Yes — Zenodo/FigShare upload |
| Replication scope | No hybrid assemblies attempted | Replication | Yes — ~2–3 days compute |
| Claim precision | β-lactamase "unique variants" over-precise | Paper | Yes — clarify variant vs locus |
| Technology snapshot | MinIONASM quality tied to Guppy v3 | Paper | Yes — caveat + optional re-basecall |
| Database drift | VF counts non-portable across VFDB versions | Community | Yes — pin + snapshot databases |
| Mixed-culture N | Single co-culture, replication skipped it | Both | Yes — replicate + expand |

---

## 5. Bottom Line

The paper is **honest and internally consistent**, and the parts of it that could be verified independently (reference-genome ground truth, short-read assembly ranges, biological plausibility) verified cleanly. The parts that could not be verified failed for boring, non-adversarial reasons: no deposited assemblies, and a replication effort that intentionally did not carry the compute to close that gap.

The verdict is PARTIAL — not because the paper is wrong, but because the gap between "what the paper claims" and "what a light-weight independent reader can confirm without significant compute" is real and non-trivial. That gap is jointly owned by the authors (didn't deposit assemblies) and by this replication (chose not to run hybrid pipelines).
