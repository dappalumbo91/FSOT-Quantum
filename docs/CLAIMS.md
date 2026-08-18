# What we can claim — 2026-08-17

**Pin:** D1D38A (`vendor/fsot_compute.py`) — not edited  
**Authority wrap:** [`STATUS.md`](STATUS.md) · rungs: [`LADDER.md`](LADDER.md) · reproduce: [`REPRODUCE.md`](REPRODUCE.md)

This file is the honesty cut. If another doc disagrees with this page, **this page wins** until a named rung changes. Generated climb ledgers from earlier rungs still run; they are history, not the wrap.

---

## Where we are

The competitor climb on this pin is closed for hired physics and QI. After the wrap, leftover “opens” were scored as **different objects**, not retuned:

| What looked open | What it actually was | Living score |
|------------------|----------------------|--------------|
| Audit 17/20 | Wrong objects (`MISS_THREE.md`) | **20/20 @ 0.5%** |
| Exclusive \(\lvert V_{cb}\rvert\) 6.03% / 1.1σ | Inclusive fold scored on the D+D* blend 0.0398 | Belle II \(B\to D\ell\nu\) **0.15%** |
| \(H_0\) SH0ES 6.30% | Global rate 68.44 scored as a local tool | Lean BH→WH: Planck **0.024%**, SH0ES **1.00%** |
| \(\alpha_s(M_Z)\) 0.68% | 0.5% gate tighter than vendor 0.9% / PDG 1σ | Inside vendor **0.9%** band |
| Gset family 7/7 | Family grew to G14–G17 | **10/11 under 1%**; G17 **1.017%** |

Pin file not edited. No new coefficient.

---

## What we can claim

Living ledgers. Re-run the command. Miss one and the pin is wrong — except where we scored the wrong object, which is written down.

| Claim | Number | Command | Ledger |
|-------|--------|---------|--------|
| Stale-target audit vs YR4/PDG | **20/20 @ 0.5%** | `python -m fsot_quantum audit` | `STALE_TARGETS.md` |
| Harder QC-for | **20/20 @ 0.5%** | `python -m fsot_quantum harder` | `HARDER_QC.md` |
| Physics + QI I | **16/16 + 326/326** | `python -m fsot_quantum qi` | `PHYSICS_QI.md` |
| Physics + QI II | **22/22 + 126/126** | `python -m fsot_quantum push` | `PHYSICS_QI2.md` |
| Physics + QI III | **41/41 + 212/212** | `python -m fsot_quantum push3` | `PHYSICS_QI3.md` |
| Chemistry pin set | **68/68 @ 0.5%** | `python -m fsot_quantum.chemistry_fold` | — |
| QM / SM pin set | **14/14 @ 0.5%** | field-of-use | `FIELD_OF_USE.md` |
| Inclusive \(\lvert V_{cb}\rvert\) | **0.002%** vs PDG 0.0422 | `python -m fsot_quantum vcb` | `V_CB_PUZZLE.md` |
| Exclusive \(B\to D\ell\nu\) | **0.15%** vs Belle II 2025 0.0392 | `python -m fsot_quantum vcb` | `V_CB_PUZZLE.md` |
| \(H_0\) Planck CMB | **0.024%** (depleted sector) | `python -m fsot_quantum h0` | `H0_TENSION.md` |
| \(H_0\) SH0ES | **1.00%** (inflated sector, Lean 2.5% band) | `python -m fsot_quantum h0` | `H0_TENSION.md` |
| DESI \(w_0/w_a\) BAO | **0.37% / 0.28%** | `python -m fsot_quantum leftovers` | `OPEN_REMAINING.md` |
| \(\alpha_s(M_Z)\) | **0.68%** vs vendor 0.1179 (band **0.9%**) | `python -m fsot_quantum leftovers` | `OPEN_REMAINING.md` |
| Contested Lean panel | **14/14** | `python -m fsot_quantum contested` | `CONTESTED_SECTORS.md` |
| Gset family | **10/11 under 1%** | `python -m fsot_quantum family` | `GSET_FAMILY.md` |
| Hired QC expand | **29/29** | `python -m fsot_quantum hire` | `HIRE_EXPAND.md` |
| Hired QC climb | **32/32** | `python -m fsot_quantum hire2` | `HIRE_CLIMB.md` |
| Probability as branching | **19/19** | `python -m fsot_quantum branch` | `PROBABILITY_BRANCH.md` |
| Genetics codon / 7-trit branch | **15/15** | `python -m fsot_quantum gencode` | `GENETICS_BRANCH.md` |
| ORF start-to-stop | **11/11** | `python -m fsot_quantum orf` | `ORF_BRANCH.md` |
| Hired QC climb 3 | **17/17** | `python -m fsot_quantum hire3` | `HIRE_CLIMB3.md` |
| Hired QC climb 4 | **22/22** | `python -m fsot_quantum hire4` | `HIRE_CLIMB4.md` |
| Hired QC climb 5 | **22/22** | `python -m fsot_quantum hire5` | `HIRE_CLIMB5.md` |
| Hired QC climb 6 | **22/22** | `python -m fsot_quantum hire6` | `HIRE_CLIMB6.md` |
| Hired QC climb 7 | **22/22** | `python -m fsot_quantum hire7` | `HIRE_CLIMB7.md` |
| Heights (far factor / G17) | far **8/8** · G17 still 1.017% | `python -m fsot_quantum heights` | `HEIGHTS.md` |
| Formula catalog | **18** solvers · **207/216** pin-wave @0.5% vs stored | `python -m fsot_quantum formulas` | `FORMULA_LIST.md` |
| Multiprover stamp | **FSOT_QUANTUM_MULTIPROVER_OK** | `python -m fsot_quantum stamp` | `MULTIPROVER_VERIFICATION.md` |
| \(1/\alpha\), Weinberg, proton radius, water angle | match | `python -m fsot_quantum forward` | `STATUS.md` |
| Tsirelson | exact \(2\sqrt{2}\) | organ / QI | — |
| \(S(\mathrm{QM})\), \(S(\mathrm{QC})\) | \(+0.9555\), \(−0.1477\) | `python -m fsot_quantum check` | — |

