# LUCID Resource / Tools / Methods Ledger Extract

Generated from `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications` report directories. Scope: LUCID Wave 6 + Wave 7 report directories present locally, including the additional Cordoni 2023 stochastic-Poisson replication directory found with the same LUCID reports.

## Totals

- Records: **31**
- Estimated CPU time: **268 min** (4.47 h), conservative local/subagent estimate
- Estimated GPU time: **0 h**
- Token estimates: **null** for each record; no reliable per-task token summaries were available in the project files.
- Heavy external engines explicitly **not run** where blocked: TOPAS-nBio, Geant4/Geant4-DNA, FLUKA/HIT, PARTRAC, BioDynaMo full stack, proprietary UNIVERSE GPU pipeline.

## Verdict Counts

- PARTIAL: 11
- REPLICATED: 6
- NO-GO: 3
- PARTIAL / SPOT-CHECK: 1
- REPLICATED with data limitations: 1
- PARTIAL strong: 1
- REPLICATED (TLK portion): 1
- REPLICATED/PARTIAL: 1
- PARTIAL, mechanistic core replicated: 1
- PARTIAL analytical-figure replication: 1
- SPOT-CHECK: 1
- REPLICATED pathway-level / partial full MC: 1
- PARTIAL / REPLICATED: 1
- REPLICATED-STRUCTURAL: 1

## Method Frequency Counts

- digitized figures: 10
- figure reproduction: 6
- pdftotext audit: 3
- ODE: 3
- Monte Carlo: 3
- RBE arithmetic: 2
- image-analysis: 2
- LQ fit: 2
- RBE calculation: 2
- review triage: 2
- uncertainty propagation: 2
- supplement parameter audit: 2
- linear dose-response fit: 1
- MIRD dosimetry chain: 1
- object evaluation parameter reimplementation: 1
- ROC/correlation analysis: 1
- public dataset validation: 1
- D10/RBE arithmetic: 1
- dose-rate table check: 1
- Monte Carlo method audit: 1
- analytic equation reproduction: 1
- DSB scoring rule reimplementation: 1
- decay-yield spot-check: 1
- repair-kinetics photon model: 1
- dose-rate R_TD50 table reproduction: 1
- closed-code boundary audit: 1
- figure/source-data inventory: 1
- curve reconstruction: 1
- table audit: 1
- IMK/SLDR survival model: 1
- MCMC parameter refit: 1
- kinetic GLOBLE model: 1
- LQ equivalence check: 1
- supplement table audit: 1
- RNA-seq DEG table analysis: 1
- RNA-seq ORA: 1
- interaction-gene verification: 1
- quantitative-content inventory: 1
- TLK ODE: 1
- nonlinear least-squares refit: 1
- supplement CSV audit: 1
- survival/FAR curve reproduction: 1
- agent-based model surrogate: 1
- LQ critical-volume model: 1
- equation reimplementation: 1
- parameter sensitivity: 1
- analytical gamma-H2AX model: 1
- parameter refit: 1
- integrated microdosimetric-kinetic model: 1
- ODE/equation reimplementation: 1
- LQ survival: 1
- parameter fitting: 1
- mechanistic DNA repair/survival model: 1
- GitHub code execution: 1
- SDD output parsing: 1
- review/wet-lab triage: 1
- figure inventory: 1
- reaction-network reconstruction: 1
- SciPy solve_ivp: 1
- exponential repair model: 1
- correlation analysis: 1
- statistical refit: 1
- analytical formula reimplementation: 1
- track-structure formula audit: 1
- survival-curve audit: 1
- sequence alignment: 1
- docking-score consistency audit: 1
- radiobiology arithmetic: 1
- foci-counting algorithm audit: 1
- synthetic/benchmark data analysis: 1
- spot-check: 1
- ANOVA/dose-response recomputation: 1
- wet-lab figure audit: 1
- NHEJ kinetic model: 1
- ODE/stochastic model: 1
- Monte Carlo spot-check: 1
- early DDR network model: 1
- RBE/additivity arithmetic: 1
- gamma-H2AX foci analysis: 1
- Gillespie SSA: 1
- linear-noise approximation: 1
- ODE/moment equations: 1
- Ornstein-Uhlenbeck simulation: 1
- stochastic simulation: 1
- ODE/moment model: 1
- biodosimetry model: 1
- curve/correlation validation: 1
- statistical comparison: 1
- table algebra audit: 1
- linear regression: 1
- foci-count reconstruction: 1
- figure/table reproduction: 1
- formula/table audit: 1
- repair-kinetics model: 1
- Monte Carlo approximation: 1

