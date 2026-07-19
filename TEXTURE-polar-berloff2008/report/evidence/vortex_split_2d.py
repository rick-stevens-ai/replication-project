"""
Berloff 2008 (arXiv 0801.2964) - 2D subcritical NLS, charge-2 vortex splitting.
Independent reimplementation from Eqs (16), (21), (41).

Equation (dimensionless; signs reconciled so bulk psi=1 is stationary and Eq 21
is its radial ODE):
    i psi_t = -1/2 lap psi + [ |psi|^{2(1+g)} - 2 xi |psi|^2 - (1 - 2 xi) ] psi

Drive (Eq 41):  xi(t) = xi0 + eps*sin(pi t / 2 eta), xi0 = (1+g)/(2+g).
When xi0+eps > xi_crit the negative pressure expands the vortex core (paper Sec 4).

Physics under test: a multiply-charged (s=2) vortex is dynamically unstable and
splits into two s=1 vortices (paper line 332: only s=+-1 are stable).
We track the two core positions (subpixel, via density minima) -> separation d(t).
Split-step Fourier + absorbing sponge for emitted sound.
"""
import numpy as np
import json, time
from scipy import ndimage


def run(gamma=1, N=192, L=48.0, dt=0.004, T=200.0,
        seed_amp=0.03, eps=0.08, eta=100.0, drive=True, save_every=100):
    xi0 = (1 + gamma) / (2 + gamma)          # 2/3 for gamma=1
    x = (np.arange(N) - N // 2) * (L / N)
    X, Y = np.meshgrid(x, x, indexing="ij")
    dx = L / N
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    KX, KY = np.meshgrid(k, k, indexing="ij")
    K2 = KX**2 + KY**2
    Khalf = np.exp(-1j * dt * 0.5 * (0.5 * K2))   # exp(-i dt/2 * T), T=(1/2)k^2

    r = np.sqrt(X**2 + Y**2)
    th = np.arctan2(Y, X)
    core = 2.0
    amp = r**2 / (r**2 + core**2)             # ~ r^2 near 0 (|s|=2), ->1 far
    psi = amp * np.exp(2j * th)
    psi = psi * (1.0 + seed_amp * np.cos(2 * th) * np.exp(-r**2 / 18.0))
    psi = psi.astype(np.complex128)

    r_abs = 0.42 * L
    sponge = np.clip(np.where(r > r_abs, ((r - r_abs) / (0.5 * L - r_abs))**2, 0.0), 0, 1)

    def step(psi, xi, dt):
        psi = np.fft.ifft2(Khalf * np.fft.fft2(psi))
        rho = np.abs(psi)**2
        V = rho**(1 + gamma) - 2 * xi * rho - (1 - 2 * xi)
        psi = psi * np.exp(-1j * dt * V)
        psi = psi * np.exp(-dt * 3.0 * sponge)
        psi = np.fft.ifft2(Khalf * np.fft.fft2(psi))
        return psi

    def winding_cores(psi):
        # locate +1 winding plaquettes, cluster them, return centroids & total charge
        ph = np.angle(psi)
        wrap = lambda d: (d + np.pi) % (2 * np.pi) - np.pi
        d1 = wrap(ph[1:, :-1] - ph[:-1, :-1]); d2 = wrap(ph[1:, 1:] - ph[1:, :-1])
        d3 = wrap(ph[:-1, 1:] - ph[1:, 1:]);  d4 = wrap(ph[:-1, :-1] - ph[:-1, 1:])
        w = np.round((d1 + d2 + d3 + d4) / (2 * np.pi)).astype(int)
        cen = r[:-1, :-1] < 0.30 * L
        pos = (w > 0) & cen
        ntot = int(np.sum(w[pos]))
        # cluster adjacent positive plaquettes
        lbl, n = ndimage.label(pos, structure=np.ones((3, 3)))
        pts = []
        Xh = X[:-1, :-1] + dx / 2; Yh = Y[:-1, :-1] + dx / 2
        for i in range(1, n + 1):
            sel = lbl == i
            pts.append((Xh[sel].mean(), Yh[sel].mean()))
        d = 0.0
        for a in range(len(pts)):
            for b in range(a + 1, len(pts)):
                d = max(d, np.hypot(pts[a][0] - pts[b][0], pts[a][1] - pts[b][1]))
        return d, len(pts), ntot

    def core_radius(psi):
        # effective core radius: area where rho<0.5 in center -> R=sqrt(A/pi)
        rho = np.abs(psi)**2
        A = np.sum((rho < 0.5) & (r < 0.30 * L)) * dx * dx
        return np.sqrt(A / np.pi)

    nsteps = int(T / dt)
    times, seps, ncore, chg, xit, rcore = [], [], [], [], [], []
    t0 = time.time()
    for n in range(nsteps + 1):
        t = n * dt
        xi = xi0 + (eps * np.sin(np.pi * t / (2 * eta)) if drive else 0.0)
        if n % save_every == 0:
            d, nc, q = winding_cores(psi)
            times.append(t); seps.append(d); ncore.append(nc)
            chg.append(q); xit.append(xi); rcore.append(core_radius(psi))
        psi = step(psi, xi, dt)
    return dict(gamma=gamma, N=N, L=L, dt=dt, T=T, xi0=xi0, eps=eps, eta=eta,
                drive=drive, xi_crit_paper=0.689, times=times, seps=seps,
                ncore=ncore, charge=chg, xit=xit, rcore=rcore,
                elapsed=time.time() - t0)


if __name__ == "__main__":
    import sys
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 128
    T = float(sys.argv[2]) if len(sys.argv) > 2 else 200.0
    eps = float(sys.argv[3]) if len(sys.argv) > 3 else 0.08
    drive = (sys.argv[4] != "0") if len(sys.argv) > 4 else True
    res = run(N=N, T=T, eps=eps, drive=drive)
    print(f"xi0={res['xi0']:.4f} eps={eps} drive={drive} grid={N} T={T} "
          f"elapsed={res['elapsed']:.1f}s")
    for t, s, nc, q, xi, rc in zip(res["times"], res["seps"], res["ncore"],
                                   res["charge"], res["xit"], res["rcore"]):
        print(f"  t={t:7.1f} xi={xi:.3f} n_cores={nc} totchg={q} sep={s:.3f} rcore={rc:.2f}")
