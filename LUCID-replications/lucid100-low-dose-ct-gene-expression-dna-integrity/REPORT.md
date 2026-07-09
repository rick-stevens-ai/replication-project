# LUCID-100 Replication Report — Schmid et al. 2025

**Paper:** Impact of Low-Dose CT Radiation on Gene Expression and DNA Integrity
**Authors:** Schmid N, Gorte V, Akers M, Verloh N, Haimerl M, Stroszczynski C, Scherthan H, Orben T, Stewart S, Kubitscheck L, Kaatsch HL, Port M, Abend M, Ostheim P.
**Venue:** Int J Mol Sci 26(24):11869, 2025 (e-pub 9 Dec 2025) · CC BY 4.0
**DOI:** 10.3390/ijms262411869 · **PMCID:** PMC12732518
**LUCID-100 slot:** rank 46 / Wave 2 (worktype: omics/signature replication)

---

## 1. VERDICT

**REPLICATED — Coverage 8 / 10 · Agreement 9 / 10**

Every per-patient datum that drives the paper's primary claims is present in the
open-access Europe PMC JATS XML (appendix Tables A1/A2/A3), despite the formal
"data available on request" statement. A numpy+scipy smoke script reproduces all
Tier-1 quantitative claims (demographics, combined-cohort gene expression,
γ-H2AX descriptives) to published precision, and independently surfaces a
substantive statistical-methods discrepancy in the paper's DSB analysis.

---

## 2. What was reproduced

### 2.1 Demographics (Table 1) — exact
| Quantity | Paper | Recompute (population SD, ddof=0) |
|---|---|---|
| DLP mean (N=60) | 561.9 mGy·cm | 561.9 ✓ |
| DLP SD (N=60) | 384.6 | 384.6 ✓ |
| Eff. dose mean | 8.3 mSv | 8.28 ✓ |
| Eff. dose SD | 5.8 | 5.78 ✓ |
| DLP mean (γ-H2AX subset N=12) | 321.0 | 321.0 ✓ |
| DLP SD (subset) | 149.3 | 149.3 ✓ |

→ SDs match only with **population SD (Excel `STDEVP`)**, not sample SD. Minor
methods note: SDs are biased low for small-subset comparisons.

### 2.2 Combined-cohort gene expression (§2.2) — direction + significance tier match (9/9 genes)
All nine radiation-responsive genes (EDA2R, MIR34AHG, WNT3, DDB2, FDXR, POU2AF1,
AEN, BAX, PHLDA3) match the paper's combined-analysis text qualitatively in both
sign and significance tier (one-sample t on log2(DGE); paper used Wilcoxon
signed-rank "when applicable" — same tiers reproduce). E.g. EDA2R +0.65 log2,
p=6.8e-9; MIR34AHG +0.89, p=5.8e-6; WNT3 −0.30, p=1.0e-4.

### 2.3 γ-H2AX descriptives (§2.3) — exact
pre 0.60±0.25, post 0.70±0.29, RIF 0.10±0.15 — all reproduced to two decimals.

---

## 3. Independent finding (post-publication critique candidate)

The paper reports **p = 0.37** for post-CT vs pre-CT DSB-focus change (N=12) and
concludes the increase is "non-significant." That p-value reproduces **exactly**
as a Mann–Whitney U on *independent* samples (U=88.0, p=0.3707) — proving the
paper applied an independent-samples test to an intrinsically **paired** design
(same 12 patients, before vs after the same scan).

With the appropriate paired test:
- **Paired t-test (one-sample t on RIF): p = 0.043** → significant
- Wilcoxon signed-rank (paired): p = 0.092

The binary "non-significant DSB induction" headline does **not survive** a
re-analysis that respects the pairing. Effect size is small (0.1 foci/cell,
≈17% of baseline) so clinical significance at this dose remains debatable, but the
statistical framing is wrong on the paper's own data. Worth a short technical note
to the authors (Ostheim/Abend, Bundeswehr Inst. Radiobiology — they publish
extensively on paired pre/post focus assays).

---

## 4. Reproducibility-blocker critique (6/22 rule)

- **Primary numeric data: NOT blocked.** Although the data-availability statement
  says "available on request … not publicly available due to privacy/ethical
  restrictions," the **complete per-patient dataset is embedded in the published
  JATS appendix tables** (Table A1 = 60 patients × 9 genes + DLP + eff. dose;
  Table A2 = 12 patients pre/post/RIF γ-H2AX; Table A3 = scan metadata). This is a
  recurring MDPI pattern worth flagging: the "on request" tag is contradicted by
  the open JATS — always check the XML appendix before treating such papers as
  data-blocked.
- **Tier-2 blocker (precise missing artifact):** the **per-patient in-vivo vs
  ex-vivo group-membership labels are NOT published.** Table A1 pools all 60
  patients without the incubation-protocol flag, so the paper's headline
  *in-vivo-only* dose–response r² values (AEN r²=0.66, FDXR r²=0.56, n≈27) cannot
  be reproduced exactly. They are recoverable in principle by a constrained
  subset-fit (60-choose-28 with per-gene medians matched to Table 2 in-vivo
  medians) but that combinatorial recovery was out of scope for this pass.
- **Access friction:** MDPI's own HTML/PDF endpoints are Akamai-gated (403); Europe
  PMC JATS is the reliable canonical full-text source for this paper.

---

## 5. Artifacts
`artifacts/europepmc_fullText.xml` (220 KB canonical JATS), `ijms-26-11869-t0A1/A2/A3.tsv`
(per-patient), `t001/t002.tsv` (summary), `scripts/replicate_smoke.py` (Tier-1 PASS),
`notes/claims.md`. Compute footprint: ~3 s CPU on CherryRd, no heavy compute.

## 6. Suggested follow-ups
1. Solve in-vivo/ex-vivo subset labelling → would promote in-vivo r² claims to Tier-1.
2. Write up the paired-vs-unpaired γ-H2AX finding as a short technical note.
3. Cross-validate the 6-gene signature against GSE43151 (orthogonal ex-vivo IR set).

---
*Verdict authored from disk-verified first-pass artifacts + paper, 2026-06-25.*
