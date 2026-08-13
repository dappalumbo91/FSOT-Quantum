# Gset family — more than one graph

**overall_ok:** `True` · **7/7** under 1% · **7/7** under 5%

Same object as G1 (unweighted MaxCut). One graph is a point. Aspiration <1% of published champion. No new coefficients.

| Graph | n | m | fold | published | rel% | <1% |
|-------|--:|--:|-----:|----------:|-----:|:---:|
| G1 | 800 | 19176 | 11563 | 11624 | 0.525 | True |
| G2 | 800 | 19176 | 11579 | 11620 | 0.353 | True |
| G3 | 800 | 19176 | 11589 | 11622 | 0.284 | True |
| G4 | 800 | 19176 | 11615 | 11646 | 0.266 | True |
| G5 | 800 | 19176 | 11582 | 11631 | 0.421 | True |
| G22 | 2000 | 19990 | 13245 | 13359 | 0.853 | True |
| G23 | 2000 | 19990 | 13257 | 13344 | 0.652 | True |

```powershell
python -m fsot_quantum.gset_family
```
