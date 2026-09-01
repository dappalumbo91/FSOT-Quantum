# Consumer hardware vs a quantum computer — where we actually are

**Pin:** D1D38A · living jobs: [`HIRED_JOBS.md`](HIRED_JOBS.md)

This fold runs on an ordinary PC (Python, optional GPU). That is not a bug. The competitor claim is: **the same hired questions as a QPU, no fridge.** Consumer hardware is the point.

Three comparisons get mixed up. They are not the same.

## 1. Vs a cryogenic QPU (the hire)

This is the comparison we are built for. Today’s QPUs do **not** answer the questions they are sold for at the sizes on our ledgers.

| Hired question | QPU today | This fold on a PC | Who answers the question? |
|----------------|-----------|-------------------|---------------------------|
| Factor | Compiled Shor on \(N=15\) (2001-class demos) | RSA-**shaped** moduli through **80-bit ECM** and balanced **81 / 95 / 103 / 111-bit** | This fold, by a wide margin |
| Grover | toy oracles, few qubits | exact marked search through **10⁷** | This fold |
| MaxCut / QAOA | ~10–20 noisy qubits, ratio often 0.7–0.9 | Gset **n=800–2000**, **11/11 under 1%** of published champion | This fold on size; champions still unmatched |
| HHL | tiny circuits | integer \(Ax=b\) through **8×8** | This fold on the linear system |
| VQE chemistry | H2/LiH STO-3G Hamiltonian, often misses 1.6 mHa | pin chemistry **68/68 @ 0.5%**; H2 De **0.25%**; Kolos derived 0.75% written | Different objects — see [`VQE_OBJECT.md`](VQE_OBJECT.md) |
| CKM / \(H_0\) / \(V_{cb}\) | not a QPU output | inclusive \(V_{cb}\) **0.002%**; Planck \(H_0\) **0.024%** | This fold; QPUs are not in that business |

**Innovative vs QPU: yes.** No fridge, no \(2^n\) amplitudes, same questions, larger instances, published answers. That is already a replacement pitch for the *machine they are selling*, not for GNFS or Gurobi.

## 2. Vs consumer classical computing (FLOPS / complexity)

This is the comparison a cryptographer or SAT solver would make. Honesty:

| Job | This fold | Ordinary classical | Innovative vs classical FLOPS? |
|-----|-----------|--------------------|--------------------------------|
| 80-bit factor | seed-locked ECM, seconds | Pollard ρ / ECM / QS in milliseconds | **No.** 80-bit is easy on a laptop either way. |
| 90-bit ECM miss | elliptic group not B-smooth at our B | ρ factors a 33-bit \(p\) in \(\sim\sqrt{p}\) steps — **0.1 s here** | The miss was **our B**, not the PC. |
| SAT-32, TSP n=11, HHL 8×8 | exact folds | trivial | **No.** |
| Gset n=800 under 1% of BKS | KL + spectral + BFS | published heuristics (BLS, Gurobi, …) often closer to champion | **Respectable heuristic, not a record.** QAOA still cannot run this size. |
| RSA-2048 | not run (smoothness / \(\sqrt{p}\) wall) | GNFS, not a laptop afternoon | The real crypto object. Neither we nor a QPU have it. |

The **innovation vs classical is the law, not the FLOPS**: zero free parameters, pin D1D38A, folds instead of \(2^n\), the same \(K\) on every job. We refuse to raise B when ECM misses. That is theory discipline, not a speed claim.

## 3. When would this become “Shor threatens RSA”?

RSA-2048 is two ~1024-bit primes. Shor’s QPU story is a million+ clean qubits we do not have. Our story is smoothness / \(\sqrt{p}\) on this pin.

- ECM with bitlen-locked B hits while some curve order is B-smooth. That failed at **90-bit unbalanced** and still often hits **81-bit balanced**.
- Pollard ρ costs \(\sim\sqrt{p}\). A 40-bit factor is a million steps (laptop). A 64-bit factor is \(\sim 2^{32}\) (painful in Python). A 1024-bit factor is not consumer hardware and not our current B.

We are **in the innovative state vs QPUs**. We are **not** in the innovative state vs classical factoring records. Both sentences are true. The competitor we named is the QPU.

## What we keep climbing on this PC

1. RSA-**shaped** (two similar-bit primes, not twins) at rising bit length, still seed-locked, still not RSA-2048.
2. Gset champions (G17 13 edges, G22 98) — QAOA’s job, laptop-sized graphs.
3. Right object for VQE / Kolos / STO-3G — already split.

```powershell
python -m fsot_quantum heights15
```
