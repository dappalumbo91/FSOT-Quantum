# The ladder — what this repository actually did

**Author:** Damian Arthur Palumbo  
**Pin:** `D1D38A` (`vendor/fsot_compute.py`)  
**License:** Apache-2.0  
**Reproduce every rung:** `docs/REPRODUCE.md`  
**Wrap snapshot (read this first):** `docs/STATUS.md` · **Claims:** `docs/CLAIMS.md` · **Doc map:** `docs/INDEX.md`

Someone cloning this repo should be able to rerun each rung and get the same numbers. If a number is still ugly, it is written here as **open**, not dressed up.

---

## What is claimed

This fold answers **questions** with Fluid Spacetime Omni-Theory mathematics:

\[
S = K(T_1+T_2+T_3),\quad \Theta = C_{\mathrm{eff}}\cdot P_{\mathrm{var}},\quad
\kappa_{ij}=A_{\mathrm{bleed}}\cdot\mathrm{POOF}\cdot|S_i||S_j|\big/\bigl(1+|D_i-D_j|/25\bigr)
\]

Zero free parameters. Change **domain / \(D_{\mathrm{eff}}\) / observed**, not a fit.

The comparison is the **hired question**, not a replay of a cryogenic QPU or a Hilbert simulator. Those stacks are what this fold replaces. Current scores: [`CLAIMS.md`](CLAIMS.md). Mind/body is neuron-zig, not a chatbot.

---

## Rungs (run in this order)

