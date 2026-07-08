import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
d=json.load(open('results.json'))
fig,ax=plt.subplots(1,2,figsize=(11,4.2))
# left: Var vs N (measured) log scale
vv=d['runs']['var_vs_N']['data']
N=[x['N'] for x in vv]; V=[x['var'] for x in vv]
ax[0].semilogy(N,V,'o-',label='measured Var[grad]')
fit=d['runs']['var_vs_N']['fit_lnVar_vs_N']
Nx=np.array(N); ax[0].semilogy(Nx,np.exp(fit['slope']*Nx+fit['intercept']),'--',
    label=f"exp fit c={1/fit['factor_per_qubit']:.2f}, R2={fit['r2']:.3f}")
ax[0].set_xlabel('qubit count N'); ax[0].set_ylabel('Var[dH/dtheta]')
ax[0].set_title('C2: Barren plateau — Var decays exp. in N'); ax[0].legend(); ax[0].grid(True,alpha=.3)
# right: projected qMPS vs qTTN
pj=d['runs']['projection']
Nm=[x['N'] for x in pj['qmps']]; Vm=[x['var_proj'] for x in pj['qmps']]
Nt=[x['N'] for x in pj['qttn']]; Vt=[x['var_proj'] for x in pj['qttn']]
ax[1].semilogy(Nm,Vm,'s-',label='qMPS (dist~N) exp decay')
ax[1].semilogy(Nt,Vt,'^-',label=f"qTTN (dist~logN) poly N^{pj['qttn_lnVar_vs_lnN']['exponent']:.2f}")
ax[1].set_xlabel('qubit count N'); ax[1].set_ylabel('projected Var[grad]')
ax[1].set_title('C3/C4: qMPS barren vs qTTN trainable'); ax[1].legend(); ax[1].grid(True,alpha=.3)
plt.tight_layout(); plt.savefig('bp_figures.png',dpi=110)
print('saved bp_figures.png')