## Tool / Library Frequency Counts

- Python: 28
- matplotlib: 28
- numpy: 27
- scipy: 20
- pdftotext: 14
- pandas: 6
- vision digitization: 4
- pdfinfo: 3
- Python/text scan: 3
- Geant4 not run: 2
- TOPAS-nBio not run: 2
- FLUKA not run: 2
- pdftoppm: 1
- scipy/sklearn-style ROC: 1
- GitHub repo: AutoFoci: 1
- 7z manual dataset: 1
- Java source inspected: 1
- pdftotext/pdfinfo: 1
- MIRDsoft/ICRP-107 spot-check: 1
- Geant4-DNA not run: 1
- HIT beamline model unavailable: 1
- table transcription/digitization: 1
- MCMC custom script: 1
- pdftotext/markdown source: 1
- openpyxl: 1
- pandas/TSV processing: 1
- MSigDB ORA/reference gene sets: 1
- PDF tool attempted but failed: 1
- MDPI supplement CSVs: 1
- Ceres Solver not used: 1
- Zenodo Code.zip: 1
- BioDynaMo source inspected not built: 1
- PLOS supplementary DOCX/TIFs: 1
- digitized CSVs: 1
- GitHub repo: Medras-MC: 1
- SDD files: 1
- openpyxl/xlsx radial-energy tables: 1
- scipy solve_ivp/LSODA: 1
- MDPI supplement: 1
- Hat 2016 supplement: 1
- vision/OCR digitization: 1
- PARTRAC not run: 1
- sequence alignment tools/libraries: 1
- PDB/docking values audited not rerun: 1
- scipy/skimage if available: 1
- image-analysis scripts: 1
- scipy/statsmodels style calculations: 1
- supplement tables: 1
- Gillespie SSA custom code: 1
- GPU UNIVERSE code not available: 1

## Per-record Short Ledger

### lucid-actinium-lutetium-dose-effect
- **Title:** In vitro dose-effect relationships of actinium-225- and lutetium-177-labelled radiopharmaceuticals
- **Verdict:** PARTIAL / SPOT-CHECK — coverage 6, agreement 7.5
- **Methods:** linear dose-response fit, MIRD dosimetry chain, RBE arithmetic, digitized figures
- **Tools:** Python, numpy, scipy, matplotlib, pdftoppm, vision digitization, Geant4 not run
- **Code artifacts:** 1 (code/replicate_lucid.py)
- **Data artifacts:** 8 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** Wet-lab assays and full Geant4 dosimetry not rerun; linear fits depend on figure/table extraction.

