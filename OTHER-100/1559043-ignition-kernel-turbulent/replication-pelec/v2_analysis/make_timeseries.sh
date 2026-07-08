#!/bin/bash
# Walk all plt files, extract time-series of Tmax, OHmax, H2Omax, CO2max for each phi.
FEX=/home/stevens/software/combustion-codes/PeleC/Submodules/PelePhysics/Submodules/amrex/Tools/Plotfile/fextrema.gnu.ex
BASE=/home/stevens/software/combustion-codes/PeleC/Exec/Production/IgnitionKernel/runs_v2
OUT=$1

getmax() { $FEX -v "$1" "$2" 2>/dev/null | awk -v v="$1" '$1==v {print $NF; exit}'; }
gettime() { $FEX -v Temp "$1" 2>/dev/null | awk '/time =/ {print $3; exit}'; }

echo "phi,t,Tmax,OHmax,H2Omax,CO2max,CH4max" > $OUT
for p in 0.6 0.8 1.0 1.2; do
  for P in $BASE/phi_$p/plt*; do
    [ -d "$P" ] || continue
    t=$(gettime "$P")
    tmax=$(getmax Temp "$P")
    oh=$(getmax "Y(OH)" "$P")
    h2o=$(getmax "Y(H2O)" "$P")
    co2=$(getmax "Y(CO2)" "$P")
    ch4=$(getmax "Y(CH4)" "$P")
    echo "$p,$t,$tmax,$oh,$h2o,$co2,$ch4" >> $OUT
  done
done
echo "Wrote $OUT"
