# Spin texture of an irradiated warped topological insulator surface

**Debabrata Sinha** — The Institute of Mathematical Sciences, Chennai; TIFR Centre for Interdisciplinary Sciences, Hyderabad
arXiv:1604.04081v2 [cond-mat.str-el] 16 Aug 2016 · EPL (Europhysics Letters)

> **EXTRACTION NOTE.** The `marker` and `nougat` neural PDF-to-markdown binaries
> are not installed in this environment (`which marker_single nougat` → empty;
> only `/usr/bin/pdftotext` is present). This file is therefore an **interim,
> hand-normalized markdown transcription** produced from `pdftotext -layout`
> output (`extraction/pdftotext_layout.txt`) plus the pre-existing corpus text
> dump (`../textures-polar-sinha2016.txt`), with equations reconstructed into
> LaTeX from the two-column raw stream. It carries the same structural content a
> marker run would (headers, equations, figure captions) but was not produced
> by the marker pipeline. Regenerate with marker when the binary is available.

## Abstract

Topological insulator is a new state of matter which exhibits exotic surface
electronic properties. Determining the spin texture is of paramount importance
for understanding its topological order and for spintronics applications. Here
the author investigates the surface state of a TI with hexagonal warping
subjected to an **off-resonant circularly polarized light**. The resulting
electronic ground state exhibits a novel spin texture that **breaks the
conventional spin-momentum locking**. The observed spin texture is shown to be
a consequence of the symmetry group ($C_{3v}$) of the underlying crystal.

## Model and Floquet Theory

Warped TI surface Hamiltonian (Fu model):

$$H_0(\vec k) = \hbar v k\,(k_x\sigma_y - k_y\sigma_x) + \frac{\lambda}{2}(k_+^3 + k_-^3)\sigma_z \tag{1}$$

with $k_\pm = k_x \pm i k_y$. First term = spin-orbit (spin-momentum) locking;
last term = cubic (hexagonal) warping, invariant under $C_{3v}$.

Circularly polarized drive via Peierls substitution $\hbar k_i \to \hbar k_i + eA_i$,
$\vec A(t) = A_0(\sin\omega t, \cos\omega t)$. Time-dependent Hamiltonian
$H(\vec k,t) = H_0 + V(t)$ with

$$V(t) = ev[A_x\sigma_y - A_y\sigma_x] + \frac{3e\lambda}{2\hbar}[k_+^2 A_+ + k_-^2 A_-]\sigma_z + O(A^2,A^3).$$

**Off-resonant (van Vleck / high-frequency) effective Hamiltonian:**

$$H_{\rm eff} = H_0 + \frac{[V_{-1}, V_{+1}]}{\hbar\omega} \tag{3}$$

with $V_{-1} = i\alpha(i\sigma_x - \sigma_y) + i\beta[2ik_xk_y - (k_x^2-k_y^2)]\sigma_z$,
$V_{+1} = V_{-1}^\dagger$, $\alpha = \tfrac{evA_0}{2}$, $\beta = \tfrac{3e\lambda A_0}{2\hbar}$.

Result:

$$H_{\rm eff} = \hbar v[(k_x + K_1)\sigma_y - (k_y + K_2)\sigma_x] + \frac{\lambda}{2}(k_+^3+k_-^3)\sigma_z + \Delta_\omega\sigma_z \tag{4}$$

with $K_1 = -\frac{4\alpha\beta}{\hbar^2\omega v}(k_x^2-k_y^2)$,
$K_2 = \frac{8\alpha\beta}{\hbar^2\omega v}k_xk_y$, and the **light-induced gap**
$\Delta_\omega = \frac{4\alpha^2}{\hbar\omega} = \frac{(evA_0)^2}{\hbar\omega}$.

Matrix form:

$$H_{\rm eff} = \begin{pmatrix} \Delta(k,\theta) & \hbar v(-ik_- + iak_+^2) \\ \hbar v(ik_+ - iak_-^2) & -\Delta(k,\theta)\end{pmatrix} \tag{5}$$

with $\Delta(\vec k,\theta) = \lambda k^3\cos(3\theta) + \Delta_\omega = \lambda(k_x^3 - 3k_xk_y^2) + \Delta_\omega$,
$\theta = \tan^{-1}(k_y/k_x)$, and $a = \frac{4\alpha\beta}{\hbar^2\omega v}$.

**Energy eigenvalues:**

