#!/usr/bin/env python3
"""
Replication of OSTI 1606674:
"Common-Mode Voltage Reduction of Single-Phase Quasi-Z-Source Inverter-Based
Photovoltaic System with Active Power Filtering"

This script:
  1. Generates SPWM + shoot-through gating for S1..S4 of the qZSI H-bridge
     under (a) traditional modulation and (b) the proposed modulation
     (ZS1 state replaced with ZS2).
  2. Derives the leg-to-ground voltages U10, U20 and common-mode voltage
     UCM = (U10 + U20) / 2 for each scheme.
  3. Uses PySpice + ngspice to simulate the common-mode equivalent circuit
     (Fig. 2(b) / Eq. 5-6 of the paper) driven by UCM(t) and records the
     leakage current iLK through the PV-to-ground stray capacitance Cg.
  4. Produces comparison plots (CMV waveforms, leakage current,
     FFT spectra) and prints quantitative metrics.

Author: Replication subagent (Ollie, OpenClaw)
"""

from __future__ import annotations

import os
import numpy as np
import matplotlib.pyplot as plt

try:
    from PySpice.Spice.Netlist import Circuit
    from PySpice.Unit import u_V, u_Ohm, u_F, u_H, u_s
    HAVE_PYSPICE = True
except Exception as e:  # pragma: no cover
    print(f"[WARN] PySpice import failed: {e}; falling back to scipy ODE")
    HAVE_PYSPICE = False

# ---------- circuit / modulation parameters (Table 4 of paper) ----------
V_PN        = 400.0       # dc-link peak (V)  [VPN]
F_GRID      = 50.0        # grid fundamental (Hz)
F_SW        = 10_000.0    # switching frequency (Hz)
M_INDEX     = 0.78        # modulation index
D_ST        = 0.125       # shoot-through duty
LF          = 3e-3        # grid-side filter inductor Lf (H)
RF          = 2.0         # ESR/damping of Lf (ohm) — assumed (Q~30 at fs)
CG          = 2.2e-9      # PV-to-ground stray capacitance (F) — typical small PV panel
RG          = 100.0       # CM ground return impedance (ohm) — includes CM choke damping
N_CYCLES    = 4           # grid cycles to simulate (4 @ 50 Hz = 80 ms)
FS_TIME     = 2_000_000.0 # time-grid sampling frequency (Hz) -> 0.5 us
OUT_DIR     = os.path.dirname(os.path.abspath(__file__))


