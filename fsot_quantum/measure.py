"""Measurement via fsot_lib collapse threshold + domain S resolve."""

from __future__ import annotations

from fsot_lib.seeds import COLLAPSE_THRESHOLD
from fsot_lib.trinary import collapse, code_to_signed
from fsot_quantum.domains import DOMAIN_SPIN_LAW, domain_scalar
from fsot_quantum.register import TritRegister


def resolve_superposed(domain: str = DOMAIN_SPIN_LAW) -> int:
    s = domain_scalar(domain)
    if s > 0:
        return 1
    if s < 0:
        return -1
    return 0


def measure_spin(t: int, domain: str = DOMAIN_SPIN_LAW) -> int:
    t = int(t)
    if t != 0:
        return t
    return resolve_superposed(domain)


def measure_field_value(v: float, domain: str = DOMAIN_SPIN_LAW) -> int:
    codes = collapse([float(v)])
    if hasattr(codes, "tolist"):
        codes = codes.tolist()
    code = int(codes[0])
    # fsot_lib pure collapse returns codes 0/1/2
    if code in (0, 1, 2):
        signed = code_to_signed(code)
    else:
        signed = code
    if signed != 0:
        return signed
    return resolve_superposed(domain)


def measure_register(
    reg: TritRegister,
    *,
    wires: list[int] | None = None,
    domain: str | None = None,
) -> TritRegister:
    dom = domain or reg.domain or DOMAIN_SPIN_LAW
    out = reg.copy()
    idxs = wires if wires is not None else list(range(out.n))
    if out.field:
        for i in idxs:
            out.spins[i] = measure_field_value(out.field[i], dom)
    else:
        for i in idxs:
            out.spins[i] = measure_spin(out.spins[i], dom)
    # hard poles after measure
    thr = COLLAPSE_THRESHOLD
    from fsot_lib.seeds import SEEDS

    mag = thr + SEEDS.poof
    out.field = [mag if s > 0 else (-mag if s < 0 else 0.0) for s in out.spins]
    return out
