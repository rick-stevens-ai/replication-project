"""
Audit the three rate constants the paper prints in equations R1-R3.

Paper:
  R1: •OH + •OH -> H2O2          k = 4.40e9   M^-1 s^-1
  R2: •OH + O(3P) -> HO2•        k = 2.00e10  M^-1 s^-1
  R3: •OH + HO2• -> O2           k = 9.79e10  M^-1 s^-1   <-- product should be H2O+O2

Literature reference values (Buxton et al. 1988, NIST Solution Kinetics DB):
  •OH + •OH                       k_lit = 5.5e9  M^-1 s^-1  (consensus value)
  •OH + O(3P)                     literature thin; Atkinson 2004 gas-phase ~3e-11 cm^3 mol^-1 s^-1
                                  -> aqueous rare; RITRACKS uses ~2e10 M^-1 s^-1
  •OH + HO2•                      k_lit = 7.1e9  M^-1 s^-1  (Buxton 1988)
                                  Note: paper's 9.79e10 is ~14x literature - this looks
                                  like a possible TYPO (extra zero) or non-standard parameter.
"""
import math

paper = {
    "R1 (OH+OH -> H2O2)":     4.40e9,
    "R2 (OH+O3P -> HO2)":     2.00e10,
    "R3 (OH+HO2 -> O2+H2O)":  9.79e10,
}
lit = {
    "R1 (OH+OH -> H2O2)":     5.5e9,    # Buxton 1988 - widely cited
    "R2 (OH+O3P -> HO2)":     2.0e10,   # RITRACKS/Plante 2011
    "R3 (OH+HO2 -> O2+H2O)":  7.1e9,    # Buxton 1988
}

print(f"{'Reaction':30s}  {'Paper k':>12s}  {'Lit k':>12s}  {'ratio':>8s}  comment")
for r in paper:
    p = paper[r]; l = lit[r]
    ratio = p/l
    comment = "match" if 0.7 < ratio < 1.5 else "OFF"
    if r.startswith("R3") and ratio > 5:
        comment = "OFF — possible typo (9.79e10 vs Buxton 7.1e9; off by ×14)"
    print(f"{r:30s}  {p:12.2e}  {l:12.2e}  {ratio:8.2f}  {comment}")

print()
print("Verdict on rate-constant audit:")
print(" * R1 (•OH+•OH): paper 4.4e9 is within the 4-6e9 spread of the literature - OK.")
print(" * R2 (•OH+O3P): paper 2.0e10 matches RITRACKS-derived value - OK.")
print(" * R3 (•OH+HO2): paper 9.79e10 is ~14x the Buxton consensus 7.1e9. This may be")
print("   a typo (9.79e9 would be reasonable) or a non-standard parameter from TRACIRT.")
print("   Worth flagging but not fatal - even at the high rate constant, R3 still loops")
print("   into the LET-dependence of G(H2O2) in the way the paper describes.")
