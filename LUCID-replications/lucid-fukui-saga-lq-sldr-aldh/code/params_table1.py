"""
Table 1 from Fukui et al. 2022 (Sci Rep), verbatim.
Means and standard deviations of the IMK model parameters.
"""

# Each cell line provides:
#   alpha0_p_star, beta0_p_star, apc_p_star, w_SLDR (h^-1 multiplier),
#   alpha0_s, beta0_s, apc_H, f_s, gamma
#
# Stem-cell parameters (alpha0_s, beta0_s, (a+c)_H) are reported for the
# parental cell line and re-used for its resistant counterpart.

PARENT_ONLY_FIELDS = ("alpha0_s", "beta0_s", "apc_H")

TABLE1 = {
    "SAS": {
        "alpha0_p_star": (0.208, 0.095),
        "beta0_p_star":  (0.044, 0.012),
        "apc_p_star":    (1.279, 0.687),
        "w_SLDR":        (1.000, 0.000),
        "alpha0_s":      (0.074, 0.098),
        "beta0_s":       (0.027, 0.007),
        "apc_H":         (1.355, 0.745),
        "f_s":           (0.012, 0.006),
        "gamma":         0.954,
    },
    "SAS-R": {
        "alpha0_p_star": (0.197, 0.093),
        "beta0_p_star":  (0.041, 0.012),
        "apc_p_star":    (1.355, 0.745),
        "w_SLDR":        (1.059, 0.123),
        # stem-cell params inherited from SAS:
        "alpha0_s":      (0.074, 0.098),
        "beta0_s":       (0.027, 0.007),
        "apc_H":         (1.355, 0.745),
        "f_s":           (0.083, 0.046),
        "gamma":         0.954,
    },
    "HSC2": {
        "alpha0_p_star": (0.166, 0.160),
        "beta0_p_star":  (0.168, 0.054),
        "apc_p_star":    (1.499, 0.911),
        "w_SLDR":        (1.000, 0.000),
        "alpha0_s":      (0.194, 0.110),
        "beta0_s":       (0.019, 0.010),
        "apc_H":         (2.842, 1.856),
        "f_s":           (0.014, 0.004),
        "gamma":         0.954,
    },
    "HSC2-R": {
        "alpha0_p_star": (0.088, 0.087),
        "beta0_p_star":  (0.089, 0.036),
        "apc_p_star":    (2.842, 1.856),
        "w_SLDR":        (1.896, 0.453),
        # stem-cell params inherited from HSC2:
        "alpha0_s":      (0.194, 0.110),
        "beta0_s":       (0.019, 0.010),
        "apc_H":         (2.842, 1.856),
        "f_s":           (0.127, 0.068),
        "gamma":         0.954,
    },
}


def mean_params(cell: str) -> dict:
    """Return mean values only (no SD) for a cell line, ready to pass to model."""
    p = TABLE1[cell]
    return {
        "alpha0_p_star": p["alpha0_p_star"][0],
        "beta0_p_star":  p["beta0_p_star"][0],
        "apc_p_star":    p["apc_p_star"][0],
        "alpha0_s":      p["alpha0_s"][0],
        "beta0_s":       p["beta0_s"][0],
        "apc_H":         p["apc_H"][0],
        "f_s":           p["f_s"][0],
        "gamma":         p["gamma"],
    }
