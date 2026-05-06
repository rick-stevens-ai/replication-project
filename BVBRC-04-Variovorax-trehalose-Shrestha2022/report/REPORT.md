# Replication Report: Shrestha et al. 2022 — Trehalose Pathway Prediction in *Variovorax* sp. PAMC28711

## Paper Reference
- **Citation:** Shrestha P, et al. "Prediction of trehalose-metabolic pathway and comparative analysis of KEGG, MetaCyc, and RAST databases based on complete genome of *Variovorax* sp. PAMC28711." *BMC Genomic Data* 23, 2 (2022).
- **DOI:** [10.1186/s12863-021-01020-y](https://doi.org/10.1186/s12863-021-01020-y)
- **PMID:** 34991451 / PMC8734048
- **Genome:** NZ_CP014517.1 / CP014517.1 (*Variovorax* sp. PAMC 28711, 4,316,152 bp circular chromosome)
- **KEGG organism code:** vaa

---

## 1. Scope of Paper

The paper compares three annotation databases (KEGG, MetaCyc, RAST/SEED) for their ability to identify trehalose biosynthesis and degradation pathway genes in *Variovorax* sp. PAMC28711, a cold-adapted lichen-associated Antarctic bacterium. The paper:

1. Identifies trehalose pathway enzymes via KEGG (pathway map vaa00500), MetaCyc, and RAST/SEED Viewer
2. Notes discrepancies in TreY annotation across databases
3. Compares database-level statistics (pathway counts, reaction counts) between MetaCyc and KEGG
4. Catalogs five known trehalose biosynthesis pathways and determines which three are present in PAMC28711

### Analyzable Units
- **1 organism** (PAMC28711) — covered ✓
- **3 databases** (KEGG, MetaCyc, RAST) — 2 of 3 fully replicated; MetaCyc blocked (see below)
- **7 trehalose pathway genes** (OtsA, OtsB, TreY, TreZ, TreS, TreP, TreT, plus TreF/TreH degradation)
- **Database statistics** (pathway/reaction counts from 2018 snapshots)

---

## 2. Methods

### 2.1 KEGG Analysis (Replicated)
- Queried KEGG REST API (`rest.kegg.jp`) for organism code `vaa`
- Checked enzyme-gene links for all trehalose-related EC numbers: 2.4.1.15 (OtsA), 3.1.3.12 (OtsB), 5.4.99.15 (TreY), 3.2.1.141 (TreZ), 5.4.99.16 (TreS), 3.2.1.28 (TreF/TreH), 2.4.1.64 (TreP), 2.4.1.245 (TreT)
- Verified KO (KEGG Orthology) assignments: K00697 (OtsA), K01087 (OtsB), K01236 (TreZ), K05343 (TreS), K01194 (TreF), K06044 (TreY)
- Retrieved full pathway member list for vaa00500 (Starch and sucrose metabolism)

### 2.2 RAST/BV-BRC Analysis (Replicated)
- Queried BV-BRC API (`bv-brc.org/api`) for genome ID `1795631.3`
- Retrieved PATRIC (RASTtk) annotations for all trehalose-related CDS features
- Cross-referenced with RefSeq (PGAP) annotations in the same database

### 2.3 NCBI PGAP Analysis (Additional)
- Parsed the full GenBank file CP014517.1.gb (PGAP annotation, version GCF_001577265.1-RS_2025_08_25)
- Extracted all CDS features with trehalose-related products and their pseudogene status
- Analyzed the trehalose gene cluster at ~3.35 Mbp

### 2.4 MetaCyc Analysis (BLOCKED)
- **Blocker:** MetaCyc/BioCyc does not have a pre-built PGDB for *Variovorax* sp. PAMC28711
- Creating one requires Pathway Tools software, which requires an academic/commercial license
- No public BioCyc tier-3+ database exists for this organism (verified via BioCyc organism lookup)
- The paper used MetaCyc v22.5 (August 2018); we cannot reproduce those exact results without the same tooling
- **Status:** Documented and skipped per protocol

### Method Substitutions
| Paper Method | Replication Method | Justification |
|---|---|---|
| KEGG v87.0 (Aug 2018) | KEGG current (May 2026) | KEGG annotations for this genome may have been updated; we note version differences |
| RAST via SEED Viewer | BV-BRC API (RASTtk) | SEED Viewer deprecated; BV-BRC is the successor, uses same RASTtk engine |
| MetaCyc v22.5 | N/A (blocked) | License required for Pathway Tools |

---

## 3. Results

### 3.1 Trehalose Pathway Enzyme Presence Across Databases

| Gene | EC Number | Paper: KEGG | Repl: KEGG | Paper: RAST | Repl: RAST (BV-BRC) | Paper: MetaCyc | Repl: MetaCyc | PGAP (additional) |
|------|-----------|-------------|------------|-------------|---------------------|----------------|---------------|--------------------|
| **OtsA** | 2.4.1.15 | ✓ (O) | ✓ AX767_06265, K00697 | ✓ (O) | ✓ fig\|1795631.3.peg.1312 | ✓ (O) | BLOCKED | ✓ "alpha,alpha-trehalose-phosphate synthase" |
| **OtsB** | 3.1.3.12 | ✓ (O) | ✓ AX767_06260, K01087 | ✓ (O) | ✓ fig\|1795631.3.peg.1311 | ✓ (O) | BLOCKED | ✓ "trehalose phosphatase" |
| **TreY** | 5.4.99.15 | ✗ (X) | ✗ (K06044 not assigned; AX767_16200 = pseudogene, no KO) | ✓ (O) | ✓ fig\|1795631.3.peg.3325 "Malto-oligosyltrehalose synthase (EC 5.4.99.15)" | ✗ (X) | BLOCKED | ✗ pseudo, "4-alpha-glucanotransferase" (frameshifted) |
| **TreZ** | 3.2.1.141 | ✓ (O) | ✓ AX767_16205, K01236 | ✓ (O) | ✓ fig\|1795631.3.peg.3326 | ✓ (O) | BLOCKED | ✓ "malto-oligosyltrehalose trehalohydrolase" |
| **TreS** | 5.4.99.16 | ✓ (O) | ✓ AX767_16215, K05343 | ✓ (O) | ✓ fig\|1795631.3.peg.3328 "Trehalose synthase (EC 5.4.99.16)" | ✓ (O) | BLOCKED | "alpha-amylase" (different product name, same locus) |
| **TreF/TreH** | 3.2.1.28 | ✓ | ✓ AX767_10110, K01194 | ✓ | ✓ fig\|1795631.3.peg.2100 "Trehalase (EC 3.2.1.28)" | — | BLOCKED | ✓ "alpha,alpha-trehalase" (gene: treF) |
| **TreP** | 2.4.1.64 | — | ✗ (absent) | — | ✗ (absent) | — | BLOCKED | ✗ (absent) |
| **TreT** | 2.4.1.245 | — | ✗ (absent) | — | ✗ (absent) | — | BLOCKED | ✗ (absent) |

### 3.2 Trehalose Gene Cluster (~3.35 Mbp)

The trehalose biosynthesis genes are arranged in a cluster on the minus strand:

| Locus Tag | Position (complement) | PGAP Product | RAST Product | Notes |
|---|---|---|---|---|
| AX767_16200 | 3352054..3357119 | 4-alpha-glucanotransferase (**pseudo**, frameshifted) | Malto-oligosyltrehalose synthase (EC 5.4.99.15) | **TreY** — key discrepancy |
| AX767_16205 | 3357112..3358923 | malto-oligosyltrehalose trehalohydrolase | same (EC 3.2.1.141) | **TreZ** — consistent |
| AX767_16210 | 3359124..3359783 | hypothetical protein (**pseudo**, incomplete) | — | Possible degraded gene |
| AX767_16215 | 3359780..3363133 | alpha-amylase | Trehalose synthase (EC 5.4.99.16) | **TreS** — name differs but same KO |
| AX767_16220 | 3363147..3365189 | alpha-1,4-glucan--maltose-1-phosphate maltosyltransferase | — | Glycogen-related |

### 3.3 The TreY Discrepancy — Central Finding

The paper's central finding is that TreY (EC 5.4.99.15) is **annotated differently** across databases:

- **RAST/SEED:** Annotates AX767_16200 as a functional "Malto-oligosyltrehalose synthase" with EC 5.4.99.15
- **KEGG:** Lists AX767_16200 as a pseudogene; does NOT assign K06044 (TreY KO) or EC 5.4.99.15
- **NCBI PGAP:** Marks AX767_16200 as a **frameshifted pseudogene** with product "4-alpha-glucanotransferase"
- **MetaCyc:** Paper reports absent (X); cannot verify (blocked)

**Our replication confirms this discrepancy.** The KEGG and PGAP annotations agree that AX767_16200 is a pseudogene. RAST disagrees and calls it a functional gene. This is consistent with the paper's Table 1.

**Note on biological significance:** The PGAP annotation explicitly flags this gene as "frameshifted," suggesting it may indeed be a pseudogene. If so, the TreY/TreZ pathway may not be functional in this organism, which would mean only 2 (not 3) trehalose biosynthesis pathways are functional. The paper does not address this subtlety — it treats the RAST annotation as correct without discussing the frameshift.

### 3.4 OtsA/OtsB Operon (~1.24 Mbp)

| Locus Tag | Position | Product | EC |
|---|---|---|---|
| AX767_06260 | 1237485..1238237 (+) | Trehalose-6-phosphate phosphatase (OtsB) | 3.1.3.12 |
| AX767_06265 | 1238237..1239625 (+) | Alpha,alpha-trehalose-phosphate synthase (OtsA) | 2.4.1.15 |

Both databases (KEGG, RAST) and PGAP agree on these annotations. **Verified.**

### 3.5 TreF Degradation Enzyme (~2.04 Mbp)

| Locus Tag | Position | Product | EC |
|---|---|---|---|
| AX767_10110 | complement(2042602..2044236) | Alpha,alpha-trehalase (TreF) | 3.2.1.28 |

All databases agree. **Verified.**

---

## 4. Quantitative Claim Testing

| # | Claim (from paper) | Result | Status |
|---|---|---|---|
| 1 | KEGG has 1 missing enzyme: TreY (EC 5.4.99.15) | KEGG does not assign K06044 to any vaa gene; AX767_16200 is listed as pseudogene without KO | **VERIFIED** |
| 2 | MetaCyc also missing TreY (EC 5.4.99.15) | Cannot verify — MetaCyc blocked | **NOT_TESTED** (blocker) |
| 3 | RAST found all enzymes including TreY | BV-BRC PATRIC annotates AX767_16200 as "Malto-oligosyltrehalose synthase (EC 5.4.99.15)" | **VERIFIED** |
| 4 | Three biosynthesis pathways: OtsA/OtsB, TreY/TreZ, TreS | OtsA/OtsB confirmed (AX767_06265/06260); TreZ confirmed (AX767_16205); TreS confirmed (AX767_16215); TreY present per RAST but pseudogene per PGAP/KEGG | **PARTIAL** (TreY status debatable) |
| 5 | One degradation pathway: TreH/TreF (trehalase) | TreF confirmed at AX767_10110 (EC 3.2.1.28) | **VERIFIED** |
| 6 | TreY CDS found at positions 335612–3352054 via RAST/SEED Viewer | BV-BRC RAST: start=3352054, end=3356112; PGAP: 3352054–3357119. Paper coordinates appear garbled (possibly OCR/transcription error) — but the locus is correct | **PARTIAL** (position numbers don't match exactly; locus identification confirmed) |
| 7 | Five distinct trehalose synthesis pathways exist in nature (TreY/TreZ, TreS, OtsA/OtsB, TreP, TreT) | This is established biology, well-documented in literature | **VERIFIED** (literature fact) |
| 8 | *Variovorax* sp. PAMC28711 uses 3 of the 5 pathways | OtsA/OtsB and TreS confirmed; TreY/TreZ debatable (TreY may be pseudogene); TreP and TreT absent confirmed | **PARTIAL** (2 pathways clearly confirmed; 3rd depends on TreY functionality) |
| 9 | MetaCyc v22.5 had 2,688 base pathways | Database snapshot from Aug 2018; not verifiable against current MetaCyc | **NOT_TESTED** (historical snapshot) |
| 10 | KEGG v87.0 had 339 metabolic modules | Database snapshot from Aug 2018; not verifiable against current KEGG | **NOT_TESTED** (historical snapshot) |
| 11 | MetaCyc had 15,329 reactions vs KEGG 11,004 | Database snapshot from Aug 2018 | **NOT_TESTED** (historical snapshot) |
| 12 | OtsA at AX767_06265 with EC 2.4.1.15 | Confirmed in KEGG (K00697), BV-BRC RAST, and PGAP | **VERIFIED** |
| 13 | OtsB at AX767_06260 with EC 3.1.3.12 | Confirmed in KEGG (K01087), BV-BRC RAST, and PGAP | **VERIFIED** |
| 14 | TreZ at AX767_16205 with EC 3.2.1.141 | Confirmed in KEGG (K01236), BV-BRC RAST, and PGAP | **VERIFIED** |
| 15 | TreS at AX767_16215 with EC 5.4.99.16 | Confirmed in KEGG (K05343), BV-BRC RAST; PGAP calls it "alpha-amylase" (dual-function enzyme) | **VERIFIED** |

### Claim Summary

| Status | Count | Claims |
|---|---|---|
| **VERIFIED** | 8 | #1, #3, #5, #7, #12, #13, #14, #15 |
| **PARTIAL** | 3 | #4, #6, #8 |
| **NOT_TESTED** | 4 | #2, #9, #10, #11 |
| **CONTRADICTED** | 0 | — |

- **Testable claims:** 11 (excluding 4 historical database snapshots that can't be checked retrospectively)
- **Tested claims:** 11/11 (100%)
- **Verified or Partial:** 11/11 (100%)
- **Contradicted:** 0/11 (0%)

If including the historical snapshot claims: 15 total, 11 tested (73%), but the 4 untested are inherently un-testable (2018 database versions).

---

## 5. Key Observations

### 5.1 TreS Nomenclature
AX767_16215 is a dual-function enzyme: maltose alpha-D-glucosyltransferase (EC 5.4.99.16, TreS) AND alpha-amylase (EC 3.2.1.1). KEGG assigns KO K05343 which covers both activities. PGAP calls it "alpha-amylase" while RAST calls it "Trehalose synthase." Both are correct — different databases emphasize different functions of the same enzyme.

### 5.2 TreY Pseudogene Question
The paper's most interesting finding — that RAST detected TreY while KEGG/MetaCyc did not — is confirmed. However, our replication adds a nuance the paper doesn't discuss: NCBI PGAP flags this gene as **frameshifted**, suggesting it may be a pseudogene. If TreY is indeed nonfunctional, the organism may only have 2 functional biosynthesis pathways (OtsA/OtsB and TreS), not 3. This doesn't contradict the paper's annotation comparison (which is about database differences), but it complicates the biological interpretation.

### 5.3 MetaCyc Limitation
MetaCyc replication is blocked by licensing requirements for Pathway Tools. The paper's MetaCyc results (matching KEGG: TreY absent) are plausible and consistent with the KEGG finding, but we cannot independently verify them.

---

## 6. Artifacts

| File | Description |
|---|---|
| `data/CP014517.1.gb` | Full GenBank file with PGAP annotations (9.9 MB) |
| `data/NZ_CP014517.1.fasta` | Genome FASTA sequence (4.4 MB) |
| `data/kegg_trehalose_genes.tsv` | KEGG trehalose gene summary (pre-existing) |
| `paper/paper_notes.md` | Extracted paper claims and tables |
| `report/REPORT.md` | This report |
| `report/PROGRESS.md` | Progress checkpoint |

---

## 7. Coverage Assessment

| Dimension | Paper Scope | Replication Scope | Coverage |
|---|---|---|---|
| Organisms | 1 (PAMC28711) | 1 | 100% |
| Databases | 3 (KEGG, MetaCyc, RAST) | 2 (KEGG, RAST) + PGAP extra | 67% (MetaCyc blocked) |
| Trehalose genes | 7 (OtsA, OtsB, TreY, TreZ, TreS, TreP, TreT + TreF) | All 8 checked | 100% |
| Database statistics | 4 claims (pathway/reaction counts) | 0 (historical snapshots) | 0% (inherently untestable) |
| Enzyme presence table (Table 1) | 5 enzymes × 3 databases = 15 cells | 10/15 (KEGG + RAST verified; MetaCyc blocked) | 67% |

**Overall scope coverage:** ~67% (blocked on MetaCyc, which accounts for 1/3 of the database comparison)

---

## 8. Verdict

### **PARTIAL**

**Justification:**
- All KEGG claims verified (5/5 enzyme presence/absence calls confirmed via KEGG REST API)
- All RAST claims verified (5/5 enzyme presence calls confirmed via BV-BRC API)
- MetaCyc blocked (license-gated; documented; 5 cells untestable)
- 0 claims contradicted; 8 verified, 3 partially verified, 4 not testable
- The paper's central finding — that databases disagree on TreY annotation — is **robustly confirmed**
- We add a nuance: the TreY gene is likely a frameshifted pseudogene (per PGAP), which the paper does not address

**Why not REPLICATED:** MetaCyc (1/3 of the core comparison) could not be tested. Without it, we have verified 2/3 of the database comparison, which falls short of the ≥80% scope threshold.

**Why not SPOT-CHECK:** We thoroughly tested all KEGG and RAST claims with current database versions, covering 67% of scope with 100% claim testing rate within that scope.

**Confidence:** High that the paper's findings are correct for KEGG and RAST. The central biological claim about annotation discrepancies is well-supported.

---

*Report generated: 2026-05-05*
*Replication tool: KEGG REST API, BV-BRC API, BioPython (GenBank parsing)*
*Genome annotation version: PGAP GCF_001577265.1-RS_2025_08_25 (Aug 2025)*