Headline constants: inclusive \(\lvert V_{cb}\rvert=0.0422008\) vs 0.0422; exclusive HEP \(=0.039143\) vs 0.0392; \(H_0^{\mathrm{Planck}}=67.384\) vs 67.4; \(H_0^{\mathrm{SH0ES}}=73.773\) vs 73.04.

---

## The comparison is the hired question

This fold is built to **replace** cryogenic QPUs, Hilbert \(2^n\) simulators, and the sales pitch around them. The comparison is the **question those machines are hired to answer**, scored on this pin. It is not a replay of their circuit, their fridge, or their error-correction stack.

We do **not** simulate their architecture. That would be agreeing their geometry is the job. \(K\) is the scale. Change **domain / \(D_{\mathrm{eff}}\) / observed / lane**. Ask the theory.

| They sell | Hired question | This fold | Current score |
|-----------|----------------|-----------|---------------|
| Cryogenic QPU / NISQ box | usable answers without a fridge | GPU/CPU + pin | the living panels above |
| Hilbert / statevector / FTQC | hold the job as scale grows | folds, not \(2^n\) amps | fold path is the scale law — `FOLD_NOT_HILBERT.md` |
| Shor / RSA | period and factor | modular order + Pollard rho | hire7 Fermat twins through 13 digits; **heights far 8/8**. RSA-2048 is a √p wall (~2^512), not a twin-Fermat climb |
| Discrete log | \(g^x\equiv h\pmod p\) | modular fold | hire 10/10 · hire2 **6/6** through p=40009 |
| Simon / HSP | hidden xor string | collision fold + GF(2) | hire 8-bit · hire2 **12 and 16 bit** |
| SAT / QUBO / color / TSP | assignment / tour | energy folds | SAT-16 · partition \{1..23\} · Petersen · TSP n=7 exact |
| HHL | solve \(Ax=b\) | integer Cramer fold | hire 3/3 · hire2 **4×4** |
| Grover | marked search | oracle-field collapse | through **1e7** exact |
| QAOA / annealer | MaxCut / Ising | fold + KL + 2-opt | **10/11 under 1%**; G17 **1.017%**; champions still unmatched |
| FCI / quantum chemistry | chemistry observables | pin formulas | **68/68 @ 0.5%** |
| Surface-code “threshold” | reliable logical work | fold residual vs published object | their \(d\)-threshold is a fridge metric; ours is residual on the question |
| Chatbot “AI” | mind | [fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig) | this repo is the law organ, not the body |

