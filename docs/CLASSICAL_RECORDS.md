# Classical FLOPS / crypto records — the other competitor

**Pin:** D1D38A · QPU comparison: [`CONSUMER_VS_QPU.md`](CONSUMER_VS_QPU.md)

We already beat **today’s QPUs** on the hired questions we run. The other board is classical records: GNFS factoring, MaxCut BKS, SAT solvers. This page is that ladder. No pretend RSA-2048.

## Factoring (the crypto object)

RSA moduli are two primes of **similar bit length**, not twins and not 32-bit × 48-bit.

| Object | Bits of \(N\) | Who factored it | This fold |
|--------|---------------|-----------------|-----------|
| Textbook Shor \(N=15\) | 4 | QPU demos | exact |
| RSA-shaped 41×41 | **81** | laptop, this pin | **12/12** ECM/ρ (`heights12`) |
| RSA-shaped 48×48 | **95** | laptop, this pin | **8/8** ECM/ρ (`heights13`) |
| RSA-100 | 330 | 1991, distributed QS | not run |
| RSA-129 | 426 | 1994, QS | not run |
| RSA-155 (512-bit) | 512 | 1999, GNFS | not run |
| RSA-768 | 768 | 2009, GNFS | not run |
| RSA-250 | 829 | 2020, GNFS | not run |
| RSA-2048 | 2048 | **nobody** (QPU or classical public break) | not run — smoothness / \(\sqrt{p}\) wall |

Pollard ρ costs \(\sim\sqrt{p}\). On this PC in Python: 48-bit \(p\) is millions of steps (seconds). 64-bit \(p\) is \(\sim 2^{32}\) (painful). 1024-bit \(p\) is not a laptop.

ECM with **bitlen-locked B** hits while some curve order is B-smooth. We do **not** raise B when it misses.

## MaxCut (the QAOA classical object)

Published BKS champions on Gset are the record, not QAOA.

| Graph | Champion | This fold | Short |
|-------|----------|-----------|------:|
| G1 n=800 | 11624 | 11585 | 39 |
| G17 n=800 | 3047 | 3034 | 13 |
| G22 n=2000 | 13359 | 13261 | 98 |
| Family | — | **11/11 under 1%** | aspiration met, champions unmatched |

## What “beat classical” means next

1. Keep climbing **balanced** bit length (48 → 52 → 56-bit primes) on this pin, still seed-locked.
2. Do not call 95-bit factoring a crypto record. RSA-100 is the first named challenge on that list.
3. Gset: close G17’s 13 edges / G22’s 98 without a crawl.
4. RSA-2048 remains the shared unsolved poster — QPU and GNFS-on-a-PC both unsolved.

```powershell
python -m fsot_quantum heights13
```
