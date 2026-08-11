# Quantum pathway — on FSOT-GPU implementation

## Instruction

Use **FSOT-GPU `fsot_lib`** as the runtime. Do not invent alternate collapse/pack/consensus.

## Domains

| Domain | D_eff | observed |
|--------|------:|:--------:|
| Quantum_Mechanics | 6 | yes |
| Quantum_Computing | 11 | no |

`S` from `fsot_lib.scalar.compute_scalar` at those routes.

## Forward (same as FSOT-GPU HOW_IT_WORKS)

```
field → coherence_norm
      → phase_rotation
      → collapse → trit codes
      → trit_similarity / consensus_aggregate
      → measure (collapse + domain sign resolve for superposed)
```

## Spins

Signed: −1 / 0 / +1  
Pack codes (fsot_lib): 0 / 1 / 2  

## Files

| File | Role |
|------|------|
| `fsot_lib/*` | **Your** implementation (vendored from FSOT-GPU) |
| `fsot_quantum/engine.py` | Calls fsot_lib only |
| `fsot_quantum/gates.py` | Domain fold gates on trit algebra |
| `phase2_native_gpu/` | **Your** CUDA/torch engine |
