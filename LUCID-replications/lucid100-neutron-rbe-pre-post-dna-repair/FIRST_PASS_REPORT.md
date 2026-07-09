# FIRST_PASS_REPORT — lucid100-neutron-rbe-pre-post-dna-repair

**DOI:** 10.1088/1361-6560/ae36e1
**Paper:** Desjardins-Proulx & Kildea, *In silico neutron RBE estimations for Pre-DNA repair and post-DNA repair endpoints*, Phys. Med. Biol. 71 025012 (2026)
**Slot:** LUCID100 Wave 5 max-rate backfill slot 45 (master row 76)
**Date:** 2026-06-09 CDT
**Operator:** subagent on CherryRd (one shot, no author contact, no paid endpoints, no heavy compute)

---

## Verdict

> **PARTIAL reduced-analytic replication — KEEP.**
> First-pass artifacts harvested, equations/parameters/tables extracted,
> CPU smoke green (max-RBE within 1.3–9.2 % of paper across all four
> endpoints), public code imports cleanly and passes a synthetic test.
> Exact per-energy yield reproduction is blocked by the need to re-run the
> upstream TOPAS-nBio / Geant4-DNA / DaMaRiS pipeline — HPC plan documented.

## What works

1. **OA paper acquired** in full (CC-BY, 16 pages, 1.4 MB) from IOP directly,
   plus a 56 KB `pdftotext` extraction that exposes every equation and
   parameter table.
2. **Public Zenodo release identified and pulled** (code-only, 4.7 MB) at
   `doi:10.5281/zenodo.17087505` under MIT. This includes:
   * the complete TOPAS extension source (geometry, physics, scoring, mods),
   * the SDD clusterer `payload/ComplexDSbCounter.py`,
   * **and crucially the 165 relative-dose files** (the CHMC outputs `d_S(E)`
     for 18 neutron energies × 3 scoring volumes × 3 secondary species),
     which means the first half of the pipeline (Section 2.2) is *already
     reproducible without any TOPAS install*.
3. **Reduced-analytic smoke runs in &lt; 1 s on CherryRd CPU** and reproduces
   the paper's four headline maximal-RBE values to within ~ 1–9 %:

   | endpoint     | smoke max RBE | paper max RBE | dev |
   |--------------|--------------:|--------------:|----:|
   | DSB site     |          2.70 |       2.54(3) | 6.4 % |
   | complex DSB  |          5.22 |       4.78(8) | 9.2 % |
   | DSB cluster  |         15.80 |        16(1)  | 1.3 % |
   | misrepair    |         21.82 |        23(1)  | 5.1 % |

4. **Author clusterer is functional**. `ComplexDSbCounter.py` imports
   cleanly, all internal helpers callable, synthetic 2-DSB / 1-distal-DSB
   block-table test yields the expected `(Baiocco=1, Complex=1)` count.

## What is blocked

1. **Exact per-energy yield reproduction (Figures 3, 4, 6, 7).**
   Requires regenerating the TSMC simulations: 18 neutron energies ×
   3 secondaries × 100 reps + 950 photon reps with TOPAS v3.6.1 +
   TOPAS-nBio 1.0 + Geant4 v10.04.p02 + Geant4-DNA. Total ~ 25–40 k CPU-h.
   **Not attempted on CherryRd.** Plan in `docs/HPC_JOB_PLAN.md`.
2. **Misrepair curve shape (Section 3, Figure 4(b)).**
   Requires DaMaRiS NHEJ over the SDD outputs from (1). The author ships
   the SDD outputs themselves as a 690 MB Data.zip on Zenodo, so a
   medium-cost path (skip TSMC, run DaMaRiS only) is feasible on
   uicgpu/Aurora.
3. **Energy-of-peak in the smoke**. The smoke's flat per-species `Y_S`
   places the maximal RBE at 10 MeV neutrons; the paper's TSMC places it
   at 0.5 MeV. This is *expected* (the energy peak is driven by per-energy
   secondary-proton LET spectra that only the TSMC simulation produces)
   and *not a bug*. The smoke contract is to reproduce magnitudes of
   maxima and endpoint ordering, both of which it does.

## What was deliberately not done

