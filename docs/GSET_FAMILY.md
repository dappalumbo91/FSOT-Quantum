# Gset family — more than one graph

**overall_ok:** `True` · **11/11** under 1% · **11/11** under 5%

Same object as G1 (unweighted MaxCut). Signed Gset (G6–G13, G18–G21) is a different object. Aspiration <1% of published champion. No new coefficients. Family is **11/11 under 1%**. Champions still unmatched (G17 13 edges / 0.427%; G22 98 edges). G16 moved 3027→3031 on the negative-gain ridge (sparse G14–G17 only).

| Graph | n | m | fold | published | rel% | <1% |
|-------|--:|--:|-----:|----------:|-----:|:---:|
| G1 | 800 | 19176 | 11585 | 11624 | 0.336 | True |
| G2 | 800 | 19176 | 11582 | 11620 | 0.327 | True |
| G3 | 800 | 19176 | 11583 | 11622 | 0.336 | True |
| G4 | 800 | 19176 | 11614 | 11646 | 0.275 | True |
| G5 | 800 | 19176 | 11582 | 11631 | 0.421 | True |
| G14 | 800 | 4694 | 3042 | 3064 | 0.718 | True |
| G15 | 800 | 4661 | 3027 | 3050 | 0.754 | True |
| G16 | 800 | 4672 | 3031 | 3052 | 0.688 | True |
| G17 | 800 | 4667 | 3034 | 3047 | 0.427 | True |
| G22 | 2000 | 19990 | 13261 | 13359 | 0.734 | True |
| G23 | 2000 | 19990 | 13271 | 13344 | 0.547 | True |

```powershell
python -m fsot_quantum.gset_family
```
