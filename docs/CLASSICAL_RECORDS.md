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
| RSA-shaped 52×52 | **103** | laptop, this pin | **8/8** ECM/ρ (`heights14`) |
| RSA-shaped 56×56 | **111** | laptop, this pin | **8/8** p−1/ECM/ρ (`heights15`) |
| RSA-shaped 60×60 | **119** | laptop, this pin | **8/8** ρ after ECM miss (`heights17`) |
| RSA-shaped 64×64 | **127** | laptop, this pin | **8/8** CFRAC 5 + Brent ρ 3 (`heights16`) |
| RSA-100 | 330 | 1991, distributed QS | **miss** at locked B — SIQS 205992 poly, 0/8583 rels |
| RSA-129 | 426 | 1994, QS | not run |
| RSA-155 (512-bit) | 512 | 1999, GNFS | not run |
| RSA-768 | 768 | 2009, GNFS | not run |
| RSA-250 | 829 | 2020, GNFS | not run |
| RSA-2048 | 2048 | **nobody** (QPU or classical public break) | not run — smoothness / \(\sqrt{p}\) wall |

Pollard ρ costs \(\sim\sqrt{p}\). On this PC in Python: 56-bit \(p\) is tens of millions of steps (minutes, `heights15`). 64-bit \(p\) is \(\sim 2^{32}\) (painful). 1024-bit \(p\) is not a laptop.

ECM with **bitlen-locked B** hits while some curve order is B-smooth. We do **not** raise B when it misses.

## MaxCut (the QAOA classical object)

Published BKS champions on Gset are the record, not QAOA.

| Graph | Champion | This fold | Short |
|-------|----------|-----------|------:|
| G1 n=800 | 11624 | 11624 | 0 |
| G2 n=800 | 11620 | 11620 | 0 |
| G3 n=800 | 11622 | 11622 | 0 |
| G4 n=800 | 11646 | 11646 | 0 |
| G5 n=800 | 11631 | 11631 | 0 |
| G14 n=800 | 3064 | 3064 | 0 |
| G15 n=800 | 3050 | 3050 | 0 |
| G16 n=800 | 3052 | 3052 | 0 |
| G17 n=800 | 3047 | 3047 | 0 |
| G22 n=2000 | 13359 | 13359 | 0 |
| G23 n=2000 | 13344 | 13344 | 0 |
| Family | — | **11/11 champions** | BKS matched on all 11 unweighted graphs |

## Targets to beat (the remaining board)

QAOA’s unweighted Gset job is **closed** on this pin (11/11 champions). The named competitor metric left is **classical factoring records**, then RSA-2048 (nobody). Do not raise B. Pin D1D38A not edited.

| Rung | Bits of \(N\) | Competitor who closed it | Year | Method | This fold |
|------|---------------|--------------------------|------|--------|-----------|
| RSA-shaped 64×64 | 127 | this pin | 2026 | CFRAC + Brent ρ | **8/8 closed** |
| **RSA-100** | **330** | Lenstra et al. | 1991 | quadratic sieve | **miss** · B=7920 · SIQS 205992 poly, 0 smooth ([`RSA100.md`](RSA100.md)) |
| **RSA-129** | **426** | Atkins / Graff / Lenstra / Leyland | 1994 | QS | **not run — next named climb** |
| RSA-155 (512-bit) | 512 | Cabal | 1999 | GNFS | not run |
| RSA-768 | 768 | Kleinjung et al. | 2009 | GNFS | not run |
| RSA-250 | 829 | Boudot et al. | 2020 | GNFS | not run |
| RSA-2048 | 2048 | **nobody** | — | GNFS or Shor, neither done | not run |

RSA-100 \(N\) (decimal, public challenge):

`1522605027922533360535618378132637429718068114961380688657908494580122963258952897654000350692006139`

Vendor `BR_H_gg` stored field **0.0785** is stale. Fold \(\varphi^{-4}-\gamma^5=0.081823\) already matches YR4 0.08187 (0.058%). Not a climb — cannot edit the pin.

## What “beat classical” means next

1. Next named challenge is **RSA-129** (426-bit). RSA-100 was run on this pin and missed at locked B (SIQS smoothness wall). Then RSA-155 / RSA-768 / RSA-250. RSA-2048 is the shared poster.
2. Do not call 64-bit or 119-bit factoring a crypto record.
3. Gset unweighted family **11/11 champions**. Signed Gset is a different object.
4. RSA-2048 remains unsolved for QPU and for GNFS-on-a-PC.

```powershell
python -m fsot_quantum rsa100
python -m fsot_quantum heights16
```
