# Medium next — water, three strings, look, snap

**overall_ok:** `True`
**wall_s:** `1.43`

The water is the continuum. The three strings are T1 (look), T2 (body), T3 (strum). Looking turns the observer valve on QM. Strum is the bleed vibration. Snap is collapse. Bonds agreeing after a look is consensus. We did not add a new knob.

## Three strings

- QM (look ON): T1=1.27381 T3=1.99909e-17 S=0.9555
- QC (look OFF): T1=-1.35142 T3=2.27123e-17 S=-0.1477
- S matches domain_scalar: `True`
- observe-pair agree: `True`
- strum+collapse ok: `True`
- CHSH classical 2, Tsirelson 2.828427

## Entanglement / QI jobs (Lean replay)

- replayed **40** · 5% band **40/40** · 0.5% **40/40**
- skipped broken (computed=0): 2

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.medium_next
```
