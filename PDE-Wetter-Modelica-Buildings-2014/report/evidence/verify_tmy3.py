#!/usr/bin/env python3
"""Direct read of Chicago-OHare TMY3 (as embedded in Buildings library) — compare
to what our simulation extracted."""
import numpy as np
import sys

path = sys.argv[1]
# Skip Modelica header lines starting with # or 'double'
data = []
with open(path) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('double'):
            continue
        parts = line.split('\t')
        if len(parts) < 5:
            continue
        try:
            row = [float(x) for x in parts]
            data.append(row)
        except ValueError:
            continue

arr = np.array(data)
print(f"Read {len(arr)} rows, {arr.shape[1]} cols")
# C1 = time (s), C2 = TdryBulC, C9 = GHI Wh/m^2 (hourly, so W/m^2 avg)
t = arr[:, 0]
Tdry = arr[:, 1]  # already Celsius
GHI = arr[:, 8]   # Wh/m2 in previous hour

print(f"\nTime range: {t[0]} to {t[-1]} s = {t[-1]/86400:.1f} days = {t[-1]/3600:.0f} hours")
print(f"Tdry range: {Tdry.min():.2f} to {Tdry.max():.2f} C, mean={Tdry.mean():.3f} C")

# Filter obvious sentinel values (99.9 for temp is missing indicator in TMY3)
Tclean = Tdry[np.abs(Tdry) < 60]
print(f"Tdry cleaned (|T|<60): mean={Tclean.mean():.3f} C, n={len(Tclean)}")

# Compute HDD/CDD from daily means
n_hours = len(Tdry)
n_days = n_hours // 24
Tdry_daily = Tdry[:n_days*24].reshape(n_days, 24).mean(axis=1)
HDD_65F = np.sum(np.maximum(18.3 - Tdry_daily, 0))  # °C-day
CDD_65F = np.sum(np.maximum(Tdry_daily - 18.3, 0))
print(f"HDD (base 18.3C = 65F): {HDD_65F:.1f} C-day")
print(f"CDD (base 18.3C = 65F): {CDD_65F:.1f} C-day")
# Also base 65F in °F-days
HDD_F = HDD_65F * 9/5
print(f"HDD (base 65F): {HDD_F:.0f} F-day  [NOAA norm Chicago ~6100-6500 F-day]")

# Total GHI
# GHI col is Wh/m^2/h (hourly integral). Sum = kWh/m2/yr
GHI_total_kWh = GHI.sum() / 1000
print(f"Annual GHI: {GHI_total_kWh:.1f} kWh/m^2 (Chicago published: ~1400-1500)")

# Extreme reference from DESIGN CONDITIONS header
print("\nHeader-reported climate design values:")
print("  99.6% heating DB: -20 C  = -4 F")
print("  0.4% cooling DB: 33.3 C = 92 F")
print(f"Our TMY3 extracted extremes: min={Tdry.min():.1f} C, max={Tdry.max():.1f} C")
