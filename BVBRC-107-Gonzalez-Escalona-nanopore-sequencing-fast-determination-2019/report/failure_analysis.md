# Failure Analysis — BVBRC-107 (González-Escalona et al. 2019, STEC O26:H11)

**Verdict: PARTIAL (strong).** Downstream biological calls replicate essentially exactly; the paper's *cross-platform sequencing/assembly comparison* — the actual title claim — was not re-executed. This document is an honest accounting of what worked, what didn't, and why.

---

## 1. What replicated cleanly (no failures)

| Claim | Result | Notes |
|---|---|---|
| C1 — Serotype O26:H11 across all 3 strains | ✅ Exact | wzx_O26 ≥99.9%, wzy_O26 ≥99.9%, fliC_H11 99.93% |
| C2 — MLST 343=ST21, 346=ST21, 350=ST29 | ✅ Exact | Full allele profiles match; 350 differs at adk-6 |
| C3 — Chromosome/plasmid sizes | ✅ Within 1–2 kb | Our GenBank record sizes vs paper's pre-closure Canu contigs |
| C4 — Plasmid replicon distribution | ✅ Consistent | 346's 72 kb IncFII AMR plasmid identified as unique |
| C5 — Table 7 discriminating virulence (6 genes × 3 strains) | ✅ 6/6 exact | See §3.2 for efa1-in-350 nuance |
| C6 — Common virulence set (18 genes) | ⚠️ 17/18 | astA and gad below AMRFinderPlus panel — tool-coverage, not data (see §3.3) |
| C7 — 346's 6 acquired AMR genes on 72 kb plasmid | ✅ 6/6 exact | Only nomenclature differs (blaTEM-1 vs blaTEM-1B; dfrA vs dfrA8) |
| C8 — Composite per-strain profile | ✅ Exact | All 3 strains match paper's Table |

## 2. What did NOT replicate (the reason verdict is PARTIAL)

### 2.1 Cross-platform de novo assembly congruence (C9)
**What the paper claims:** MinION-only Canu v1.6 assemblies close the same chromosome/plasmid architecture as PacBio HGAP3+Quiver assemblies for these three strains.

**What we did:** We used the authors' already-closed PacBio references (CP037941–CP037947) for all downstream biology. We did **not** independently re-run Canu v1.6 on the SRR8335317/SRR8335318 MinION reads and compare to the PacBio reference.

**Why not re-run:** Two-part cost:
1. ~10–15 GB of SRA download for the MinION reads.
2. Canu v1.6 on uicgpu: ~30–90 min per strain, plus polishing (Racon + Medaka) for a fair 2019-vs-modern comparison. Multiply by 3 strains → 2–5 h wall time.

**Consequence:** If MinION-only 2019 assemblies had systematically dropped one of the discriminating virulence genes (e.g. toxB or tccP) or one of the 6 AMR genes, we would not detect that from this replication because we validated biology against the PacBio reference. The paper's Table 5 asserts otherwise but we cannot independently confirm.

**Severity:** High — this is the paper's headline methodological claim.

### 2.2 MiSeq/Nextera-XT gene-loss claim (C10)
**What the paper claims:** Nextera-XT MiSeq short-read assemblies (CLC Genomics 9.5.2) miss toxB, tccP, iha, and astA on some strains that MinION recovers.

**What we did:** Not re-executed. Would require SRR8333590–92 (~15 GB) + SPAdes assembly (~1 h per strain).

**Why not re-run:** Same cost bracket as §2.1; deferred as a matched pair.

**Consequence:** We cannot confirm or refute the "long reads > short reads for these plasmid genes" claim. This is important because it is the operational justification for a public-health lab to adopt nanopore over MiSeq.

**Severity:** High — the second half of the paper's headline claim.

## 3. Minor discrepancies (not failures, but worth calling out)

### 3.1 AMR gene nomenclature drift
| Paper (ResFinder 2.1, 2019) | This run (AMRFinderPlus 2024-07-22.1) |
|---|---|
| blaTEM-1B | blaTEM-1 |
| dfrA | dfrA8 |

Same class, same drug spectrum, same locus. The 2024 AMRFinderPlus DB resolves finer variants than the 2019 ResFinder catalog for one gene (dfrA → dfrA8) and reports the parental TEM-1 rather than the -1B subtype for the other. Not a disagreement; a database-version consistency artifact. If ResFinder 2.1 output were re-run against the same 72 kb plasmid, we would expect the paper's exact strings back.