### lucid-autofoci-detection
- **Title:** AutoFoci automated foci-detection/object evaluation parameter
- **Verdict:** REPLICATED — coverage 8, agreement 9
- **Methods:** image-analysis, object evaluation parameter reimplementation, ROC/correlation analysis, public dataset validation
- **Tools:** Python, numpy, scipy/sklearn-style ROC, pandas, matplotlib, GitHub repo: AutoFoci, 7z manual dataset, Java source inspected
- **Code artifacts:** 16 (code/autofoci_reimpl.py, code/evaluate.py, repo/AutoFoci/src/AutoFoci.java, repo/AutoFoci/src/AutoFoci/AnalyzeDialog.java, repo/AutoFoci/src/AutoFoci/AutoThreshold.java, repo/AutoFoci/src/AutoFoci/CustomTabbedPaneUI.java, repo/AutoFoci/src/AutoFoci/GreenGUI.java, repo/AutoFoci/src/AutoFoci/HistAnalyzer.java)
- **Data artifacts:** 80 listed in JSON
- **Compute:** CPU ~15 min; GPU 0 h
- **Main blocker/limitation:** Equation 3 weighting factor under-specified; Java implementation/source inspected but replication uses independent Python OEP.

### lucid-bnct-radioresistant-hcc
- **Title:** BNCT response in radioresistant hepatocellular carcinoma cells
- **Verdict:** PARTIAL — coverage 5, agreement 8
- **Methods:** LQ fit, D10/RBE arithmetic, digitized figures, dose-rate table check
- **Tools:** Python, numpy, scipy, pandas, matplotlib, pdftotext/pdfinfo, vision digitization
- **Code artifacts:** 1 (code/replicate.py)
- **Data artifacts:** 5 listed in JSON
- **Compute:** CPU ~8 min; GPU 0 h
- **Main blocker/limitation:** Wet-lab mechanism panels lack raw data; BNCT survival points digitized from figures; no raw clonogenic counts.

### lucid-cu64-topas-nbio-lethal-damage
- **Title:** Lethal damage in DNA for Auger electron-emitting radionuclides by TOPAS-nBio Monte Carlo methods
- **Verdict:** PARTIAL — coverage 5, agreement 10
- **Methods:** Monte Carlo method audit, analytic equation reproduction, DSB scoring rule reimplementation, decay-yield spot-check
- **Tools:** Python, numpy, matplotlib, pdftotext, MIRDsoft/ICRP-107 spot-check, TOPAS-nBio not run, Geant4-DNA not run
- **Code artifacts:** 4 (code/01_lethal_damage_equation.py, code/02_proximity_dsb_scoring.py, code/03_track_correlated_dsb.py, code/04_make_figures.py)
- **Data artifacts:** 6 listed in JSON
- **Compute:** CPU ~8 min; GPU 0 h
- **Main blocker/limitation:** End-to-end TOPAS-nBio/Geant4-DNA MC blocked by heavy toolchain and 400k-history runs; analytic core only.

### lucid-dna-repair-kinetics-doserate-rbe
- **Title:** DNA repair kinetics and dose-rate effects in RBE predictions
- **Verdict:** PARTIAL — coverage 6, agreement 9
- **Methods:** repair-kinetics photon model, dose-rate R_TD50 table reproduction, RBE calculation, closed-code boundary audit
- **Tools:** Python, numpy, scipy, matplotlib, pdftotext, FLUKA not run, HIT beamline model unavailable
- **Code artifacts:** 4 (code/fig12_photon_trend.py, code/fig4_left_rtd50.py, code/plot_rtd50.py, code/universe_photon.py)
- **Data artifacts:** 5 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** Full mixed-LET FLUKA/HIT SOBP benchmark closed/unavailable; photon-side submodel only.

### lucid-dsb-repair-history-review-triage
- **Title:** Historical review of DNA double-strand-break repair and RIANS/nucleo-shuttling model
- **Verdict:** NO-GO — coverage N/A, agreement N/A
- **Methods:** review triage, pdftotext audit, figure/source-data inventory
- **Tools:** pdftotext, pdfinfo, Python/text scan
- **Code artifacts:** 0 (none found)
- **Data artifacts:** 0 listed in JSON
- **Compute:** CPU ~5 min; GPU 0 h
- **Main blocker/limitation:** Narrative/historical review; no original data, tables, meta-analysis, or self-contained fitted model.