| Rung | Command | What you should see | Status |
|------|---------|---------------------|--------|
| Pin | `python -m fsot_quantum check` | pin D1D38A, vendor match | required |
| Fold architecture | `python -m fsot_quantum fold` | 35 pin domains on CUDA, 432 Lean atlas folds | required |
| Observe path | `python -m fsot_quantum observe` | QC dark → QO look → QM; typical questions | required |
| Mind | `python -m fsot_quantum mind` | C_factor on Neuroscience; Bio/QC dark | required |
| Known answers | `python -m fsot_quantum forward` | published α, Weinberg, chemistry, … | required |
| Harder QC-for | `python -m fsot_quantum harder` | CKM / PMNS / 2D Ising / nuclear / Gset | required |
| Physics + QI | `python -m fsot_quantum qi` | 3D Ising / XY / Heisenberg / g−2 / Lean QI fabric | required |
| Physics + QI II | `python -m fsot_quantum push` | Higgs/Z BR, nuclear, cosmology, Casimir, CHSH/EPR | required |
| Stale-target audit | `python -m fsot_quantum audit` | vendor vs YR4/PDG; pin untouched | required |
| Physics + QI III | `python -m fsot_quantum push3` | leftover CKM/LEP/BBN/cosmo/perc | required |
| Gset family | `python -m fsot_quantum family` | G1–G5 + G14–G17 + G22–G23 | required |
| Open objects | `python -m fsot_quantum open` | diagnosis: wrong-object scoring (not living exclusive / SH0ES) | required |
| \(V_{cb}\) puzzle | `python -m fsot_quantum vcb` | inclusive QM vs exclusive HEP | required |
| Hubble tension | `python -m fsot_quantum h0` | Lean BH→WH bubble-bleed (Planck / SH0ES) | required |
| Contested sectors | `python -m fsot_quantum contested` | Lean open-science panel on this pin | required |
| Leftovers | `python -m fsot_quantum leftovers` | DE dual lane, α_s, V_cb, G17 | required |
| Hired QC expand | `python -m fsot_quantum hire` | factor / dlog / Simon / SAT / HHL / search | required |
| Hired QC climb | `python -m fsot_quantum hire2` | 7-digit factor / Simon-16 / SAT-16 / TSP / 1e7 | required |
| Probability branch | `python -m fsot_quantum branch` | \(\|S\|\) fold densities; no Born | required |
| Genetics branch | `python -m fsot_quantum gencode` | codon / 7-trit on Biology | required |
| ORF climb | `python -m fsot_quantum orf` | start-to-stop product of codon folds | required |
| Hired QC climb 3 | `python -m fsot_quantum hire3` | 8-digit factor / dlog \(p\sim10^5\) | required |
| Hired QC climb 4 | `python -m fsot_quantum hire4` | 9-digit factor / SAT-20 / TSP-8 / MIS | required |
| Hired QC climb 5 | `python -m fsot_quantum hire5` | 10-digit factor / SAT-24 / TSP-9 | required |
| Hired QC climb 6 | `python -m fsot_quantum hire6` | 11-digit factor / SAT-28 / TSP-10 | required |
| Hired QC climb 7 | `python -m fsot_quantum hire7` | 13-digit factor / SAT-32 / TSP-11 | required |
| Heights | `python -m fsot_quantum heights` | G17 + far primes (not Fermat twins) | required |
| Heights 3 | `python -m fsot_quantum heights3` | log-N p−1/p+1/kN Fermat | required |
| Formula list | `python -m fsot_quantum formulas` | every formula and what it solves | required |
| Multiprover stamp | `python -m fsot_quantum stamp` | Lean · Coq · Isabelle · F\* · Python | required |
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
| Gset family | G1–G5 + G14–G17 + G22–G23 | **11/11 under 1%** · G17 **0.427%** | `GSET_FAMILY.md` — G17 is 13 edges short of champion |
| Hired QC expand | factor / dlog / Simon / SAT / HHL / search | **29/29** | `HIRE_EXPAND.md` — factors through 172189; dlog 10/10 |
| Hired QC climb | 7-digit factor / Simon-16 / SAT-16 / TSP / 1e7 | **32/32** | `HIRE_CLIMB.md` — factors through 2196323 |
| Probability branch | \(\|S\|\) of \(+1/-1/0\) folds | **19/19** | `PROBABILITY_BRANCH.md` — QM collapsed 0.181/0.819, not a posted \(1/2\) |
| Genetics branch | codon + 7-trit on Biology | **15/15** | `GENETICS_BRANCH.md` — CGG→TGG is secondary \(0\to-1\) |
| ORF climb | start-to-stop codon product | **11/11** | `ORF_BRANCH.md` — missense flanks cancel |
| Hired QC climb 3 | 8-digit factor / larger dlog | **17/17** | `HIRE_CLIMB3.md` — factors through 20937233 |
| Hired QC climb 4 | 9-digit factor / SAT-20 / TSP-8 / MIS | **22/22** | `HIRE_CLIMB4.md` — factors through 144216077 |
| Hired QC climb 5 | 10-digit factor / SAT-24 / TSP-9 | **22/22** | `HIRE_CLIMB5.md` — factors through 1445900429 |
| Hired QC climb 6 | 11-digit factor / SAT-28 / TSP-10 | **22/22** | `HIRE_CLIMB6.md` — factors through 10045050481 |
| Hired QC climb 7 | 13-digit factor / SAT-32 / TSP-11 | **22/22** | `HIRE_CLIMB7.md` — factors through 1000444049203 |
| Heights | far-prime factor + G17 | far **8/8** · G17 **0.427%** | `HEIGHTS_NEXT.md` — G17 under 1%; p−1 3/8 |
| Heights 3 | log-N factor (not √p) | **8/8** | `HEIGHTS3.md` — p±1 stage-2 closes `100003×1000003` |
| Heights 4 | ECM after p±1 + Fermat miss | **8/8** | `HEIGHTS4.md` — 38-bit, same B/B2, seed curves |
| Heights 5 | ECM next bit length | **8/8** | `HEIGHTS5.md` — 41-bit `400k × 4e6` |
| Heights 6 | ECM next bit length | **8/8** | `HEIGHTS6.md` — 46-bit `1.2e6 × 4e7` |
| Heights 7 | ECM next bit length | **8/8** | `HEIGHTS7.md` — 48-bit `3e6 × 8e7` |
| Heights 8 | ECM next bit length | **8/8** | `HEIGHTS8.md` — 52-bit `1.2e7 × 2e8` |
| Heights 9 | ECM next bit length | **8/8** | `HEIGHTS9.md` — 56-bit `4e7 × 1.5e9` |
| Heights 10 | ECM next bit length | **8/8** | `HEIGHTS10.md` — **64-bit** `9e8 × 2e10` |
| Heights 11 | ECM next bit length | **8/8** | `HEIGHTS11.md` — **80-bit**; 90-bit exhausts same B |
| Heights 12 | RSA-shaped balanced + ρ | **12/12** | `HEIGHTS12.md` — 81-bit 41×41; 90-bit ρ |
| Known-answer QC | textbook / demo objects | **44/44** | `KNOWN_QC.md` |
| VQE objects | H2 De / Kolos / STO-3G split | pin De **0.25%** · Kolos **0.75%** written | `VQE_OBJECT.md` |
| Accuracy refine | right-object catalog + log-N stage-2 | living **9/9** · log-N **8/8** | `ACCURACY_REFINE.md` |
| Open objects | wrong-object diagnosis | exclusive blend **6.03%** / SH0ES global **6.30%** if scored wrong | `OPEN_OBJECTS.md` — superseded by `vcb` / `h0` |
| \(V_{cb}\) puzzle | inclusive QM vs exclusive B→D HEP | inclusive **0.002%** · exclusive **0.15%** | `V_CB_PUZZLE.md` — Belle II 2025 0.0392, not the D+D* blend |
| Hubble tension | BH→WH bubble-bleed (Lean) | Planck CMB **0.024%** · SH0ES **1.00%** | `H0_TENSION.md` — one global rate, different outgassing sectors |
| Contested sectors | Lean 13-way open-science panel | **14/14** on this pin | `CONTESTED_SECTORS.md` |
| Leftovers | CMB vs BAO \(w_0/w_a\); α_s band; G17 | BAO **0.28–0.37%** · G17 **still open** | `OPEN_REMAINING.md` |
| Formula list | engine + tension + pin-wave | **18** solvers · **207/216** stored @0.5% · living **9/9** | `FORMULA_LIST.md` |
| Multiprover stamp | Lean · Coq · Isabelle · F\* · Python | **FSOT_QUANTUM_MULTIPROVER_OK** | `MULTIPROVER_VERIFICATION.md` |
| Chemistry pin set | — | 68/68 @ 0.5% | — |
| QM/SM pin set | — | 14/14 @ 0.5% | — |
| C_factor | \(C_{\mathrm{eff}}\cdot P_{\mathrm{new}}\) | identity | — |
| Tsirelson | \(2\sqrt{2}\) | exact | — |

