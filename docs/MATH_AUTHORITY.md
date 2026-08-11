# FSOT-Quantum — Math Authority

**Pin:** `D1D38A` (`vendor/fsot_compute.py` from [FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean))  
**Law:** \(S = K(T_1 + T_2 + T_3)\)  
**Free parameters:** **ZERO**

This repository does **not** invent a second theory. It is the **quantum computing domain fold** of the same fluid spacetime engine used in:

| Repo | Fold |
|------|------|
| FSOT-2.1-Lean | Formal + multi-domain residual atlas |
| FSOT-GPU | GPU trinary consensus attention |
| fsot-neuron-zig | Neural mind / bare-metal trit body |
| FSOT-Genetics | Genetics / structure formulas |
| Protofluid-Language-Translator | Language densify |

---

## Seeds (Layer 0)

\[
\pi,\; e,\; \varphi=\frac{1+\sqrt{5}}{2},\; \gamma,\; G_{\mathrm{Catalan}}
\]

All derived constants (`α`, `ψ_con`, `η_eff`, `β`, `C_eff`, `P_var`, `K`, …) come from closed forms of these seeds only.

---

## Scalar engine

\[
\begin{aligned}
T_1 &= \text{observer-modulated base (includes }\mathbf{C}_{\mathrm{factor}}\text{ when observed)} \\
T_2 &= \text{linear modulation} \\
T_3 &= \text{valve–acoustic–phase (Poof, Suction, Chaos, bleed)} \\
S &= K\cdot(T_1+T_2+T_3)
\end{aligned}
\]

Code: `fsot_quantum/scalar.py` (structure twin of `vendor/fsot_compute.py`).

---

## Domain interfaces for this pathway

| Domain | \(D_{\mathrm{eff}}\) | observed | Role |
|--------|---------------------:|:--------:|------|
| **Quantum_Mechanics** | 6 | yes | Spin law / measurement resolve |
| **Quantum_Computing** | 11 | no | Bare compute substrate |

When residuals fail: change **domain / \(D_{\mathrm{eff}}\)**, do not invent fit coefficients.

---

## Trinary spins (quantum state)

\[
\mathbb{T} = \{-1,\,0,\,+1\}
\]

| Value | Name | Role |
|------:|------|------|
| \(+1\) | Spin up | emergent pole |
| \(0\) | Superposition | continuum / quiet |
| \(-1\) | Spin down | damped pole |

**Not** complex Hilbert amplitudes. Continuous pre-collapse field \(v\in\mathbb{R}\) collapses by:

\[
\Theta = C_{\mathrm{eff}}\cdot P_{\mathrm{var}}
\]

\[
\mathrm{collapse}(v) =
\begin{cases}
+1 & v > \Theta \\
-1 & v < -\Theta \\
0 & |v| \le \Theta
\end{cases}
\]

Superposed discrete sites resolve with \(\mathrm{sign}(S(\mathrm{domain}))\) — no free Born RNG.

---

## Forbidden

1. New free fit parameters  
2. Softmax / complex-amplitude “quantum” bolted on as ad-hoc  
3. Silent rescale of measured targets  
4. Changing seed constants without pin re-verify  

---

## Reproduce

```powershell
python -m fsot_quantum.verify
python parity\run_parity.py
python scripts\run_demo.py
```
