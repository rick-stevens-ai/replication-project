# Failure Analysis — BVBRC-04 Shrestha 2022 Re-pass

**Paper:** Shrestha et al. 2022, *BMC Genomic Data* 23:4, DOI 10.1186/s12863-021-01020-y.
**Genome:** NZ_CP014517.1 / *Variovorax* sp. PAMC28711.
**Verdict:** PARTIAL. Re-pass 2026-06-23; document generated 2026-07-05.

The re-pass scored COVERAGE = 9/10 and AGREEMENT = 9/10, but the verdict is PARTIAL, not
REPLICATED. This document is an explicit account of *why* — what did not replicate, what
could not be tested, and what the paper itself glosses over. It is deliberately unflattering
where honesty requires it.

---

## 1. Hard blockers (structural — cannot be resolved on free compute)

### 1.1 MetaCyc column of Table 1 (5 of 15 cells)
- **What is blocked:** OtsA / OtsB / TreY / TreZ / TreS presence in MetaCyc for PAMC28711.
- **Why:** MetaCyc's per-organism PGDBs are built with Pathway Tools, which is license-gated.
  No public PAMC28711 PGDB exists.
- **Attempted workarounds:** none that succeed on free compute. Approximating via KEGG KOs
  would replace the paper's actual measurement with a proxy — that is a different experiment,
  not a replication.
- **Effect on verdict:** 5 rows permanently `NOT_TESTED` in `results/repass/claims_enumerated.json`
  (claims 2, 5, 8, 11, 14). Caps testable claim count at 26 / 37.

### 1.2 Table 2 database snapshot statistics (6 numbers)
- **What is blocked:** MetaCyc 2,688 base pathways; KEGG 339 modules; MetaCyc 381 superpathways;
  KEGG 530 pathway maps; MetaCyc 15,329 vs KEGG 11,004 reactions; MetaCyc "2,859 pathways / 3,185
  organisms" from Discussion.
- **Why:** All are August-2018 snapshots. Current KEGG / MetaCyc APIs do not expose historical
  versions in a form that reproduces the 2018 numbers.
- **Attempted workarounds:** Wayback Machine / archived stat pages would only give an
  approximation, not a reproducible query.
- **Effect on verdict:** 6 rows permanently `NOT_TESTED` (claims 16–20 and 31). Not the paper's
  fault — database statistics drift.

### 1.3 External citation (1 claim)
- **What is blocked:** Ref [3] Han et al. 2016 "opine-utilizing" phenotype for PAMC28711.
- **Why:** Out-of-scope for genome replication; the phenotype claim rides on a separate paper.
- **Effect on verdict:** 1 row `NOT_TESTED` (claim 22).

**Total structurally-untestable:** 11 of 37 claims.

---

## 2. Partial replications (something is off, but the paper survives)

### 2.1 TreY coordinate typo (claim 25)
- **The paper says:** "started and stopped at 335612 to 3352054" — one digit is missing.
- **Re-pass finding:** two clean digit restorations both point at the same locus.
  `3356112..3352054` matches BV-BRC RAST peg.3325 (4,059 nt / 1,352 aa) exactly;
  `3357112..3352054` matches PGAP AX767_16200 within 7 bp (3,352,054..3,357,119).
- **Assessment:** typesetting error in the paper, not an analysis error. Marked PARTIAL because
  the string as printed is literally not decodable to a unique locus, even though the biology
  is safe. Peer review missed this.

### 2.2 "Three functional trehalose-biosynthesis pathways" (claims 27, 33)
- **The paper concludes:** PAMC28711 has three biosynthesis pathways operative
  (OtsA-OtsB, TreS, and TreY/TreZ), with MetaCyc biosynthesis I, IV, V represented (V "incomplete").
- **Re-pass finding:** OtsA-OtsB and TreS are cleanly present and functional. The TreY/TreZ
  pathway is partly broken. TreY (AX767_16200) is flagged `/pseudo` by PGAP with a frameshift,
  and KEGG K06044 has ZERO vaa hits. TreZ, TreX, and the full glycogen cluster upstream are
  all functional — everything except the central TreY step is intact.
- **Assessment:** the "three functional pathways" framing is biologically weaker than the paper
  admits. The TreY pseudogene call is publicly available and was not addressed in the paper.
  This is a paper-level interpretive gap, not a replication failure per se — the paper's KEGG
  and RAST tables are all correct — but any honest read of the same evidence should have
  flagged the pseudogene.

