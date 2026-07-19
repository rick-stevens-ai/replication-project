"""
Berloff 2008 (arXiv 0801.2964) - stationary straight-line vortex profile.
Independent reimplementation from Eq (21):

  (1/2)(1/r) d/dr( r df/dr ) - s^2/(2 r^2) f + 2 xi f^3 + (1-2 xi) f - f^{2(1+gamma)+1} = 0

BC: f(0)=0, f->1 as r->inf.  Solve by relaxation (Newton on finite differences).
Validate slope-at-origin a1 and xi_crit vs Table 1 (gamma=1: a1(0)=0.9575, xi_crit=0.689;
text: a1(xi=5/8)=0.286).
"""
import numpy as np

def solve_profile(xi, gamma=1, s=1, R=30.0, N=3000):
    r = np.linspace(0, R, N + 1)
    dr = r[1] - r[0]
    # initial guess: tanh-like
    f = np.tanh(r / np.sqrt(2))
    f[0] = 0.0
    p = 2 * (1 + gamma) + 1  # exponent on f in last term

    for it in range(500):
        F = np.zeros(N + 1)
        # residual at interior points
        rr = r[1:-1]
        lap = (f[2:] - 2 * f[1:-1] + f[:-2]) / dr**2
        drf = (f[2:] - f[:-2]) / (2 * dr)
        F[1:-1] = (0.5 * (lap + drf / rr) - s**2 / (2 * rr**2) * f[1:-1]
                   + 2 * xi * f[1:-1]**3 + (1 - 2 * xi) * f[1:-1]
                   - f[1:-1]**p)
        # Jacobian (tridiagonal) for interior
        n = N - 1
        lo = np.zeros(n); di = np.zeros(n); up = np.zeros(n)
        di += 0.5 * (-2 / dr**2) - s**2 / (2 * rr**2) + 2 * xi * 3 * f[1:-1]**2 \
              + (1 - 2 * xi) - p * f[1:-1]**(p - 1)
        lo += 0.5 * (1 / dr**2 - 1 / (2 * dr) / rr)
        up += 0.5 * (1 / dr**2 + 1 / (2 * dr) / rr)
        # BCs: f[0]=0 fixed, f[N]=1 fixed
        b = -F[1:-1].copy()
        # Thomas solve
        c = up.copy(); d = b.copy(); a = lo.copy(); bb = di.copy()
        for i in range(1, n):
            m = a[i] / bb[i - 1]
            bb[i] -= m * c[i - 1]
            d[i] -= m * d[i - 1]
        x = np.zeros(n)
        x[-1] = d[-1] / bb[-1]
        for i in range(n - 2, -1, -1):
            x[i] = (d[i] - c[i] * x[i + 1]) / bb[i]
        f[1:-1] += x
        f[0] = 0.0; f[-1] = 1.0
        if np.max(np.abs(x)) < 1e-11:
            break
    a1 = f[1] / r[1]  # slope at origin
    return r, f, a1


if __name__ == "__main__":
    gamma = 1
    # a1(0): extrapolate small xi
    _, _, a1_small = solve_profile(0.01, gamma=gamma)
    _, _, a1_0 = solve_profile(1e-4, gamma=gamma)
    print(f"gamma=1  a1(xi->0) ~ {a1_0:.4f}   (paper Table 1: 0.9575)")
    _, _, a1_625 = solve_profile(0.625, gamma=gamma)
    print(f"gamma=1  a1(xi=5/8) = {a1_625:.4f}  (paper text: 0.286)")
    # xi_crit: where a1 -> 0
    for xi in [0.5, 0.6, 0.65, 0.68, 0.689, 0.70]:
        _, _, a1 = solve_profile(xi, gamma=gamma)
        print(f"  xi={xi:.3f}  a1={a1:.4f}")
    # phenomenological a1(0)*sqrt(1-xi/xi_crit) with xi_crit=0.689
    print("check law a1(0.625)=0.9575*sqrt(1-.625/.689) =",
          0.9575 * np.sqrt(1 - 0.625 / 0.689))
