# Architecture

```
FSOT-2.1-Lean pin D1D38A
        │
        ▼
fsot_lib  ←── vendored from FSOT-GPU (YOUR implementation)
  seeds · scalar · trinary · coherence · consensus · learn · backend
        │
        ▼
fsot_quantum  ←── domain fold only
  domains (QM D=6 / QC D=11) · register · gates · circuit · engine
        │
        ├── pure Python (always)
        └── torch CUDA buffers (prefer_device) — same as FSOT-GPU smoke_owned
```

phase1_formal_gpu / phase2_native_gpu = vendored from FSOT-GPU.
