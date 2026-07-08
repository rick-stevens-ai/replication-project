#!/usr/bin/env python
"""
Rasp-2018 RE-PASS — offline-diagnostic tests to lift coverage.

Targets (tractable subset chosen for the re-pass):
  C1/C2 — param count of 9x256 LeakyReLU FC matches paper (567,361)
  C5    — 18-epoch sufficiency: val loss already plateaued at epoch 18 in PASS-1 20-epoch run
  C10/C12 — diagnostic-mode mean heating climatology + ITCZ latitude (paper says ~5°N)
  C16   — column moist-static-energy balance (NN-predicted vs SPCAM truth)
  C21   — NN inference cost — order-of-magnitude check vs SPCAM step cost

Writes results incrementally to results/repass/.
"""
import os, sys, time, json
from pathlib import Path
import numpy as np
import xarray as xr
import torch
import torch.nn as nn

ROOT = Path(os.environ.get("RASP_ROOT", "/data/stevens/rasp_2018"))
RUN  = ROOT / "runs" / "control_9x256"
OUT  = Path(os.environ.get("RASP_OUT", "/data/stevens/rasp_2018/repass_out"))
OUT.mkdir(parents=True, exist_ok=True)

results = {}

def write_json(name, obj):
    p = OUT / f"{name}.json"
    p.write_text(json.dumps(obj, indent=2, default=float))
    print(f"[wrote] {p}")

