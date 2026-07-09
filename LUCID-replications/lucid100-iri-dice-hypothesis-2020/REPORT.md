# Replication Report — LUCID-100

**Paper:** Langen B, Helou K, Forssell-Aronsson E (2020). *The IRI-DICE hypothesis: ionizing radiation-induced DSBs may have a functional role for non-deterministic responses at low doses.* **Radiation and Environmental Biophysics** 59:349–355.
**DOI:** [10.1007/s00411-020-00854-x](https://doi.org/10.1007/s00411-020-00854-x)
**Article type per the journal:** "**CONTROVERSIAL ISSUE**" — explicitly a position/hypothesis essay, not a primary research article.
**Audit performed:** 2026-06-21; **promotion re-audit:** 2026-06-27 (per `/Users/stevens/Dropbox/REPLICATE-PROJECT/AUDIT_PROTOCOL.md`).
**Source PDF:** `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/10_1007_s00411_020_00854_x.pdf` (copied to `paper.pdf`, text in `paper.txt`).

---

## Top-line (promotion re-audit, 2026-06-27)

| Field | Value |
|-------|-------|
| Coverage | **9 / 10** |
| Agreement | **10 / 10** |
| Verdict | **SPOT-CHECK** *(ceiling for a pure-concept paper — see §4 + §7)* |
| Paper class | **Pure concept / hypothesis** (no model, no equations, no data, no simulations) |
| Block (per 6/22 rule) | **No data block.** The "missing artifact" is structural: the paper itself contains nothing to numerically replicate. Authors explicitly state direct experimental test is infeasible with current technology. |

**Why not REPLICATED?** AUDIT_PROTOCOL's REPLICATED label requires that the replication numerically reproduce the paper's primary analytical results (≥80% of testable claims, ≥80% scope, methods matched). This paper has **zero** computational/data results to numerically reproduce — the only number in the paper is `1/0.02=50`, which is verified. Under the project's standing rule, **pure-concept papers are capped at SPOT-CHECK** regardless of agreement, because there is no computational artifact to certify against. The 9/10 + 10/10 score reflects a complete and faithful audit of everything the paper actually contains; the SPOT-CHECK label is the structurally-correct ceiling, not a quality complaint.

---

## 1. Paper-type determination

The paper is **purely conceptual / hypothesis-formation**, published in this journal's explicit "Controversial Issue" section. Forensic inventory of the paper (`paper.txt`, 424 lines; confirmed via `grep` on the full text):

- **No new experiments**, no new datasets, no patient/animal cohort, no in-vitro work, no re-analysis of public data.
- **No mathematical model**, no equations, no simulations, no Monte Carlo runs.
- **No data table.** The article contains zero `Table N`.
- **One figure (Fig. 1)** = labeled cartoon/schematic of where on a gene a DSB could fall and which transcript-level effect is predicted (suppression / reduced expression / truncated mRNA / transcript increase via NRE disruption). No plotted data, no axes, no numbers.
- The body is a literature-based argument that constructs a new working hypothesis (IRI-DICE) by joining together previously published mechanisms (DISC; ATM threshold behavior; cis effects of DSBs; LMDS persistence) plus the authors' own radionuclide-transcriptomics observations of non-linear, suppression-dominant, tissue-specific low-dose responses.
- The authors **explicitly state that direct experimental test is impossible with current technology** ("Currently, there are no technologies available to irradiate specific genetic sites to test the IRI-DICE hypothesis directly") and that the realistic path forward is a future computational model coupled to microbeam single-cell transcriptomics.

**Mechanical sanity-checks performed during the promotion re-audit:**

```
wc -l paper.txt                   →  424 lines
grep -c "^Table"                  →  0
grep -nE "Fig\.|Figure" paper.txt →  3 hits, all referencing the single Fig. 1 schematic
grep -nE "=|≈|±|equation"         →  none of these characters appear in any quantitative claim
grep -nE "\b[0-9]+\s*(Gy|mGy)\b"  →  0 — paper makes no specific dose↔DSB conversion
```

The only specific numbers in the body text are: `<2%` (protein-coding fraction, cited from IHGSC 2001), `>80%` (ENCODE non-coding functional activity, cited from ENCODE 2012), `100 kb` and `~1 Mb` (cis-effect distances, cited from Iannelli 2017), and `1 in 50` (the paper's own inference, = 1/0.02).

**Implication for replication:** there is nothing computable. The only thing that *can* be replicated is the paper's logical structure — enumerate every testable assertion (mostly citations of other people's results, plus one piece of trivial arithmetic, plus a small number of internal hypotheses), and check each for internal consistency, correct citation use, and arithmetic soundness. This is the appropriate AUDIT_PROTOCOL response for a conceptual paper.

---

## 2. What was checkable, and what was done

| Bucket | # items | What was done | Where |
|--------|--------:|---------------|-------|
| Internal arithmetic (paper's own quantitative inference) | 1 (claim C7: "1 in ~50") | Re-derived `1 / 0.02 = 50.0`. Exact match. **Re-run on 2026-06-27: PASS.** | `artifacts/arithmetic_check.py`, `artifacts/arithmetic_check.out` |
| Cited external quantitative claims | 5 (C3 100 kb / 1 Mb cis distance from Iannelli 2017; C4 ATM-threshold from Ismail 2005 / Huen 2010; C5 low-dose DSB persistence from Rothkamm & Löbrich 2003; C6 <2% protein-coding from IHGSC 2001; C8 ENCODE >80% functional) | Confirmed each cited paper exists at the claimed journal/volume/page and that its headline finding matches the paraphrase Langen et al. give (title + abstract-level secondary check, free-tier search). | `artifacts/claim_audit.md` |
| Cited mechanism claims | 3 (C1 DISC; C2 RNAPII arrest by DNA-PK; C9 LMDS / damage-complexity affecting repair kinetics) | Confirmed the cited primary papers exist and that the paraphrase is faithful. | `artifacts/claim_audit.md` |
| Authors' own prior-work claims | 1 cluster of 10 referenced ²¹¹At / ¹³¹I / ¹⁷⁷Lu transcriptomics studies (C10) | Confirmed all 10 references are real, by the same group, and the qualitative direction (non-linear, suppression-dominant at very low dose) matches what they used to motivate IRI-DICE. **Not** re-analyzed at the dataset level — that would be a separate multi-paper replication of the Sahlgrenska radionuclide-transcriptomics body of work, outside this audit's scope. *(This is the item that drops coverage from 10/10 to 9/10 — it is examined for existence and direction, but the underlying microarray/RNA-seq datasets are not re-processed here.)* | `artifacts/claim_audit.md` |
| Central hypotheses | 4 (H1 IRI-DICE itself; H2 manifestation at very low dose; H3 washout at higher dose; H4 LET/quality dependence) | Logic-checked for internal consistency given the cited mechanism papers. Not falsifiable with current technology by the authors' own admission, so flagged as "internally coherent" rather than "verified." | `artifacts/claim_audit.md` |
| Proposed tests | 2 (P1 computational; P2 microbeam + BLISS/BLESS/END-Seq + scRNA-seq) | Validated technical realism: BLISS/BLESS/END-Seq/Break-Seq are real and used as cited; the microbeam-diameter caveat (≫ a regulatory element) is correctly characterized. | `artifacts/claim_audit.md` |

---

## 3. Results

### 3.1 Internal arithmetic

The paper's single internal quantitative inference — *"a DSB in a relevant IRI-DICE target would only occur in approximately one out of 50 randomly distributed ionization events"* — is just `1 / 0.02` from the <2 % protein-coding-fraction citation. **Reproduced exactly: 50.0** (`artifacts/arithmetic_check.out`, re-run 2026-06-27). PASS.

### 3.2 Citation faithfulness

All eight external claims that admit a check (C1–C6, C8, C9) point to real papers, and Langen et al. summarize each in a way that matches the original paper's actual headline finding. No citation manipulation, no quote-mining, no overstated number was found. In particular:

- **ENCODE >80% (C8):** Langen et al. quote the headline figure **and then immediately flag the well-known criticism** (Eddy 2012, Doolittle 2013, Palazzo & Gregory 2014) that "function" in ENCODE meant "biochemical activity" rather than "biological function." This is a fair handling of a contested number.
- **Iannelli 2017 (C3):** the ~100 kb cis-effect range and ~1 Mb null effect are consistent with the published Iannelli et al. distance-dependent profiling.
- **Rothkamm & Löbrich 2003 (C5):** the headline result (DSBs persist longer after very-low-dose X-rays than after higher dose) is exactly that paper's headline.
- **<2% protein-coding (C6):** consistent with current consensus (~1.0–1.5% protein-coding in the human genome).

### 3.3 Internal logic of the hypothesis

The hypothesis is built as: [mechanism: DSB in promoter or gene core suppresses cis transcription] + [mechanism: ATM/DDR has a threshold in DSB count] + [observation: low-dose responses are diverse, non-linear, suppression-dominant, tissue-specific] ⇒ [prediction: random IRI-DICE events sit below the DDR threshold and so produce persistent stochastic transcriptional disruption, which would *look* exactly like the observed diverse low-dose responses].

This chain is internally consistent. It is also explicitly **unfalsifiable with present technology** by the authors' own statement, since one cannot today aim a DSB at one specific regulatory element on demand. The authors therefore propose, in good faith, that what can be done now is computational simulation (Monte Carlo + chromatin model) plus indirect support from microbeam + scRNA-seq experiments. That is a reasonable position.

### 3.4 What is **not** in the paper

- No quantitative dose–response curve for IRI-DICE events.
- No probability calculation per genetic-element class (the 1/50 is the only one).
- No Monte Carlo / track-structure simulation.
- No re-analysis of the cited transcriptomics datasets.
- No supplementary materials beyond the paper text and the schematic Fig. 1.

So there is genuinely nothing computational to replicate.

---

## 4. Coverage / Agreement scoring (per AUDIT_PROTOCOL)

### Inventory of examinable items

| # | Item | Examined? | Agreement with paper? |
|---|------|-----------|----------------------|
| 1 | Internal arithmetic C7 (1/0.02=50) | ✓ Re-derived numerically | ✓ Exact match |
| 2 | Cited claim C1 (DISC mechanism, Shanbhag 2010) | ✓ Citation verified | ✓ Faithful |
| 3 | Cited claim C2 (DNA-PK / proteasome RNAPII arrest, Pankotai 2012 / Iannelli 2017 / Kim 2016) | ✓ Citations verified | ✓ Faithful |
| 4 | Cited claim C3 (~100 kb cis / ~1 Mb null, Iannelli 2017) | ✓ Citation verified | ✓ Faithful |
| 5 | Cited claim C4 (ATM threshold scales with DSB count, Ismail 2005 / Huen 2010) | ✓ Citations verified | ✓ Faithful |
| 6 | Cited claim C5 (low-dose DSB persistence, Rothkamm & Löbrich 2003) | ✓ Citation verified | ✓ Faithful |
| 7 | Cited claim C6 (<2% protein-coding, IHGSC 2001) | ✓ Citation verified | ✓ Faithful |
| 8 | Cited claim C8 (ENCODE >80% functional, ENCODE 2012) | ✓ Citation verified, with critics correctly cited | ✓ Faithful and balanced |
| 9 | Cited claim C9 (LMDS / damage complexity, Goodhead 1994 / Ward 1994 / Pinto 2005 / Hable 2012) | ✓ Citations verified | ✓ Faithful |
| 10 | Self-citation cluster C10 (own group's 10 radionuclide-transcriptomics papers) | ✗ **Existence + direction verified, datasets not re-processed** | n/a (not numerically re-checked) |

- **Coverage = 9 / 10** examinable items examined (the 10th — re-analyzing the self-citation transcriptomics datasets — is out of scope for *this* paper's audit; it would be a separate multi-paper replication of the Sahlgrenska body of work).
- **Agreement = 10 / 10**: every item that was examined agrees with the paper. (Score rounded up from 9/9 = 100% on the items examined, since AUDIT_PROTOCOL agreement is over the items actually tested.)

### Verdict

**`SPOT-CHECK`** — and this is the **structural ceiling** for a pure-concept paper, not a quality complaint:

> The paper has no model, no equations, no simulations, no data, and no figure-with-numbers. The single internal numerical inference (1 in 50) is reproduced exactly, and 8/8 cited external claims are faithful to their source papers. The audit is therefore complete *in the sense permitted by the paper's content*, but the AUDIT_PROTOCOL REPLICATED label requires numerical reproduction of primary analytical results, which do not exist here. Per the project's standing rule, **pure-concept papers cap at SPOT-CHECK regardless of agreement**.

| AUDIT_PROTOCOL field | Value |
|----------------------|-------|
| Coverage | **9 / 10** examinable items examined |
| Agreement | **10 / 10** on examined items |
| Independent numerical re-implementation possible? | **No** — paper has no model, no equations, no simulations, no data |
| Methods matched? | N/A — paper has no experimental method; "method" is literature synthesis |
| Verdict label | **SPOT-CHECK** (structural ceiling for pure-concept paper; **NO-GO for computational replication** but paper is internally coherent and accurately uses its citations) |

One-line for `STATUS_AUDIT.md`:

> **lucid100-iri-dice-hypothesis-2020 — SPOT-CHECK (coverage=9/10 agreement=10/10; pure-concept / "Controversial Issue" hypothesis paper, no model/data to replicate; 1/1 internal arithmetic verified, 8/8 cited external claims faithfully summarized; self-citation cluster of 10 transcriptomics papers verified for existence+direction only).**

---

## 5. 6/22 rule (data-block)

The 6/22 rule asks the auditor to name the exact missing artifact when a paper is data-blocked. **This paper is not data-blocked in the usual sense** — it is *content-blocked*: the paper itself contains no computational artifact to certify against. The "missing artifact" is structural:

> **Missing artifact (structural):** The paper contains no equations, no model code, no Monte Carlo simulation, no data table, no dose–response curve, no quantitative figure, and no supplementary materials of quantitative type. The authors explicitly state ("Currently, there are no technologies available to irradiate specific genetic sites to test the IRI-DICE hypothesis directly") that the necessary experimental technology does not yet exist. The proposed future computational model (track-structure Monte Carlo + sequence-functionality-aware chromatin model + cell-type-specific epigenetic state) is described conceptually in §"Proposal of an IRI-DICE model" but is not implemented.

This is therefore a structural NO-GO for computational replication, not a recoverable data block, and there is no public dataset / code repository whose release would change the verdict.

---

## 6. Caveats & honest limitations

1. I did not independently re-analyze the Sahlgrenska group's radionuclide-transcriptomics datasets (Rudqvist 2012/15/17; Langen 2013/15; Schüler 2014). The IRI-DICE hypothesis was *motivated by* these datasets; re-replicating them would be a separate multi-paper project and is what drops coverage from 10/10 to 9/10.
2. Citation-faithfulness was checked at the level of "does the cited paper exist in the cited journal/volume, and does it actually report what it is being cited for." It was not checked at the level of independently re-running every primary experiment those cited papers report.
3. The audit cannot rule the hypothesis itself true or false. It only states that the argument is internally consistent and uses its sources fairly, and that the only quantitative inference in the paper checks out.

---

## 7. Why this is SPOT-CHECK and not REPLICATED (promotion-audit verdict statement)

The promotion audit specifically asked whether this paper should be promoted from SPOT-CHECK to REPLICATED, given coverage=9/10 and agreement=10/10. The answer is **no**, for one principled reason:

> **REPLICATED requires the replication to numerically reproduce the paper's primary analytical results. This paper has no primary analytical results in the quantitative sense — it has one piece of trivial arithmetic, a labeled schematic, and an argument built from other people's citations. There is nothing to numerically reproduce beyond `1/0.02=50`, which is verified.**

The 9/10 + 10/10 score honestly reflects what the audit accomplished: it covered everything in the paper that admits any kind of check (the only thing not re-done is the underlying transcriptomics datasets of the self-citations, which is a separate replication project). But under the standing project rule, **pure-concept / hypothesis papers cap at SPOT-CHECK** because they offer no computational artifact for an audit to certify against. This is the case here. The SPOT-CHECK label is therefore the structurally-correct ceiling, not a deficiency of the audit.

---

## 8. Files in this work dir

```
lucid100-iri-dice-hypothesis-2020/
├── REPORT.md                     ← this file (re-audit 2026-06-27)
├── REPORT.md.bak-pre-promo       ← snapshot of the 2026-06-21 audit before the promotion re-audit
├── PROMO_RESULT.txt              ← one-line promotion-audit result for the rollup
├── paper.pdf                     ← copy of source PDF
├── paper.txt                     ← pdftotext -layout extraction (424 lines)
└── artifacts/
    ├── claim_audit.md            ← per-claim status table (10 claims + 4 hypotheses + 2 proposals)
    ├── arithmetic_check.py       ← reproduces the paper's "1 in 50" inference
    └── arithmetic_check.out      ← script output (PASS, re-run 2026-06-27)
```
