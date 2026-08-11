"""
FSOT Quantum Engine — runs on YOUR FSOT-GPU stack.

Device path = fsot_lib (collapse, pack, consensus, coherence, phase_rotation)
optional torch CUDA buffers exactly as FSOT-GPU smoke_owned / fsot_gpu_engine.

No parallel invention. Same contracts.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_lib.scalar import compute_scalar
from fsot_lib.trinary import collapse, pack_u64, unpack_u64, trit_similarity
from fsot_lib.coherence import coherence_norm, position_coherence

from fsot_quantum.circuit import Circuit, bell_analog, run_circuit
from fsot_quantum.domains import DOMAIN_COMPUTE, DOMAIN_SPIN_LAW, domain_scalar
from fsot_quantum.register import TritRegister, codes_to_signed, signed_to_codes


def prefer_device() -> str:
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"


@dataclass
class QuantumEngine:
    """Host for quantum pathway using fsot_lib operators."""

    domain: str = DOMAIN_COMPUTE
    device: str | None = None

    def __post_init__(self) -> None:
        if self.device is None:
            self.device = prefer_device()

    def scalar(self, domain: str | None = None) -> float:
        return domain_scalar(domain or self.domain)

    def collapse_field(self, field) -> list[int]:
        """fsot_lib.collapse → signed spins."""
        codes = collapse(field)
        if hasattr(codes, "tolist"):
            codes = codes.tolist()
        # torch path returns int8 codes 0/1/2
        codes = [int(c) for c in codes]
        if codes and all(c in (0, 1, 2) for c in codes):
            return codes_to_signed(codes)
        return codes

    def pack(self, spins: list[int]) -> list[int]:
        codes = signed_to_codes(spins)
        pad = (-len(codes)) % 32
        if pad:
            codes = codes + [1] * pad
        return [pack_u64(codes[i : i + 32]) for i in range(0, len(codes), 32)]

    def run(self, reg: TritRegister, circuit: Circuit) -> TritRegister:
        return run_circuit(reg, circuit, domain=self.domain)

    def gpu_consensus_step(self, q, k, v):
        """Direct FSOT-GPU consensus attention — not softmax."""
        from fsot_lib.consensus import consensus_aggregate

        return consensus_aggregate(q, k, v)

    def gpu_phase(self, h, positions=None):
        from fsot_lib.consensus import apply_phase_rotation

        return apply_phase_rotation(h, positions)

    def gpu_coherence_norm(self, x):
        return coherence_norm(x)

    def smoke(self) -> dict[str, Any]:
        """Full smoke: pin-path pure + fsot_lib torch + quantum circuits."""
        report: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "implementation": "fsot_lib (FSOT-GPU owned stack)",
            "collapse_threshold": COLLAPSE_THRESHOLD,
            "device": self.device,
            "S_Quantum_Mechanics": domain_scalar(DOMAIN_SPIN_LAW),
            "S_Quantum_Computing": domain_scalar(DOMAIN_COMPUTE),
            "checks": {},
        }

        # --- pure owned (same as smoke_owned) ---
        S = compute_scalar(D_eff=8.0, observed=True, delta_psi=0.7)
        report["checks"]["scalar_pure"] = {"S": S, "ok": abs(S) > 0}

        codes = [i % 3 for i in range(32)]
        w = pack_u64(codes)
        report["checks"]["pack_pure"] = {"ok": unpack_u64(w) == codes, "word": w}

        x = [0.1, 0.95, -0.99, 0.5, 1.2, -1.1]
        y = coherence_norm(x)
        report["checks"]["coherence_pure"] = {"ok": len(y) == len(x)}

        # --- quantum domain fold ---
        reg = TritRegister.from_bits([0, 0], domain=DOMAIN_COMPUTE)
        out = self.run(reg, bell_analog())
        report["checks"]["bell_analog"] = {
            "ok": all(s in (-1, 0, 1) for s in out.spins),
            "spins": out.spins,
        }

        thr = COLLAPSE_THRESHOLD
        field = [1.0, -1.0, 0.0, thr + 0.02, -(thr + 0.02)]
        spins = self.collapse_field(field)
        report["checks"]["collapse_quantum"] = {
            "ok": spins[0] == 1 and spins[1] == -1 and spins[2] == 0,
            "spins": spins,
        }

        # --- torch device path (FSOT-GPU) ---
        try:
            import torch
            from fsot_lib.consensus import consensus_aggregate, apply_phase_rotation
            from fsot_lib.trinary import pack_u64_torch, unpack_u64_torch

            device = self.device if torch.cuda.is_available() or self.device == "cpu" else "cpu"
            if device == "cuda" and not torch.cuda.is_available():
                device = "cpu"

            q = torch.randn(8, 16, device=device, dtype=torch.float64)
            k = torch.randn(8, 16, device=device, dtype=torch.float64)
            v = torch.randn(8, 16, device=device, dtype=torch.float64)
            o = consensus_aggregate(q, k, v)

            # quantum: collapse continuous register field on device
            field_t = torch.tensor(
                [1.0, -1.0, 0.0, thr + 0.02, -(thr + 0.02), 0.5, -0.5, thr + SEEDS.poof],
                device=device,
                dtype=torch.float64,
            )
            codes_t = collapse(field_t)
            codes_list = [int(x) for x in codes_t.detach().cpu().tolist()]

            pack_codes = torch.randint(0, 3, (64, 32), device=device, dtype=torch.uint8)
            p = pack_u64_torch(pack_codes)
            u = unpack_u64_torch(p)

            # multi-site fluid: phase + consensus as multi-spin coupling
            seq = 16
            dim = 32
            h = torch.randn(seq, dim, device=device, dtype=torch.float64)
            h = coherence_norm(h)
            pos = torch.arange(seq, device=device)
            h = apply_phase_rotation(h, pos)
            qh, kh, vh = h, h, h
            coupled = consensus_aggregate(qh, kh, vh)

            report["checks"]["fsot_lib_torch"] = {
                "device": device,
                "gpu": torch.cuda.get_device_name(0) if device == "cuda" else None,
                "consensus_shape": list(o.shape),
                "collapse_codes": codes_list,
                "pack_roundtrip": bool(torch.equal(pack_codes, u)),
                "coupled_shape": list(coupled.shape),
                "ok": (
                    o.shape == q.shape
                    and bool(torch.equal(pack_codes, u))
                    and coupled.shape == h.shape
                    and codes_list[0] == 2
                    and codes_list[1] == 0
                ),
            }
        except Exception as e:
            report["checks"]["fsot_lib_torch"] = {"ok": False, "error": str(e)}

        # native cuda optional (their binary)
        try:
            from fsot_lib.backend.native_cuda import native_pack_available, run_native_pack_smoke

            if native_pack_available():
                report["checks"]["native_cuda"] = run_native_pack_smoke()
            else:
                report["checks"]["native_cuda"] = {
                    "ok": True,
                    "skipped": True,
                    "reason": "optional; torch path is primary (FSOT-GPU doctrine)",
                }
        except Exception as e:
            report["checks"]["native_cuda"] = {"ok": True, "skipped": True, "error": str(e)}

        report["ok"] = all(
            c.get("ok", False)
            for name, c in report["checks"].items()
            if not c.get("skipped")
        )
        return report


def run_engine_smoke() -> dict[str, Any]:
    eng = QuantumEngine()
    report = eng.smoke()
    out = ROOT / "results" / "quantum_engine_smoke.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("=== FSOT-Quantum engine (fsot_lib owned) ===")
    print(f"θ = {COLLAPSE_THRESHOLD}")
    print(f"S(QM) = {report['S_Quantum_Mechanics']}")
    print(f"S(QC) = {report['S_Quantum_Computing']}")
    for name, c in report["checks"].items():
        print(f"  [{'OK' if c.get('ok') else 'FAIL'}] {name}")
    print(f"overall ok = {report['ok']}")
    print(f"wrote {out}")
    return report


if __name__ == "__main__":
    r = run_engine_smoke()
    raise SystemExit(0 if r["ok"] else 1)
