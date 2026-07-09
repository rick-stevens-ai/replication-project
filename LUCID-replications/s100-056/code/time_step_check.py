"""
Verify the GFDE-SBS time-step accounting claims from the paper.

Paper says (Methods):
  - 40 steps per order of magnitude (log-spaced)
  - Water radiolysis: up to 1 µs simulation time -> 240 steps
    smallest step = 0.059 ps, largest step = 55.71 ns
  - Fricke: up to 100 s simulation time -> 560 steps
    smallest step = 0.059 ps, largest step = 5.58 s
"""
import math

def steps_and_widths(t_max_s, t_min_s=None, steps_per_decade=40):
    """
    Produce log-spaced time grid where, by construction, smallest step
    is roughly t_min_s, largest step approx t_max_s/(10^(1/40)-1) etc.

    Convention (matches paper): step_i = t_i - t_{i-1} for i = 1..N
    with t_i = t_min * 10^(i/steps_per_decade) and choose t_min so that
    the *first step width* (t_1 - t_0=0) equals 0.059 ps.
    Equivalently: t_min * (10^(1/40)-1) ~ 0.059 ps.
    """
    # number of decades from t_min to t_max
    if t_min_s is None:
        t_min_s = 0.059e-12  # given by paper as the smallest step
    decades = math.log10(t_max_s / t_min_s)
    N = int(round(decades * steps_per_decade))
    # smallest step width:
    smallest = t_min_s * (10**(1/steps_per_decade) - 1)
    # largest step width near t_max
    largest = t_max_s * (1 - 10**(-1/steps_per_decade))
    return N, smallest, largest

# 1 microsecond run
N1, s1, l1 = steps_and_widths(1e-6)
print(f"Water radiolysis up to 1 µs: N={N1} steps  "
      f"smallest≈{s1*1e12:.3f} ps  largest≈{l1*1e9:.2f} ns")
print(f"  paper:                    N=240          "
      f"smallest=0.059 ps    largest=55.71 ns")

# 100 s run
N2, s2, l2 = steps_and_widths(100.0)
print(f"\nFricke up to 100 s:        N={N2} steps  "
      f"smallest≈{s2*1e12:.3f} ps  largest≈{l2:.2f} s")
print(f"  paper:                    N=560          "
      f"smallest=0.059 ps    largest=5.58 s")

# Performance gain check from Table 1
print("\nTable 1 performance gain checks (GFDE HPS / CONV HPS):")
for ion, gfde, conv, gain in [
    ("1H+",   777, 58, 13.3),
    ("4He2+", 695, 50, 13.9),
    ("12C6+", 667, 67, 9.9),
]:
    computed = gfde/conv
    ok = "OK" if abs(computed-gain)/gain < 0.02 else "MISMATCH"
    print(f"  {ion:7s} 20 MeV/u: {gfde}/{conv} = {computed:5.2f}  paper={gain}  [{ok}]")
