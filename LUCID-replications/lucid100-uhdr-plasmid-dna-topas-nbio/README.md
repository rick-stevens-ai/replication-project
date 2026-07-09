# LUCID100 slot 48 — UHDR-dependent plasmid DNA damage with TOPAS-nBio

**Paper:** Masilela T A M, D-Kondo J N, Shin W-G, Rezaee M, LaVerne J A, Paganetti H, Faddegon B, Schuemann J, Ramos-Méndez J. *Ultra-high dose rate dependent modeling of plasmid DNA damage with TOPAS-nBio.* Phys. Med. Biol. **71** (2026) 095013.
**DOI:** [10.1088/1361-6560/ae62c6](https://doi.org/10.1088/1361-6560/ae62c6)
**License:** CC-BY 4.0 (open access)
**Funding:** NIH/NCI R01CA187003, R01CA266419
**Replication slot:** Wave 5, rank 79, tier A, priority 14 (`candidate_curated`)

## TL;DR (verdict)

- **First-pass: GO (smoke-only).** Paper is fully open and CC-BY; full PDF, abstract, methods, all equations, Table 1 (43 reactions + rate constants), Table 2 (experimental comparator dataset), and numerical results for SSB and DSB yields at four scavenging capacities × {CONV, UHDR} are recovered.
- Full reproduction requires a TOPAS-nBio v4.0 dev build on Geant4-11.1.3 with the modified TsEmDNAPhysics list (ELSEPA elastic + Meesungnoen thermalization) and 5×10⁸ condensed-history primaries + IRT chemistry. **Not feasible on CherryRd**; HPC job plan is in `notes/HPC_JOB_PLAN.md`.
- A **reduced analytical/numerical smoke** is feasible *and implemented*: reproduce the SSB-yield-vs-scavenging-capacity scaling (Eq. 4) and the qualitative ·OH lifetime-vs-intertrack-separation comparison (Fig. 4) using only the published rate constants and pulse timing. See `scripts/smoke_scavenging_capacity.py`.

## Authors & affiliations

| Author | Affiliation | ORCID |
|---|---|---|
| Thongchai A M Masilela (1st) | UCSF Radiation Oncology | 0000-0002-1717-6761 |
| J Naoki D-Kondo | UCSF | 0000-0002-4410-1925 |
| Wook-Geun Shin | MGH / Harvard | 0000-0002-8622-1888 |
| Mohammad Rezaee | Johns Hopkins | 0000-0003-4607-9570 |
| Jay A LaVerne | Notre Dame Radiation Lab | – |
| Harald Paganetti | MGH / Harvard | 0000-0002-6257-2413 |
| Bruce Faddegon | UCSF | 0000-0002-4573-1582 |
| Jan Schuemann | MGH / Harvard | 0000-0002-7554-8818 |
| **José Ramos-Méndez** (corresponding) | UCSF | 0000-0002-8106-5142 |

Group page: https://ramoslab.ucsf.edu/dna-damage-modeling

## Folder layout

```
lucid100-uhdr-plasmid-dna-topas-nbio/
├── README.md                # this file
├── PROGRESS.md              # phase log
├── ARTIFACT_MANIFEST.md     # provenance for everything in artifacts/
├── FIRST_PASS_REPORT.md     # verdict + reproducibility scoring
├── artifacts/
│   ├── paper.pdf            # CC-BY full text (downloaded from iopscience)
│   ├── paper.txt            # pdftotext layout extract used for analysis
│   ├── crossref.json        # Crossref metadata
│   ├── semanticscholar.json # S2 record (abstract, authors, refs elided)
│   ├── openalex.json        # OpenAlex record (OA status, locations)
│   ├── unpaywall.json       # Unpaywall (this paper)
│   ├── unpaywall_dkondo2024.json   # precursor: D-Kondo 2024 oxygen effect paper (PMC OA)
│   ├── unpaywall_dkondo2021.json   # precursor: D-Kondo 2021 plasmid DNA model
│   ├── ae62c6_esummary.json # NCBI PubMed esummary
│   └── ae62c6_epmc.xml      # Europe PMC full-text probe (empty — paper not in EPMC fulltext)
├── scripts/
│   ├── smoke_scavenging_capacity.py   # analytical SSB-vs-σ + intertrack-lifetime reproducer
│   └── chemistry_table1.csv            # machine-readable Table 1 (43 reactions, kobs)
├── figures/                            # smoke-script output PNGs
└── notes/
    ├── HPC_JOB_PLAN.md                 # how to actually rerun this on Aurora/uicgpu/Sophia
    └── REPRODUCIBILITY_SCORECARD.md    # what is/isn’t reproducible from public artifacts
```

## Openness scorecard (1=closed, 5=ideal)

| Item | Score | Note |
|---|---|---|
| Paper full text | 5 | CC-BY 4.0, PDF in `artifacts/paper.pdf` |
| Supplement | n/a | "All data … are included within the article" — no separate supplement |
| Code released | 2 | TOPAS-nBio core is open (`topas-nbio/TOPAS-nBio-v2.0`), but the **specific chemistry parameter files for Models 1 & 2** are NOT yet released. Paper states they "will be released as an example in a future version of TOPAS-nBio." OpenTOPAS v4.0.0 is open at https://opentopas.github.io |
| Raw simulation data | 2 | Not deposited; only summary numbers in paper |
| External datasets needed | 3 | Experimental comparators (Milligan 1993, Tomita 1995, Klimczak 1993, Sforza 2024, Wanstall 2024, Perstin 2022, Konishi 2023, Kunz 2025, Wang 2025, Ohsawa 2022, Small 2021) — most paywall-mixed but the *values used* are tabulated in Table 2 of the paper itself |
| **Overall replicability** | **2.5/5** | Methods are fully specified to the equation level; missing pieces are (a) the as-built TOPAS-nBio v4.0 dev branch, (b) the chemistry .topas decks for Models 1 & 2, (c) the DSB-scoring Python script |
| Endpoints needed | free-only | TOPAS-nBio (open), Python (open). No paid API. |

## Quick reproduction (what we did locally)

```bash
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-uhdr-plasmid-dna-topas-nbio
python3 scripts/smoke_scavenging_capacity.py
# → figures/smoke_ssb_vs_sigma.png, figures/smoke_intertrack_vs_oh_lifetime.png
# → scripts/smoke_results.csv
```

What this checks (does NOT replace TOPAS-nBio):
1. Computes the ·OH scavenging capacity σ (s⁻¹) for each (DMSO, O₂, DNA) cocktail from Table 1 reaction rates, including R31* (·OH+DMSO, 7.1×10⁹·[DMSO]) and reproduces the per-condition σ values used in the paper.
2. Evaluates Eq. (4): `k_obs(·OH+DNA→break) = 1.32×10⁷ · σ^0.29`, multiplies by the published efficiency factor (24% for R34, 0.8% for R35), and plots the predicted SSB yield against the paper’s reported CONV values (`3.63e-7, 9.31e-8, 1.63e-8, 6.59e-10 /Gy/Da`) at DMSO `{1e-5, 1e-4, 1e-3, 0.1} M`.
3. Computes mean ·OH lifetime `τ = 1/σ` at each DMSO concentration vs the **5.6 ns** mean inter-history time spacing inside a 5 µs UHDR pulse (from the paper’s Fig. 4 sampling). This reproduces the qualitative intertrack-vs-no-intertrack argument that explains why UHDR ≠ CONV only below σ ≈ 10⁷ s⁻¹.

## What is *not* reproduced

- Absolute MC SSB/DSB G-values (need IRT chemistry — done in TOPAS-nBio).
- The 73.5% DSB reduction figure (needs the Python DSB-scoring script on per-strand IDs from TOPAS — script not released).
- Model 2 oxygen-competition / WR-1065 chemical-repair predictions (need the augmented chemistry table reactions R37–R43*).
- Sensitivity analyses on DSB bp threshold (5/10/15 bp) and DNA concentration (50→250 µg/mL).

## Next actions (in priority order)

1. **Open watch on TOPAS-nBio releases** for the Masilela chemistry deck (paper promises “future version”). Tracked: https://github.com/topas-nbio/TOPAS-nBio-v2.0
2. If a TOPAS-nBio build is needed: use **Aurora** (PBS, `datascience` allocation) or **uicgpu**. Job plan in `notes/HPC_JOB_PLAN.md`.
3. Mirror the D-Kondo 2024 precursor paper (PMC OA) for shared WR-1065 chemistry parameters — already linked: https://pmc.ncbi.nlm.nih.gov/articles/PMC12054022/
4. If TOPAS-nBio decks land before LUCID100 wave-5 closes, escalate to a full replication and bump priority to A+.

## QA retag recommendation

**Keep current QA tag** (`KEEP: relevant and replication-plausible`) but annotate the slot with `smoke-only / full-rerun blocked on author code release + HPC time`.
