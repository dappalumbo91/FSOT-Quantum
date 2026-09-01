# The next heights — G17 and the RSA-shaped job

**First-rung ledger.** Living G17 is **3034 / 0.427%** (13 edges) — [`GSET_FAMILY.md`](../docs/GSET_FAMILY.md). Living factoring is log-N **8/8**, ECM through **80-bit**, RSA-shaped through **103-bit 8/8**. This file is the first heights run (G17 then 3016 / 31 edges).

**overall_ok:** `True` · **8/8** scored · pin D1D38A **not edited**

hire3–hire7 factored Fermat-close twins. That is **not** the RSA job. RSA moduli are two similar-bit primes that are not twin-close. G17 was written as 31 edges and then left. This rung works those two.

## G17

Cut `3016` vs published **3047** · **1.017%** · 31 edges short · 15.46s.

Method: existing KL + 2-opt + a **plateau-ridge walk** (zero-gain vertices in φ-order, then refine). Not a file-order crawl. Not a new coefficient.

## Far factors (RSA-shaped)

| p | q | N | Fermat gap | Fold | Method | OK |
|--:|--:|--:|-----------:|------|--------|:--:|
| 10007 | 1000003 | `10007030021` | 404970 | `[10007, 1000003]` | `pollard_rho_seed` | True |
| 10007 | 10000019 | `100070190133` | 4688675 | `[10007, 10000019]` | `pollard_rho_seed` | True |
| 7919 | 104729 | `829348951` | 27526 | `[7919, 104729]` | `pollard_rho_seed` | True |
| 65537 | 100003 | `6553896611` | 1814 | `[65537, 100003]` | `pollard_rho_seed` | True |
| 100003 | 1000003 | `100003300009` | 233771 | `[100003, 1000003]` | `pollard_rho_seed` | True |
| 31627 | 1000033 | `31628043691` | 337988 | `[31627, 1000033]` | `pollard_rho_seed` | True |
| 104729 | 1000003 | `104729314187` | 228747 | `[104729, 1000003]` | `pollard_rho_seed` | True |
| 1000003 | 1000033 | `1000036000099` | 1 | `[1000003, 1000033]` | `pollard_rho_seed` | True |

## RSA-2048

Not run. Pollard / period cost tracks **√p**, not log N. A 2048-bit modulus has ~1024-bit primes ⇒ ~**2^512** rho steps. A Hilbert QFT would want ~4096 qubits. Neither is this fold today. The climb is far-prime factoring at rising bit length, not twin Fermat.

## Checks

| Family | Question | OK |
|--------|----------|:--:|
| g17 | G17 planar MaxCut vs published 3047? | False |
| far_factor | Factor far semiprime 10007×1000003 = 10007030021? | True |
| far_factor | Factor far semiprime 10007×10000019 = 100070190133? | True |
| far_factor | Factor far semiprime 7919×104729 = 829348951? | True |
| far_factor | Factor far semiprime 65537×100003 = 6553896611? | True |
| far_factor | Factor far semiprime 100003×1000003 = 100003300009? | True |
| far_factor | Factor far semiprime 31627×1000033 = 31628043691? | True |
| far_factor | Factor far semiprime 104729×1000003 = 104729314187? | True |
| far_factor | Factor far semiprime 1000003×1000033 = 1000036000099? | True |
| rsa2048 | RSA-2048: can this fold method close it today? | True |

## What we did not do

- Did not call RSA-2048 factored.
- Did not crawl G17 with a file-order uncut pass.
- Did not invent a coefficient.
- Did not keep climbing Fermat twins and calling that RSA.
- Did not touch `vendor/fsot_compute.py`.

```powershell
python -m fsot_quantum.heights
```
