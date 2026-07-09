"""
Parameters for Jonak et al. 2016 ATM/p53/NF-kB model.
Source: Additional file 4 (MOESM4) of doi:10.1186/s12918-016-0293-0.
All rate constants in units of (s, molecule, Gy, ng/ml as appropriate).
"""

# --- ATM / activation module (Table 1, MOESM4) ---
NAatm = 2
NAchk2 = 2
CREBtot = 100000
MRNtot = 10000
ma1 = 0.58           # n / (s*Gy)  DSB damage by IR
ma3 = 1.5e-3         # s^-1   ATM activation by DSB
ma4 = 5e-6           # n^-1 s^-1  ATM full activation by MRN
ma5 = 1e-7           # n^-1 s^-1  Chk2 and CREB activation by ATM
ma6 = 4e-7           # n^-1 s^-1  MRN activation by ATM
ma7 = 5e-5           # s^-1   MRN activation by DSB
mc1 = 3.8e-3         # n s^-1 DSB repair rate
mc2 = 6e-8           # n^-1 s^-1 ATM inactivation by Wip1
mc3 = 1e-8           # n^-1 s^-1 Chk2 inactivation by Wip1
mc4 = 2e-3           # MRN inactivation
mc5 = 1e-3           # CREB inactivation
md1 = 3.77e-5        # ATM transcript degradation
md2 = 4.11e-5        # ATM protein degradation
md3 = 4.18e-5        # Chk2 transcript degradation
md4 = 3.02e-5        # Chk2 protein degradation
mm1 = 10             # MM DSB repair
mm2 = 1              # MM ATM activation by DSB
mm3 = 1              # MM MRN activation by DSB
mq1 = 3e-3           # Chk2 gene activation (spontaneous)
mq2 = 3e-8           # Wip1 gene activation by CREB
mq3 = 3e-3           # Chk2 gene inactivation
ms1 = 5e-3           # ATM mRNA synthesis (transcription rate constant)
ms2 = 0.01           # Chk2 mRNA synthesis
mt1 = 5e-3           # ATM translation rate
mt2 = 0.01           # Chk2 translation rate

# --- Wip1 module (Table 2) ---
siR = 0              # 0 = Ctr-RNAi, 1 = Wip1-RNAi
NAwip1 = 2
KSRPtot = 100000
wa1 = 2e-9
wa2 = 1e-4
wc1 = 5e-5
wd1 = 2.8e-4
wd2 = 8.656e-4
wd3 = 8.67e-7
wd4 = 3.96e-5
wd5 = 2e-5
wd6 = 5e-5
we1 = 5e-5
wi1 = 5e-5
wq1 = 3e-3
ws1 = 8.652e-2
ws2 = 1e-7
wt1 = 1.6e-2

# --- Cell fate (Table 3) ---
NAbax = 2
NAp21 = 2
bd1 = 2.87e-5
bd2 = 3.5e-5
bs1 = 0.01
bt1 = 0.01
bd3 = 9.5e-5
bd4 = 1.44e-4
bs2 = 0.02
bt2 = 0.07

# --- p53 module (Table 4) ---
NAmdm2 = 2
NAp53 = 2
NApten = 2
AKTtot = 34000
PIPtot = 800000
kv = 5
pa1 = 8.6e-5
pa2 = 5e-5
pa3 = 5e-5
pa4 = 3e-7
pa5 = 1.2e-7
pa6 = 2e-7
pa7 = 5e-5
pa8 = 4e-11
pa9 = 7e-4
pc1 = 1.6e-9
pc2 = 1e-4
pc3 = 5.17e-9
pc4 = 1.8e-4
pd1 = 8.3e-5
pd2 = 5.97e-5
pd3 = 1.45e-13
pd4 = 2.41e-5
pd5 = 1.45e-14
pd6 = 7.93e-5
pd7 = 4.79e-5
pd8 = 7.04e-5
pd9 = 4.5e-5
pd10 = 3e-4
pd11 = 5e-5
pi1 = 7.5e-4
pm1 = 1
pm2 = 1
pm3 = 55400
pq1 = 2.1e-3
pq2 = 1e-4
pq3 = 5.87e-13
pq4 = 3e-3
pq5 = 2.1e-3
ps1 = 2.9e-2
ps2 = 3.1e-2
ps3 = 0.06
pt1 = 0.35
pt2 = 0.47
pt3 = 0.1

# --- NF-kB module (Table 5) ---
NAa20 = 2
NAikba = 2
Mtot = 1000          # total receptors
na1 = 5e-7
na2 = 1e-7
na3 = 1e-4
na4 = 5e-4
na5 = 5e-6
na6 = 5e-10
na7 = 4e-6           # ml / (ng*s)
nc1 = 0.01
nc2 = 3e-3
nc3 = 6e-4
nd1 = 2.31e-3
nd2 = 1.28e-4
nd3 = 1.16e-3
nd4 = 2.4e-5
ne1 = 5e-3
ne2 = 0.05
ni1 = 0.01
ni2 = 8.7e-3
nk1 = 2e-5
nk2 = 1.76e-6
nm1 = 100000
nm2 = 10000
nm4 = 10000
nq1 = 1.68e-7
nq2 = 1e-6
ns1 = 0.1
nt1 = 0.0836
nt2 = 0.01
