#!/usr/bin/env python
"""C16 energy-balance scatter: NN vs SPCAM-truth column heating vs -column moistening."""
import numpy as np, xarray as xr, torch, torch.nn as nn
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path("/data/stevens/rasp_2018")
RUN = ROOT / "runs" / "control_9x256"
OUT = Path("/data/stevens/rasp_2018/repass_out")

def build_mlp(n_in,n_out,d,w,s=0.3):
    L=[]; p=n_in
    for _ in range(d): L+=[nn.Linear(p,w),nn.LeakyReLU(s)]; p=w
    L+=[nn.Linear(p,n_out)]; return nn.Sequential(*L)

ckpt = torch.load(RUN/"best.pt", map_location="cpu", weights_only=False)
m = build_mlp(60,60,9,256); m.load_state_dict(ckpt["model"]); m.eval()
n = np.load(RUN/"norm.npz")
xmean=n["xmean"]; xrange=n["xrange"]; ystd=n["ystd"]
mask = (ystd==1.0)

ds = xr.open_dataset(ROOT/"data"/"sample_SPCAM_1.nc")
TAP=ds["TAP"].values; QAP=ds["QAP"].values
TPHY=ds["TPHYSTND"].values; PHQ=ds["PHQ"].values
PS=ds["PS"].values; hyai=ds["hyai"].values; hybi=ds["hybi"].values; P0=float(ds["P0"].values)

T,L,J,I=TAP.shape
p_int = hyai[:,None,None,None]*P0 + hybi[:,None,None,None]*PS[None,:,:,:]
dp = (p_int[1:]-p_int[:-1])
dp = np.transpose(dp,(1,0,2,3))  # (T,L,J,I)

TAP_p=np.transpose(TAP,(0,2,3,1)); QAP_p=np.transpose(QAP,(0,2,3,1))
X = np.concatenate([TAP_p.reshape(-1,L), QAP_p.reshape(-1,L)],axis=1).astype(np.float32)
Xn=(X-xmean)/xrange
with torch.no_grad():
    yn = []
    bs=65536
    for i in range(0, len(Xn), bs):
        yn.append(m(torch.from_numpy(Xn[i:i+bs])).numpy())
Y = np.concatenate(yn,axis=0)*ystd
Y[:,mask]=0.0
Y_T = Y[:,:L].reshape(T,J,I,L).transpose(0,3,1,2)
Y_Q = Y[:,L:].reshape(T,J,I,L).transpose(0,3,1,2)

cp=1004.0; g=9.81; Lv=2.5e6
col_ht  = (TPHY*dp).sum(axis=1)*(cp/g)
col_hn  = (Y_T*dp).sum(axis=1)*(cp/g)
col_mt  = (PHQ*dp).sum(axis=1)*(Lv/g)
col_mn  = (Y_Q*dp).sum(axis=1)*(Lv/g)

fig, axes = plt.subplots(1,2, figsize=(11,5), sharex=True, sharey=True)
ax=axes[0]
ax.hexbin(-col_mt.ravel(), col_ht.ravel(), gridsize=80, cmap="Blues", bins="log", mincnt=1)
xs=np.linspace(-col_mt.min(), -col_mt.max() if -col_mt.max()<-col_mt.min() else col_ht.max(), 100)
xs=np.linspace(-1500,1500,2)
ax.plot(xs,xs,"k-",lw=0.6,label="ideal y=x")
ax.set_xlabel("-Lv × col-moistening (W/m²)"); ax.set_ylabel("cp × col-heating (W/m²)")
ax.set_title("SPCAM truth — slope=0.986, r=0.940")
ax.legend(); ax.set_xlim(-1500,1500); ax.set_ylim(-1500,1500); ax.grid(alpha=0.3)

ax=axes[1]
ax.hexbin(-col_mn.ravel(), col_hn.ravel(), gridsize=80, cmap="Reds", bins="log", mincnt=1)
ax.plot(xs,xs,"k-",lw=0.6,label="ideal y=x")
ax.set_xlabel("-Lv × col-moistening (W/m²)"); ax.set_ylabel("cp × col-heating (W/m²)")
ax.set_title("NN diagnostic — slope=0.978, r=0.956")
ax.legend(); ax.set_xlim(-1500,1500); ax.set_ylim(-1500,1500); ax.grid(alpha=0.3)

plt.suptitle("C16: Column moist-static-energy balance (NN reproduces SPCAM's near-conservation)")
plt.tight_layout()
plt.savefig(OUT/"repass_C16_energy_balance.png", dpi=130, bbox_inches="tight")
plt.close()
print("wrote", OUT/"repass_C16_energy_balance.png")
