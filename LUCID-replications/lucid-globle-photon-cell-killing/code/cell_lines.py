"""Cell-line parameters from Table 2 of Herr et al. 2014.

Two columns of fitted parameters per cell line:
  - "dose_rate": fit to dose-rate experiments
  - "split":     fit to split-dose experiments
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class ParamSet:
    eps_i: float
    eps_c: float
    hlt_i: float


CELL_LINES = {
    "C3H 10T1/2": {"dose_rate": ParamSet(0.00396, 0.0964, 2.594)},
    "CHO 10B2":  {"dose_rate": ParamSet(0.00130, 0.162,  6.100),
                  "split":     ParamSet(0.00387, 0.140,  1.337)},
    "CHO K1":    {"dose_rate": ParamSet(0.00338, 0.674,  0.0350)},
    "NFF28":     {"dose_rate": ParamSet(0.00410, 0.455,  0.487)},
    "HX118":     {"dose_rate": ParamSet(0.0108,  0.297,  0.236)},
    "HX32":      {"dose_rate": ParamSet(0.0142,  0.428,  5.685)},
    "HX58":      {"dose_rate": ParamSet(0.0150,  0.425,  0.939)},
    "MT":        {"dose_rate": ParamSet(0.00865, 0.178,  0.0859),
                  "split":     ParamSet(0.00958, 0.119,  0.288)},
    "LL":        {"dose_rate": ParamSet(0.0114,  0.543,  0.0954),
                  "split":     ParamSet(0.0179,  0.267,  0.458)},
    "B16":       {"dose_rate": ParamSet(0.00781, 0.203,  0.131),
                  "split":     ParamSet(0.00771, 0.180,  0.146)},
    "HX34":      {"dose_rate": ParamSet(0.00893, 0.320,  0.133),
                  "split":     ParamSet(0.0121,  0.193,  1.095)},
    "IN859":     {"dose_rate": ParamSet(0.00536, 0.407,  0.467)},
    "IN1265":    {"dose_rate": ParamSet(0.00913, 0.215,  0.564)},
    "SB":        {"dose_rate": ParamSet(0.00490, 0.259,  0.941)},
    "RT112":     {"dose_rate": ParamSet(0.00529, 0.195,  0.485)},
    "HX138":     {"dose_rate": ParamSet(0.0218,  0.851,  1.184)},
    "HX142":     {"dose_rate": ParamSet(0.0284,  0.809,  1.083)},
}


# Dose-rate panels reproduced (subset relevant for figures).
DOSE_RATES = {
    "C3H 10T1/2":  [55.6, 2.4, 0.49, 0.29, 0.17, 0.06],
    "CHO 10B2":   [45, 0.5, 0.12],
    "CHO K1":     [45, 0.153],
    "NFF28":      [19.98, 0.99],
    "HX118":      [90, 4.56, 0.96],
    "HX32":       [90, 0.96],
    "HX58":       [90, 0.96],
    "MT":         [90, 24, 8.4, 4.56, 0.96],
    "LL":         [90, 8.4, 4.56, 0.96],
    "B16":        [90, 8.4, 4.56, 0.96],
    "HX34":       [90, 8.4, 4.56, 0.96],
    "IN859":      [90, 4.2, 1.2, 0.678],
    "IN1265":     [90, 4.2, 1.2, 0.678],
    "SB":         [90, 4.2, 1.2, 0.678],
    "RT112":      [76.8, 30, 12, 6, 3, 1.2, 0.6],
    "HX138":      [54, 12, 6, 3, 1.2, 0.6, 0.3, 0.15],
    "HX142":      [54, 12, 1.2, 0.6, 0.3, 0.15],
}
