"""
Grid Bayesian filter, no resampling. Should converge cleanly.
Then compare to the resample-refit RFPE version.
"""
import math, numpy as np
from rfpe_sim import qpe_step_probability

TWO_PI = 2*math.pi

def wrap(d):
    return (d + math.pi) % TWO_PI - math.pi

Phi_true = 4.8741
rng = np.random.default_rng(42)

# Fine grid over [0, 2pi)
G = 4001
grid = np.linspace(0, TWO_PI, G, endpoint=False)
prior = np.exp(-0.5 * ((grid - math.pi)/math.pi)**2)
prior = prior / prior.sum()

mu = float(np.sum(grid * prior))
var = float(np.sum(prior * (grid-mu)**2))
sigma = math.sqrt(var)
print(f"init: mu={mu:.4f}, sigma={sigma:.4f}")

for step in range(60):
    M = max(1, int(math.ceil(1.25/sigma)))
    Theta = mu
    p0 = qpe_step_probability(Phi_true, Theta, M)
    E = 0 if rng.random() < p0 else 1
    arg = 0.5*M*(grid-Theta)
    lik = np.cos(arg)**2 if E == 0 else np.sin(arg)**2
    post = prior * lik
    post = post / post.sum()
    mu = float(np.sum(grid*post))
    var = float(np.sum(post*(grid-mu)**2))
    sigma = math.sqrt(max(var, 1e-24))
    prior = post
    err = abs(wrap(mu - Phi_true))
    if step < 20 or step % 5 == 0:
        print(f"  step {step+1}: M={M:4d} E={E} theta={Theta:.4f} -> mu={mu:.6f} sigma={sigma:.3e} err={err:.3e}")

print()
print(f"After 60 steps: mu={mu:.6f}, sigma={sigma:.3e}, err={abs(wrap(mu-Phi_true)):.3e} rad")
print(f"Paper single run @ 50 steps: err ~ 2.4e-4 rad, sigma ~ 4.2e-4 rad")
