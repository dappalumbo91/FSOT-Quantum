# Gset family — more than one graph

**overall_ok:** `False` · **10/11** under 1% · **11/11** under 5%

Same object as G1 (unweighted MaxCut). Signed Gset (G6–G13, G18–G21) is a different object. Aspiration <1% of published champion. No new coefficients. **G17 at 1.017% (31 edges short)** is written as a miss, not crawled.

| Graph | n | m | fold | published | rel% | <1% |
|-------|--:|--:|-----:|----------:|-----:|:---:|
| G1 | 800 | 19176 | 11563 | 11624 | 0.525 | True |
| G2 | 800 | 19176 | 11579 | 11620 | 0.353 | True |
| G3 | 800 | 19176 | 11589 | 11622 | 0.284 | True |
| G4 | 800 | 19176 | 11615 | 11646 | 0.266 | True |
| G5 | 800 | 19176 | 11582 | 11631 | 0.421 | True |
| G14 | 800 | 4694 | 3034 | 3064 | 0.979 | True |
| G15 | 800 | 4661 | 3023 | 3050 | 0.885 | True |
| G16 | 800 | 4672 | 3026 | 3052 | 0.852 | True |
| G17 | 800 | 4667 | 3016 | 3047 | 1.017 | False |
| G22 | 2000 | 19990 | 13245 | 13359 | 0.853 | True |
| G23 | 2000 | 19990 | 13257 | 13344 | 0.652 | True |

```powershell
python -m fsot_quantum.gset_family
```
