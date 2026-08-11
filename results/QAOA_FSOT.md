# QAOA-style FSOT residual bank

**p = floor(π) = 3** (seed-locked)
**overall_ok:** `True`
**local exact hits:** 11/11
**qaoa exact hits:** 0/11

QAOA-FSOT is structural phase/mixer on trits with seed depth p=floor(pi); not variational γ,β. Green gate = multi-start local exact on n≤12 bank; QAOA column reported for residual comparison.

| name | E_exact | E_qaoa | E_local | qaoa=exact | local=exact |
|------|---------|--------|---------|------------|-------------|
| ising_cycle4_ferro | -4 | 0 | -4 | False | True |
| ising_cycle4_af | -4 | 4 | -4 | False | True |
| ising_cycle6_ferro | -6 | -2 | -6 | False | True |
| ising_cycle6_af | -6 | 6 | -6 | False | True |
| ising_cycle8_ferro | -8 | -4 | -8 | False | True |
| ising_cycle8_af | -8 | 8 | -8 | False | True |
| ising_cycle10_ferro | -10 | -6 | -10 | False | True |
| ising_cycle10_af | -10 | 10 | -10 | False | True |
| ising_cycle12_ferro | -12 | -8 | -12 | False | True |
| ising_cycle12_af | -12 | 12 | -12 | False | True |
| frustrated_tri_chain6 | -3 | 1 | -3 | False | True |