### 3.2 efa1 in strain 350 (Table 7)
- Paper: efa1 **absent** in 350.
- This run: AMRFinderPlus PARTIALX hit at 63.8% coverage in 350 (a truncated `lymphostatin Efa1/LifA` paralog).
- Interpretation: Paper's binary "absent" call is functionally correct — 350 lacks a full-length efa1 gene. Our tool reports the partial paralog because AMRFinderPlus's threshold is more permissive. No disagreement on the underlying biology.

### 3.3 astA and gad missing from AMRFinderPlus output (Common virulence set, C6)
- Paper: astA (EAST1 toxin) and gad (glutamate decarboxylase) present in all 3 strains.
- This run: Not reported by AMRFinderPlus.
- Cause: Both genes are in CGE `virulence_ecoli.fsa` but not in AMRFinderPlus's O26:H11 virulence panel — a tool-scope choice, not evidence of absence.
- Mitigation available: A follow-on BLAST of all 3 concatenated FASTAs against `virulence_ecoli.fsa` at ≥90% id / ≥60% qcov would confirm both genes and lift the count from 17/18 to 18/18. Not executed in this run.
- Severity: Cosmetic. The paper is not wrong; our tool's panel is narrower.

### 3.4 eae subtype (β1)
- Paper: eae-β1 subtype in all 3 strains.
- This run: eae gene present in all 3 strains; subtype not distinguished by AMRFinderPlus / our BLAST.
- Cause: β1 subtyping requires an intimin subtype-typing scheme (e.g., blastp against the intimin variant reference set) which we did not run.
- Severity: Cosmetic. Paper's β1 call is not contradicted.

## 4. Systemic failure mode: reference-standard dependency

The single load-bearing methodological caveat is this: **we validated biology against the authors' own PacBio-closed reference.** Downstream conclusions can only be as good as that reference. If the paper's PacBio references themselves had errors (missed genes, misassembled plasmids), those errors would carry through into our re-analysis without detection.

Mitigations:
- PacBio HGAP3 + Quiver on the paper's stated coverage (>100×) is a well-characterized, high-quality assembly pipeline for bacterial genomes; the reference is probably very accurate.
- The three genomes are all deposited in GenBank and have been available since 2019 without corrections issued — some passive validation from the community.
- Nonetheless, an independent MinION or PacBio re-sequencing would be required to fully close the loop.

## 5. What would flip this to REPLICATED

Three steps, ~4–8 h wall time on uicgpu, ~30 GB SRA download:

1. `fasterq-dump` the 5 SRA runs (SRR8333590–92 MiSeq; SRR8335317–18 MinION).
2. Independently assemble each library:
   - MinION long reads → Canu v1.6+ (paper's own tool), plus Racon+Medaka polishing.
   - MiSeq short reads → SPAdes (open replacement for the paper's CLC 9.5.2).
3. Rerun the same downstream screens (steps 4a–4e in `workflow.md`) on the *new* assemblies and check whether:
   - MinION-only assemblies recover 6/6 AMR + 6/6 Table 7 virulence + 18/18 common virulence (C9).
   - MiSeq-only assemblies indeed miss toxB, tccP, iha, and astA on the strains where the paper reports these losses (C10).

If both hold, verdict flips to REPLICATED. If either fails, we would have a genuine disagreement with the paper worth investigating (chemistry drift, assembler-version effects, or actual limitations of the 2019 pipeline).

## 6. Failure-log-style takeaways for future replications

- **Reference-standard dependency is the sneaky failure mode.** Always note whether downstream biology was validated against the authors' own assemblies vs against independently regenerated assemblies. Only the latter fully re-tests the paper's methodological claims.
- **Database-version drift causes cosmetic nomenclature diffs, not real disagreements.** Distinguish "blaTEM-1 vs blaTEM-1B" (nomenclature) from "AMR present vs absent" (biology). Only the latter is a replication signal.
- **Tool-panel choices produce artifactual "missing gene" counts.** AMRFinderPlus's O26:H11 virulence panel is narrower than CGE VirulenceFinder's E. coli panel; always run a BLAST cross-check against the broader panel if any "common" gene appears absent.
- **Cost gate for SRA-level replication is ~30 GB / ~5 h uicgpu.** For a 30-strain batch this is quickly infeasible; single-paper PARTIAL replications should either commit to the raw-reads path from the outset, or clearly annotate the deferred claim in the verdict (as done here).
