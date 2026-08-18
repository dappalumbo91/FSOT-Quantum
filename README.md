# FSOT-Quantum

**Fluid Spacetime Omni-Theory — Quantum_Mechanics / Quantum_Computing domain fold**

Answers the jobs people hire quantum computers and precision-physics codes for, on ordinary GPU/CPU hardware. Zero free parameters. Scale by **folds**, not Hilbert \(2^n\).

| | |
|--|--|
| **Author** | Damian Arthur Palumbo |
| **Pin** | **D1D38A** (`vendor/fsot_compute.py`) |
| **License** | Apache-2.0 |
| **Theory** | [FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean) |
| **Runtime** | [FSOT-GPU](https://github.com/dappalumbo91/FSOT-GPU) `fsot_lib` (vendored) |
| **Mind / body** | [fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig) |

**Read first:** [`docs/STATUS.md`](docs/STATUS.md) — current system, findings, capability.  
**What we can claim:** [`docs/CLAIMS.md`](docs/CLAIMS.md) · **Rungs:** [`docs/LADDER.md`](docs/LADDER.md) · **Reproduce:** [`docs/REPRODUCE.md`](docs/REPRODUCE.md) · **Doc map:** [`docs/INDEX.md`](docs/INDEX.md)

**Current record (2026-08-17):** competitor climb closed on this pin. Audit **20/20** vs YR4/PDG, leftover hired physics **41/41**. Three earlier audit misses were wrong objects (`docs/MISS_THREE.md`), not a pin edit. Exclusive \(B\to D\ell\nu\) is **0.15%** (`docs/V_CB_PUZZLE.md`) — the old 1.1σ was the D+D* blend 0.0398. SH0ES \(H_0\) is Lean BH→WH (Planck **0.024%**, SH0ES **1.00%**) — `docs/H0_TENSION.md`. Gset family **10/11 under 1%**, G17 **1.017%** written not crawled. Contested Lean panel **14/14**. GitHub About text is the repo one-liner; this README, `docs/STATUS.md`, and `docs/CLAIMS.md` are the current record.

---

## What this is

\[
S = K(T_1+T_2+T_3),\quad
\Theta = C_{\mathrm{eff}}\cdot P_{\mathrm{var}},\quad
\kappa_{ij}=A_{\mathrm{bleed}}\cdot\mathrm{POOF}\cdot|S_i||S_j|\big/\bigl(1+|D_i-D_j|/25\bigr)
\]

\(K=\varphi\cdot(\gamma/e)\cdot\sqrt{2}/\ln(\pi)\cdot 99/100\approx 0.420222\) is the universal scale. Change **domain / \(D_{\mathrm{eff}}\) / observed**, not a fit.

Trinary spins: **−1** down · **0** superposed · **+1** up. Consensus, not softmax.

This repo is **not** a second GPU stack. It is the QM/QC fold on the same owned operators already in FSOT-GPU (`seeds`, `scalar`, `trinary`, `coherence`, `consensus`, `learn`, `backend`).

The comparison is the **hired question** (Shor, QAOA/MaxCut, chemistry, constants, QI), not a replay of a fridge or a Hilbert simulator. Those stacks are what this fold is built to replace. Current scores: [`docs/CLAIMS.md`](docs/CLAIMS.md). Mind/body is [fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig).

---

## Current findings (this wrap)

Living numbers. Miss one and the pin is wrong — except where we scored the wrong object, which is written down and fixed without touching the pin.

| Panel | Result | Ledger |
|-------|--------|--------|
| Stale-target audit vs YR4/PDG | **20/20 @ 0.5%** | [`docs/STALE_TARGETS.md`](docs/STALE_TARGETS.md) · [`docs/MISS_THREE.md`](docs/MISS_THREE.md) |
| Harder QC-for (CKM / PMNS / Ising / nuclear / Higgs) | 20/20 @ 0.5% | [`docs/HARDER_QC.md`](docs/HARDER_QC.md) |
| Physics + QI I | 16/16 + 326/326 Lean | [`docs/PHYSICS_QI.md`](docs/PHYSICS_QI.md) |
| Physics + QI II | 22/22 + 126/126 Lean | [`docs/PHYSICS_QI2.md`](docs/PHYSICS_QI2.md) |
| Physics + QI III (leftover hired physics) | **41/41 + 212/212 Lean** | [`docs/PHYSICS_QI3.md`](docs/PHYSICS_QI3.md) |
| Gset family G1–G5 + G14–G17 + G22–G23 | **10/11 under 1%** · G17 1.017% | [`docs/GSET_FAMILY.md`](docs/GSET_FAMILY.md) |
| Hired QC expand (factor / dlog / Simon / SAT / HHL) | **29/29** | [`docs/HIRE_EXPAND.md`](docs/HIRE_EXPAND.md) |
| Hired QC climb (7-digit factor / Simon-16 / TSP / 1e7) | **32/32** | [`docs/HIRE_CLIMB.md`](docs/HIRE_CLIMB.md) |
| Probability as multiverse branching | **19/19** | [`docs/PROBABILITY_BRANCH.md`](docs/PROBABILITY_BRANCH.md) |
| Exclusive \(B\to D\ell\nu\) | **0.15%** vs Belle II 2025 0.0392 | [`docs/V_CB_PUZZLE.md`](docs/V_CB_PUZZLE.md) |
| \(H_0\) Planck / SH0ES | **0.024% / 1.00%** Lean BH→WH | [`docs/H0_TENSION.md`](docs/H0_TENSION.md) |
| \(\alpha_s(M_Z)\) | 0.68% inside vendor **0.9%** band | [`docs/OPEN_REMAINING.md`](docs/OPEN_REMAINING.md) |
| Contested Lean panel | **14/14** | [`docs/CONTESTED_SECTORS.md`](docs/CONTESTED_SECTORS.md) |
| Chemistry pin set | 68/68 @ 0.5% | — |
| \(1/\alpha\), Weinberg, proton radius, water angle | match | [`docs/STATUS.md`](docs/STATUS.md) |
| Inclusive \(\lvert V_{cb}\rvert\) | 0.0422008 vs 0.0422 | inclusive PDG |
| Tsirelson | exact \(2\sqrt{2}\) | — |
| \(S(\mathrm{QM})\), \(S(\mathrm{QC})\) | \(+0.9555\), \(−0.1477\) | emergence / damping |

**Still open, written as open:** Gset G17 **1.017%** (31 edges); champions unmatched (30–114 edges); vendor `BR_H_gg` field still stale (fold already matches YR4). Exclusive 0.0398 and SH0ES 6.30% were wrong objects — see [`docs/CLAIMS.md`](docs/CLAIMS.md).

---

## Quick start

```powershell
git clone https://github.com/dappalumbo91/FSOT-Quantum.git
cd FSOT-Quantum
$env:PYTHONPATH = (Get-Location).Path
pip install -r requirements.txt   # torch optional; pin checks run without it

python -m fsot_quantum check      # pin D1D38A
python -m fsot_quantum audit      # 20/20 vs current literature
python -m fsot_quantum harder     # hired physics 20/20
python -m fsot_quantum push3      # leftover hired physics 41/41
python -m fsot_quantum family     # Gset 10/11 under 1% (G17 1.017%)
```

Optional: clone [FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean) to `_ref\FSOT-2.1-Lean` for the 432-domain atlas. Without it, atlas counts skip; pin domains still score.

CUDA is used when present. Pin and constants do not require a GPU.

---

## Field commands

```powershell
python -m fsot_quantum            # help
python -m fsot_quantum check      # pin / seeds / D_eff vs Lean clone
python -m fsot_quantum status     # print the wrap snapshot path
python -m fsot_quantum accuracy   # hired QC/QM jobs
python -m fsot_quantum ask        # DJ / BV / Grover / Shor / Ising / chem
python -m fsot_quantum hard       # hard questions via K (not foreign circuits)
python -m fsot_quantum fold       # 35 pin + Lean atlas on GPU
python -m fsot_quantum observe    # typical questions + lawful look path
python -m fsot_quantum mind       # how intelligence emerges (not an LLM)
python -m fsot_quantum forward    # known answers + QC-for questions
python -m fsot_quantum harder     # CKM / Ising / nuclear / Gset
python -m fsot_quantum qi         # physics + QI I
python -m fsot_quantum push       # physics + QI II
python -m fsot_quantum push3      # physics + QI III
python -m fsot_quantum audit      # vendor vs YR4/PDG
python -m fsot_quantum family     # Gset G1–G5 + G14–G17 + G22–G23
python -m fsot_quantum open       # diagnosis: wrong-object scoring
python -m fsot_quantum vcb        # inclusive QM vs exclusive B→D HEP
python -m fsot_quantum h0         # Lean BH→WH Hubble
python -m fsot_quantum contested  # Lean contested sectors
python -m fsot_quantum leftovers  # remaining opens (G17)
python -m fsot_quantum hire       # factor / dlog / Simon / SAT / HHL
python -m fsot_quantum hire2      # 7-digit factor / Simon-16 / SAT-16 / TSP
python -m fsot_quantum branch     # probability as \|S\| branching
python -m fsot_quantum formulas   # formula list
python -m fsot_quantum organ      # JSON for neuron-zig
python -m fsot_quantum stamp      # Lean · Coq · Isabelle · F* · Python
python -m fsot_quantum atlas      # full Lean solved atlas
python -m fsot_quantum predict    # preregistered predictions (killable)
.\run_qemu.ps1                    # FSOT-QC-OS on metal
```

Older climb panels (`climb_suite`, `fold_v2`…`fold_v6`, `capability_suite`, …) still run. They are history. The wrap is `docs/STATUS.md`.

---

## Architecture

```
FSOT-2.1-Lean pin D1D38A
        │
        ▼
fsot_lib          seeds · S=K(T1+T2+T3) · collapse · consensus · pack
        │
        ▼
fsot_quantum      domains · questions · Gset · organ export
        ├── GPU when present (organ, not mind)
        ├── formal/  Lean · Coq · Isabelle · F*
        └── zig/     QC-OS (QEMU)
                 │
                 ▼
        fsot-neuron-zig   mind authority
```

Observe path: **QC (dark) → Quantum_Optics (look) → QM (measure)**.  
Do not look at QC. That flip is the Hilbert move.

---

## Related

| Repo | Role |
|------|------|
| [FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean) | Theory pin, 432-domain atlas |
| [FSOT-GPU](https://github.com/dappalumbo91/FSOT-GPU) | Owned GPU/CPU operators |
| [fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig) | Neural mind / body; this fold is the law organ |
| [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics) | Genetics fold |
| [Protofluid-Language-Translator-2.0-Zig](https://github.com/dappalumbo91/Protofluid-Language-Translator-2.0-Zig) | Language densify |

---

## License

Apache-2.0 — see [LICENSE](LICENSE).
