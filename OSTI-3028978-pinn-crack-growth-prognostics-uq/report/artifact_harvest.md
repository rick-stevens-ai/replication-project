# Artifact harvest

## Primary paper
- **URL**: https://www.osti.gov/servlets/purl/3028978
- **OSTI ID**: 3028978
- **DOI**: 10.5194/wes-11-737-2026
- **Journal**: Wind Energy Science, vol. 11, pp. 737-752 (2026)
- **Local path**: `work/paper.pdf` (7,451,125 bytes)
- **License**: CC BY 4.0 (open access via Copernicus / Wind Energy Science)
- **Notes**: OSTI blocks non-US-University IP ranges; downloaded via `uicgpu` (University of Illinois Chicago proxy) and rsync'd back.

## Cited prerequisite paper
- **Bechhoefer & Dubé (2020)**, "Contending Remaining Useful Life Algorithms",
  PHM Society Annual Conference Proceedings.
- **URL**: https://papers.phmsociety.org/index.php/phmconf/article/download/1274/864
- **DOI**: 10.36001/phmconf.2020.v12i1.1274
- **Local path**: `work/bechhoefer2020.pdf` (1,809,525 bytes)
- **License**: CC BY 3.0
- **Notes**: Confirms Head's theory ODE structure and 1475-h HI dataset origin.

## Original vibration-based HI dataset (Bechhoefer & Dubé 2020)
- **Availability**: NOT public.
- **Paper's data-availability statement**: "Datasets used in this research
  are not publicly accessible due to either non-disclosure agreement
  protection or unavailability of raw data."
- **Bechhoefer 2020 paper confirms**: dataset collected over 55 days on a
  2.2 MW wind turbine, held by GPMS Inc. under NDA (Eric Bechhoefer,
  eric@gpsm-vt.com).
- **Implication for replication**: exact numerical match to paper's Tables 1
  & 2 is impossible without the actual HI stream. Replication uses a
  physics-consistent synthetic HI trajectory that satisfies the exact ODE
  the paper embeds in its physics loss, plus heteroscedastic noise matching
  Fig. 2a description.

## Original SCADA dataset (Eftekhari Milani et al. 2026)
- **Availability**: NOT public (referenced paper "submitted" as of 2026;
  data from unnamed 1.5 MW wind turbines, likely proprietary utility data).

## Original X-TFC / TFC code
- **Availability**: "available from the authors upon request" (paper §
  Code availability). Not downloaded.
- **Note**: X-TFC is described in Schiassi et al. 2021b (Neurocomputing);
  the algorithm has been reimplemented from scratch here based on the paper's
  Equations 17-25.

## Software stack (all installed locally in venv `work/.venv`)
- Python 3.14.6
- numpy 2.5.1
- scipy 1.18.0
- matplotlib (bundled)

## Compute
- **Where run**: local (CherryRd, macOS 26.3, Python venv). CPU only. No GPU
  required. X-TFC uses a random-projection single-layer network with L=5
  neurons and 1000 collocation points — trivially small.
- **Wall time**: full replication (Table 1 + Table 2 + physics regularization
  sweep + plotting) runs in under 5 seconds.