### lucid-franken-alpha-gamma-rbe
- **Title:** Relative biological effectiveness of alpha particles compared to gamma radiation
- **Verdict:** PARTIAL — coverage 6, agreement 10
- **Methods:** RBE arithmetic, uncertainty propagation, curve reconstruction, table audit
- **Tools:** Python, numpy, matplotlib, table transcription/digitization
- **Code artifacts:** 1 (code/refit_rbe.py)
- **Data artifacts:** 5 listed in JSON
- **Compute:** CPU ~5 min; GPU 0 h
- **Main blocker/limitation:** Raw per-dose data only plotted in figures; no supplement; cannot refit original weighted regressions from raw data.

### lucid-fukui-saga-lq-sldr-aldh
- **Title:** Tumor radioresistance caused by radiation-induced changes of stem-like cell content and sub-lethal damage repair capability
- **Verdict:** PARTIAL — coverage 7, agreement 8
- **Methods:** LQ fit, IMK/SLDR survival model, MCMC parameter refit, digitized figures
- **Tools:** Python, numpy, scipy, matplotlib, MCMC custom script, pdftotext
- **Code artifacts:** 6 (code/digitized_fig5.py, code/imk_model.py, code/params_table1.py, code/refit_mcmc.py, code/replicate_fig5.py, code/replicate_fig6.py)
- **Data artifacts:** 20 listed in JSON
- **Compute:** CPU ~15 min; GPU 0 h
- **Main blocker/limitation:** ALDH flow-cytometry and raw colony counts unavailable; split-dose Fig. 6 digitization unreliable; exact MCMC settings not specified.

### lucid-globle-photon-cell-killing
- **Title:** A Model of Photon Cell Killing Based on the Spatio-Temporal Clustering of DNA Damage in Higher Order Chromatin Structures
- **Verdict:** REPLICATED with data limitations — coverage 8, agreement 9
- **Methods:** ODE, kinetic GLOBLE model, LQ equivalence check, figure reproduction
- **Tools:** Python, numpy, scipy, matplotlib, pdftotext/markdown source
- **Code artifacts:** 3 (code/cell_lines.py, code/globle.py, code/make_figures.py)
- **Data artifacts:** 12 listed in JSON
- **Compute:** CPU ~5 min; GPU 0 h
- **Main blocker/limitation:** No raw experimental datapoints; referenced Supplement File S1 absent; author code not released.

### lucid-grandt-fibroblast-rnaseq
- **Title:** Radiation-response in primary fibroblasts of long-term survivors of childhood cancer with and without second primary neoplasms: the KiKme study
- **Verdict:** PARTIAL strong — coverage 8, agreement 9
- **Methods:** supplement table audit, RNA-seq DEG table analysis, RNA-seq ORA, interaction-gene verification
- **Tools:** Python, openpyxl, matplotlib, pandas/TSV processing, MSigDB ORA/reference gene sets, pdftotext
- **Code artifacts:** 4 (code/00_download.sh, code/01_replicate_degs.py, code/02_pathway_with_background.py, code/03_figures.py)
- **Data artifacts:** 20 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** No public GEO/SRA/FASTQ raw data; proprietary IPA scores not reproducible; analysis limited to processed supplements.

### lucid-h2ax-phosphorylation-review-triage
- **Title:** H2AX phosphorylation at the sites of DNA double-strand breaks in cultivated mammalian cells and tissues
- **Verdict:** NO-GO — coverage N/A, agreement N/A
- **Methods:** review triage, pdftotext audit, quantitative-content inventory
- **Tools:** pdftotext, pdfinfo, Python/text scan, PDF tool attempted but failed
- **Code artifacts:** 0 (none found)
- **Data artifacts:** 1 listed in JSON
- **Compute:** CPU ~2 min; GPU 0 h
- **Main blocker/limitation:** Narrative review; no methods, tables, model, code, accession, or reproducible dataset.

