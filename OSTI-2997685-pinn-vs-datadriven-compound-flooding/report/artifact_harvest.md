# Artifact harvest — OSTI-2997685

## Public artifacts pulled

| Source | Artifact | URL | Size (B) | MD5 (if from Figshare) |
|--------|----------|-----|----------|------------------------|
| OSTI | paper.pdf | https://www.osti.gov/servlets/purl/2997685 | 5 770 801 | (not from Figshare) |
| Figshare | figshare_meta.json (295-file manifest) | https://api.figshare.com/v2/articles/28890083 | ~62 KB | -- |
| Figshare | README.md | https://ndownloader.figshare.com/files/56363366 | 1 503 | 0191219b2e6674d86c157fe1497eed62 |
| Figshare | requirement_tf1.txt | (tf1 conda env) | 3 589 | e191819a4c035e525dcdfc0f375376c6 |
| Figshare | requirement_tf2.txt | (tf2 conda env) | 6 850 | ec178ed9314bcc6f3700697f83c5d24d |
| Figshare | myearth.py | (event sampler) | 6 289 | 7865a55bc5e24787cb24a3d3cff5edfc |
| Figshare | utils_ML.py | (data-driven utils) | 5 383 | 06215c32079cf768b8691cf54e0ba827 |
| Figshare | othertime.py | | 6 421 | 2d8e55bbdc1bf19b388d31527a73537c |
| Figshare | SVE_module_dynamic_uh_mff_ts_l2_new.py | (vanilla PINN core) | 33 514 | 87a3092603fe503c62f742d2d78138d6 |
| Figshare | SVE_module_dynamic_uh_mff_ts_l2_FDM.py | (FD-PINN core) | 37 473 | -- |
| Figshare | PINN_test_bnd_uh_Telemac.py | (vanilla PINN driver) | 4 400 | c30d7c420bcb25ae09a48ce658e767bb |
| Figshare | PINN_test_bnd_uh_Telemac_FDM.py | (FD-PINN driver) | 4 489 | -- |
| Figshare | PINN_test_bnd_uh_Telemac_FDM_backward.py | (FD-PINN back diff) | 4 830 | 7472e3e5b6b03393f8c75923aab7eea2 |
| Figshare | PINN_uh_Telemac.out | (vanilla PINN log; has PINN Time elapsed line) | 6 742 682 | -- |
| Figshare | PINN_uh_Telemac_FDM.out | (FD-PINN log) | 4 564 637 | -- |
| Figshare | PINN_uh_Telemac_FDM_backward.out | (FD back-diff log) | 4 553 820 | -- |
| Figshare | PINN_metrics.csv / PINN_FDM_metrics.csv / PINN_FDM_backward_metrics.csv | | ~1.6 KB total | -- |
| Figshare | metrics_{CNN, CNN_conv, CNN_LSTM, GRU, LSTM, UNet, UNet_tiny}[_Irene].csv | | ~10 KB total | -- |
| Figshare | time_{CNN, CNN_conv, CNN_LSTM, GRU, LSTM, UNet}.csv | | <1 KB each | -- |
| Figshare | train_{CNN,CNN_conv,CNN_LSTM,GRU,LSTM,UNet_tiny}.py + predict_{...}.py | | ~10 KB each | -- |
| Figshare | 8 x 7 arch = 56 `<model>_Ne<N>_array.npy` + 56 `<model>_time_Ne<N>_array.npy` | | ~5 KB each | -- |
| Figshare | 6 x 3 pickled PINN metrics `PINN_uh_Telemac*.pickle` | | 68 KB each | -- |

Also on uicgpu (large binaries, not copied to Dropbox to keep replication dir compact):

| Path (uicgpu) | Size | Purpose |
|---------------|------|---------|
| `/data/stevens/scratch/tmp/osti2997685/Telemac_output_ensemble_rp.nc` | 544 490 149 B | Telemac ensemble reference solutions |
| `.../output_high.slf` | 141 785 164 B | high-res Telemac hindcast |
| `.../output_10days_hotstart.slf` | 35 749 324 B | 10-day hotstart |
| `.../DR_1D_5cells.p01.hdf` | 12 130 489 B | HEC-RAS comparison |
| `.../mesh_1D_channel_dx100.exo` + `.slf` + `.liq` | ~350 KB | 1-D river mesh + BC |

**Retrievability**: all Figshare artifacts remain permanently accessible via
`https://ndownloader.figshare.com/files/<id>`; ID list preserved in `work/figshare_meta.json`.

## Local totals

- paper.pdf: 5.8 MB
- work/figshare_code/: 17.3 MB (212 code + metrics + 3 PINN logs)
- extraction/: 424 KB (marker.md + nougat.mmd + pdftotext_raw.txt)
- report/evidence/: 168 KB (2 figures + JSON + txt)

## Data checksums verified

Every Figshare file downloaded matches its published `supplied_md5` = `computed_md5` in the
API response, giving byte-exact provenance to the DOI-registered artifact set.
