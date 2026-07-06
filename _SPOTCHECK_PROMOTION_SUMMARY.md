# SPOT-CHECK Promotion Assessment — Combined (40 papers)
*Ollie, 2026-06-25. Per-paper detail in _SPOTCHECK_PROMOTION_BATCH1.md and _BATCH2.md.*

## Tally
- PROMOTABLE -> REPLICATED: ~5  (mostly OA papers + public DB data; bounded local compute)
- PROMOTABLE -> PARTIAL:    ~13
- CEILING (SPOT-CHECK is honest max): ~9  (review/concept papers, closed access, proprietary MC, or zero data deposit)
- Second-100 (separate, 14 SPOT-CHECK): nearly all "PROMOTABLE -> PARTIAL/REPLICATED via uicgpu TOPAS-nBio/Geant4-DNA full MC run"
- 2 mislabeled (functionally already PARTIAL): lucid100-multiscale-uhdr-survival-model, BVBRC-11-VREfm-LatAm-Rios2020 -> RE-TIER

## Highest-value, all-local-compute promotions (days-to-weeks, high confidence)
1. fipy-wave4 -> REPLICATED (FiPy is open NIST code; add 2D phase-field + BCs + convergence study, ~1 day)
2. BVBRC-16 Efaecium -> REPLICATED (genomes public; rerun Roary+ResFinder+VFDB+ISEScan, ~24 CPU-h)
3. BVBRC-17 Ecoli-B2-IBD -> REPLICATED (5,737 genomes public + GEMs in BiGG; pan-genome + COBRApy FBA)
4. lucid100-zebrafish-brain-chronic-lowdose-transcriptomics -> REPLICATED (raw RNA-seq GEO GSE206573; STAR+DESeq2)
5. BVBRC-11 VREfm -> REPLICATED (pass-2 already cov12/agr10; BEAST time-tree + virulence ref set)
6. lucid100-intensity-modulated-protective-doserate -> PARTIAL (OA + Table 1; implement IMK + WebPlotDigitizer Figs 2/3)

## Promotable via GPU MC campaign on uicgpu (engine already installed)
- Second-100 track-structure papers (s100-016/023/024/031/033/042/049/056/059/064/073/081/082/083/089)
- lucid100-targeted-alpha-single-cell-monte-carlo-dna-damage, lucid100-topas-proton-cellular-response,
  lucid100-uhdr-plasmid-dna-topas-nbio  (all -> PARTIAL with TOPAS-nBio/Geant4-DNA runs)

## Promotable via paywall/library access or author contact
- lucid-actinium-lutetium (already PARTIAL+), lucid-patra-polbeta (HDOCK/ClusPro rerun),
  lucid100-nuclear-fragmentation-carbon-rbe (paywalled BioOne), lucid100-stochastic-nhej-track-2010 (BioOne paywall),
  lucid100-multiscale-uhdr (author Julia code + TRAX-CHEM spectra)

## HARD CEILING — SPOT-CHECK is the honest maximum (do not chase)
- lucid-brahme-radiobio-optimization-review (review/opinion, predatory venue, no data/code)
- lucid-skin-inflammation-nfkb-cox2 (wet-lab; digitizable figs already done 9/10)
- lucid100-fractionated-lowdose-epigenetic-behavior (wet-lab mouse, zero deposit)
- lucid100-deinococcus-radiodurans-ir-gene-regulation (review, no primary data)
- lucid100-friedland-stochastic-dsb-photon-ion-slot67 (closed access + proprietary PARTRAC MC)
- lucid100-flash-oxygen-repair-mechanistic-model (paywall + unreleased UNIVERSE engine)
- lucid100-cho-low-dose-rate-dna-repair-deficient (closed Elsevier + zero deposit)
- lucid100-arabidopsis-aox1a-gamma-irradiation (closed T&F, lab-internal lines, wet-lab)

## EXECUTION LOG (2026-06-25 17:00-17:10)
### Promoted this session (real reproduction, disk-verified)
- fipy-wave4: SPOT-CHECK -> REPLICATED (cov8/agr9, 2nd-order convergence + mass conservation)
- BVBRC-16: -> PARTIAL (genome-feature slice reproduced)
- BVBRC-17: -> PARTIAL (COBRApy FBA slice reproduced)
- intensity-modulated-doserate: -> PARTIAL (IMK model implemented)
- multiscale-uhdr, BVBRC-11: re-tiered SPOT-CHECK -> PARTIAL (were mislabeled)
- zebrafish-brain: HELD at PARTIAL (DESeq2 on deposited counts reproduces direction, not exact 27/200/530; honest, no fabrication)

### In flight (local/web, no uicgpu)
- BVBRC-19 (ModelSEED+COBRApy FBA), patra-polbeta (docking/digitize), actinium-lutetium (re-tier confirm)

### uicgpu MC engine — CONFIRMED WORKING (for Second-100 track-structure batch)
- Reachable ONLY via ProxyJump=nuc13 (direct ssh uicgpu hangs — same path issue as 2026-06-18 incident).
- Geant4-DNA 11.4.2 in conda env /gpustor/stevens/anaconda3/envs/radmc; activate: source /gpustor/stevens/radmc/env.sh
- 3 built binaries: dnadamage1, clustering, chem6 (/gpustor/stevens/radmc/builds/<name>/). CPU-MC (255 cores), GPU not required.
- Campaign scope: ~19 Second-100 track-structure papers (s100-016/023/024/031/033/042/049/056/059/064/073/081/082/083/089 + 3 LUCID TOPAS). Each = per-paper geometry/physics/source setup -> run -> compare. Multi-hour to multi-day; needs proper scoping, NOT a blind 5-subagent fire.

### HARD CEILING — cannot promote (no fabrication): brahme review, skin-inflammation, fractionated-epigenetic, deinococcus-IR review, friedland-PARTRAC, flash-oxygen-UNIVERSE, cho-low-dose, arabidopsis (+ zebrafish capped without FASTQ realign)

## uicgpu Geant4-DNA MC CAMPAIGN — LAUNCHED 2026-06-25 17:28 CDT
- Driver: uicgpu:/gpustor/stevens/radmc/campaign_clustering.sh (setsid-detached, survives SSH disconnect)
- Engine: Geant4-DNA 11.4.2 clustering example, -mac run.in (NOTE: binary needs -mac flag, bare positional aborts rc=134)
- Sweep: 11 energies {0.5,1,2,5,10,20,50,100,200,500,1000} keV x 20,000 events each, 11-way parallel
- Output: campaign/clustering/E_<E>keV/clusters_output.root + clustering.log
- Yields DSB/SSB cluster complexity vs energy -> compare to Second-100 track-structure papers (s100-016/023/024/031/033/042/049/056/059/064/073/081/082/083/089 + LUCID TOPAS)
- ACCESS: uicgpu only via `ssh -o ProxyJump=nuc13 uicgpu` (direct hangs). env.sh prints harmless `mkdir: cannot create directory ''` warning.
- HARVEST: read clusters_output.root per energy, extract mean DSB/SSB yields, map to each paper's reported energy points, update verdicts.

## BVBRC-19 -> PARTIAL (written 2026-06-25 from disk-verified fba_replication.json after subagent timed out pre-write)
- COBRApy FBA on 6 authors' GEMs: all solve (mu 0.79-1.02), glucose-dependency reproduced, propionate secretion universal, auxotrophy hierarchy + vitamin nesting EXACT. cov7/agr9.
