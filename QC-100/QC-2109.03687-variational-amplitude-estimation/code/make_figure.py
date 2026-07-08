"""Reproduce a mini version of Fig. 4 of arXiv:2109.03687."""

import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
EV = os.path.abspath(os.path.join(HERE, "..", "report", "evidence"))
with open(os.path.join(EV, "experiment_results.json")) as fh:
    R = json.load(fh)

fig, ax = plt.subplots(figsize=(6.5, 5.0))

mc_Nq   = [r["Nq"] for r in R["classical_mc"]]
mc_err  = [r["median_dtheta"] for r in R["classical_mc"]]
ax.loglog(mc_Nq, mc_err, "o-", color="tab:blue", label="Classical MC (this work)")

mlae_Nq  = [r["Nq"] for r in R["mlae_linear"]]
mlae_err = [r["median_dtheta"] for r in R["mlae_linear"]]
ax.loglog(mlae_Nq, mlae_err, "s-", color="tab:orange", label="MLAE linear (this work)")

vq_Nq  = [r["Nq_samp"] for r in R["naive_vqae_k1_d3"]]
vq_err = [r["median_dtheta"] for r in R["naive_vqae_k1_d3"]]
ax.loglog(vq_Nq, vq_err, "D-", color="tab:red", label="Naïve VQAE k=1, d=3 (this work)")

# reference lines
Nq_ref = np.logspace(2, 6, 40)
c_mc   = mc_err[3] / (mc_Nq[3] ** -0.5)
c_mlae = mlae_err[3] / (mlae_Nq[3] ** -0.75)
ax.loglog(Nq_ref, c_mc * Nq_ref ** -0.5, ":", color="tab:blue",
          alpha=0.6, label="slope -1/2 (paper: MC)")
ax.loglog(Nq_ref, c_mlae * Nq_ref ** -0.75, "--", color="tab:orange",
          alpha=0.6, label="slope -3/4 (paper: MLAE linear)")

ax.set_xlabel("Number of queries $N_q$")
ax.set_ylabel(r"Amplitude estimation error $\delta\theta$")
ax.set_title(
    "Replication of Fig. 4 (arXiv:2109.03687)\n"
    "Cauchy-Lorentz $p(x)$ on $n=4$ qubits, $f(x)=x$"
)
ax.legend(fontsize=8, loc="lower left")
ax.grid(True, which="both", alpha=0.3)
plt.tight_layout()
out = os.path.join(EV, "fig4_replication.png")
plt.savefig(out, dpi=150)
print("wrote", out)