### lucid-hsgc-c5-repair-performance
- **Title:** Two-lesion kinetics repair-performance model for HSGc-C5 cells
- **Verdict:** REPLICATED (TLK portion) — coverage 6, agreement 9
- **Methods:** TLK ODE, nonlinear least-squares refit, supplement CSV audit, survival/FAR curve reproduction
- **Tools:** Python, numpy, scipy, pandas, matplotlib, MDPI supplement CSVs, Ceres Solver not used, Geant4 not run
- **Code artifacts:** 5 (code/finalize.py, code/refit.py, code/replicate.py, code/tlk_model.py, data/_decode.py)
- **Data artifacts:** 18 listed in JSON
- **Compute:** CPU ~1 min; GPU 0 h
- **Main blocker/limitation:** Track-structure/PHITS/Geant4 DSB-yield half not rerun; uses paper-reported DSB yields and open supplement curves.

### lucid-lung-fibrosis-abm
- **Title:** Mechanistic model of radiation-induced lung fibrosis ABM/Monte Carlo
- **Verdict:** PARTIAL — coverage 5, agreement 6
- **Methods:** agent-based model surrogate, LQ critical-volume model, equation reimplementation, parameter sensitivity
- **Tools:** Python, numpy, scipy, matplotlib, Zenodo Code.zip, BioDynaMo source inspected not built, TOPAS-nBio not run
- **Code artifacts:** 11 (code/abm_lite.py, data/code/ABM model/src/AEC.h, data/code/ABM model/src/AEC2bystander.h, data/code/ABM model/src/Macrophage.h, data/code/ABM model/src/Mesenchymal.h, data/code/ABM model/src/alv_cell.h, data/code/ABM model/src/behavior.h, data/code/ABM model/src/custom_ops.h)
- **Data artifacts:** 34 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** BioDynaMo/TOPAS-nBio stack not built or run; 3D dose-distribution and proton/photon RBE results blocked by heavy MC workflow.

### lucid-mariotti-split-dose-gamma-h2ax
- **Title:** Use of the γ-H2AX assay to investigate DNA repair dynamics after split-dose irradiation
- **Verdict:** REPLICATED — coverage 7, agreement 9
- **Methods:** analytical gamma-H2AX model, supplement parameter audit, digitized figures, parameter refit
- **Tools:** Python, numpy, scipy, matplotlib, PLOS supplementary DOCX/TIFs, digitized CSVs
- **Code artifacts:** 3 (code/model.py, code/refit.py, code/validate.py)
- **Data artifacts:** 23 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** Raw γ-H2AX foci counts and clonogenic data not tabulated; comparisons partly digitized from figures.

### lucid-matsuya-nte-integrated
- **Title:** Integrated microdosimetric-kinetic model for targeted and non-targeted effects
- **Verdict:** REPLICATED/PARTIAL — coverage 10, agreement 7
- **Methods:** integrated microdosimetric-kinetic model, ODE/equation reimplementation, LQ survival, digitized figures, parameter fitting
- **Tools:** Python, numpy, scipy, matplotlib, pdftotext
- **Code artifacts:** 3 (code/imk_model.py, code/make_figures.py, code/reference_data.py)
- **Data artifacts:** 12 listed in JSON
- **Compute:** CPU ~25 min; GPU 0 h
- **Main blocker/limitation:** Experimental data are figure-only/data-on-request; digitized at ~5-10% precision; several parameter fits are degenerate or internally inconsistent.