$$E(\vec k) = s\sqrt{\Delta(\vec k,\theta)^2 + \hbar^2v^2(k^2 + a^2k^4 - 2ak^3\cos 3\theta)} \tag{6}$$

$s = \pm$ (conduction/valence). Band structure is three-fold symmetric
($\theta \to \theta \pm 2\pi/3$), reduced from the six-fold symmetry of the
time-reversal-symmetric case — signature of TR breaking.

**Parameters (paper):** $\hbar\omega = 8$ eV, $\lambda = 0.2$ eV·nm³.
- $evA_0 = 0.5$ eV → $a = 0.17$ nm, $\Delta_\omega = 0.03$ eV
- $evA_0 = 0.9$ eV → $a = 0.55$ nm, $\Delta_\omega = 0.10$ eV

## Spin Texture (Eqs. 9–11)

$$S_x = \frac{\hbar}{2}\,C_s^2\,\frac{\hbar v[-4ak_xk_y - 2k_y]}{E_s+\Delta} \tag{9}$$
$$S_y = \frac{\hbar}{2}\,C_s^2\,\frac{\hbar v[-2a(k_x^2-k_y^2) + 2k_x]}{E_s+\Delta} \tag{10}$$
$$S_z = \frac{\hbar}{2}\,C_s^2\left[1 - \frac{\hbar^2v^2(k^2 + a^2k^4 - 2ak^3\cos 3\theta)}{(E_s+\Delta)^2}\right] \tag{11}$$

with $C_s^2 = \left[1 + \frac{\hbar^2v^2(k^2+a^2k^4-2ak^3\cos 3\theta)}{(E_s+\Delta)^2}\right]^{-1}$ (Eq. 8).

## In-Plane Spin Density (Eq. 12–13)

$$S_{\rm tot}(k,\theta) = \frac{\hbar v k\sqrt{1 + a^2k^2 - 2ak\cos 3\theta}}{\sqrt{\hbar^2v^2k^2(1+a^2k^2-2ak\cos 3\theta) + \Delta^2}}\,C_s^2 \tag{12}$$

For $a=0$, $\Delta_\omega=0$ (gapless): $S_{\rm tot} = \hbar vk/\sqrt{\hbar^2v^2k^2 + \lambda^2k^6\cos^2 3\theta}$ (Eq. 13), six-fold symmetric.

## Out-of-Plane Spin (Eq. 14) & TR breaking

Gapless ($a=0,\Delta_\omega=0$): $S_z = \pm\frac{\hbar}{2}\frac{\lambda(k_x^3-3k_xk_y^2)}{\sqrt{\hbar^2v^2k^2+\lambda^2(k_x^3-3k_xk_y^2)^2}}$ (Eq. 14) — symmetric ±, net $S_z = 0$ (TR invariance).
Floquet (gapped): $S_z$ picks up **maximum $\hbar/2$ at $k=0$** due to TR breaking.

## Angle of Deviation (Eq. 15)

$$\delta_\omega = \cos^{-1}\!\left[\frac{-ak\sin 3\theta}{\sqrt{1 + a^2k^2 - 2ak\cos 3\theta}}\right] - \frac{\pi}{2} \tag{15}$$

$\delta_\omega = 0$ for $\theta = 0$ or $\pm\pi/3$ **independent of k**. For other
$\theta$ it has symmetric ± regions — the deviation from perpendicularity is the
direct measure of broken spin-momentum locking. Along $\Gamma$–M
($H_{\rm eff}^{\Gamma-M} = \hbar v[ak_y^2\sigma_y - k_y\sigma_x] + \Delta_\omega\sigma_z$,
Eq. 16) the $ak_y^2\sigma_y$ term breaks mirror symmetry → finite $S_y$ →
non-orthogonal spin. Along $\Gamma$–K (Eq. 17) only $S_y$ survives → orthogonal.

## Conclusions

Off-resonant circularly polarized light on a hexagonally warped TI surface
(i) opens a TR-breaking gap $2\Delta_\omega$ and (ii) breaks the conventional
in-plane spin-momentum locking, producing a $C_{3v}$-symmetric non-trivial spin
texture. Unlike the higher-order-warping mechanism of Ref. [22] (which gives
$\delta_\omega=0$ along both $\Gamma$–K and $\Gamma$–M), the light-induced
texture has $\delta_\omega=0$ only along $\Gamma$–K and $\theta=\pi/3$ — the
distinguishing experimental fingerprint.
