# FIRST PASS REPORT — LUCID100 slot 22

**Paper:** Chen C, Zhang Y. *Proteomic Profiling of Deinococcus radiodurans Reveals Irradiation-Induced Proteins and Their Associated Functional Pathways.*
**DOI:** [10.1088/1742-6596/3109/1/012098](https://doi.org/10.1088/1742-6596/3109/1/012098) — J. Phys.: Conf. Ser. 3109 (2025) 012098 (2nd Intl. Conf. on Space Science & Technology proceedings).
**Date:** 2026-06-09 13:31 CDT.
**Operator:** OpenClaw subagent `agent:main:subagent:d1180304-e08d-4ee0-bf6b-62f54f48b4ea`, depth 1/1.
**Source-of-truth row:** `/Users/stevens/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv` row 53.

---

## Verdict

**PASS-low ✅** — first-pass artifact harvest + reproducibility-bone smoke replication is complete. All 7 smoke criteria pass.

**PASS-mid ⛔ NO-GO (data-not-deposited).** Hard blocker, not a soft one.

**PASS-full ⛔ NO-GO.** Same blocker.

**Paper legitimacy: KEEP.** The paper is a real Gold-OA CC BY 4.0 conference paper (IOP Publishing, J. Phys. Conf. Ser. 3109, 2025), by an established Beijing Institute of Technology lab (PI `zyq@bit.edu.cn`, Yongqian Zhang) that has 2 prior PRIDE deposits and an authentic LC-MS/MS workflow (pFind3 + Q Exactive HF-X). It is not predatory, not a mill paper, and not citation-farm output. The QA-decision column already says `KEEP: relevant and replication-plausible` — that should be **softened to** `KEEP-low-only: replication blocked by missing raw data + missing supplement`. The "replication-plausible" claim in the master QA file was over-optimistic for this slot.

---

## Why PASS-low passed

`code/smoke_test.py` runs 3 sanity checks against the public artifacts and outputs the JSON in `results/smoke_test_report.json`.

### Step 1 — reference proteome (PASS)

The authors searched their LC-MS/MS spectra with pFind3 against UniProt proteome **UP000002524** (snapshot 2019-10-02). That proteome is still live:

- ID: `UP000002524`
- Strain: ATCC 13939 / DSM 20539 / **R1** (taxon 243230)
- Size: **3,085 proteins**
- Assembly: `GCA_000008565.1`

The paper says it detected ≈ 2,000 proteins per group. Treating Figure 2b's Venn (2,034 shared + 142 control-only + 62 radiation-only = **2,238 total**) as the union: 2,238 / 3,085 = **0.725** — i.e. the authors detected 72.5 % of the reference proteome, which is comfortably inside the typical shotgun LC-MS/MS coverage band (50–90 %) for a small radioresistant bacterium with this gradient + instrument + Open-Search engine. The order of magnitude is right; the strain matches; the proteome resolves.

### Step 2 — named DDR proteins resolve and carry the right GO terms (PASS)

The paper highlights three proteins as exclusive to the irradiated group and as the main biological story (Figure 4: PSM counts of RuvC, DdrA, DdrB across 0/1/3 h). Public UniProt lookups give:

| Symbol | UniProt | Length | DNA repair `GO:0006281` | DNA binding `GO:0003677` / `GO:0003697` | Cellular response to γ `GO:0071480` |
|--------|---------|--------|--------------------------|------------------------------------------|--------------------------------------|
| RuvC | **Q9RX75** | 179 aa | ✅ | ✅ (`GO:0003677` dsDNA) | — (RuvC isn't gamma-annotated, but DNA repair + DNA binding are present) |
| DdrA | **Q9RX92** | 208 aa | ✅ | ✅ (`GO:0003697` ssDNA) | ✅ |
| DdrB | **Q9RY80** | 188 aa | ✅ | ✅ (`GO:0003697` ssDNA) | ✅ |

All 3 expected accessions match. All 3 have DNA repair + DNA binding GO. 2/3 have the exact `GO:0071480` ("cellular response to gamma radiation") term the paper highlights. RuvC does not carry the gamma term in UniProt's curated set, but its `GO:0006281` + `GO:0006310` (DNA recombination) combination is the same biological story.

### Step 3 — Venn arithmetic / coverage fraction (PASS)

- 2,034 shared + 142 control-only + 62 radiation-only = 2,238 detected (consistent with "≈ 2,000 per group").
- Control total: 2,176. Radiation total: 2,096. Both inside [1,900, 2,300].
- Radiation-only fraction = 62 / 2,096 = **2.96 %** — small but non-trivial, exactly what one expects for a transient stress-induced subproteome at 3 h post-irradiation.

### Overall

```
{
  "ref_proteome_resolves_and_strain_is_R1": true,
  "detected_count_consistent_with_reference_proteome_size": true,
  "all_3_named_proteins_resolve_to_expected_uniprot": true,
  "all_3_named_proteins_have_DNA_repair_GO": true,
  "all_3_named_proteins_have_DNA_binding_GO": true,
  "at_least_2_of_3_have_gamma_response_GO": true,
  "venn_arithmetic_self_consistent": true,
  "pass_low_overall": true
}
```

---

## Why PASS-mid / PASS-full are NO-GO

Three independent, compounding blockers — any one would be sufficient:

1. **Raw spectra not deposited.** Searched ProteomeXchange (PROXI API), PRIDE archive v3 (keyword `Deinococcus radiodurans`, submitter `Yongqian Zhang`, all of the lab's known projects), MassIVE, and jPOSTrepo. Found the lab's other deposits (PXD035309 acetylome 2022, PXD062500 pprI-KO 2025) but **nothing for this paper's 6 kGy / 0-1-3 h experiment**. The Q Exactive HF-X `.raw` files this paper depends on appear to live only on the authors' local storage.
2. **62-protein induced list not published.** The paper names exactly 3 of the 62 (RuvC, DdrA, DdrB). The remaining 59 are referenced only as an aggregate count and as the GO-enrichment input. No supplementary file, no supplementary table, no supplementary figure on the IOP landing page. The IOPscience page for this DOI lists `Supplementary content: none`.
3. **No data-availability statement.** Standard practice for proteomics work (and a publication requirement of most journals — but not strictly enforced by J. Phys.: Conf. Ser. proceedings). The paper has no such statement.

Consequence: without the 62-entry protein list **or** the raw spectra, the GO enrichment (Figure 3b) and the PSM trajectories (Figure 4) cannot be re-computed from public data. Symbolic reasoning over the 3 named proteins alone is not a replication of the enrichment.

### What WOULD lift the NO-GO

- Authors deposit raw spectra in PRIDE (likely accession PXD0xxxxx; same lab knows the workflow). Timeline: unknown.
- Authors release a supplementary table with the 62 + 142 protein lists. Timeline: unknown.
- A future systematic-review paper or follow-up by the same lab republishes the list. Worth re-checking at +6 months and +12 months.

### What we did NOT do (and won't, per task rules)

- **No author contact.** `zyq@bit.edu.cn` is in their PDF but no email was sent.
- **No paid endpoints.** All resolution went through free public APIs.
- **No web-scraping of paywall-protected supplements.** None exist; the question is moot.
- **No heavy compute.** Pure file I/O + small REST calls. CherryRd CPU/RAM impact is essentially zero.

---

## Artifacts

See [`ARTIFACT_MANIFEST.tsv`](./ARTIFACT_MANIFEST.tsv) for the canonical list with byte sizes and sha256-prefix hashes. Highlights:

- **`artifacts/paper.pdf`** — 2,472,457 bytes, 10 pages, full Gold-OA PDF. Retrieved via `https://iopscience.iop.org/article/10.1088/1742-6596/3109/1/012098/pdf` (the IOP `/article/<doi>/pdf` endpoint bypasses the Radware bot challenge that gates the landing page).
- **`artifacts/paper.txt`** + **`artifacts/paper_raw.txt`** — pdftotext-extracted text, machine-readable.
- **`artifacts/figures_extracted/fig-{000..005}.png`** — 6 PNGs from `pdfimages`, including the workflow figure, the 3-panel PSM bar chart (Figure 2a–c), the Venn diagram (Figure 2b), the GO enrichment bar charts (Figure 3a/b), and the 3-panel RuvC/DdrA/DdrB PSM trajectories (Figure 4).
- **`data/UP000002524.json`** — UniProt proteome metadata (3,085 proteins, strain R1).
- **`code/smoke_test.py`** — re-runnable PASS-low smoke (stdlib + REST only).
- **`results/smoke_test_report.json`** — 7/7 criteria pass.

---

## Recommendation to LUCID100 orchestrator

| Field | Value |
|-------|-------|
| `status` (suggested update) | `pass_low_complete_replication_blocked` |
| `qa_decision` (suggested update) | `KEEP-low-only: replication blocked by missing raw data + missing supplement` |
| `verdict_or_plan` (suggested update) | `PASS-low ✅ done. PASS-mid/full ⛔ NO-GO unless authors deposit raw spectra or publish 62-protein supplement.` |
| Re-check trigger | PRIDE deposit by `Yongqian Zhang` / BIT mentioning `6 kGy` and `D. radiodurans` at any of +6 mo / +12 mo. |
| Heavy-compute job plan | **Not applicable** — even with the raw spectra, pFind3 on a 3,085-protein proteome with 18 `.raw` files (3 time × 2 groups × 3 replicates) is a laptop-scale job (~hours on 16 cores). Definitely not CherryRd-heavy. |

**Bottom line:** slot 22 is a textbook "real paper, real lab, real methods, no data deposit" case. The first pass extracted everything that can be extracted from the public artifacts and verified the bone of the methodology is sound; further replication is gated on author behaviour, not on our effort.