### lucid-medras-mc
- **Title:** A Mechanistic DNA Repair and Survival Model (Medras): Applications to Intrinsic Radiosensitivity, RBE and Dose-Rate
- **Verdict:** PARTIAL, mechanistic core replicated — coverage 4, agreement 8
- **Methods:** Monte Carlo, mechanistic DNA repair/survival model, GitHub code execution, SDD output parsing
- **Tools:** Python, numpy, pandas, matplotlib, GitHub repo: Medras-MC, SDD files, openpyxl/xlsx radial-energy tables
- **Code artifacts:** 13 (Medras-MC/damagegenerator/SDDWriter.py, Medras-MC/damagegenerator/chromModel.py, Medras-MC/damagegenerator/damageModel.py, Medras-MC/damagegenerator/trackModel.py, Medras-MC/repairanalysis/analyzeAberrations.py, Medras-MC/repairanalysis/medrasparser.py, Medras-MC/repairanalysis/medrasrepair.py, Medras-MC/repairanalysis/misrepaircalculator.py)
- **Data artifacts:** 34 listed in JSON
- **Compute:** CPU ~5 min; GPU 0 h
- **Main blocker/limitation:** Paper-level survival/RBE/dose-rate figures require external Paganetti/PIDE datasets; PIDE is registration-gated; deterministic seed not fully exposed.

### lucid-nuclear-matrix-uv-repair-triage
- **Title:** Nuclear matrix association of UV-induced DNA repair in human fibroblasts
- **Verdict:** NO-GO — coverage N/A, agreement N/A
- **Methods:** review/wet-lab triage, pdftotext audit, figure inventory
- **Tools:** pdftotext, pdfinfo, Python/text scan
- **Code artifacts:** 0 (none found)
- **Data artifacts:** 18 listed in JSON
- **Compute:** CPU ~3 min; GPU 0 h
- **Main blocker/limitation:** 1988 wet-lab paper; no tables, equations, supplementary data, code, or machine-readable dataset.

### lucid-p53-repair
- **Title:** Modeling of DNA Damage Repair and Cell Response in Relation to p53 System Exposed to Ionizing Radiation
- **Verdict:** PARTIAL — coverage 6, agreement 6
- **Methods:** ODE, reaction-network reconstruction, SciPy solve_ivp, figure reproduction
- **Tools:** Python, scipy solve_ivp/LSODA, numpy, matplotlib, pdftotext, MDPI supplement, Hat 2016 supplement
- **Code artifacts:** 2 (code/p53_model.py, code/run_experiments.py)
- **Data artifacts:** 12 listed in JSON
- **Compute:** CPU ~1 min; GPU 0 h
- **Main blocker/limitation:** Original LUCID source code not released; p53 stochastic simulator reimplemented independently; supplement access initially bot-gated but recovered via MDPI static CDN.

### lucid-pariset-53bp1-mouse-strains
- **Title:** 53BP1 DNA repair kinetics and radiosensitivity across mouse strains
- **Verdict:** PARTIAL — coverage 6, agreement 8
- **Methods:** exponential repair model, correlation analysis, digitized figures, statistical refit
- **Tools:** Python, numpy, scipy, matplotlib, pdftotext, vision/OCR digitization
- **Code artifacts:** 1 (code/replicate_pariset.py)
- **Data artifacts:** 7 listed in JSON
- **Compute:** CPU ~8 min; GPU 0 h
- **Main blocker/limitation:** Per-strain numerical outcome data and raw foci/survival data not deposited; main correlation digitized from bar charts.

### lucid-partrac-analytical-formulas
- **Title:** PARTRAC analytical formulas
- **Verdict:** PARTIAL analytical-figure replication — coverage 7, agreement 7
- **Methods:** analytical formula reimplementation, digitized figures, track-structure formula audit
- **Tools:** Python, numpy, scipy, matplotlib, PARTRAC not run
- **Code artifacts:** 3 (code/formulas.py, code/parameters.py, code/run_replication.py)
- **Data artifacts:** 8 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** PARTRAC itself not run; source numerical figure data unavailable, so formula/figure-level replication only.

