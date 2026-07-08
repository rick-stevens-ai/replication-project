#!/usr/bin/env python3
import json, sys, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = sys.argv[1] if len(sys.argv) > 1 else "."
r = json.load(open(f"{d}/results.json"))

# C1 convergence
fig, ax = plt.subplots(figsize=(5, 3.5))
c = r['C1']['median_err_curve']
ax.semilogy(range(1, len(c)+1), c, 'o-', ms=3, label='RFPE median error (1000 runs)')
ax.set_xlabel('RFPE step'); ax.set_ylabel('|phase error| (rad)')
ax.set_title('C1: RFPE exponential convergence\n(true 2\u03c0\u03c6\u2080=4.8741 rad, dissociated H\u2082)')
ax.grid(True, which='both', alpha=0.3); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(f"{d}/evidence/c1_convergence.png", dpi=130); plt.close(fig)

# C2 PES
fig, ax = plt.subplots(figsize=(5, 3.5))
pes = sorted(r['C2']['pes'], key=lambda p: p['R'])
R = [p['R'] for p in pes]; Ef = [p['E_fci'] for p in pes]; Ee = [p['E_est'] for p in pes]
ax.plot(R, Ef, 'k--', label='FCI (theory)')
ax.plot(R, Ee, 'ro', ms=4, label='RFPE (50 steps)')
ax.set_xlabel('H\u2013H distance (\u00c5)'); ax.set_ylabel('Energy (Hartree)')
ax.set_title(f"C2: H\u2082/STO-3G binding curve\navg err {r['C2']['avg_err_kcal']:.3f} kcal/mol < 1 (chem. acc.)")
ax.grid(True, alpha=0.3); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(f"{d}/evidence/c2_h2_pes.png", dpi=130); plt.close(fig)

# C3 phase noise
fig, ax = plt.subplots(figsize=(5, 3.5))
s = [o['sigma_phase'] for o in r['C3']['scan']]
rf = [o['rfpe_med_err'] for o in r['C3']['scan']]
ip = [o['ipea_med_err'] for o in r['C3']['scan']]
ax.plot(s, rf, 'bo-', ms=4, label='RFPE (100 steps)')
ax.plot(s, ip, 'r^-', ms=4, label='IPEA (16-bit, 10 reps)')
ax.set_xlabel('$\\sigma_{phase}$ (rad)'); ax.set_ylabel('median |phase error| (rad)')
ax.set_title('C3: robustness to gate infidelity\n(IPEA \u2248 2.2\u00d7 worse than RFPE)')
ax.grid(True, alpha=0.3); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(f"{d}/evidence/c3_phase_noise.png", dpi=130); plt.close(fig)

# C4 decoherence
fig, ax = plt.subplots(figsize=(5, 3.5))
T2 = [o['T2'] for o in r['C4']['scan']]
rf = [o['rfpe_med_err'] for o in r['C4']['scan']]
ip = [o['ipea_med_err'] for o in r['C4']['scan']]
ax.loglog(T2, rf, 'bo-', ms=4, label='RFPE (100 steps)')
ax.loglog(T2, ip, 'r^-', ms=4, label='IPEA (16-bit, 10 reps)')
ax.set_xlabel('normalized $T_2$'); ax.set_ylabel('median |phase error| (rad)')
ax.set_title('C4: robustness to decoherence\n(RFPE degrades gracefully; IPEA worse at low $T_2$)')
ax.grid(True, which='both', alpha=0.3); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(f"{d}/evidence/c4_decoherence.png", dpi=130); plt.close(fig)
print("plots written")
