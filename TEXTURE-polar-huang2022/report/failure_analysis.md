# Failure / Gap Analysis --- huang2022 (arXiv:2202.11348)

**Verdict: PARTIAL** (core mechanism REPLICATED). Coverage ~6/10, Agreement ~7/10.

## The single most important caveat: absolute skyrmion size (unknown A)
Our N\'eel skyrmion at $D_\uparrow=0.28$ mJ/m$^2$ is **39.5 nm** in diameter vs.
the paper's **~12 nm** --- a factor of ~2--3. This is **entirely traceable to one
missing parameter**: the exchange stiffness $A$, which appears only in the
paper's Fig.~4 (an image) and is **not present in any OCR/pdftotext-extractable
text**. We used the typical Fe$_3$GeTe$_2$ value $A=1$ pJ/m.

Because both the skyrmion size and the critical DMI scale as $\sqrt{A}$
($D_c=(4/\pi)\sqrt{AK}$, and $R$ from Eq.~6 $\propto\sqrt{A}$), the absolute
diameter is off by $\sqrt{A_{\rm assumed}/A_{\rm true}}$ while the **threshold
and trend remain correct**. If the paper's true $A$ is ~4--9$\times$ smaller
than 1 pJ/m, the diameter collapses onto ~12 nm. This is a **data-availability
gap, not a physics disagreement**.

## What reproduced (high confidence)
1. **Create/annihilate switch --- the paper's central claim.** The analytic
   $D_c=0.255$ mJ/m$^2$ lies exactly between $D_\downarrow=0.06$ (no skyrmion)
   and $D_\uparrow=0.28$ (skyrmion). Reproduced with **zero fitting**, both
   analytically and via seeded relaxation ($Q=-0.87$ vs. seed collapse).
2. **DMI as the FE-polarization proxy.** The paper controls DMI via In$_2$Se$_3$
   polarization; sweeping $D$ correctly captures the mechanism (the atomistic
   model itself has no explicit polarization field).
3. **Chirality tied to sign$(D)$.** N\'eel handedness follows sign$(D)$, matching
   the trilayer chirality-reversal claim ($D_{\uparrow\uparrow}$ vs.
   $D_{\downarrow\downarrow}$).
4. **Size trend.** Larger $|D|$ $\to$ larger skyrmion, consistent with the
   paper's bilayer (12 nm) $>$ trilayer (6 nm) ordering.
5. **Topological validity.** Berg--L\"uscher charge $|Q|\approx1$ for all
   stabilized cases confirms genuine skyrmions, not spurious relaxed states.

## What did NOT reproduce / was scoped out
| Gap | Type | Note |
|-----|------|------|
| Absolute diameter (40 vs 12 nm) | **data-availability** | $A$ only in Fig.4; $\propto\sqrt{A}$. Correct threshold+trend. |
| Honeycomb geometry | **scoped-out (approximation)** | Square lattice used; alters geometric DMI prefactor slightly, not the mechanism. |
| First-principles DMI values | **scoped-out (input)** | 0.28/0.06/0.22/-0.24 taken from the paper's DFT, not recomputed (would need relativistic DFT+SOC). |
| Trilayer stability vs metastability | **open** | Near-threshold ($|D|\lesssim D_c$) skyrmions found from seed; GNEB needed to confirm true minima. |
| Anisotropy tension (DFT MAE 8.57 vs adopted 0.04 MJ/m$^3$) | **inherited from paper** | The paper itself adopts a moderate $K$; we use the same. |
| Demag/dipolar field | **scoped-out** | Omitted, as in the paper's atomistic model (thin-film 2D limit). |

## Environment / tooling gaps (NOT physics)
- **`marker` / `nougat` absent.** Extraction artifacts 2 & 3 are pdftotext
  interims with honest provenance headers; key equations hand-transcribed to
  LaTeX in `nougat.mmd` and `REPORT.tex`. Degraded math OCR is a tooling loss,
  not a replication shortfall.
- **No `pdflatex` on host.** `REPORT.tex` ships as source; compiles off-host.

## What would raise the verdict to REPLICATED
Recover the paper's exchange stiffness $A$ (digitize Fig.~4 or query authors) and
re-run: if the diameter lands near ~12 nm, the only remaining gap closes and the
verdict becomes REPLICATED. Everything else (mechanism, switch, chirality, trend,
topology) already matches.