# -----------------------------------------------------------------------
# 1.  PWM generation
# -----------------------------------------------------------------------
def build_pwm(proposed: bool):
    """Return (t, U10, U20, UCM, states) for the chosen scheme.

    Switching states in the qZSI H-bridge (legs 1 & 2):
        ACT1 : S1=S4=1, S2=S3=0   -> U10=VPN, U20=0       -> UCM=VPN/2
        ACT2 : S1=S4=0, S2=S3=1   -> U10=0,   U20=VPN     -> UCM=VPN/2
        ZS1  : S1=S3=1, S2=S4=0   -> U10=VPN, U20=VPN     -> UCM=VPN   (high CM)
        ZS2  : S1=S3=0, S2=S4=1   -> U10=0,   U20=0       -> UCM=0
        ST   : all on             -> both legs shorted    -> UCM=0

    Traditional unipolar SPWM uses ZS1 and ZS2 in alternate carrier
    half-cycles; the proposed method forces every ZS1 -> ZS2, clamping
    UCM to {0, VPN/2}.
    """
    Tgrid = 1.0 / F_GRID
    dt = 1.0 / FS_TIME
    t = np.arange(0.0, N_CYCLES * Tgrid, dt)
    n = t.size

    # Carrier (triangle, 0..1) and reference signals (unipolar SPWM: two refs
    # vr_a = +M sin(wt),  vr_b = -M sin(wt))
    car = np.abs(((t * F_SW) % 1.0) * 2.0 - 1.0)              # 0..1 triangle
    ref_a = 0.5 + 0.5 * M_INDEX * np.sin(2 * np.pi * F_GRID * t)
    ref_b = 0.5 - 0.5 * M_INDEX * np.sin(2 * np.pi * F_GRID * t)

    # Baseline (no shoot-through) leg switching
    # Leg 1: S1 on when ref_a > car ; S2 = NOT S1
    # Leg 2: S3 on when ref_b > car ; S4 = NOT S3
    # H-bridge uses S1/S4 as one pair and S2/S3 as the other; follow paper labels.
    S1 = (ref_a > car).astype(np.int8)
    S3 = (ref_b > car).astype(np.int8)
    S2 = 1 - S1
    S4 = 1 - S3

    # Determine pre-ST state string
    # Pattern mapping:
    #   S1=1,S4=1,S2=0,S3=0 -> ACT1
    #   S1=0,S4=0,S2=1,S3=1 -> ACT2
    #   S1=1,S3=1 (S2=0,S4=0) -> ZS1
    #   S1=0,S3=0 (S2=1,S4=1) -> ZS2
    is_ZS1 = (S1 == 1) & (S3 == 1)
    is_ZS2 = (S1 == 0) & (S3 == 0)

    # Insert shoot-through pulses around each carrier peak/valley.
    # Total ST duty = D_ST over a switching period. Split equally into two pulses
    # per switching period (one near carrier=0, one near carrier=1).
    car_phase = ((t * F_SW) % 1.0)                             # 0..1 sawtooth
    half_d = D_ST / 2.0                                        # per-pulse width
    ST_pulse = ((car_phase < half_d / 2) |
                (car_phase > 1 - half_d / 2) |
                (np.abs(car_phase - 0.5) < half_d / 2))        # three pulses? simplify
    # Simpler: one pulse near each carrier valley (car_phase ~ 0) and one near peak (0.5)
    ST_pulse = ((car_phase < half_d / 2) |
                (car_phase > 1 - half_d / 2) |
                ((car_phase > 0.5 - half_d / 2) & (car_phase < 0.5 + half_d / 2)))
    # We'll consider this adequate for CMV study; during ST, all switches on -> UCM=0.

    # === Proposed scheme: replace ZS1 with ZS2 ===
    if proposed:
        # Where we WERE in ZS1 (S1=S3=1), force to ZS2 (S1=S3=0, S2=S4=1)
        S1_out = np.where(is_ZS1, 0, S1)
        S3_out = np.where(is_ZS1, 0, S3)
        S2_out = 1 - S1_out
        S4_out = 1 - S3_out
    else:
        S1_out, S2_out, S3_out, S4_out = S1, S2, S3, S4

    # Override with ST pulses (all on)
    S1_out = np.where(ST_pulse, 1, S1_out)
    S2_out = np.where(ST_pulse, 1, S2_out)
    S3_out = np.where(ST_pulse, 1, S3_out)
    S4_out = np.where(ST_pulse, 1, S4_out)

    # Compute leg-to-ground voltages.
    # During ST, the dc-link is shorted so both leg midpoints sit at roughly
    # the midpoint of the qZS network; for CM analysis the paper treats this
    # as UCM = 0 (legs clamped by shoot-through short). We follow that.
    U10 = np.where(ST_pulse, 0.0, S1_out * V_PN)   # leg1 high if S1 on & not ST
    U20 = np.where(ST_pulse, 0.0, S3_out * V_PN)
    # Note: during ZS1 (if still present) U10=U20=VPN -> UCM=VPN
    #       during ZS2              U10=U20=0   -> UCM=0
    #       during ACT1/ACT2        one high one low -> UCM=VPN/2

    UCM = 0.5 * (U10 + U20)
    return t, U10, U20, UCM