### lucid-patra-polbeta-radiosensitivity
- **Title:** Polβ radiosensitivity and repair-defect claims
- **Verdict:** PARTIAL — coverage 5, agreement 7
- **Methods:** survival-curve audit, sequence alignment, docking-score consistency audit, radiobiology arithmetic
- **Tools:** Python, numpy, scipy, matplotlib, sequence alignment tools/libraries, PDB/docking values audited not rerun
- **Code artifacts:** 3 (code/01_sequence_check.py, code/02_lq_fit.py, code/03_quantitative_audit.py)
- **Data artifacts:** 25 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** Survival claim survives but cDNA/protein deletion story and docking-score units have serious inconsistencies; raw supporting data limited.

### lucid-pyfoci-miscounting
- **Title:** PyFoci / foci miscounting replication
- **Verdict:** PARTIAL — coverage 6, agreement 7
- **Methods:** image-analysis, foci-counting algorithm audit, synthetic/benchmark data analysis, figure reproduction
- **Tools:** Python, numpy, scipy/skimage if available, matplotlib, image-analysis scripts
- **Code artifacts:** 15 (code/PyFoci_Colab/PyFoci.ipynb, code/analyze_cached_pyfoci.py, code/pyfoci/demo.py, code/pyfoci/pyfoci-save.py, code/pyfoci/pyfoci-view.py, code/pyfoci/pyfoci/__init__.py, code/pyfoci/pyfoci/bioProcessing.py, code/pyfoci/pyfoci/fociCounter.py)
- **Data artifacts:** 80 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** Depends on available image/benchmark artifacts; full original microscopy workflow not necessarily rerun.

### lucid-skin-inflammation-nfkb-cox2
- **Title:** Skin inflammation NF-kB/COX-2 radiation response
- **Verdict:** SPOT-CHECK — coverage 3, agreement 9
- **Methods:** spot-check, digitized figures, ANOVA/dose-response recomputation, wet-lab figure audit
- **Tools:** Python, numpy, scipy/statsmodels style calculations, matplotlib, pdftotext, vision digitization
- **Code artifacts:** 3 (code/digitized_figures.py, code/make_figures.py, code/replicate_stats.py)
- **Data artifacts:** 26 listed in JSON
- **Compute:** CPU ~8 min; GPU 0 h
- **Main blocker/limitation:** Wet-lab paper; only selected figure-level ANOVA/dose-response/PGE2 checks possible; no raw data.

### lucid-slow-fast-nhej
- **Title:** Slow/fast non-homologous end joining model
- **Verdict:** REPLICATED pathway-level / partial full MC — coverage 8, agreement 8
- **Methods:** NHEJ kinetic model, ODE/stochastic model, Monte Carlo spot-check, figure reproduction
- **Tools:** Python, numpy, scipy, matplotlib
- **Code artifacts:** 3 (code/experimental_data.py, code/figures.py, code/nhej_model.py)
- **Data artifacts:** 17 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** Full Monte Carlo/pathway details only partially reproduced; raw data/source outputs limited.

### lucid-spatiotemporal-early-dna-damage
- **Title:** Spatiotemporal early DNA-damage response network model
- **Verdict:** REPLICATED — coverage 7, agreement 8
- **Methods:** ODE, early DDR network model, supplement parameter audit, figure reproduction
- **Tools:** Python, numpy, scipy, matplotlib, supplement tables
- **Code artifacts:** 4 (code/figure11_replication.py, code/figure_overlay.py, code/lucid_model.py, code/quantitative_check.py)
- **Data artifacts:** 15 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** Replication bounded to published/supplement model parameters; raw experimental basis not fully available.

### lucid-staaf-mixed-beam-gamma-h2ax
- **Title:** Mixed-beam alpha/gamma gamma-H2AX foci additivity and RBE
- **Verdict:** PARTIAL / REPLICATED — coverage 7, agreement 7
- **Methods:** RBE/additivity arithmetic, digitized figures, gamma-H2AX foci analysis, uncertainty propagation
- **Tools:** Python, numpy, scipy, matplotlib, pdftotext, vision digitization
- **Code artifacts:** 2 (code/replicate.py, data/digitized_data.py)
- **Data artifacts:** 8 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** Digitized figure data only; raw foci measurements not deposited.

