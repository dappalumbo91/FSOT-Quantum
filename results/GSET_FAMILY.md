# Gset family — more than one graph

**overall_ok:** `True` · **11/11** under 1% · **11/11** under 5%

Same object as G1 (unweighted MaxCut). Signed Gset (G6–G13, G18–G21) is a different object. Aspiration <1% of published champion. No new coefficients. Family is **11/11 under 1%**. Champions still unmatched (G17 is 13 edges / 0.427%).

| Graph | n | m | fold | published | rel% | <1% |
|-------|--:|--:|-----:|----------:|-----:|:---:|
| G1 | 800 | 19176 | 11585 | 11624 | 0.336 | True |
| G2 | 800 | 19176 | 11582 | 11620 | 0.327 | True |
| G3 | 800 | 19176 | 11583 | 11622 | 0.336 | True |
| G4 | 800 | 19176 | 11614 | 11646 | 0.275 | True |
| G5 | 800 | 19176 | 11582 | 11631 | 0.421 | True |
| G14 | 800 | 4694 | 3042 | 3064 | 0.718 | True |
| G15 | 800 | 4661 | 3027 | 3050 | 0.754 | True |
| G16 | 800 | 4672 | 3027 | 3052 | 0.819 | True |
| G17 | 800 | 4667 | 3034 | 3047 | 0.427 | True |
| G22 | 2000 | 19990 | 13245 | 13359 | 0.853 | True |
| G23 | 2000 | 19990 | 13258 | 13344 | 0.644 | True |

```powershell
python -m fsot_quantum.gset_family
```
