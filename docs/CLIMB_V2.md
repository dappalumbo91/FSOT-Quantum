# Competitor climb v2

**overall_ok:** `True`
**wall_s:** `5.96`
**device/GPU:** `NVIDIA GeForce RTX 5070`

## Panels

- **surface code:** 4/4 ok=True noise={'require': 'd3 @ p=0.01 → p_logical < 0.15', 'p_logical': 0.0, 'ok': True}
- **Shor GPU:** 8/8 ok=True
- **mega GPU:** ok=True highlights={'max_amp_updates_per_sec': 288135634.849888, 'max_circuits_per_sec': 701345.8443790947, 'max_pack_trits_per_sec': 3390028013.779111, 'max_opt_ips': 16417.62330390909, 'max_peak_mem_mb': 8422.85205078125, 'vram_frac_peak': 0.688897803514377, 'jobs_ok': '21/21'}
- **chemistry strict:** ok=True 0.5%=67/68 median=0.02202261701877489
- **fused GPU:** ok=True
- **opt GPU:** ok=True
- **QAOA exact:** {'qaoa_exact': '11/11', 'local_exact': '11/11', 'require': 'qaoa_exact_hits == total'}

## Now implemented (v2)

- planar surface-code Z-plaquette stabilizers d=3/5/7 + greedy MWPM decoder
- GPU modular Shor ladder N∈{15,21,33,35,39,51}
- mega-batch GPU occupancy (pack + fused Hilbert + MaxCut + surface spins)
- chemistry strict 5% band + 0.5% green fraction ledger

## Still not claimed

- cryptographically large Shor (RSA-scale)
- device-scale surface-code FTQC threshold proofs
- full molecular FCI / CASSCF
- 100% chemistry observables @ 0.5% (aspiration)

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.climb_v2
```

Watch load: `nvidia-smi -l 1` while running.