# -----------------------------------------------------------------------
# 2.  Common-mode equivalent circuit via PySpice
# -----------------------------------------------------------------------
def simulate_cm_circuit(t: np.ndarray, ucm: np.ndarray, tag: str):
    """Drive the CM equivalent loop (Lf + Rf in series, Cg to ground) with UCM(t).

    Topology per paper Fig.2(b) / Eq.6:
        UCM --Rf--Lf--+--Cg--GND
                      +--Rg--GND   (series ground-return path)

    We model this as: source UCM in series with Rf, Lf, through node X;
    from X through Cg and Rg to ground.  Current through Cg is iLK.
    """
    # Downsample the PWL to keep ngspice happy (0.5 us -> 1 us is ample)
    step = 2
    tt = t[::step]
    uu = ucm[::step]
    # PySpice PWL limit: format as list of (time_s, voltage_V)
    pwl = []
    for ti, vi in zip(tt, uu):
        pwl.append(ti)
        pwl.append(vi)

    circ = Circuit(f'CM-equivalent-{tag}')
    # PWL voltage source in tabular form
    # PySpice accepts values= in PieceWiseLinearVoltageSource
    from PySpice.Spice.Netlist import Circuit as _C  # noqa
    src = circ.PieceWiseLinearVoltageSource(
        'cm', 'vcm', circ.gnd,
        values=list(zip(tt.tolist(), uu.tolist())),
    )
    circ.R('f', 'vcm', 'nLf', RF)
    circ.L('f', 'nLf', 'nX', LF)
    circ.C('g', 'nX', 'nG', CG)
    circ.R('g', 'nG', circ.gnd, RG)

    simulator = circ.simulator(temperature=25, nominal_temperature=25)
    tstop = float(tt[-1])
    tstep = 1e-6
    analysis = simulator.transient(step_time=tstep, end_time=tstop, use_initial_condition=True)

    ta = np.array(analysis.time)
    v_vcm = np.array(analysis['vcm'])
    v_nX  = np.array(analysis['nx'])
    v_nG  = np.array(analysis['ng'])
    # Rg is from nG to ground, carrying the full leakage-loop current
    i_lk  = v_nG / RG
    return ta, v_vcm, i_lk


# Fallback: solve the CM equivalent ODE with scipy if PySpice unavailable
def simulate_cm_ode(t, ucm):
    """State: x1 = i (inductor current = i_lk at DC), x2 = vCg (cap voltage).
       Lf di/dt = UCM - Rf*i - vCg - Rg*i
       Cg dv/dt = i
       => di/dt = (UCM - (Rf+Rg)*i - vCg) / Lf ; dvCg/dt = i/Cg
    """
    dt = t[1] - t[0]
    i = np.zeros_like(t)
    v = np.zeros_like(t)
    for k in range(1, t.size):
        di = (ucm[k-1] - (RF + RG) * i[k-1] - v[k-1]) / LF
        dv = i[k-1] / CG
        i[k] = i[k-1] + dt * di
        v[k] = v[k-1] + dt * dv
    return t, ucm, i


# -----------------------------------------------------------------------
# 3.  Analysis helpers
# -----------------------------------------------------------------------
def metrics(t, ucm, ilk, tag):
    cm_peak = float(np.max(np.abs(ucm)))
    cm_rms  = float(np.sqrt(np.mean(ucm ** 2)))
    lk_peak = float(np.max(np.abs(ilk)))
    lk_rms  = float(np.sqrt(np.mean(ilk ** 2)))
    print(f"[{tag}] CMV peak = {cm_peak:7.2f} V    CMV rms = {cm_rms:7.2f} V")
    print(f"[{tag}] iLK peak = {lk_peak*1e3:7.2f} mA  iLK rms = {lk_rms*1e3:7.2f} mA")
    return dict(cm_peak=cm_peak, cm_rms=cm_rms, lk_peak=lk_peak, lk_rms=lk_rms)


def fft_db(t, y):
    dt = t[1] - t[0]
    N = y.size
    Y = np.fft.rfft(y * np.hanning(N))
    f = np.fft.rfftfreq(N, dt)
    mag = np.abs(Y) / N * 2
    return f, mag


