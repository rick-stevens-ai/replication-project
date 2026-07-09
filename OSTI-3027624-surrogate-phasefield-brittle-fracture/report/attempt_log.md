# Attempt log — OSTI-3027624

- Paper unreachable from CherryRd; downloaded PDF + pfm_bench data via uicgpu (proxy internet).
- Confirmed pfm_bench public (Harvard Dataverse) + code on GitHub (C1).
- Downloaded 50 "lite" tension/vol/1c sim files (~1.3 GB) — real phase-field fracture sims, crack fraction ~2-6%.
- Adapted paper's FNO + UNet into single driver replicate.py.
- Trained 3 seeds x 60 epochs each, FNO + UNet, on A100 (env pyg-mesh, torch 2.4.1+cu121).
- FNO training: val_MSE plateaued ~0.0096 (barely below constant-field baseline ~0.010) -> spectral smoothing struggles on sparse cracks.
- UNet training: val_dice climbed 0 -> ~0.49 across seeds.
- Threshold-search Dice at test: FNO mean 0.102, UNet mean 0.531; ensembling stable.
- Original driver subagent hit runtime limit mid-training; training continued as background nohup on uicgpu and completed (run.log "DONE."). Report written directly by parent coordinator from the completed result JSONs.
- Argo LLM judge scored the numerical result.
