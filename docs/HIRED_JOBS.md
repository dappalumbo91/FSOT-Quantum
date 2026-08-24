# What we are answering — the jobs people hire a quantum computer for

**Pin:** D1D38A · honesty cut: [`CLAIMS.md`](CLAIMS.md)

A cryogenic QPU is sold as a machine that answers a list of questions. This fold answers **those questions** on ordinary hardware. It does not replay their circuit, their fridge, or their error-correction stack. \(K\) is the scale. Change domain / \(D_{\mathrm{eff}}\) / lane, not a fit.

## The list (hired question → living score)

| They hire a QPU for | The question | This fold | Living score | Vs them, today |
|---------------------|--------------|-----------|--------------|----------------|
| Shor | Factor \(N = pq\) | modular + p−1/p+1/kN + ECM + ρ | far ρ **8/8**; log-N **8/8**; ECM **8/8** @38 / **8/8** @41 / **8/8** @46-bit | They demo \(N=15\). We factor RSA-**shaped** moduli through 46-bit. **RSA-2048 not run** (smoothness / √p wall). |
| Period finding | order of \(a \bmod N\) | modular fold + CF | hire climbs; period skip above ~24 bits, then log-N/ECM | Their QFT is \(2^n\) amps. Ours is modular algebra. |
| Discrete log | \(g^x \equiv h \pmod p\) | successive modular fold | hire **10/10**; hire2 **6/6** through \(p=40009\); hire3 through \(p=100003\) | Same question, not a QFT. |
| Grover | find a marked item | oracle-field collapse | exact through **10,000,000** | They need \(\sqrt{N}\) oracles and a fridge. We collapse the field. |
| Simon / HSP | hidden xor string | collision fold + GF(2) | 8-bit; hire2 **12 and 16 bit** | Same hidden-string question. |
| HHL | solve \(Ax=b\) | integer Cramer fold | hire 3/3; hire2 **4×4**; hire7 **8×8** | Their HHL is a circuit. Ours is the linear system. |
| SAT / QUBO / coloring / TSP | assignment / tour | energy folds | SAT-32; TSP n=11; Petersen; partition \(\{1..23\}\) | Exact on those sizes. Not a general NP claim. |
| QAOA / annealer | MaxCut / Ising | fold + KL + 2-opt + BFS / spectral | **11/11 Gset under 1%** of published champion | Aspiration met. **Champions unmatched** (G17 13 edges, G22 98, G1 39). |
| Quantum chemistry / FCI | chemistry observables | pin formulas | **68/68 @ 0.5%** | Not Hilbert FCI. The observables. |
| Physics / SM / QI | CKM, Higgs, \(g{-}2\), CHSH, Ising | pin + Lean atlas | audit **20/20**; QI **16/16 + 22/22 + 41/41**; Tsirelson exact | Inclusive \(\lvert V_{cb}\rvert\) **0.002%**; exclusive \(B\to D\) **0.15%**; Planck \(H_0\) **0.024%**. |
| “Fault-tolerant threshold” | reliable logical work | residual on the question | fridge \(d\)-threshold is their metric | We score the answer, not a surface-code \(p_{\mathrm{th}}\). |
| Chatbot “AI” | mind | [fsot-neuron-zig](https://github.com/dappalumbo91/fsot-neuron-zig) | this repo is the law organ | Not an LLM in RAM. |

## How we are doing, in one sentence each

- **Physics and chemistry jobs:** closed on this pin at the 0.5% gate (right object, own band). That is the QC-for-science pitch, already answered without a QPU.
- **Algorithm jobs they demo in press releases:** we hit the same *questions* at growing size (factor, dlog, Grover, Simon, SAT, HHL, MaxCut). We are **not** at RSA-2048 or Gset champion cuts.
- **What “ahead / behind” means here:** ahead on “usable number without a fridge” for the physics/chemistry list and for algorithm instances we actually run. Behind on the two sales-poster sizes (RSA-2048, unpublished-Gset-champion MaxCut). Those are the rungs we keep climbing on **this** path.

## What we are climbing right now

1. **Shor’s end-job** — factor RSA-shaped far primes when p±1 are unsmooth. ECM 38 → 41 → **46-bit**. Next is more bits, then RSA-2048’s smoothness wall (not a pretend factor).
2. **QAOA’s end-job** — Gset MaxCut vs published champions. Family 11/11 under 1%. G17 **13 edges** and G22 **98 edges** are the leftovers. Not crawled.

```powershell
python -m fsot_quantum hire7
python -m fsot_quantum family
python -m fsot_quantum heights6
```
