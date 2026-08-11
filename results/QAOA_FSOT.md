# QAOA-style FSOT residual bank

**p = floor(π) = 3** (seed-locked)
**QAOA exact hits: 11/11**
**local exact hits: 11/11**
**overall_ok:** `True`

Pipeline: `prepare_layers → multi-start polish (incl. warm) → exact enum if n<=12 and needed`

| name | E_exact | E_raw | E_qaoa_final | E_local | qaoa=exact | fallback |
|------|---------|-------|--------------|---------|------------|----------|
| ising_cycle4_ferro | -4 | 0 | -4 | -4 | True | False |
| ising_cycle4_af | -4 | 4 | -4 | -4 | True | False |
| ising_cycle6_ferro | -6 | -2 | -6 | -6 | True | False |
| ising_cycle6_af | -6 | 6 | -6 | -6 | True | False |
| ising_cycle8_ferro | -8 | -4 | -8 | -8 | True | False |
| ising_cycle8_af | -8 | 8 | -8 | -8 | True | False |
| ising_cycle10_ferro | -10 | -6 | -10 | -10 | True | False |
| ising_cycle10_af | -10 | 10 | -10 | -10 | True | False |
| ising_cycle12_ferro | -12 | -8 | -12 | -12 | True | False |
| ising_cycle12_af | -12 | 12 | -12 | -12 | True | False |
| frustrated_tri_chain6 | -3 | 1 | -3 | -3 | True | False |
