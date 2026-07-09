# PROGRESS — LUCID100 slot 42 (Wave 5)
**Paper:** Yu, Geng, Tang — Med Phys 2024 — BNCT via cellular DNA damage repair model
**DOI:** 10.1002/mp.17446
**Started:** 2026-06-09 14:05 CDT
**Subagent session:** agent:main:subagent:ab69e327-ae46-4935-9b1e-86be3d8551fb

## Checklist

- [x] Pull row from `LUCID100_SOLID_MASTER_QA.tsv` (slot 42, Wave 5, A14)
- [x] Create workspace `lucid100-bnct-dna-damage-repair-model/`
- [x] Locate open-access copy of the paper (free PDF on NUAA mirror)
- [x] Download PDF to `refs/paper.pdf` (3.13 MB, OK)
- [x] Extract methods + equations + parameters with `pdftotext -layout`
- [x] Identify model: **MEDRAS** (McMahon, Front. Oncol. 2021) extended with Geant4-DNA + TOPAS-nBio
- [x] Check public availability of MEDRAS → `https://github.com/sjmcmahon/MEDRAS` (public, Python)
- [x] Clone MEDRAS into `artifacts/medras_analytic/`
- [x] Verify MEDRAS runs locally (default human fibroblast survival curve, OK)
- [x] Check for data/code availability statement in the paper → **NONE**
- [x] Confirm whether full reproduction requires heavy compute → YES (Geant4-DNA + TOPAS-nBio)
- [x] Write reduced analytic smoke script `scripts/medras_bnct_smoke.py`
- [x] Run smoke script, capture output → `artifacts/smoke_output.txt`
- [x] Author README.md, REPORT.md (= FIRST_PASS_REPORT.md), ARTIFACT_MANIFEST.md
- [x] Write JSON progress record to `~/.openclaw/workspace/memory/subagent-progress/`
- [x] QA retag recommendation issued in README + REPORT

## Time log

| time (CDT)     | event |
|----------------|---|
| 14:05          | task received, workspace created |
| 14:06          | paper PDF downloaded from NUAA mirror |
| 14:07          | pdftotext extraction; identified MEDRAS as the core model |
| 14:08          | MEDRAS analytic version found public on GitHub; cloned |
| 14:09          | MEDRAS smoke test passes (default cell survival curve runs) |
| 14:10          | LQ-fit + RBE prototype confirms methodology reproduces |
| 14:11          | full smoke script written, run, output captured |
| 14:12          | README / PROGRESS / REPORT / MANIFEST / JSON record written |

## Blockers

- None for the first-pass / reduced analytic deliverable.
- For full Table 1 / Figures 7-8 reproduction: the authors did not release
  (a) their BNCT extension to MEDRAS-MC,
  (b) Geant4-DNA radial-deposition tables for α (10 energies) + ⁷Li (5 energies) + recoil protons,
  (c) TOPAS-nBio F and W factors for BPA / BSH microdistributions.
  These would have to be re-generated locally (job plan in README).

## Next actions (if escalated)

1. Stand up Geant4-DNA on uicgpu (or chiatta00), regenerate the radial-deposition tables in `Geant4-DNA G4EmDNAPhysics` for the energy grid described in §2.3.1.
2. Build the TOPAS-nBio 3×3×3 cell-nucleus geometry (§2.3.2-2.3.3) and compute F and W for BPA and BSH.
3. Feed the SDD-format DNA damage distributions into MEDRAS Monte Carlo (request MC version from McMahon group, or fall back to molecularDNA / Geant4-DNA's built-in repair example, ref. 13 in the paper — `chatzipapas2023molecularDNA`).
4. Refit LQ per component on the generated SF curves; apply Eq. 6 with the paper's exact dose splits to reproduce Table 1.
5. Compare to experimental refs 4 (Hiratsuka 1991 melanoma) and 41.

## Final status

`PARTIAL_REDUCED_ANALYTIC` — first pass complete, methodology reproduces, exact-number reproduction blocked on unreleased authors' microdistribution data.
