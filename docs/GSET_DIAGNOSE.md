# Why Gset MaxCut is missing the champion

Diagnosis only. No new coefficients.

## Graph objects

| Graph | n | m | density | deg mean | weights | published | pub/m |
|-------|--:|--:|--------:|---------:|---------|----------:|------:|
| G1 | 800 | 19176 | 0.0600 | 47.9 | `{'1': 19176}` | 11624 | 0.606 |
| G14 | 800 | 4694 | 0.0147 | 11.7 | `{'1': 4694}` | 3064 | 0.653 |
| G22 | 2000 | 19990 | 0.0100 | 20.0 | `{'1': 19990}` | 13359 | 0.668 |

## Where the cut is lost

| Graph | best WITH greedy-uncut | best SKIP greedy | greedy hurts? | rel with | rel skip |
|-------|-----------------------:|-----------------:|:-------------:|---------:|---------:|
| G1 | 11431 | 11408 | False | 1.66% | 1.86% |
| G14 | 2913 | 2925 | True | 4.93% | 4.54% |
| G22 | 12766 | 12839 | True | 4.44% | 3.89% |

Greedy-uncut = flip the second endpoint of every uncut edge in file order. That is not a fold law. If skip-greedy is better, that pass is the failure.

## Cause (measured)

1. Weights are all `+1`. `abs(w)` is not the bug.
2. Every start reaches a **1-flip local maximum** (leftover +gain = 0).
3. Snap through Θ does nothing there — the flip-gain field is ≤ 0, below Θ.
4. G14 collapses every start onto the **same** 1-opt cut (2913). One basin.
5. Published champions sit **above** 1-opt (and above 2-opt). They are found by variable-depth search (Kernighan–Lin / breakout), not by another coefficient.

So the residual is not a wrong pin and not a wrong graph file. The fold was stopping at 1-local-opt. That is the failure.

## Per-start stages

### G1

| start | raw | after greedy | 1-flip from greedy | 1-flip skip greedy | snap | leftover +gain |
|-------|----:|-------------:|-------------------:|-------------------:|-----:|---------------:|
| all+ | 0 | 9916 | 11375 | 11300 | 11375 | 0 |
| all- | 0 | 9916 | 11375 | 11300 | 11375 | 0 |
| check2 | 9602 | 9933 | 11350 | 11342 | 11350 | 0 |
| golden | 9592 | 9916 | 11431 | 11408 | 11431 | 0 |
| phi0 | 9585 | 9898 | 11360 | 11322 | 11360 | 0 |
| phi1 | 9463 | 9916 | 11375 | 11366 | 11375 | 0 |
| phi2 | 9682 | 9874 | 11311 | 11310 | 11311 | 0 |

### G14

| start | raw | after greedy | 1-flip from greedy | 1-flip skip greedy | snap | leftover +gain |
|-------|----:|-------------:|-------------------:|-------------------:|-----:|---------------:|
| all+ | 0 | 2667 | 2913 | 2925 | 2913 | 0 |
| all- | 0 | 2667 | 2913 | 2925 | 2913 | 0 |
| check2 | 2368 | 2667 | 2913 | 2911 | 2913 | 0 |
| golden | 2344 | 2667 | 2913 | 2906 | 2913 | 0 |
| phi0 | 2322 | 2667 | 2913 | 2917 | 2913 | 0 |
| phi1 | 2279 | 2667 | 2913 | 2892 | 2913 | 0 |
| phi2 | 2391 | 2667 | 2913 | 2900 | 2913 | 0 |

### G22

| start | raw | after greedy | 1-flip from greedy | 1-flip skip greedy | snap | leftover +gain |
|-------|----:|-------------:|-------------------:|-------------------:|-----:|---------------:|
| all+ | 0 | 10958 | 12750 | 12839 | 12750 | 0 |
| all- | 0 | 10958 | 12750 | 12839 | 12750 | 0 |
| check2 | 10075 | 11134 | 12727 | 12786 | 12727 | 0 |
| golden | 9890 | 11018 | 12763 | 12731 | 12763 | 0 |
| phi0 | 10049 | 10938 | 12766 | 12679 | 12766 | 0 |
| phi1 | 9927 | 10994 | 12714 | 12754 | 12714 | 0 |
| phi2 | 9879 | 10888 | 12749 | 12760 | 12749 | 0 |
