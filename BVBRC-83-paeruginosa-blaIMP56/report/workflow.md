# Workflow — BVBRC-83 Independent Replication

**Paper:** Gómez-Martínez et al. 2022, *Microorganisms* 10(9): 1863
**Target:** GenBank CP102481.1 (pPE52IMP, 27,635 bp, *P. aeruginosa* PE52)
**Run date:** 2026-07-03
**Compute:** Local (Argo proxy free tier for LLM judges; no paid API calls)

---

## Stage 0 — Scope & claim extraction

**Input:** paper PDF + supplementary tables (open access, CC-BY).
**Output:** 13-row `claims table` (C1–C13) tagging each claim as Numeric / Structural / Compositional / Classification / Phylogenetic, plus a "testable from public data?" column.

Rationale: the paper mixes hard structural claims (size, %GC, gene inventory) with softer interpretive claims (novel family, non-typeable). Splitting them up front decides which are targets of the replication and which are noted-but-not-tested.

**Decision:** 12/13 claims addressable from public data; C13 (PBRT non-typeability) requires wet-lab and is scored as "indirect" only.

---

## Stage 1 — Data fetch

**Tool:** `curl` against NCBI EUtils `efetch.fcgi`
**Records pulled:**

| Accession       | Plasmid              | Role     |
|-----------------|----------------------|----------|
| CP102481.1      | pPE52IMP             | target   |
| AM778842.1      | pMATVIM-7            | sibling  |
| CP033834.1      | unnamed FDAARGOS_570 | sibling  |
| KX169264.1      | pD5170990            | sibling  |
| KP975076.1      | pMRVIM0713           | sibling  |
| MN336501.1      | p4130-KPC            | sibling  |

**Format:** GenBank flat file (`rettype=gb&retmode=text`).
**Storage:** `work/genbank/*.gb` (not read by this backfill run; artifacts_summary lists them).

---

## Stage 2 — Structural analysis (self-check of C1–C6, C9)

**Script:** `work/analyze_ppe52imp.py`
**Libraries:** Biopython 1.85 (`Bio.SeqIO`, `Bio.SeqUtils.gc_fraction`)
**Python:** 3.14

**Per-plasmid computations:**
1. Parse LOCUS line → topology (circular/linear).
2. Recompute total length from raw nucleotide string → cross-check LOCUS length.
3. Recompute `gc_fraction(record.seq)` → cross-check paper's %GC.
4. Enumerate `record.features` where `feature.type == 'CDS'` → CDS count.
5. For each CDS, concatenate `/product`, `/gene`, `/note` qualifiers and substring-match against a keyword list: `merR|merT|merP|merA|merD|merE|parB|phd|doc|intI1|blaIMP|aadA1|blaOXA|qacE|sul1|traJ|traK|virB4|trbJ|blaVIM|blaKPC|kfrA|RepA|MOB|relaxase`.

**Output:** per-plasmid presence/absence tally + numeric metrics table.

---

## Stage 3 — Central-claim test: RepA & MOBP11 phylogenetic clustering (C10, C11)

**Rationale.** The paper's headline novelty ("new plasmid family") is a phylogenetic-clustering claim: pPE52IMP's RepA groups with five named siblings. The strongest computational proxy for that specific membership claim is pairwise protein-sequence identity — a tree topology adds nothing if the leaves are 100% identical.

**Procedure:**
1. Locate candidate RepA on pPE52IMP: 301 aa "DNA-binding domain-containing protein" at bp 7370–8276.
2. Locate candidate MOBP11 relaxase: 609 aa "relaxase/mobilization nuclease domain-containing protein" at bp 9568–11398.
3. Export both as FASTA (query set, 2 sequences).
4. Extract all CDS from the five sibling GenBank files (subject set, 222 proteins total).
5. `makeblastdb -in siblings_all_proteins.faa -dbtype prot`
6. `blastp -query queries.faa -db siblings_all_proteins -evalue 1e-3 -outfmt 6 -out repa_mobp11_vs_siblings.tsv`
7. For each sibling plasmid, keep the best (lowest e-value) hit per query.

**Tool versions:** NCBI BLAST 2.17.0 (Homebrew).

**Passing criterion:** RepA present at ≥ 40% identity in ≥ 4 of 5 siblings = paper's clustering claim supported. (Observed: 100% identity in 4 of 5; the 5th, pD5170990, is expected to be missing per the paper's own Fig 3.)

