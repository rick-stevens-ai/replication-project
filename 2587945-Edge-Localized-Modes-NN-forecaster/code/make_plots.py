"""Plot MSE vs lead time + a sample forecast."""
import json, sys, os, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
sys.path.insert(0, os.path.dirname(__file__))
from data import build_datasets
from models import ConstantBaseline, FNO2DForecaster, ConvLSTMSeq2Seq

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/results"
m = json.load(open(OUT+"/metrics.json"))

# 1) MSE vs lead time
plt.figure(figsize=(6,4))
for name,color in [("constant","gray"),("fno","C0"),("convlstm","C3")]:
    plt.plot(np.arange(1, len(m[name]["mse_per_step"])+1), m[name]["mse_per_step"], label=name, color=color)
plt.xlabel("lead step (µs)"); plt.ylabel("MSE"); plt.legend(); plt.title("MSE vs lead time")
plt.grid(alpha=.3); plt.tight_layout(); plt.savefig(OUT+"/mse_vs_lead.png", dpi=120)

# 2) Bar chart of metrics
fig, ax = plt.subplots(1,3, figsize=(12,3.2))
names=["constant","fno","convlstm"]
labels=["constant","FNO","ConvLSTM"]
for i,(metric,title) in enumerate([("rho_pred_mean","ρ_pred"),("rho_resid_mean","ρ_resid"),("onset_roc_auc","Onset ROC-AUC")]):
    vals=[m[n][metric] for n in names]
    ax[i].bar(labels, vals, color=["gray","C0","C3"])
    ax[i].set_title(title); ax[i].grid(alpha=.3, axis="y")
    for j,v in enumerate(vals): ax[i].text(j,v,f"{v:.3f}",ha="center",va="bottom",fontsize=9)
plt.tight_layout(); plt.savefig(OUT+"/metric_bars.png", dpi=120)

# 3) Sample forecast
device = "cuda" if torch.cuda.is_available() else "cpu"
_,_,test,_ = build_datasets(n_train=4,n_val=1,n_test=1,T=20000,delta=30,H=30,stride=80,max_per_shot=200)
hist, targ = test[10]
hist_b = hist.unsqueeze(0).to(device); targ_b = targ.unsqueeze(0).to(device)
fno = FNO2DForecaster(30,30,32,4,4).to(device); fno.load_state_dict(torch.load(OUT+"/fno.pt", map_location=device))
clstm = ConvLSTMSeq2Seq(30,30,32).to(device); clstm.load_state_dict(torch.load(OUT+"/convlstm.pt", map_location=device))
const = ConstantBaseline(30).to(device)
fno.eval(); clstm.eval()
with torch.no_grad():
    pf = fno(hist_b).cpu().numpy()[0]
    pc = clstm(hist_b).cpu().numpy()[0]
    pk = const(hist_b).cpu().numpy()[0]
tg = targ.numpy()
# Plot mean signal
fig,ax=plt.subplots(figsize=(8,4))
t_hist = np.arange(-30,0); t_fwd=np.arange(0,30)
ax.plot(t_hist, hist.numpy().mean(axis=(1,2)), "k-", label="history")
ax.plot(t_fwd, tg.mean(axis=(1,2)), "k--", label="truth")
ax.plot(t_fwd, pk.mean(axis=(1,2)), color="gray", label="constant")
ax.plot(t_fwd, pf.mean(axis=(1,2)), color="C0", label="FNO")
ax.plot(t_fwd, pc.mean(axis=(1,2)), color="C3", label="ConvLSTM")
ax.axvline(0,color="r",alpha=.3); ax.legend(); ax.set_xlabel("step (µs)"); ax.set_ylabel("mean BES intensity (norm)")
ax.set_title("Sample 30-step forecast (mean over 8x8 channels)")
ax.grid(alpha=.3); plt.tight_layout(); plt.savefig(OUT+"/sample_forecast.png", dpi=120)

print("Plots saved to", OUT)