### lucid-stochastic-poisson-dna-damage
- **Title:** On the Emergence of the Deviation from a Poisson Law in Stochastic Mathematical Models for Radiation-Induced DNA Damage: A System Size Expansion
- **Verdict:** REPLICATED-STRUCTURAL — coverage 8, agreement 8
- **Methods:** Gillespie SSA, linear-noise approximation, ODE/moment equations, Ornstein-Uhlenbeck simulation, Monte Carlo
- **Tools:** Python, numpy, scipy, matplotlib, Gillespie SSA custom code
- **Code artifacts:** 2 (code/gsm2_model.py, code/run_replication.py)
- **Data artifacts:** 7 listed in JSON
- **Compute:** CPU ~1 min; GPU 0 h
- **Main blocker/limitation:** No author code or raw numerical figure values; theoretical equations are explicit, so replication is structural/qualitative rather than numeric figure matching.

### lucid-stochastic-rejoining
- **Title:** Stochastic DNA fragment rejoining model
- **Verdict:** REPLICATED — coverage 9, agreement 8
- **Methods:** stochastic simulation, ODE/moment model, Monte Carlo, figure reproduction
- **Tools:** Python, numpy, scipy, matplotlib
- **Code artifacts:** 4 (code/gillespie_rejoining.py, code/run_fig3_impact_factors.py, code/run_fig4_kinetics.py, code/smoke_test.py)
- **Data artifacts:** 5 listed in JSON
- **Compute:** CPU ~15 min; GPU 0 h
- **Main blocker/limitation:** Raw numerical figure data not distributed; comparison limited to reconstructed model behavior and generated figures.

### lucid-turner-gamma-h2ax-biodosimetry
- **Title:** Gamma-H2AX biodosimetry model and validation correlations
- **Verdict:** REPLICATED — coverage 9, agreement 9
- **Methods:** biodosimetry model, curve/correlation validation, digitized figures, statistical comparison
- **Tools:** Python, numpy, scipy, pandas, matplotlib, pdftotext
- **Code artifacts:** 2 (code/replicate_turner.py, code/use_paper_params.py)
- **Data artifacts:** 19 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** Bounded by available paper tables/figures; raw experimental records not fully deposited.

### lucid-ulyanenko-gammah2ax-patm-msc
- **Title:** Gamma-H2AX and pATM foci in mesenchymal stem cells
- **Verdict:** REPLICATED — coverage 8, agreement 9
- **Methods:** table algebra audit, linear regression, foci-count reconstruction, figure/table reproduction
- **Tools:** Python, numpy, scipy, pandas, matplotlib, pdftotext
- **Code artifacts:** 2 (code/digitize_from_tables.py, code/make_figures.py)
- **Data artifacts:** 9 listed in JSON
- **Compute:** CPU ~8 min; GPU 0 h
- **Main blocker/limitation:** Relies on published tables/figures; raw foci images/counts not available.

### lucid-universe-repair-doserate-rbe
- **Title:** Impact of DNA Repair Kinetics and Dose Rate on RBE Predictions in the UNIVERSE
- **Verdict:** PARTIAL — coverage 6, agreement 6
- **Methods:** formula/table audit, repair-kinetics model, RBE calculation, Monte Carlo approximation
- **Tools:** Python, numpy, scipy, matplotlib, FLUKA not run, GPU UNIVERSE code not available
- **Code artifacts:** 4 (code/kiefer_chatterjee.py, code/lightweight_universe_audit.py, code/simulate_universe.py, code/universe_core.py)
- **Data artifacts:** 5 listed in JSON
- **Compute:** CPU ~10 min; GPU 0 h
- **Main blocker/limitation:** No public UNIVERSE code/raw simulation outputs; FLUKA SOBP beamline and GPU three-step diffused RDD parameters unavailable.
