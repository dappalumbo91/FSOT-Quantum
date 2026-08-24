# Known-answer QC jobs — fold vs published

**44/44** · pin D1D38A **not edited**

These are the numbers a QPU is hired to obtain: textbook Shor, DJ/BV/Grover/Simon, HHL, SAT/QUBO/TSP/color, MaxCut on graphs with exact champions, knapsack, counting, hidden period. Cross-check is fold vs the **published object**. Not their circuit.

| Family | Question | Published | Fold | Cite | OK |
|--------|----------|-----------|------|------|:--:|
| shor_factor | Factor 15? | `[3, 5]` | `[3, 5]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 21? | `[3, 7]` | `[3, 7]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 33? | `[3, 11]` | `[3, 11]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 35? | `[5, 7]` | `[5, 7]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 39? | `[3, 13]` | `[3, 13]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 51? | `[3, 17]` | `[3, 17]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 55? | `[5, 11]` | `[5, 11]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 77? | `[7, 11]` | `[7, 11]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 85? | `[5, 17]` | `[5, 17]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 91? | `[7, 13]` | `[7, 13]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 119? | `[7, 17]` | `[7, 17]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 143? | `[11, 13]` | `[11, 13]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 187? | `[11, 17]` | `[11, 17]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 209? | `[11, 19]` | `[11, 19]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 221? | `[13, 17]` | `[13, 17]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 247? | `[13, 19]` | `[13, 19]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 323? | `[17, 19]` | `[17, 19]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_factor | Factor 341? | `[11, 31]` | `[11, 31]` | textbook / compiled Shor demos (Vandersypen 2001 class) | True |
| shor_order | order of 7 mod 15? | `4` | `4` | Shor period-finding textbook object | True |
| shor_order | order of 2 mod 21? | `6` | `6` | Shor period-finding textbook object | True |
| shor_order | order of 4 mod 15? | `2` | `2` | Shor period-finding textbook object | True |
| shor_order | order of 8 mod 21? | `2` | `2` | Shor period-finding textbook object | True |
| shor_order | order of 11 mod 15? | `2` | `2` | Shor period-finding textbook object | True |
| deutsch_jozsa | Is f constant or balanced (n=4, constant 0)? | `constant` | `constant` | Deutsch–Jozsa | True |
| deutsch_jozsa | Is f constant or balanced (n=4, parity)? | `balanced` | `balanced` | Deutsch–Jozsa | True |
| bernstein_vazirani | BV secret s=10110100? | `[1, 0, 1, 1, 0, 1, 0, 0]` | `[1, 0, 1, 1, 0, 1, 0, 0]` | Bernstein–Vazirani | True |
| grover | Grover: marked item in 1024 is 733? | `733` | `733` | Grover search end-job | True |
| simon | Simon hidden string n=8 s=10110010? | `178` | `178` | Simon HSP | True |
| dlog | 3^x ≡ 13 (mod 17)? | `4` | `4` | discrete log (Shor's other job) | True |
| hhl | Solve [[2,1],[1,2]] x = [3,3]? | `[1, 1]` | `[1, 1]` | HHL end-job (integer Cramer) | True |
| qubo_partition | Partition {1..15} into equal sums? | `0` | `0` | number partition / QAOA hire | True |
| color | 3-color the Petersen graph? | `chromatic number 3` | `[2, 0, 2, 1, 0, 1, 2, 0, 0, 1]` | Petersen χ=3 | True |
| tsp | TSP n=5 seed metric — exact tour length? | `118` | `118` | QAOA / annealer TSP hire | True |
| sat | 3-SAT n=8, seed witness — satisfiable? | `0` | `0` | Grover/QAOA SAT hire | True |
| qi | Tsirelson bound for CHSH? | `2.8284271247461903` | `2.8284271247461903` | Cirel'son 1980; QI hardware demos | True |
| maxcut | MaxCut C5? | `4` | `4` | exact MaxCut C5 = 4 | True |
| maxcut | MaxCut K5? | `6` | `6` | exact MaxCut K5 = 6 | True |
| maxcut | MaxCut Petersen? | `12` | `12` | Petersen exact MaxCut (n=10 enum) | True |
| knapsack | 0/1 knapsack w=[2,3,4,5,9,7,6,8] v=[3,4,8,8,10,11,6,7] C=20? | `31` | `31` | QUBO / annealer knapsack hire; DP optimum is the object | True |
| hidden_shift | Hidden shift n=8 s=11010010? | `210` | `210` | bent-function hidden shift (QFT hire) | True |
| subset_sum | Subset-sum of {3,5,7,11,13,17,19,23} to 42? | `42` | `42` | knapsack cousin / QUBO | True |
| hidden_period | Hidden period of f(x)=x mod 12 on 0..95? | `12` | `12` | HSP / Shor period cousin | True |
| counting | How many marked items in 64 (φ-mask)? | `25` | `25` | quantum counting end-job | True |
| chemistry | H2O bond angle (deg)? | `104.5` | `104.53680149989006` | pin Water_bond_angle vs 104.5° (not NISQ VQE H2 FCI) | True |

H2/LiH/BeH2 *FCI Hamiltonians* are a different object from pin chemistry formulas (68/68). VQE on those molecules is not scored here — see `MARGIN_VS_QPU.md`. Water angle is the pin chemistry job.

```powershell
python -m fsot_quantum.known_qc
python -m fsot_quantum known
```
