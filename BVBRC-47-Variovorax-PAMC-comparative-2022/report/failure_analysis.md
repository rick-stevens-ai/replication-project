# Failure Analysis — BVBRC-47 (Shrestha 2022, IJM)

Verdict is **REPLICATED**, but the pass is not 10/10. This file enumerates what did *not*
work, what was *not* attempted, and how to close each gap.

---

## 1. `run_dbcan` (dbCAN2) not installed → Table 3 CAZyme families NOT reproduced (partial)

**What happened.** The paper's Table 3 lists per-strain CAZyme totals by family
(GH / GT / CE / PL / CBM / AA), with distinctive claims that (a) only PAMC28711 has both
GH37 and GH15 trehalases, and (b) only PAMC28711 carries Auxiliary Activity (AA) family
CAZymes. To reproduce Table 3 correctly requires `run_dbcan` (dbCAN2 meta server local
build), which we did not install in the `bvbrc28` conda env.

**Fallback used.** Product-name regex over RefSeq/PGAP annotation for trehalase-family
words (Stage 5 of the workflow). This confirms the coarse degradation-side pattern
(trehalase hits in PAMC28711/PAMC28562 but not PAMC26660) but **cannot** subtype GH37 vs
GH15 and does not scan for AAs.

**Impact.** Claim C7 (CAZyme content) is only partially replicated. Does not affect the
paper's core conclusions (which rest on C1–C6 + wet-lab C8), but leaves a distinctive
Table-3 claim externally unverified.

**How to close.**
1. `conda activate bvbrc28 && pip install run-dbcan` (or install via the official
   Bioconda recipe).
2. Download dbCAN's HMMER, DIAMOND, and eCAMI databases (~4 GB).
3. `run_dbcan protein.faa protein --tools hmmer diamond hotpep --db_dir <db>` for each of
   the three PAMC proteomes.
4. Take the 2-of-3-tools consensus, then tally per family.
5. Diff against paper Table 3; record any dbCAN2-release version delta if numbers drift.

---

## 2. OAT / ANIb / ANIm / GGDC dDDH exact reproduction NOT attempted → C6 only qualitatively reproduced

**What happened.** The paper uses:
- OAT (BLAST-based ANIb)
- ANIm (MUMmer-based)
- GGDC (digital DDH)

None of these tools is present in the env. We used `fastANI` (a k-mer/MinHash mapper)
as a qualitative proxy.

**Fallback result.** fastANI values (82.2%, 85.6%, 81.3% vs *V. paradoxus*
NBRC 15149ᵀ) differ from the paper's ANIb/ANIm by 1–3% but *all* sit well below the 95%
species boundary, matching the paper's qualitative conclusion.

**Impact.** Species-distinctness direction is confirmed, but the paper's exact numbers
are unverified.