### 2.3 MetaCyc "biosynthesis V incomplete" (claim 33)
- **The paper says:** MetaCyc pathway V is present but incomplete in PAMC28711.
- **Re-pass finding:** cannot verify MetaCyc directly (see §1.1). We *can* verify the paper's
  underlying logic: pathway V requires TreX + TreY + TreZ; PAMC28711 has 2 TreX copies + broken
  TreY + functional TreZ + a complete glycogen cluster upstream. So "incomplete" is consistent
  with the free-compute evidence, but the paper's actual MetaCyc-side claim is not directly
  reproducible.

---

## 3. What the paper does not do (methodological limitations)

### 3.1 No functional validation
- The paper's biological conclusions rest 100% on annotation-database output. Zero RT-qPCR,
  zero proteomics, zero growth assays under osmotic or cold stress, zero enzyme activity assays.
- Consequence: the TreY pseudogene story is invisible in KEGG's presence/absence column but
  visible in PGAP's `/pseudo` qualifier. Any in-vitro validation would have caught this.
- Fix (out of scope for a replication): see `report/open_questions.json` Q5 for a minimal in-vitro design.

### 3.2 TreX omitted from Table 1
- Fig 2A of the paper explicitly names TreX (EC 3.2.1.68) as required for MetaCyc pathway V,
  but Table 1 (the "presence in KEGG / MetaCyc / RAST" comparison) has no TreX row.
- Re-pass added TreX and confirmed two functional copies in vaa (AX767_11830 K02438 and
  AX767_10865 K01214). Their absence from Table 1 makes the tri-database comparison
  structurally incomplete for pathway V.

### 3.3 MetaCyc procedure under-described
- The paper reports MetaCyc results without documenting the PGDB build steps, without stating
  a Pathway Tools version, and without recording query dates beyond "August 2018".
- Consequence: even a licensed reader with 2018 archives would struggle to reproduce the
  MetaCyc column exactly.

### 3.4 No cross-strain comparison
- The paper compares three annotation systems on one strain. It never compares one annotation
  system across multiple *Variovorax* spp. or across the Comamonadaceae family. That leaves
  open whether the TreY pseudogenization is strain-specific, clade-level, or family-wide —
  material for interpreting the finding (see `open_questions.json` Q1 and Q3).

### 3.5 No compatible-solute trade-off analysis
- PAMC28711 is Antarctic and lichen-associated — a habitat where osmoprotectants matter. The
  paper never asks what replaces trehalose in a strain where the TreY/TreZ pathway is broken.
  Sucrose, ectoine, and glycine-betaine alternatives are unexamined. (See `open_questions.json` Q2.)

### 3.6 No regulatory-element analysis
- Precise operon coordinates are established in the re-pass (otsBA at 1.238 Mb; treZ/treY/treS
  cluster at 3.35 Mb) but neither the paper nor the re-pass looks upstream for σ-factor binding
  sites, OtsR-family motifs, or cold/osmo-stress promoters. (See `open_questions.json` Q4.)

---

## 4. Confidence summary

| Sub-claim | Confidence | Rationale |
|---|---|---|
| Annotation-divergence thesis (paper's methodological point) | High | KEGG absence of K06044 confirmed by direct link query; RAST presence confirmed by BV-BRC; PGAP flags the same locus `/pseudo`. Every free-compute line of evidence agrees with the paper. |
| Genome features (size, GC, CDS, rRNA, tRNA) | High | Recomputed directly from the PGAP GenBank flatfile. |
| Isolation context (Antarctic, lichen, *Himantormia*, 2015) | High | BV-BRC + PGAP qualifiers all consistent. |
| KEGG vaa infrastructure statements (no dedicated trehalose module) | High | Direct REST queries. |
| MetaCyc column of Table 1 | Not verifiable | License-gated; no PGDB. |
| Table 2 2018 database statistics | Not verifiable | Snapshots not queryable. |
| "Three functional biosynthesis pathways" biological framing | Moderate | Weakened by unaddressed TreY pseudogene. |
| Han 2016 opine-utilizing claim | Not verified | Out-of-scope external citation. |

---

## 5. Bottom line

The paper's *methodological* contribution — documenting real annotation-system divergence on a
concrete biological example — is sound, reproduces cleanly, and is corroborated by an
independent annotator (PGAP) that was not part of the original comparison. That is the piece
we can defend.

The paper's *biological* narrative — that PAMC28711 has three functional trehalose-biosynthesis
pathways — is over-stated. Public evidence (PGAP `/pseudo` on TreY, zero KEGG K06044 hits)
suggests the TreY/TreZ pathway is not functional in this strain, and the paper does not address
this. That is the piece a reviewer should have pushed back on.

Neither of these findings contradicts the paper's data; both point at things it did not do.
Hence PARTIAL, not REPLICATED and not REFUTED.
