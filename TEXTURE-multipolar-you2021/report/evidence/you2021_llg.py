#!/usr/bin/env python3
"""
Macrospin LLG replication of You et al. (2021):
"Cluster magnetic octupole induced out-of-plane spin polarization in
antiperovskite antiferromagnet Mn3SnN" -- field-free deterministic SOT
switching of an adjacent perpendicular ferromagnet (Co/Pd).

CORE THEORY CLAIM (Fig.4c, Eq.1, torque decomposition p.9):
  Out-of-plane spin polarization sigma_z (in addition to sigma_y) is generated
  when current J // cluster octupole T; it produces
     tau_B ~ m x sigma_z            (field-like)         theta_FL,z = 0.053
     tau_C ~ m x (m x sigma_z)      (antidamping)        theta_AD,z = 0.003
  The tau_C (antidamping, sigma_z) term breaks the up/down degeneracy of a
  PMA magnet WITHOUT any external field -> DETERMINISTIC field-free switching,
  with polarity set by the sign of the current.
  When J _|_ T, sigma_z vanishes (only sigma_y remains) -> NO deterministic
  field-free switching (needs external H, as in conventional SOT).

We reproduce this qualitatively/semi-quantitatively with a single-macrospin
LLG integration. No external field anywhere.

Units: dimensionless / reduced. m is a unit vector. Fields in units of the
anisotropy field H_k. Time in units of 1/(gamma H_k). Torque terms enter as
effective fields h_DL, h_FL scaled by current.
"""
import json, math, os, sys
import numpy as np

def cross(a, b):
    return np.array([a[1]*b[2]-a[2]*b[1],
                     a[2]*b[0]-a[0]*b[2],
                     a[0]*b[1]-a[1]*b[0]])

def llg_rhs(m, h_eff, damp, tau_dl, tau_fl, p):
    """
    m: unit magnetization
    h_eff: conservative effective field (anisotropy) in reduced units
    damp: Gilbert alpha
    tau_dl: damping-like coefficient (antidamping SOT), polarization p
    tau_fl: field-like coefficient, polarization p
    Landau-Lifshitz form:
      dm/dt = -m x H_tot + alpha m x dm/dt  (implicit); we use explicit LL:
      dm/dt = -(m x H) - alpha m x (m x H) + tau_DL m x(m x p) + tau_FL m x p
    """
    H = h_eff.copy()
    # precession + Gilbert damping about conservative field
    mxH = cross(m, H)
    dm = -mxH - damp*cross(m, mxH)
    # SOT: damping-like (antidamping) tau_DL * m x (m x p)
    dm += tau_dl*cross(m, cross(m, p))
    # SOT: field-like tau_FL * (m x p)
    dm += tau_fl*cross(m, p)
    return dm

def anisotropy_field(m, hk=1.0):
    # uniaxial PMA along z: E = -0.5 hk mz^2 -> H = hk mz zhat
    return np.array([0.0, 0.0, hk*m[2]])

def integrate(m0, p, tau_dl, tau_fl, damp=0.1, hk=1.0,
              dt=0.02, nsteps=8000, pulse_frac=0.6):
    """RK4 integrate LLG. Current pulse ON for first pulse_frac of time,
    then OFF (relax) to test whether the final state is deterministic."""
    m = np.array(m0, float); m /= np.linalg.norm(m)
    npulse = int(nsteps*pulse_frac)
    traj_z = np.empty(nsteps+1); traj_z[0] = m[2]
    for i in range(nsteps):
        on = 1.0 if i < npulse else 0.0
        td = tau_dl*on; tf = tau_fl*on
        def f(mm):
            return llg_rhs(mm, anisotropy_field(mm, hk), damp, td, tf, p)
        k1 = f(m)
        k2 = f(m+0.5*dt*k1)
        k3 = f(m+0.5*dt*k2)
        k4 = f(m+dt*k3)
        m = m + (dt/6.0)*(k1+2*k2+2*k3+k4)
        m /= np.linalg.norm(m)
        traj_z[i+1] = m[2]
    return m, traj_z

def final_state(m):
    return "up" if m[2] > 0 else "down"

