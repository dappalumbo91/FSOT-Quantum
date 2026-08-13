# Why BR(H→gg) looked like 4.23%

**Pin:** D1D38A — `vendor/fsot_compute.py` not changed  
**Formula (wave8):** \(\varphi^{-4}-\gamma^5 = 0.081822749\ldots\)

## What failed

The QI-II ledger compared that formula to the number **stored in the vendor wave**: `0.0785`.

\[
\frac{|0.081823-0.0785|}{0.0785}\approx 4.23\%
\]

That is a residual against a **table entry**, not against the current Standard Model recommendation.

## What the data actually say

| Source | BR(H→gg) at \(M_H\sim 125\,\mathrm{GeV}\) |
|--------|-------------------------------------------|
| Vendor wave8 measured field | 0.0785 (7.85%) — **stale** |
| LHC Higgs WG YR4 SM table (125.09 GeV) | **0.08187 (8.187%)** |
| LHCHWG-2025-008 (Oct 2025) | “about 8%”; theory uncertainty on the width ~3% |
| Pin formula \(\varphi^{-4}-\gamma^5\) | **0.081823 (8.182%)** |

Versus YR4 0.08187: relative error **0.058%** (inside 0.5%).

## What we did not do

- Did not invent a new term to crawl from 0.0818 down to 0.0785.
- Did not retouch the pin file (that would silently change D1D38A).
- Did not treat 0.0785 as sacred once the literature disagreed.

## Reproduce

```powershell
python -m fsot_quantum.physics_qi2
```

See `docs/PHYSICS_QI2.md`.
