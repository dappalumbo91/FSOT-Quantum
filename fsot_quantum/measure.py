"""
Measurement / collapse — FSOT valve path only.

Collapse threshold Θ = C_eff · P_var (seed-derived).
Superposed resolution uses domain scalar sign (no free RNG, no Born ad-hoc).

When a continuous field is present, collapse_scalar is the authority.
When only discrete trits are present, ±1 are already eigenstates;
superposed (0) resolves via sign(S(domain)).
"""

from __future__ import annotations

from fsot_quantum.domains import DOMAIN_SPIN_LAW
from fsot_quantum.qubit import TritRegister, hard_embed_spins
from fsot_quantum.scalar import domain_scalar
from fsot_quantum.seeds import COLLAPSE_THRESHOLD
from fsot_quantum.trinary import SPIN_DOWN, SPIN_UP, SUPERPOSED, collapse_scalar


def resolve_superposed(domain: str = DOMAIN_SPIN_LAW) -> int:
    """
    Resolve 0 using domain scalar sign.
    Quantum_Mechanics: S > 0 → UP (emergence under observation).
    Quantum_Computing: S < 0 → DOWN (compute substrate damping).
    """
    s = domain_scalar(domain)
    if s > 0:
        return int(SPIN_UP)
    if s < 0:
        return int(SPIN_DOWN)
    return int(SUPERPOSED)


def measure_spin(t: int, domain: str = DOMAIN_SPIN_LAW) -> int:
    """Measure one discrete spin (superposed resolves)."""
    t = int(t)
    if t != 0:
        return t
    return resolve_superposed(domain)


def measure_field_value(v: float, domain: str = DOMAIN_SPIN_LAW) -> int:
    """Collapse continuous fluid sample."""
    c = collapse_scalar(float(v), COLLAPSE_THRESHOLD)
    if c != 0:
        return c
    # exactly in superposed band — domain resolve
    return resolve_superposed(domain)


def measure_register(
    reg: TritRegister,
    *,
    wires: list[int] | None = None,
    domain: str | None = None,
    collapse_field: bool = True,
) -> TritRegister:
    """
    Measure selected wires (default all). Returns new register of eigen-spins.
    """
    dom = domain or reg.domain or DOMAIN_SPIN_LAW
    out = reg.copy()
    idxs = wires if wires is not None else list(range(out.n))

    if collapse_field and out.field:
        for i in idxs:
            out.spins[i] = measure_field_value(out.field[i], dom)
        # refresh field to hard poles after measure
        out.field = hard_embed_spins(out.spins)
    else:
        for i in idxs:
            out.spins[i] = measure_spin(out.spins[i], dom)
        out.field = hard_embed_spins(out.spins)
    return out


def coherence_fraction(spins: list[int]) -> float:
    """Fraction of non-superposed spins (active poles)."""
    if not spins:
        return 0.0
    return sum(1 for s in spins if int(s) != 0) / len(spins)