---

## Stage 4 — Cross-plasmid structural cross-tab (C12 and paper Fig 3 / Table S2)

**Procedure:** for each of the six plasmids (target + 5 siblings), tally presence (1/0/count) of the following features by qualifier-substring match: `traJ, traK, trbJ, merA, blaKPC, blaVIM, blaOXA, intI1`.

**Passing criterion for C12 specifically:** `traJ == 0 AND traK == 0 AND kfrA == 0` in pD5170990 only.
(Observed: pD5170990 uniquely satisfies this — matches paper's Fig 3 explicit call-out.)

---

## Stage 5 — LLM-judge verdict

**Judges:** two Argo-proxy free-tier models — `argo:gpt-4o` and `argo:gpt-5.2`.
**Prompt:** the full 13-claim reproduction table (paper column vs independent column vs delta), plus a fixed rubric asking each judge to return a JSON object:
```json
{ "n_match": int, "n_close": int, "n_supported": int, "n_mismatch": int,
  "verdict": "REPLICATED|PARTIAL|FAILED|INCONCLUSIVE", "one_sentence": string }
```
**Auth:** `Authorization: Bearer stevens` against `http://127.0.0.1:44497/v1` (Argo wrapper).
**Cost:** $0.00 (Argo free tier per standing "免费 endpoint 唯一" policy).

**Concurrence check:** both judges returned identical scores (11 / 1 / 1 / 0) and identical verdict (REPLICATED). Recorded as a weak-independent concurrence — see critique §5 for why this is not two-independent-experts strength.

---

## Stage 6 — Verdict + WAVE_RESULT emission

**Verdict rule (project convention):**
- REPLICATED   = n_mismatch == 0 AND (n_match + n_close + n_supported) / total ≥ 0.85
- PARTIAL      = 0 < n_mismatch ≤ 20% of total
- FAILED       = n_mismatch > 20% of total OR any headline claim mismatches
- INCONCLUSIVE = one or more claims un-testable AND remainder passes but with < 8 tested claims

**Observed:** 11 match + 1 close + 1 supported + 0 mismatch of 13 → REPLICATED.

**Emission line (canonical, machine-parseable):**
```
WAVE_RESULT set=BVBRC paper=BVBRC-83 verdict=REPLICATED
dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-83-paeruginosa-blaIMP56/
one_line=pPE52IMP (CP102481.1) 27,635 bp / 62.2% GC / blaIMP-56 integron /
         MOBP11 relaxase all confirmed; RepA=KfrA 100% identical to 4/5 sibling plasmids
```

---

## Stage 7 — Backfill (this run)

**Purpose:** the primary REPORT.md was already produced. This backfill turn writes the standard five sidecar artifacts (`REPORT.tex`, `open_questions.json`, `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`) from REPORT.md without re-running any analysis, so the project directory conforms to the fleet-wide replication-artifact schema.

**Rule respected:** no fetches, no re-analysis, no `work/` reads. All new files are derived from `report/REPORT.md` text only.

---

## Explicitly NOT attempted (with reason)

| Skipped step                              | Reason                                                                                             |
|-------------------------------------------|----------------------------------------------------------------------------------------------------|
| De novo Illumina assembly (plasmidSPAdes) | Paper deposited final assembly (CP102481.1); rerun would re-derive same sequence.                  |
| MEGA v11 UPGMA tree over 33 taxa          | Pairwise BLAST at 100% identity is strictly stronger than any tree-topology metric for the specific membership claim. |
| Wet-lab PBRT PCR                          | Not doable computationally; requires physical PCR panel with degenerate primers.                   |
| oriT / MOB-suite completeness typing      | Not required for the 13 claims scored; flagged as OQ1 next-steps.                                 |
| BLDB / CARD allele-level blaIMP re-typing | Not required for C7 (accepted GenBank product qualifier); flagged as OQ3 next-steps.               |

---

## Reproduction pointer

To re-run this workflow on a different plasmid paper:
1. Extract 10–15 testable claims into a `claims table` (Stage 0).
2. Pull deposited sequence + sibling records from NCBI EUtils (Stage 1).
3. Structural self-check in Biopython (Stage 2).
4. Central-claim pairwise BLASTp (Stage 3).
5. Feature cross-tab (Stage 4).
6. Two-judge LLM verdict via Argo (Stage 5).
7. Emit WAVE_RESULT + write the 5 sidecar artifacts (Stages 6–7).
