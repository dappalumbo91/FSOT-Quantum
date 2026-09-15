# CFRAC-B2 — √N-sized Q at SIQS smoothness

**miss** on RSA-100 · **hit** on 60-bit and 64-bit RSA-shaped · pin D1D38A **not edited** · B **not raised** · factors **not looked up**

The RSA wall is \(u=\ln|Q|/\ln(\mathrm{bound})\). SIQS sieved a ~N-sized value at B2 (\(u\approx 10.4\)). Living CFRAC sieved a √N-sized value at B (\(u\approx 12.7\)). This lane is the unused pairing: **√N-sized Q, bound B2** (same stage-2 product, \(u\approx 9.4\)). Not a raised B.

| Object | method | rels | wall |
|--------|--------|------|------|
| 60-bit smoke | `cfrac_b2_smooth` | 1833/1833 | split |
| 64-bit RSA-shaped | `cfrac_b2_smooth` | 3675/3675 | split, 113 s |
| RSA-100 | `cfrac_b2_exhausted` | **0/8583** | 4,561,920 steps × k=1,2,3 · 9926 s |

RSA-100 produced **0** full-smooth and **0** 1-LP at this cap. \(\rho(9.4)\times 4.56\cdot 10^6\) is \(\ll 1\). The pairing is the right object; the count is still the wall. Next mechanical reduction of \(u\) without raising B is a **degree-\(\lfloor\pi\rfloor\) field sieve** (norm \(\sim N^{1/d}\)), not a pin edit.

```powershell
python -m fsot_quantum.fold_cfrac_b2
```