# -----------------------------------------------------------------------
# 4.  Main
# -----------------------------------------------------------------------
def main():
    print("=" * 70)
    print("qZSI CMV-reduction replication (OSTI 1606674)")
    print("=" * 70)
    print(f"VPN={V_PN} V  fs={F_SW} Hz  f0={F_GRID} Hz  M={M_INDEX}  D_ST={D_ST}")
    print(f"Lf={LF*1e3} mH  Cg={CG*1e9} nF  Rg={RG} ohm  Rf={RF} ohm")
    print(f"{N_CYCLES} grid cycles, dt={1e6/FS_TIME:.2f} us\n")

    # Generate CMV for both schemes
    t, U10_a, U20_a, UCM_a = build_pwm(proposed=False)
    _, U10_b, U20_b, UCM_b = build_pwm(proposed=True)

    # Run CM equivalent circuit simulation
    if HAVE_PYSPICE:
        print("Simulating CM equivalent circuit with PySpice/ngspice...")
        ta, ucm_a_sim, ilk_a = simulate_cm_circuit(t, UCM_a, 'traditional')
        tb, ucm_b_sim, ilk_b = simulate_cm_circuit(t, UCM_b, 'proposed')
    else:
        print("Simulating CM equivalent circuit with scipy ODE...")
        ta, ucm_a_sim, ilk_a = simulate_cm_ode(t, UCM_a)
        tb, ucm_b_sim, ilk_b = simulate_cm_ode(t, UCM_b)

    # Metrics (computed on the original high-res CMV; iLK on simulated grid)
    print()
    m_a = metrics(t, UCM_a, np.interp(t, ta, ilk_a), "traditional")
    m_b = metrics(t, UCM_b, np.interp(t, tb, ilk_b), "proposed   ")

    cm_red = 100 * (1 - m_b['cm_peak'] / m_a['cm_peak'])
    lk_red = 100 * (1 - m_b['lk_rms']  / m_a['lk_rms'])
    print()
    print(f"==> CMV peak reduction : {cm_red:5.1f} %   (paper claims ~50%)")
    print(f"==> iLK RMS reduction  : {lk_red:5.1f} %   (paper claims ~75%)")

    # ---------------- Plots ----------------
    # Zoom window: ~2 ms near the middle to show switching detail
    # Zoom at 1/4 grid period (sine peak) to see ACT states dominate
    t_mid = 0.25 / F_GRID  # 5 ms -> sine peak of first cycle
    win_w = 200e-6  # 200 us zoom -> 2 switching periods at 10 kHz
    win   = (t > t_mid) & (t < t_mid + win_w)
    winLK_a = (ta > t_mid) & (ta < t_mid + win_w)
    winLK_b = (tb > t_mid) & (tb < t_mid + win_w)

    fig, ax = plt.subplots(3, 2, figsize=(12, 9), sharex='col')

    # Row 0: CMV over the whole run
    ax[0, 0].plot(t * 1e3, UCM_a, color='C3', lw=0.6)
    ax[0, 0].set_title("Traditional SPWM – UCM(t)")
    ax[0, 0].set_ylabel("UCM [V]")
    ax[0, 0].set_ylim(-50, V_PN * 1.1)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(t * 1e3, UCM_b, color='C0', lw=0.6)
    ax[0, 1].set_title("Proposed (ZS1→ZS2) – UCM(t)")
    ax[0, 1].set_ylim(-50, V_PN * 1.1)
    ax[0, 1].grid(alpha=0.3)

    # Row 1: zoom of CMV
    ax[1, 0].step((t[win]-t_mid) * 1e6, UCM_a[win], color='C3', where='post', lw=1.2)
    ax[1, 0].set_title("Zoom: CMV (200 µs, µs axis)")
    ax[1, 0].set_xlabel("t - t0 [µs]")
    ax[1, 0].set_ylabel("UCM [V]")
    ax[1, 0].set_ylim(-50, V_PN * 1.1)
    ax[1, 0].grid(alpha=0.3)
    ax[1, 0].axhline(V_PN,     color='k', ls=':', alpha=0.5)
    ax[1, 0].axhline(V_PN / 2, color='k', ls=':', alpha=0.5)

    ax[1, 1].step((t[win]-t_mid) * 1e6, UCM_b[win], color='C0', where='post', lw=1.2)
    ax[1, 1].set_title("Zoom: CMV (200 µs, µs axis)")
    ax[1, 1].set_xlabel("t - t0 [µs]")
    ax[1, 1].set_ylim(-50, V_PN * 1.1)
    ax[1, 1].grid(alpha=0.3)
    ax[1, 1].axhline(V_PN,     color='k', ls=':', alpha=0.5)
    ax[1, 1].axhline(V_PN / 2, color='k', ls=':', alpha=0.5)

    # Row 2: leakage current
    ax[2, 0].plot(ta * 1e3, ilk_a * 1e3, color='C3', lw=0.5)
    ax[2, 0].set_title("Leakage current iLK(t)")
    ax[2, 0].set_ylabel("iLK [mA]")
    ax[2, 0].set_xlabel("t [ms]")
    ax[2, 0].grid(alpha=0.3)

    ax[2, 1].plot(tb * 1e3, ilk_b * 1e3, color='C0', lw=0.5)
    ax[2, 1].set_title("Leakage current iLK(t)")
    ax[2, 1].set_xlabel("t [ms]")
    ax[2, 1].grid(alpha=0.3)

    fig.suptitle("OSTI 1606674 replication – CMV & leakage current comparison", y=1.00)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_cmv_ilk_compare.png"), dpi=130)
    plt.close(fig)
    print(f"Saved: fig_cmv_ilk_compare.png")

    # Spectra
    fa, Ma = fft_db(t, UCM_a)
    fb, Mb = fft_db(t, UCM_b)
    fig, ax = plt.subplots(1, 1, figsize=(10, 4.5))
    ax.semilogx(fa, 20*np.log10(Ma + 1e-9), label='Traditional', color='C3', alpha=0.8)
    ax.semilogx(fb, 20*np.log10(Mb + 1e-9), label='Proposed',    color='C0', alpha=0.8)
    ax.set_xlim(10, 5 * F_SW)
    ax.set_ylim(-80, 60)
    ax.set_xlabel("Frequency [Hz]")
    ax.set_ylabel("|UCM| [dBV]")
    ax.set_title("CMV spectrum (4 grid cycles, Hann window)")
    ax.legend()
    ax.grid(alpha=0.3, which='both')
    for k in (1, 2, 3, 4):
        ax.axvline(k * F_SW, color='k', ls=':', alpha=0.3)
        ax.text(k * F_SW, 55, f"{k}fs", ha='center', fontsize=8, alpha=0.7)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_cmv_spectrum.png"), dpi=130)
    plt.close(fig)
    print("Saved: fig_cmv_spectrum.png")

    # Dump metrics to file
    with open(os.path.join(OUT_DIR, "metrics.txt"), "w") as f:
        f.write("OSTI 1606674 replication metrics\n")
        f.write("=" * 40 + "\n")
        for name, m in [("traditional", m_a), ("proposed", m_b)]:
            f.write(f"[{name}] CMV_peak={m['cm_peak']:.2f} V  CMV_rms={m['cm_rms']:.2f} V  "
                    f"iLK_peak={m['lk_peak']*1e3:.2f} mA  iLK_rms={m['lk_rms']*1e3:.2f} mA\n")
        f.write(f"\nCMV peak reduction : {cm_red:.1f} %   (paper claims ~50%)\n")
        f.write(f"iLK RMS reduction  : {lk_red:.1f} %   (paper claims ~75%)\n")
    print("Saved: metrics.txt")


if __name__ == "__main__":
    main()