def main():
    outdir = "/home/stevens/textures-100/corpus/textures-multipolar-you2021/work"
    # Reduced-unit torque strengths. Ratio FL/AD ~ 0.053/0.003 ~ 17.7 from paper.
    # We scale to reduced units where antidamping must exceed damping*hk to switch.
    # Use current-scaled amplitudes chosen so J//T (sigma_z present) switches.
    theta_ad_z = 0.003
    theta_fl_z = 0.053
    # Effective reduced coefficients: multiply by a current-strength factor C so
    # that antidamping-like sigma_z torque is strong enough to overcome damping.
    C = 30.0   # current strength (reduced); a single value tested both polarities
    results = {}

    # ---- Case A: J // T  => sigma_z present (p has strong z-component) ----
    # sigma_z dominant polarization (out-of-plane). Also small sigma_y.
    p_z_pos = np.array([0.0, 0.2, 1.0]); p_z_pos /= np.linalg.norm(p_z_pos)
    p_z_neg = -p_z_pos
    caseA = {}
    for init in ("up","down"):
        m0 = [0.01,0.0, 1.0] if init=="up" else [0.01,0.0,-1.0]
        # positive current
        mf_pos,_ = integrate(m0, p_z_pos, C*theta_ad_z, C*theta_fl_z)
        mf_neg,tz = integrate(m0, p_z_neg, C*theta_ad_z, C*theta_fl_z)
        caseA[init] = {"I_pos_final": final_state(mf_pos),
                       "I_pos_mz": round(float(mf_pos[2]),4),
                       "I_neg_final": final_state(mf_neg),
                       "I_neg_mz": round(float(mf_neg[2]),4)}
    # determinism: for +I both inits -> same state; for -I both inits -> same (opposite) state
    detA = (caseA["up"]["I_pos_final"]==caseA["down"]["I_pos_final"] and
            caseA["up"]["I_neg_final"]==caseA["down"]["I_neg_final"] and
            caseA["up"]["I_pos_final"]!=caseA["up"]["I_neg_final"])

    # ---- Case B: J _|_ T => sigma_z vanishes, only sigma_y (in-plane) ----
    p_y = np.array([0.0,1.0,0.0])
    caseB = {}
    for init in ("up","down"):
        m0 = [0.01,0.0, 1.0] if init=="up" else [0.01,0.0,-1.0]
        mf_pos,_ = integrate(m0, p_y, C*theta_ad_z, C*theta_fl_z)
        mf_neg,_ = integrate(m0, -p_y, C*theta_ad_z, C*theta_fl_z)
        caseB[init] = {"I_pos_final": final_state(mf_pos),
                       "I_pos_mz": round(float(mf_pos[2]),4),
                       "I_neg_final": final_state(mf_neg),
                       "I_neg_mz": round(float(mf_neg[2]),4)}
    detB = (caseB["up"]["I_pos_final"]==caseB["down"]["I_pos_final"] and
            caseB["up"]["I_neg_final"]==caseB["down"]["I_neg_final"] and
            caseB["up"]["I_pos_final"]!=caseB["up"]["I_neg_final"])

    # ---- Critical current sweep for Case A (find threshold) ----
    Csweep = []
    for Ctry in np.linspace(2,40,20):
        m0=[0.01,0,1.0]
        mfp,_=integrate(m0,p_z_pos,Ctry*theta_ad_z,Ctry*theta_fl_z)
        mfn,_=integrate(m0,p_z_neg,Ctry*theta_ad_z,Ctry*theta_fl_z)
        switched = (final_state(mfp)!=final_state(mfn))
        Csweep.append({"C":round(float(Ctry),2),"deterministic":bool(switched)})
    Ccrit = next((s["C"] for s in Csweep if s["deterministic"]), None)

    results = {
        "paper":"You et al. 2021, Mn3SnN cluster octupole sigma_z field-free SOT switching",
        "model":"single-macrospin LLG (RK4), reduced units, PMA along z, no external field",
        "torque_model":{
            "conservative":"uniaxial anisotropy H = hk*mz zhat (hk=1)",
            "antidamping_SOT":"tau_DL * m x (m x p)",
            "field_like_SOT":"tau_FL * m x p",
            "theta_AD_z_paper":theta_ad_z,"theta_FL_z_paper":theta_fl_z,
            "current_strength_C":C,"gilbert_alpha":0.1},
        "caseA_J_parallel_T_sigma_z_present":{
            "polarization_p":[round(float(x),3) for x in p_z_pos],
            "per_init":caseA,"deterministic_field_free_switching":bool(detA)},
        "caseB_J_perp_T_sigma_z_absent":{
            "polarization_p":[round(float(x),3) for x in p_y],
            "per_init":caseB,"deterministic_field_free_switching":bool(detB)},
        "critical_current_sweep":Csweep,
        "critical_C_for_determinism":Ccrit,
        "claim":"sigma_z (J//T) enables deterministic field-free switching; polarity set by current sign; J_perp_T (sigma_z absent) does NOT.",
        "verdict_local":("SUPPORTS claim: deterministic field-free switching ONLY with sigma_z (Case A), not Case B"
                         if (detA and not detB) else
                         "DOES NOT cleanly reproduce claim")
    }
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir,"you2021_result.json"),"w") as fh:
        json.dump(results, fh, indent=2)
    print(json.dumps(results, indent=2))

if __name__=="__main__":
    main()
