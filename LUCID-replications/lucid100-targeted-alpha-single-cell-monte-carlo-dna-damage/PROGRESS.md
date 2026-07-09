# PROGRESS — LUCID100 Slot 41

**Paper:** Jolly & Fielding 2025, *Modelling single cell dosimetry and DNA damage of targeted alpha therapy using Monte-Carlo techniques*  
**DOI:** 10.1007/s13246-025-01605-2  
**Status:** first-pass reduced smoke complete / HPC-gated full replication  
**Updated:** 2026-06-09T19:09:50Z

## Completed

- Harvested open-access paper PDF and layout-preserved text.
- Documented TOPAS/TOPAS-nBio/Geant4-DNA setup and DBSCAN damage-model parameters.
- Implemented three reduced CPU smoke checks:
  1. radionuclide alpha decay-chain summaries for Ac-225, Ra-223, Pb-212, At-211;
  2. CSDA/range/geometry analytical dose sanity check for nucleus vs membrane source placement;
  3. DBSCAN lesion clustering model unit tests using the paper's 5/37.5 eV ramp, 16% DNA fraction, and 3.2 nm clustering radius.
- Verified 6/6 reduced smoke checks.

## Not run locally

Full TOPAS-nBio/Geant4-DNA transport was intentionally not run on CherryRd. It needs a Geant4/OpenTOPAS stack and many track-structure jobs; see `HPC_JOB_PLAN.md`.

## Current verdict

**PARTIAL / KEEP.** The paper is open and methodologically well specified, but full numerical reproduction is HPC-gated and no public code/raw scorer dumps are supplied. Reduced analytical checks reproduce the main physical expectations and validate the DNA-damage clustering implementation.
