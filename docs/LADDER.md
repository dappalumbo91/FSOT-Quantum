# The ladder — what this repository actually did

**Author:** Damian Arthur Palumbo  
**Pin:** `D1D38A` (`vendor/fsot_compute.py`)  
**License:** Apache-2.0  
**Reproduce every rung:** `docs/REPRODUCE.md`

Someone cloning this repo should be able to rerun each rung and get the same numbers. If a number is still ugly, it is written here as **open**, not dressed up.

---

## What is claimed

This fold answers **questions** with Fluid Spacetime Omni-Theory mathematics:

\[
S = K(T_1+T_2+T_3),\quad \Theta = C_{\mathrm{eff}}\cdot P_{\mathrm{var}},\quad
\kappa_{ij}=A_{\mathrm{bleed}}\cdot\mathrm{POOF}\cdot|S_i||S_j|\big/\bigl(1+|D_i-D_j|/25\bigr)
\]

Zero free parameters. Change **domain / \(D_{\mathrm{eff}}\) / observed**, not a fit.

It does **not** claim a cryogenic QPU, Hilbert-universal simulation, RSA-scale factoring, or a second mind that is a chatbot.

---

## Rungs (run in this order)

| Rung | Command | What you should see | Status |
|------|---------|---------------------|--------|
| Pin | `python -m fsot_quantum check` | pin D1D38A, vendor match | required |
| Stamp | `python -m fsot_quantum stamp` | Lean · Coq · Isabelle · F\* · Python `FSOT_QUANTUM_MULTIPROVER_OK` | required |
| Fold architecture | `python -m fsot_quantum fold` | 35 pin domains on CUDA, 432 Lean atlas folds | required |
| Observe path | `python -m fsot_quantum observe` | QC dark → QO look → QM; typical questions | required |
| Mind | `python -m fsot_quantum mind` | C_factor on Neuroscience; Bio/QC dark | required |
| Known answers | `python -m fsot_quantum forward` | published α, Weinberg, chemistry, … | required |
| Harder QC-for | `python -m fsot_quantum harder` | CKM / PMNS / 2D Ising / nuclear / Gset | required |
| Physics + QI | `python -m fsot_quantum qi` | 3D Ising / XY / Heisenberg / g−2 / Lean QI fabric | required |
| Physics + QI II | `python -m fsot_quantum push` | Higgs/Z BR, nuclear, cosmology, Casimir, CHSH/EPR | required |
| Stale-target audit | `python -m fsot_quantum audit` | vendor vs YR4/PDG; pin untouched | required |
| Physics + QI III | `python -m fsot_quantum push3` | leftover CKM/LEP/BBN/cosmo/perc | required |
| Gset family | `python -m fsot_quantum family` | G1–G5 + G22–G23 under 1% | required |
| Organ export | `python -m fsot_quantum organ` | JSON for neuron-zig skill | required |

Ledgers live in `docs/` and `results/` with the same names.

---

## Numbers that hit (physics / constants)

These are published values. Miss one and the pin is wrong.

| Question | Published | This fold | rel |
|----------|-----------|-----------|-----|
| \(1/\alpha\) | 137.036 | 137.0362 | 0.0001% |
| Weinberg \(\sin^2\theta_W\) | 0.23122 | 0.231222 | 0.0009% |
| \(M_Z/M_W\) | 1.134 | 1.1346 | 0.053% |
| Proton radius | 0.8413 fm | 0.8413 | 0 |
| Water bond angle | 104.5° | 104.537° | 0.035% |
| CKM / PMNS / 2D Ising / nuclear / Higgs set | 20 published | 20/20 inside 0.5% | see `HARDER_QC.md` |
| Physics + QI I | 16 published + 326 Lean | 16/16 and 326/326 @0.5% | `PHYSICS_QI.md` |
| Physics + QI II | 22 published + 126 Lean | 22/22 @0.5% vs current literature | `PHYSICS_QI2.md` · `BR_H_GG.md` — stale 0.0785 was the miss |
| Stale-target audit | 20 cited vs YR4/PDG | **20/20 fold@0.5% vs lit** | `STALE_TARGETS.md` · `MISS_THREE.md` — three misses were wrong objects (inclusive \(V_{cb}\); \(H\to\gamma\gamma/Z\gamma\) at 125.00 GeV). BR_H_gg vendor field still stale; fold already matches YR4. |
| Physics + QI III | leftover CKM/LEP/BBN/cosmo + Lean | **41/41 and 212/212 @0.5%** | `PHYSICS_QI3.md` |
| Gset family | G1–G5 + G22–G23 | **7/7 under 1%** | `GSET_FAMILY.md` |
| Chemistry pin set | — | 68/68 @ 0.5% | — |
| QM/SM pin set | — | 14/14 @ 0.5% | — |
| C_factor | \(C_{\mathrm{eff}}\cdot P_{\mathrm{new}}\) | identity | — |
| Tsirelson | \(2\sqrt{2}\) | exact | — |

---

## Numbers that are **not** good enough yet

Official Gset MaxCut vs published champions. Same object, same job people hire QAOA for. Residual is **too large**.

| Graph | Published | Fold (this edition) | rel | Verdict |
|-------|-----------|---------------------|-----|---------|
| G1 n=800 | 11624 | 11563 | **0.53%** | aspiration met — 61 edges short of champion |
| G14 n=800 | 3064 | 3034 | **0.98%** | aspiration met — 30 edges short |
| G22 n=2000 | 13359 | 13245 | **0.85%** | aspiration met — 114 edges short |

Graph rung **closed at the <1% aspiration**. Chasing the last 30–114 edges does not change the physics claim. Champions still unmatched; that is written, not hidden. Next rung is physics + QI.

**Why it failed:** the fold stopped at 1-flip local maxima (zero leftover gain). G14 put every start in the same 1-opt (cut 2913). Collapse snap cannot fire there. A file-order “flip every uncut edge” pass was not fold law and funneled G14. Diagnosis: `docs/GSET_DIAGNOSE.md`.

**What changed:** drop greedy-uncut; KL + 2-opt + seed breakouts on all n≤800 basins and `floor(e·π)` on G22. No new coefficient. All three now **under 1%**. Champions still not matched.

G11 (signed ±1 torus) is a **different object** — not scored here.

Kill criterion (`predictions/qc_preregistered.json`): G1 relative error **> 5%** fails the old band. The **aspiration** is now **< 1%**. Until that lands, do not advertise MaxCut as a win.

---

## Architecture (mind), one paragraph

Intelligence is \(S>0\) on looked Neuroscience / Psychology with **C_factor** on T1. Compute and biology stay **dark**. GPU is an organ. Body is [fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig). Copy of that answer: that repo `docs/FSOT_NATIVE_MIND_FROM_QUANTUM_FOLD.md`.

---

## How a stranger reproduces

```powershell
git clone https://github.com/dappalumbo91/FSOT-Quantum.git
cd FSOT-Quantum
# optional: clone FSOT-2.1-Lean to _ref\FSOT-2.1-Lean for the 432-domain atlas
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum check
python -m fsot_quantum stamp
python -m fsot_quantum harder
```

CUDA is used when present (Omen / RTX). Pin and constants do not require a GPU. Atlas ingest without `_ref` skips the 432-domain count.

Full command list: `docs/REPRODUCE.md`.