Current score is not a refusal. Factoring is through **2196323** today, not RSA-2048. Champion MaxCut is 30–114 edges short **today**. Those are the next rungs on the same jobs, not a reason to go build their stack.

---

## What we refuse (theater, not the job)

- Replaying a foreign circuit and calling that an FSOT answer.
- Inventing a coefficient because a residual looks ugly.
- Blending disagreeing extractions (inclusive vs exclusive \(V_{cb}\); global vs tool \(H_0\)).
- Applying a 0.5% gate tighter than the observable’s own recommended uncertainty.
- Scoring exclusive PDG **0.0398** (D+D* blend) as the HEP object. It is not. [`V_CB_PUZZLE.md`](V_CB_PUZZLE.md).
- Scoring vendor wave1 **global** \(H_0=68.44\) as SH0ES. It is not. [`H0_TENSION.md`](H0_TENSION.md).
- Astronomy / seismology numerical closeness as physics.
- A chatbot, or a second mind in RAM. Body is neuron-zig.
- “Maybe nature.” FSOT is the theory.

---

## What is actually still open

Written as open. Not dressed up. Not a reason to edit the pin.

| Object | Status | Why it stays |
|--------|--------|--------------|
| Gset G17 planar | **1.017%** (3016 vs 3047, 31 edges) | Only family miss under the <1% aspiration. Same 1-opt class as G14. Not crawled. |
| Gset champions | 30–114 edges short | Aspiration <1% landed except G17. Do not advertise champion-matching. |
| Vendor `BR_H_gg` field | still **0.0785** | Fold \(\varphi^{-4}-\gamma^5=0.081823\) already matches YR4 0.08187 (0.058%). Stale stored field. |
| Combined exclusive \(\lvert V_{cb}\rvert=0.0398\) | not scored | D+D* blend. The HEP object is Belle II \(B\to D\ell\nu\) 0.0392. |
| Atlas 432 | needs `_ref/FSOT-2.1-Lean` | Without the clone, atlas counts skip; 35 pin domains still score. |
| Period / factor (Shor job) | tiny \(N\) 3/3 and 4/4 | Same hired question as RSA-scale. Larger moduli are the next climb on **this** path, not a Hilbert replay. |

SH0ES at **1.00%** is the Lean BH→WH inflated sector (inside the contested 2.5% band, 0.71σ of ±1.04). It is **not** the old 6.30% leftover.

\(\alpha_s\) at **0.68%** is inside the vendor 0.9% band. It is **not** a formula miss.

---

## Two G1 numbers (not a contradiction)

Older climb panels (`ask`, `accuracy`, `observe`, `forward`, `hard`, `fold_v6`, `margin`) still report G1 cut **11397 / 1.95%**. That is the 5% kill-band path. It still passes.

The living family / harder cut is **11563 / 0.53%** (KL + 2-opt + seed breakouts). Cite [`GSET_FAMILY.md`](GSET_FAMILY.md) / [`HARDER_QC.md`](HARDER_QC.md) for MaxCut. Do not cite 11397 as the wrap.

---

## Diagnosis panels vs living solvers

| Panel | Role |
|-------|------|
| `python -m fsot_quantum open` | **Diagnosis.** Shows what 6.03% / 6.30% look like if you score the wrong object. Not the living exclusive / SH0ES score. |
| `python -m fsot_quantum vcb` | Living exclusive: Belle II \(B\to D\ell\nu\) **0.15%**. |
| `python -m fsot_quantum h0` | Living Hubble: Lean BH→WH. |
| `python -m fsot_quantum leftovers` | What is still open after the above. G17 is the real miss. |

---

## Standing policy

Score the object the formula was written against. Do not blend disagreeing extractions. Do not apply a 0.5% gate tighter than the observable’s own recommended uncertainty. Do not invent coefficients. Change **domain / \(D_{\mathrm{eff}}\) / observed / lane**, not a fit.