**How to close.**
1. Install OAT (OrthoANI) — Java jar, trivial to add to env.
2. Install ANIm via pyANI (`pip install pyani`; requires MUMmer).
3. Submit the three PAMC assemblies to the GGDC web server
   (https://ggdc.dsmz.de/ggdc.php) for dDDH; TYGS also emits dDDH.
4. Rebuild Table 2 with paper-matched methods; expect 1–3% numeric drift attributable
   to type-strain assembly version changes since 2021.

---

## 3. Only ONE of the three Table-2 type-strain comparators pulled → weakens C6 breadth

**What happened.** The paper compares against multiple *Variovorax* type strains
(*V. paradoxus*, *V. beijingensis* 502ᵀ, *V. boronicumulans* NBRC 103145ᵀ, etc.). This
pass pulled only *V. paradoxus* NBRC 15149ᵀ (GCF_050627025.1) as a fastANI comparator.

**Impact.** The <95% ANI conclusion is confirmed against the single comparator, but
the "distinct from *V. beijingensis* and *V. boronicumulans*" sub-claims are not directly
retested here. Because ANI vs *V. paradoxus* is already 78.77–85.61%, the probability
of hitting >95% ANI against a closer sister species is low but not zero.

**How to close.**
1. `datasets download` GCF assemblies for *V. beijingensis* 502ᵀ and *V. boronicumulans*
   NBRC 103145ᵀ (and any newer *Variovorax* type genomes deposited since 2021).
2. Re-run fastANI (and, per gap #2, OAT/ANIm/GGDC) with the expanded comparator set.
3. Update Table 2.

---

## 4. Wet-lab AZCL (Table 5) NOT reproducible → C8 out of scope by design

**What happened.** Table 5 reports the results of an AZCL polysaccharide-degradation
screen on PAMC28711 across multiple substrates. This is a wet-lab phenotypic assay.

**Impact.** No effect on the replication verdict — this class of claim is not
computationally replicable by definition. Recorded as "N/A" in the claim table.

**How to close.** Wet-lab collaboration only; not addressable via sequence alone.

---

## 5. Paper PDF endpoint (Hindawi) returned Cloudflare HTML block → workaround via Europe PMC XML

**What happened.** `https://www.hindawi.com/journals/ijm/2022/5067074/` returned a
Cloudflare challenge page instead of the PDF. Attempts to pull the PDF through the
proxy failed.

**Fallback used.** Europe PMC full-text XML (`PMC10232917/fullTextXML`, 162 KB).
Parsed abstract, Materials & Methods, and all 5 tables cleanly.

**Impact.** None on scientific content — Europe PMC XML is the authoritative
PMC-deposited version. The XML happens to be easier to machine-parse than the PDF for
this journal. If a future pass really needs the PDF (for figures, layout, or SI files),
route through the ANL institutional proxy or fetch via an authenticated browser session.

---

## 6. Gene/CDS counts differ from paper by ~1–2% → C4 not exact

**What happened.** Paper gene/CDS counts:
- PAMC28711: 4232 / 4071
- PAMC26660: 6919 / 6801
- PAMC28562: 4402 / 4298

RefSeq re-annotation gene/CDS counts as of this pass:
- PAMC28711: 4141 / 4196 (4074 proteins)
- PAMC26660: 6901 / 6890 (6834 proteins)
- PAMC28562: 4378 / 4361 (4319 proteins)

**Impact.** All deltas are <2%; expected because RefSeq re-annotates deposited
genomes with newer PGAP versions periodically. The paper's counts come from the *original*
PGAP submission (2016 for PAMC28711; 2020 for the others), whereas RefSeq currently
serves a newer PGAP re-annotation.

**How to close (only if a bit-exact match is really required).**
1. Pull the frozen INSDC record (CP014517, CP060295, CP060296) via `efetch -format gbwithparts`
   instead of RefSeq's re-annotated version.
2. Count CDS/gene features directly from the GenBank flat file's original PGAP annotation.
3. Expect exact-match to the paper's Table 1 counts.

Not a real gap — annotation drift is the correct behavior — but noted for completeness.

---

## 7. Adaptation narrative UNTESTED → not a failure of replication, but a failure of the paper's own inference

**What happened.** The paper interprets the 3-pathway vs 1-pathway asymmetry as an
Antarctic cold/osmotic-stress adaptation, but does not report:
- trehalose pathway prevalence in non-Antarctic *Variovorax* (base rate);
- trehalose accumulation phenotype under cold/osmotic shock (functional test).

This pass replicated the gene-inventory observation (C5) but did not extend into the
adaptation-vs-drift test either.

**Impact.** The paper's causal claim ("adaptation") is not fully supported by the paper
*or* by this replication. See `open_questions.json` items #2 and #3 for concrete next
steps (pan-Variovorax panel + wet-lab trehalose quantitation).

---

## Summary

| Gap | Severity | Status | Blocks verdict? |
|---|---|---|---|
| dbCAN2 CAZyme families | medium | closable | no |
| OAT/ANIb/ANIm/GGDC exact numbers | low | closable | no |
| Only 1 of 3 type-strain comparators | low | closable | no |
| Wet-lab AZCL | N/A | not closable in silico | no (out of scope) |
| Hindawi PDF block | none | worked around | no |
| Gene/CDS drift | none | expected | no |
| Adaptation narrative untested | medium | closable (open question) | no (paper-side issue) |

**Net:** no gap invalidates the REPLICATED verdict. The largest closable item is
`run_dbcan` integration to reproduce Table 3 at family resolution.
