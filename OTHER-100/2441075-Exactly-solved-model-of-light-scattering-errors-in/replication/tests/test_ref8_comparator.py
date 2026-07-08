"""Sanity tests for ref8_scattering_comparator.py."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'src'))
sys.path.insert(0, SRC)

from ref8_scattering_comparator import (
    reference_branching_from_clebsch_gordan,
    reference_rates,
    PAPER_F_LEAK, PAPER_F_RAMAN, PAPER_F_ELASTIC,
)


def test_branching_sums_to_unity():
    br = reference_branching_from_clebsch_gordan()
    s = br['f_leak'] + br['f_raman'] + br['f_elastic']
    assert abs(s - 1.0) < 1e-12, s


def test_branching_matches_paper_within_3pct():
    br = reference_branching_from_clebsch_gordan()
    assert abs(br['f_leak']    - PAPER_F_LEAK)    / PAPER_F_LEAK    < 0.01
    assert abs(br['f_raman']   - PAPER_F_RAMAN)   / PAPER_F_RAMAN   < 0.02
    assert abs(br['f_elastic'] - PAPER_F_ELASTIC) / PAPER_F_ELASTIC < 0.03


def test_rates_quadratic_in_Omega_over_Delta():
    r1 = reference_rates(1e-3)
    r2 = reference_rates(2e-3)
    assert abs(r2.Gamma_total / r1.Gamma_total - 4.0) < 1e-9


if __name__ == '__main__':
    test_branching_sums_to_unity()
    test_branching_matches_paper_within_3pct()
    test_rates_quadratic_in_Omega_over_Delta()
    print("ALL PASS")