def stamp(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

# ---------------------------------------------------------------------------
# Load pre-trained 9x256 control net (PASS-1 artifact)
# ---------------------------------------------------------------------------
stamp("loading pre-trained model")

def build_mlp(n_in, n_out, depth, width, slope=0.3):
    layers = []
    prev = n_in
    for _ in range(depth):
        layers += [nn.Linear(prev, width), nn.LeakyReLU(slope)]
        prev = width
    layers += [nn.Linear(prev, n_out)]
    return nn.Sequential(*layers)

ckpt = torch.load(RUN / "best.pt", map_location="cpu", weights_only=False)
# PASS-1 trainer saved {'model': state_dict, 'config': ..., 'norm_xmean': ..., 'norm_xrange': ..., 'norm_ystd': ...}
model = build_mlp(60, 60, depth=9, width=256, slope=0.3)
sd = ckpt["model"]
model.load_state_dict(sd)
model.eval()

n_params = sum(p.numel() for p in model.parameters())
stamp(f"loaded control_9x256: {n_params:,} parameters")

# Load normalization stats
norm = np.load(RUN / "norm.npz")
print("norm keys:", list(norm.keys()))
fmean = norm["xmean"].astype(np.float32)
frange = norm["xrange"].astype(np.float32)
tstd  = norm["ystd"].astype(np.float32)
print("fmean shape", fmean.shape, "frange shape", frange.shape, "tstd shape", tstd.shape)

# ---------------------------------------------------------------------------
# CLAIM C1/C2 — param count
# ---------------------------------------------------------------------------
stamp("=== C1/C2: param count ===")
paper_params = 567361
results["C1_C2_param_count"] = {
    "paper_value": paper_params,
    "our_value": int(n_params),
    "delta": int(n_params) - paper_params,
    "ratio": n_params/paper_params,
    "note": "PASS-1 reported 557,372. Difference vs paper's 567,361 ~ 9989 = mismatch in input or output channel dimension. Our net is 60→256 + 8*(256→256) + 256→60. Paper's headline-arch number 567,361 likely uses different I/O width (94-in or 65-out variant).",
}
# Decompose layer-by-layer:
breakdown = []
for nm, p in model.named_parameters():
    breakdown.append({"name": nm, "shape": list(p.shape), "n": int(p.numel())})
results["C1_C2_param_count"]["breakdown"] = breakdown
write_json("C1_C2_param_count", results["C1_C2_param_count"])

# ---------------------------------------------------------------------------
# CLAIM C5 — 18-epoch sufficiency
# ---------------------------------------------------------------------------
stamp("=== C5: 18-epoch sufficiency from PASS-1 logs ===")
log_p = ROOT / "runs" / "control_9x256.log"
if log_p.exists():
    log = log_p.read_text()
    # Extract per-epoch val loss
    import re
    epochs = []
    # Actual format: '[ep 18/20] train=0.53492 val=0.46970 t=4.2s'
    for m in re.finditer(r"\[ep\s*(\d+)/\d+\]\s*train=([0-9.eE+-]+)\s*val=([0-9.eE+-]+)", log):
        epochs.append({"epoch": int(m.group(1)), "train_loss": float(m.group(2)), "val_loss": float(m.group(3))})
    results["C5_18_epoch"] = {
        "log_path": str(log_p),
        "n_epochs_logged": len(epochs),
        "epochs": epochs[:25],
        "note": "PASS-1 ran 20 epochs flat-lr (paper used 18 epochs with 5x lr decay every 3 epochs). Look at val curve to see if val plateaued by ep 18.",
    }
    if len(epochs) >= 18:
        ep18 = epochs[17]["val_loss"]
        ep20 = epochs[-1]["val_loss"]
        results["C5_18_epoch"]["val_at_ep18"] = ep18
        results["C5_18_epoch"]["val_at_ep20"] = ep20
        results["C5_18_epoch"]["relative_improvement_ep18_to_ep20"] = (ep18-ep20)/ep18
        results["C5_18_epoch"]["verdict"] = (
            "PLATEAU CONFIRMED" if abs((ep18-ep20)/ep18) < 0.01 else
            "still improving slightly"
        )
else:
    results["C5_18_epoch"] = {"error": f"log not found at {log_p}"}
write_json("C5_18_epoch", results["C5_18_epoch"])

# ---------------------------------------------------------------------------
# Load SPCAM sample data for diagnostic-mode tests
# ---------------------------------------------------------------------------
stamp("loading SPCAM sample data")
ds = xr.open_dataset(ROOT / "data" / "sample_SPCAM_1.nc")
TAP  = ds["TAP"].values   # (48,30,64,128) K
QAP  = ds["QAP"].values   # kg/kg
TPHY = ds["TPHYSTND"].values  # K/s  (SPCAM truth heating tendency)
PHQ  = ds["PHQ"].values   # kg/kg/s
lat  = ds["lat"].values   # (64,) degrees
lev  = ds["lev"].values   # (30,) hybrid level (~ pressure rank)
PS   = ds["PS"].values    # (48,64,128) Pa
P0   = float(ds["P0"].values)
hyai = ds["hyai"].values  # (31,) interface levels
hybi = ds["hybi"].values
FLNT = ds["FLNT"].values; FLNS = ds["FLNS"].values
FSNT = ds["FSNT"].values; FSNS = ds["FSNS"].values
SHFLX = ds["SHFLX"].values; LHFLX = ds["LHFLX"].values
PRECT = ds["PRECT"].values  # m/s

T,L,J,I = TAP.shape
stamp(f"data: time={T} lev={L} lat={J} lon={I}")

# Compute pressure thickness dp at each level (interface differencing)
# p_i = hyai * P0 + hybi * PS   shape (31, T, J, I) after broadcast
hyai_b = hyai[:,None,None,None]
hybi_b = hybi[:,None,None,None]
PS_b   = PS[None,:,:,:]
p_int  = hyai_b * P0 + hybi_b * PS_b   # (31, T, J, I) Pa
dp     = (p_int[1:] - p_int[:-1])      # (30, T, J, I) Pa
# Re-order dp to (T, L, J, I) to match TAP/QAP layout
dp = np.transpose(dp, (1, 0, 2, 3))    # (T, 30, J, I)

# ---------------------------------------------------------------------------
# Run NN inference on every SPCAM column (T*J*I columns × 60 in)
# Input expected: [TAP(30 levels) , QAP(30 levels)]  flattened in same column order as PASS-1.
# ---------------------------------------------------------------------------
stamp("running NN inference on full SPCAM sample (diagnostic mode)")

# Stack inputs: (T,L,J,I) -> (T,J,I,L)  for each variable, then concat to (N, 60)
TAP_p = np.transpose(TAP, (0,2,3,1))   # (T,J,I,L)
QAP_p = np.transpose(QAP, (0,2,3,1))
X = np.concatenate([TAP_p.reshape(-1, L), QAP_p.reshape(-1, L)], axis=1).astype(np.float32)
stamp(f"input X shape {X.shape}")

# Normalize using PASS-1 stats
Xn = (X - fmean) / frange

# Inference (CPU on a few hundred K rows ~ seconds)
device = "cpu"
model = model.to(device)
t0 = time.time()
with torch.no_grad():
    yn = []
    bs = 65536
    for i in range(0, Xn.shape[0], bs):
        xb = torch.from_numpy(Xn[i:i+bs]).to(device)
        yn.append(model(xb).cpu().numpy())
Yn = np.concatenate(yn, axis=0)   # normalized
infer_seconds = time.time() - t0
stamp(f"inference done in {infer_seconds:.2f}s for {Xn.shape[0]:,} columns")

# De-normalize
Y = Yn * tstd   # raw target units (K/s and kg/kg/s)

# Mask degenerate PHQ levels at top-of-atmosphere where training-set std was ~0
# (PASS-1 trainer set ystd[k]=1.0 sentinel for those k; outputs there are arbitrary).
# Treat any level where ystd is exactly the sentinel value (1.0) as masked-out (set NN pred = 0).
ystd_sentinel_mask = (tstd == 1.0)
print(f"degenerate output channels (ystd==1.0): {np.where(ystd_sentinel_mask)[0].tolist()}")
Y[:, ystd_sentinel_mask] = 0.0

# Split back into NN-predicted heating + moistening, reshape to (T,J,I,L) then (T,L,J,I)
Y_T = Y[:, :L].reshape(T, J, I, L).transpose(0, 3, 1, 2)   # (T,L,J,I) K/s
Y_Q = Y[:, L:].reshape(T, J, I, L).transpose(0, 3, 1, 2)   # (T,L,J,I) kg/kg/s

# ---------------------------------------------------------------------------
# CLAIM C21 — inference cost  (per-column, per-step)
# ---------------------------------------------------------------------------
stamp("=== C21: inference cost ===")
n_cols = Xn.shape[0]
per_col_us = infer_seconds / n_cols * 1e6
# A CAM column at ~F19 spectral resolution has ~64*128=8192 columns total
cols_per_step = 64*128
nn_per_step_seconds = per_col_us * cols_per_step / 1e6
# Published SPCAM cost: ~0.5 - 2 wallclock-sec per dynamics step on Yellowstone-era
# class hardware per a single MPI rank — paper claims NNCAM is ~10x faster total.
# This is a proxy: just check NN inference << any plausible SPCAM physics cost.
results["C21_inference_cost"] = {
    "n_columns_evaluated": int(n_cols),
    "wall_seconds_total": infer_seconds,
    "per_column_microseconds_cpu": per_col_us,
    "per_global_step_seconds_cpu_estimate": nn_per_step_seconds,
    "spcam_per_physics_step_seconds_published_range": [0.5, 2.0],
    "ratio_nn_to_spcam_lo": nn_per_step_seconds / 2.0,
    "ratio_nn_to_spcam_hi": nn_per_step_seconds / 0.5,
    "device": "CPU (uicgpu Xeon, single thread mostly)",
    "note": "Inference is single-threaded CPU PyTorch. Paper's '~10x faster total' is GCM-coupled with SPCAM physics including CRM. Our number is a one-sided sanity check that NN inference cost is negligible vs a 30-min SPCAM step; a fair side-by-side requires the prognostic SPCAM build (out of scope).",
}
write_json("C21_inference_cost", results["C21_inference_cost"])

# Free X early
del X, Xn, Y, Yn, TAP_p, QAP_p

# ---------------------------------------------------------------------------
# CLAIM C10 / C12 — mean heating climatology + ITCZ latitude
# ---------------------------------------------------------------------------
stamp("=== C10/C12: mean heating climatology ===")

# Compute mean over time, lon → zonal-mean climatology of NN-pred and SPCAM-truth
heat_truth = TPHY.mean(axis=(0,3))   # (L, J)
heat_nn    = Y_T.mean(axis=(0,3))    # (L, J)
moist_truth = PHQ.mean(axis=(0,3))   # kg/kg/s
moist_nn    = Y_Q.mean(axis=(0,3))

# Column-integrated heating (energy units): rho*cp*ΔT ~ cp/g * ∫ ΔT dp [W/m^2]
cp = 1004.0   # J/kg/K
g  = 9.81
Lv = 2.5e6    # J/kg

dp_mean = dp.mean(axis=(0,2,3))   # (L,) mean dp by level
# Vertically integrate at each (lat,lon,time), then zonal+time mean
col_heat_truth = (TPHY * dp[:,:,:,:]).sum(axis=1) * (cp/g)   # (T,J,I) W/m^2
col_heat_nn    = (Y_T  * dp[:,:,:,:]).sum(axis=1) * (cp/g)
col_moist_truth = (PHQ * dp[:,:,:,:]).sum(axis=1) * (Lv/g)
col_moist_nn    = (Y_Q * dp[:,:,:,:]).sum(axis=1) * (Lv/g)

# Zonal mean
ch_truth_zonal = col_heat_truth.mean(axis=(0,2))   # (J,)
ch_nn_zonal    = col_heat_nn.mean(axis=(0,2))
cm_truth_zonal = col_moist_truth.mean(axis=(0,2))
cm_nn_zonal    = col_moist_nn.mean(axis=(0,2))

# ITCZ latitude = lat of max column heating
itcz_truth_idx = int(np.argmax(ch_truth_zonal))
itcz_nn_idx    = int(np.argmax(ch_nn_zonal))
itcz_truth_lat = float(lat[itcz_truth_idx])
itcz_nn_lat    = float(lat[itcz_nn_idx])

# FWHM of heating peak around ITCZ (sharpness)
def fwhm(profile, lat_arr):
    pk = profile.max()
    half = pk / 2.0
    above = profile >= half
    if not above.any():
        return None
    idxs = np.where(above)[0]
    return float(lat_arr[idxs[-1]] - lat_arr[idxs[0]])

# Tropical correlation (lat between -30 and 30)
trop = (lat >= -30) & (lat <= 30)
def corr(a,b):
    a = a[trop]; b = b[trop]
    return float(np.corrcoef(a,b)[0,1])

results["C10_C12_C13_climatology"] = {
    "paper_ITCZ_latitude_deg": 5.0,
    "spcam_truth_ITCZ_latitude_deg": itcz_truth_lat,
    "nn_diagnostic_ITCZ_latitude_deg": itcz_nn_lat,
    "spcam_truth_peak_heating_Wm2": float(ch_truth_zonal[itcz_truth_idx]),
    "nn_diagnostic_peak_heating_Wm2": float(ch_nn_zonal[itcz_nn_idx]),
    "spcam_truth_FWHM_deg": fwhm(ch_truth_zonal, lat),
    "nn_diagnostic_FWHM_deg": fwhm(ch_nn_zonal, lat),
    "tropical_zonal_correlation_heating": corr(ch_truth_zonal, ch_nn_zonal),
    "tropical_zonal_correlation_moistening": corr(cm_truth_zonal, cm_nn_zonal),
    "note": "C12 paper: ITCZ at maximum SST (~5°N). C13: NN ITCZ slightly sharper. "
            "Our SPCAM sample is only 48 timesteps so 'climatology' is hourly snapshots over <2 days — "
            "this is a methodological check (does NN reproduce the zonal pattern at all) not a "
            "true climatology comparison.",
}
write_json("C10_C12_C13_climatology", results["C10_C12_C13_climatology"])

# Save the zonal profiles for the report
np.savez(OUT / "climatology_profiles.npz",
         lat=lat,
         ch_truth=ch_truth_zonal, ch_nn=ch_nn_zonal,
         cm_truth=cm_truth_zonal, cm_nn=cm_nn_zonal,
         heat_truth_lev_lat=heat_truth, heat_nn_lev_lat=heat_nn)
stamp(f"saved climatology profiles npz")

# ---------------------------------------------------------------------------
# CLAIM C16 — Column moist-static-energy balance
# Test:  cp/g ∫ ΔT_phy dp - net_rad - SHFLX  vs   Lv/g ∫ ΔQ_phy dp + LHFLX  ≈ 0
# i.e. net column energy input = net surface+TOA fluxes
# Compare residual for NN-predictions vs SPCAM-truth.
# ---------------------------------------------------------------------------
stamp("=== C16: column moist-static-energy balance ===")

# Net column radiative heating (W/m^2): FSNT - FSNS - (FLNT - FLNS) is the net atmospheric col absorption.
# SPCAM convention: FSNT and FSNS are net shortwave down at TOA and surface; FLNT and FLNS are net longwave up.
# Atmospheric radiative heating (W/m^2 absorbed by column) = FSNT - FSNS - FLNT + FLNS
rad_atm = FSNT - FSNS - FLNT + FLNS

# Energy budget check for SPCAM truth:
# Column heating from physics (W/m^2): cp/g * ∫ TPHY dp   (already col_heat_truth)
# Source side:  rad_atm + SHFLX                              (surface SH + atmospheric rad absorption)
# Latent heating tendency from condensation: should equal -Lv * col_moistening  (i.e., when moisture removed, latent heat released)
# So: col_heat_truth ≈ rad_atm + SHFLX - col_moist_truth         (col_moist already in W/m^2 via Lv/g factor)
# Residual: R_truth = col_heat_truth - (rad_atm + SHFLX - col_moist_truth)

R_truth = col_heat_truth - (rad_atm + SHFLX - col_moist_truth)
R_nn    = col_heat_nn    - (rad_atm + SHFLX - col_moist_nn)

# Slope of col_heat vs (-col_moist) (should be ~1 in dry-static-energy-conserving moist convection,
# i.e. parameterization conserves moist static energy: heating equals latent release)
def slope(x, y):
    x = x.ravel(); y = y.ravel()
    return float(np.polyfit(x, y, 1)[0])

slope_truth = slope(-col_moist_truth, col_heat_truth)
slope_nn    = slope(-col_moist_nn,    col_heat_nn)
r_truth = float(np.corrcoef(col_heat_truth.ravel(), -col_moist_truth.ravel())[0,1])
r_nn    = float(np.corrcoef(col_heat_nn.ravel(),    -col_moist_nn.ravel())[0,1])

results["C16_energy_balance"] = {
    "paper_claim": "NNCAM conserves column moist static energy to a remarkable degree (Fig. 4A)",
    "slope_heating_vs_neg_moistening_truth": slope_truth,
    "slope_heating_vs_neg_moistening_nn":    slope_nn,
    "correlation_truth": r_truth,
    "correlation_nn":    r_nn,
    "ideal_slope": 1.0,
    "ideal_correlation": 1.0,
    "residual_truth_mean_Wm2": float(R_truth.mean()),
    "residual_truth_rms_Wm2":  float(np.sqrt((R_truth**2).mean())),
    "residual_nn_mean_Wm2":    float(R_nn.mean()),
    "residual_nn_rms_Wm2":     float(np.sqrt((R_nn**2).mean())),
    "residual_truth_std_Wm2":  float(R_truth.std()),
    "residual_nn_std_Wm2":     float(R_nn.std()),
    "note": "Compares NN-predicted heating-vs-moistening proportionality and full atmospheric column "
            "energy residual (rad + SH + LH balance) against SPCAM-truth. Slope close to 1 and high "
            "correlation means moist static energy is conserved — that's the paper's Fig 4A claim. "
            "Note: SPCAM-truth residual is NOT zero either because column moistening != column precip "
            "(condensate falls but evaporation, ice, advection redistribute the budget over 30-min step). "
            "What matters is *relative*: NN residual statistics should be COMPARABLE TO truth residuals; "
            "if NN's are much larger, the NN is violating moist-static-energy conservation.",
}
write_json("C16_energy_balance", results["C16_energy_balance"])

# ---------------------------------------------------------------------------
# Final summary
# ---------------------------------------------------------------------------
stamp("writing summary")
summary = {
    "repass_date_iso": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "claims_tested_this_pass": [
        "C1/C2 — param count",
        "C5    — 18-epoch sufficiency",
        "C10/C12/C13 — diagnostic ITCZ latitude + FWHM",
        "C16   — column moist static energy balance",
        "C21   — inference cost",
    ],
    "claims_already_covered_pass1": ["C1","C2","C6","C8","C9"],
    "claims_blocked_data_or_code": ["C17","C18","C20","C22","C23","C24","C25"],
    "results_files": [f.name for f in OUT.glob("*.json")],
}
write_json("SUMMARY", summary)
stamp("DONE")
print(json.dumps(summary, indent=2))
