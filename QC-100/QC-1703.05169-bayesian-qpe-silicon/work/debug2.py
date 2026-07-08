"""Deeper diagnosis: what does one Bayesian update do with the RIGHT M choice?"""
import math, numpy as np
from rfpe_sim import likelihood, qpe_step_probability

rng = np.random.default_rng(0)

# Simulate ONE step by hand
mu, sigma = 0.5, 0.5
M = int(math.ceil(1.25/sigma))  # = 3
theta = mu
phi_true = 4.8741/(2*math.pi)  # 0.7757
p0 = qpe_step_probability(phi_true, theta, M)
print(f"M={M}, theta={theta}, p0={p0:.4f}")

# Do many resample+weight cycles and see sigma trajectory
mus, sigmas = [mu], [sigma]
for step in range(200):
    M = max(1, int(math.ceil(1.25/sigma)))
    theta = mu
    p0 = qpe_step_probability(phi_true, theta, M)
    E = 0 if rng.random() < p0 else 1
    particles = rng.normal(mu, sigma, size=5000)
    w = likelihood(E, particles, theta, M)
    w = w / w.sum()
    new_mu = np.sum(w*particles)
    new_var = np.sum(w*(particles-new_mu)**2)
    new_sigma = math.sqrt(max(new_var, 1e-18))
    mu, sigma = new_mu, new_sigma
    mus.append(mu); sigmas.append(sigma)
    if step < 20 or step % 20 == 0:
        print(f"  step {step+1}: M={M} E={E} theta={theta:.4f} -> mu={mu:.6f} sigma={sigma:.3e} err={abs(mu-phi_true):.3e}")

print(f"\nFinal: mu={mu:.6f} sigma={sigma:.3e} err={abs(mu-phi_true):.3e}")
print(f"Paper: after 50 steps err ~ 2.4e-4/(2pi) = {2.4e-4/(2*math.pi):.3e} in phi units")
