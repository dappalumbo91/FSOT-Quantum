# Compete QM/QC suite

**overall_ok:** `True`
**device:** `cuda`

## Panels

| Panel | OK | Detail |
|-------|----|--------|
| Hilbert universal fragment | True | Bell F=1.000000 |
| Logical qubits | True | d=3 |
| QFT | True | IQFT F=1.000000 |
| Shor tiny | True | 3/3 |
| Chemistry residual | True | S_chem=0.4079 |

## Now implemented

- complex statevector + H/X/Y/Z/S/T/CNOT/CPhase (seed angles)
- logical repetition code d=3
- QFT + IQFT roundtrip; tiny Shor CF recovery N=15,21
- vendor chemistry wave residual bridge

## Still not claimed

- cryptographically large Shor
- surface-code FTQC thresholds
- full molecular FCI / CASSCF
- device-independent quantum supremacy

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.compete_qm_qc
```
