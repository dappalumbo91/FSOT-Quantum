# Fold path v6

**overall_ok:** `True`
**wall_s:** `1.64`

- **Gset official:** official found=True pass=1/1
- **G1:** {'name': 'G1.txt', 'path': 'C:\\Users\\damia\\Desktop\\fsot quantum\\data\\gset\\G1.txt', 'official': True, 'n': 800, 'n_edges': 19176, 'cut_fold': 11397, 'ratio_lb': 0.5943366708385481, 'ratio_floor_sparse': 0.6180339887498948, 'published_cut': 11624, 'rel_err_vs_published_pct': 1.952856159669649, 'ok': True, 'hilbert_amps_if_QAOA': None, 'fold_budget_formal': 16827, 'cost': {'nominal_n': 32, 'hilbert_amplitudes': 4294967296, 'hilbert_note': 'C^{2^n} statevector entries (brute sim bottleneck)', 'fold_probe_budget': 355570, 'fold_depth': 3, 'fold_D_eff_cost_proxy': 0.7097596350416266, 'complexity_weight_phi': 0.6180339887498949, 'ratio_hilbert_over_fold': 12079.10480636724, 'winner_when': 'fold when structure admits closed form / poly probes'}}
- **arith:** 14/14 ok=True
- **GPU occupancy:** ok=True n_gpu=1

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.fold_v6
```

Gset G1 source: `https://web.stanford.edu/~yyye/yyye/Gset/G1` → `data/gset/G1.txt`
