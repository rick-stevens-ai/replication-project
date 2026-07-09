#!/usr/bin/env python3
"""
s100-064 — Eq. (3) audit
RBE_DSB = DSB_subject / DSB_{200 kVp}

Paper states (text + Table 1):
  - DSB/nucleus range for kVp X-rays (60, 100, 200, 250):  30.2 .. 41.9
  - DSB/nucleus range for 6 MV linac (1/3/5/10 cm in-field, 10 cm OOF): 22.2 .. 25.9
  - Published RBE_DSB (200 kVp = 1.00):
        60 kVp -> 1.18    100 kVp -> 1.17    250 kVp -> 1.39
        6 MV in-field 1 cm  -> 0.73
        6 MV in-field 5 cm  -> 0.76
        6 MV in-field 10 cm -> 0.85
        6 MV out-of-field 10 cm -> 0.85

We do not have the individual DSB-per-nucleus means published per beam
(paper gives only the ranges + a bar plot Fig. 4). Therefore we INFER
the per-beam means from the published RBE_DSB and from the bracketing range,
using DSB_{200 kVp} as the pivot, then re-derive RBE_DSB to confirm the
arithmetic of Eq. 3 closes self-consistently.
"""

from __future__ import annotations

# Published RBE_DSB from Table 1 (rounded to 2 dp).
rbe_pub = {
    "60 kVp":              1.18,
    "100 kVp":             1.17,
    "200 kVp (standard)":  1.00,
    "250 kVp":             1.39,
    "6 MV in-field 1 cm":  0.73,
    "6 MV in-field 5 cm":  0.76,
    "6 MV in-field 10 cm": 0.85,
    "6 MV out-of-field 10 cm": 0.85,
}

# Anchor: the 200 kVp DSB/nucleus mean. The paper states the kVp range is
# 30.2 .. 41.9. Of the four kVp beams (60, 100, 200, 250), the largest RBE
# is 250 kVp (1.39) and the smallest is 200 kVp itself (1.00). So:
#   DSB_{200} = 30.2 (lower kVp bound)
#   DSB_{250} = 30.2 * 1.39 = 41.978  ~= 41.9 (upper kVp bound).  ✓
dsb_200 = 30.2

print("=== s100-064 :: Eq. (3) audit ===")
print(f"Anchor: DSB/nucleus @ 200 kVp (standard) = {dsb_200}")
print()
print(f"{'Beam':<28s} {'RBE_pub':>8s} {'DSB_inferred':>14s} {'RBE_recovered':>15s}")
for beam, rbe in rbe_pub.items():
    dsb = rbe * dsb_200
    rbe_back = dsb / dsb_200
    print(f"{beam:<28s} {rbe:>8.2f} {dsb:>14.2f} {rbe_back:>15.3f}")

# Range cross-check.
dsbs_kvp = [rbe_pub[b] * dsb_200 for b in rbe_pub if "kVp" in b]
dsbs_mv  = [rbe_pub[b] * dsb_200 for b in rbe_pub if "MV"  in b]
print()
print(f"Inferred kVp DSB/nucleus range: {min(dsbs_kvp):.2f} .. {max(dsbs_kvp):.2f}"
      f"   (paper says 30.2 .. 41.9)")
print(f"Inferred MV  DSB/nucleus range: {min(dsbs_mv):.2f} .. {max(dsbs_mv):.2f}"
      f"   (paper says 22.2 .. 25.9)")
