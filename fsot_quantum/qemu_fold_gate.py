"""
QEMU serial gate for fold kernel tests (pack/collapse/gates/fold/cnotfold).

Wraps repo run_qemu.ps1. Copies serial into results/qemu_serial.log.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def run_qemu_fold_gate() -> dict[str, Any]:
    script = ROOT / "run_qemu.ps1"
    if not script.exists():
        return {"ok": False, "status": "fail", "reason": "run_qemu.ps1 missing"}

    qemu = shutil.which("qemu-system-x86_64")
    qemu_pf = Path(r"C:\Program Files\qemu\qemu-system-x86_64.exe")
    have_qemu = bool(qemu) or qemu_pf.exists()
    if not have_qemu:
        return {
            "ok": False,
            "status": "skip",
            "reason": "qemu-system-x86_64 not found",
        }

    cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script),
    ]
    p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=180)
    out = (p.stdout or "") + (p.stderr or "")
    log_path = ROOT / "results" / "qemu_serial.log"
    serial = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    fold_pass = "FSOT fold PASS" in serial or "FSOT fold PASS" in out
    cnot_pass = "FSOT cnotfold PASS" in serial or "FSOT cnotfold PASS" in out
    kernel_pass = "FSOT_QUANTUM_KERNEL PASS" in serial or "FSOT_QUANTUM_KERNEL PASS" in out
    jobs_pass = "FSOT_QUANTUM_JOBS PASS" in serial or "FSOT_QUANTUM_JOBS PASS" in out
    ok = p.returncode == 0 and kernel_pass and fold_pass and cnot_pass and jobs_pass
    return {
        "ok": ok,
        "status": "pass" if ok else "fail",
        "exit_code": p.returncode,
        "fold_pass": fold_pass,
        "cnotfold_pass": cnot_pass,
        "jobs_pass": jobs_pass,
        "kernel_pass": kernel_pass,
        "serial_tail": (serial or out)[-2500:],
    }