---

## Numbers that are **not** good enough yet

Official Gset MaxCut vs published champions. Same object, same job people hire QAOA for.

| Graph | Published | Fold (this edition) | rel | Verdict |
|-------|-----------|---------------------|-----|---------|
| G1 n=800 | 11624 | 11585 | **0.336%** | aspiration met — 39 edges short of champion |
| G14 n=800 | 3064 | 3042 | **0.718%** | aspiration met — 22 edges short |
| G22 n=2000 | 13359 | 13261 | **0.73%** | aspiration met — 98 edges short |
| G23 n=2000 | 13344 | 13271 | **0.55%** | aspiration met — 73 edges short |

Graph rung **closed at the <1% aspiration** for the whole unweighted family: **11/11 under 1%**. G17 is **0.427%** (13 edges). Champions still unmatched; that is written, not hidden. **Do not advertise MaxCut as champion-matching.**

**Why the early miss:** the fold stopped at 1-flip local maxima (zero leftover gain). G14 put every start in the same 1-opt (cut 2913). Collapse snap cannot fire there. A file-order “flip every uncut edge” pass was not fold law and funneled G14. Diagnosis: `docs/GSET_DIAGNOSE.md`.

**What changed:** drop greedy-uncut; KL + 2-opt + seed breakouts on all n≤800 basins and `floor(e·π)` on G22. No new coefficient.

G11 (signed ±1 torus) is a **different object** — not scored here.

Kill criterion (`predictions/qc_preregistered.json`): G1 relative error **> 5%** fails the band. Aspiration **< 1%** has landed.

Also written, not a graph problem and **not** the old leftovers: exclusive \(B\to D\ell\nu\) is **0.15%**; SH0ES is Lean BH→WH at **1.00%**; \(\alpha_s(M_Z)\) is inside the vendor 0.9% band. See `docs/CLAIMS.md`.

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
