# Attempt log — BVBRC-106 (2026-07-05, single session)

Chronological summary of what was attempted.

- 00:09 CDT — subagent spawned with WAVE_BRIEF_2026-07-01 assignment for BVBRC-106.
- 00:10 — read wave brief; created target dir `~/Dropbox/REPLICATE-PROJECT/BVBRC-106-Singh-multi-drug-resistant-enterobacter-2018/{report/evidence,work}`.
- 00:10 — pulled PubMed abstract for PMID 30466389 (BMC Microbiol 18:175). Confirmed PMC-open (PMC6251167).
- 00:11 — pulled PMC full-text XML; parsed out BioProject **PRJNA319366** (5 ISS strains) + WGS accessions (POUR/POUQ/RBVJ/POUP/POUO for ISS; FYBI/JVSD for two clinical; PRJNA310238 for MBRL-1077). Extracted Table 1 (strain → accession + paper's dDDH/ANI values).
- 00:13 — set up remote work dir on uicgpu (`~/replicate/bvbrc-106/{genomes,work,logs}`). Confirmed proxy internet works. Discovered pre-existing conda envs `bvbrc14` (AMRFinderPlus 4.2.7) and `bvbrc28` (NCBI Datasets 18.32.0, fastANI, prokka, mash, prodigal) — no need to build a new env.
- 00:14 — first `nohup ... &` background invocation of `fetch_assemblies.sh` produced empty log (backgrounded ssh child died on `mkdir ""` from an early `set -eu` + empty HF_HOME expansion in env.sh); switched to a foreground run with explicit conda-activate inline.
- 00:15 — resolved WGS accessions → assembly accessions via Entrez `esearch`/`esummary` in Python (7/8 matched; EB-247T's `FYBI00000000` needed a strain-name query to get `GCF_900324475.1`).
- 00:18 — `datasets download genome accession <8 GCFs>` succeeded (11.5 MB zip). Unzipped, symlinked strain-named FASTAs into `genomes/fastas/`. All 8 FASTAs sane (ISS ~4.93 Mbp, clinical 4.70–4.80 Mbp).
- 00:19 — `fastANI` all-vs-all 8×8 in ~2 s on 8 threads. Matrix reproduces the paper's Table 1 topology cleanly (< 0.3 % deltas).
- 00:20–00:23 — `amrfinder --organism Enterobacter_cloacae --plus` on all 8 genomes, ~40 s each. All hits consistent: 5 ISS strains have an identical AMR gene set; MBRL-1077 has the extra carbapenemase (blaIMI-1) and qnrE as the paper claims.
- 00:24 — pulled artifacts back to local Dropbox path; built 8×8 pretty CSV of ANI matrix.
- 00:25 — LLM judge run:
  - Argo `claude-opus-4.8` → 502 Bad Gateway.
  - Argo `claude-sonnet-4.6` → success. Verdict: REPLICATED. Full text saved.
- 00:26 — wrote REPORT.md, brief.md, artifact_harvest.md, this attempt_log.md.

## What worked
- Existing bvbrc14 / bvbrc28 conda envs on uicgpu already had every tool needed (AMRFinderPlus + database, NCBI Datasets, FastANI, prokka, mash).
- Direct Entrez esearch/esummary resolution of WGS accessions → assembly accessions was fast and reliable.
- FastANI's mash-based ANI reproduced JSpeciesWS BLAST-ANI values from the paper to within 0.3 %, which is well within cross-tool noise.

## What didn't work / gotchas
- `set -eu` combined with empty env-var expansion in `~/env.sh` killed backgrounded scripts silently. Fix was to run interactively with explicit conda activation.
- `EB-247T` WGS accession `FYBI00000000` did NOT resolve via WGS-database esearch (paper's accession is at ENA, not indexed in NCBI's WGS db under that master ID); fell back to strain-name query which pulled the RefSeq assembly `GCF_900324475.1`.
- Argo `claude-opus-4.8` (my configured default) was 502 at judge time; fell back to `claude-sonnet-4.6`.

## What was not done
- PathogenFinder pathogenicity-probability re-run (C9).
- RAST subsystem re-annotation (paper's C10, MAR operon detection).
Both out of scope for this timeboxed replication run; would need additional tooling.