| Item                                             | Why                                                  |
|--------------------------------------------------|------------------------------------------------------|
| Download `zenodo:17087505/Data.zip` (690 MB)     | Heavy on CherryRd; would only enable Step-3/Step-4 reproduction, which still needs the HPC plan for DaMaRiS. |
| Install Geant4 / TOPAS / TOPAS-nBio on CherryRd  | Per task rule; full pipeline is HPC.                |
| Author contact                                    | Explicitly disallowed.                              |
| Paid endpoints                                    | Explicitly disallowed.                              |

## Next actions (if/when the slot is promoted)

1. On Aurora or uicgpu, pull `zenodo:17087505/Data.zip`, point
   `payload/ComplexDSbCounter.py::clusterer` at the per-energy SDD files,
   aggregate per-species yields, plug into the (already-implemented)
   Eq. 5/Eq. 6 calculator in `smoke/smoke_eq5_eq6_rbe.py`. This alone
   should reproduce Figure 3 (pre-repair) within statistical error.
2. Optionally re-run DaMaRiS NHEJ over the SDD files to confirm the
   misrepair RBE = 23(1) at 0.5 MeV.
3. Optional bench-marking — compare to Baiocco 2016 (PHITS+PARTRAC)
   and Mentana 2025 (PHITS+PARTRAC) by importing their published RBE
   curves with WebPlotDigitizer (already cited by the paper, MIT-style
   workflow).

## QA retag recommendation

> `first_pass_complete_partial_reduced_analytic` / **KEEP**

Matches the slot-42 (`lucid100-bnct-dna-damage-repair-model`) decision pattern:
public paper + public code + CPU smoke reproduces magnitudes; full numerics
need an HPC re-run. The Zenodo SDD release for this paper makes the HPC
path *cheaper* than for slot 42 (Step 1 CHMC data is already shipped).

## Paths

* Folder:  `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-neutron-rbe-pre-post-dna-repair/`
* Smoke:   `smoke/smoke_eq5_eq6_rbe.py` → `smoke/smoke_results.json` + `smoke/smoke_report.txt`
* Manifest: `artifacts/ARTIFACT_MANIFEST.md`
* HPC plan: `docs/HPC_JOB_PLAN.md`
* Progress JSON: `/Users/stevens/.openclaw/workspace/memory/subagent-progress/lucid100-neutron-rbe-pre-post-dna-repair.json`

## Open Questions & Reproducibility Blockers

- Primary blocker: the **per-energy TSMC (Track-Structure Monte Carlo) output** that drives Figures 3, 4, 6, 7 — specifically the 18 neutron energies × 3 scoring volumes × 3 secondary species × 100 replicates of SDD-format DNA damage distributions, plus the matching 950 photon reps. The author shipped the upstream 165 relative-dose `d_S(E)` files via Zenodo (`doi:10.5281/zenodo.17087505`) — which is what lets the smoke check land within 1.3–9.2 % of the paper's max-RBE values — but the SDD outputs themselves are bundled in a separate **`Data.zip` (~690 MB)** that was NOT downloaded on CherryRd (would only enable Step-3/Step-4 reproduction, which still needs HPC for DaMaRiS). Pulling Data.zip is the cheapest next step.
- Secondary blocker: the **DaMaRiS NHEJ misrepair simulation** behind Section 3 / Fig. 4(b). DaMaRiS is referenced but not bundled in the Zenodo release; reproducing the misrepair RBE = 23(1) at 0.5 MeV requires either obtaining DaMaRiS separately or coding the two-step end-joining model from the paper's equations.
- Tertiary blocker: the **TOPAS v3.6.1 + TOPAS-nBio 1.0 + Geant4 v10.04.p02 + Geant4-DNA** software stack at exactly the cited versions. Total cost ~25–40k CPU-h (HPC plan in `docs/HPC_JOB_PLAN.md`). Not attempted on CherryRd per task rules; uicgpu or Aurora is the proper target. The energy-of-peak in the smoke (10 MeV vs paper's 0.5 MeV) is the visible signature of NOT running this stack — flat per-species `Y_S` mis-localizes the peak even when the magnitude is right.
- Open question: would running DaMaRiS over the Zenodo SDD outputs (medium-cost path: skip TSMC, run misrepair only) on uicgpu independently confirm the misrepair RBE = 23(1) at 0.5 MeV, given that the upstream CHMC tables are public?
- Open question (cross-paper): how do these results compare quantitatively to Baiocco 2016 and Mentana 2025 (PHITS+PARTRAC), once those published RBE curves are digitised via WebPlotDigitizer? The paper cites both but does not include a head-to-head overlay.

