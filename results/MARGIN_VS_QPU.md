# Margin vs what quantum computers have actually done

**overall_ok:** `True`
**wall_s:** `1.40`

This compares **jobs**, not fridge-gate fidelities. A QPU error bar is noise on a unitary. Our margin is residual of FSOT math against the same *hired answer*. Where the object differs, the table says so.

## Live FSOT margins (this repo)

- chemistry fold: **68/68 @ 0.5%** (median 0.0202%)
- QM pin waves: **14/14 @ 0.5%** (median 0.00217%)
- field Ising/MaxCut exact: **13/13**
- G1 vs published BKS 11624: **1.952856159669649%**
- S(QM)=0.9555 · S(QC)=-0.1477

## Side-by-side

| Job | Typical QPU field error | FSOT margin | Same object? |
|-----|-------------------------|-------------|--------------|
| two_qubit_gate | 0.1–1% per gate (fidelity ~99.0–99.9%) | Θ = C_eff·P_var ≈ 0.917 (not a % gate error) | False |
| readout | ~0.5–5% typical superconducting; lower on some ions | 0% RNG readout; wrong *domain* is the residual source | False |
| VQE_small_molecule | Often misses chemical accuracy (1.6 mHa) without heavy mitigation; rare demos claim <1.6 mHa on toy geometries | chemistry fold 68/68 @0.5% (median 0.0202%) | partial — both hired as 'chemistry answers'; objects differ |
| QAOA_MaxCut | Approximation ratio often ~0.7–0.9 of optimum; noise + shallow p | field opt exact 13/13; G1 rel vs published BKS 1.952856159669649% | True |
| Shor_tiny | Demo success; not a scalable period-finding machine | period/factor exact on ledgered tiny N (not RSA) | True |
| Bell_GHZ | Typically a few % below ideal fidelity | sim F=1 is not a hardware fidelity — do not advertise as beating IBM Bell | False |
| surface_code | Logical error still large at small distance; physical ~1e-3 | correctable-t exact on the abstract code; not a device threshold | False |

## Where to refine (FSOT law, not a fudge)

### Gset G1 MaxCut

- current margin: **1.9529%**
- QPU typical: NISQ QAOA rarely reports 800-vertex hardware cuts
- next: Keep collapse+consensus field; more φ-starts from seeds only. Do not add a free temperature or learning rate.
- route: `Quantum_Computing (compute) + Condensed_Matter (graph pack)`

### QM pin M_Z/M_W

- current margin: **0.0530%**
- QPU typical: QPUs do not compute α or M_Z/M_W; that is SM/data
- next: If residual grows, retune *route* (Particle / High_Energy / Atomic) not a coefficient. Default stays pin formula.
- route: `Particle_Physics D=5 / High_Energy D=7 / Atomic D=7`

### add field jobs QPUs are actually paid for

- QPU typical: sampling, small VQE, small QAOA, characterization
- next: More pin-formula QM/QC atlas rows from FSOT-2.1-Lean (Quantum_Information 21 obs, QC gap-fill 177, QM gap-fill 50) ported as *formulas*, not as 2^n circuits.
- route: `import Lean gap-fill observables; still zero free params`

## Lean atlas sitting next door (FSOT-2.1-Lean)

Not yet ported into this granular QC fold — next field-use add:

- **Quantum_Mechanics_gap_fill:** 50 records, median% ~9.5e-5
- **Quantum_Computing_gap_fill:** 177 records, median% ~3.0e-4
- **Quantum_Information:** 21 records, median% 0
- **Quantum_Optics_gap_fill:** 50 records, median% ~9.5e-5
- **source:** FSOT-2.1-Lean verified solves inventory

## Physics reading (correct me if the fluid picture differs)

QC domain is pin-unobserved and S<0 (damping). Reading used here: compute substrate sits *before* observer collapse; QM D=6 observed S>0 is the measurement law. If the fluid picture is different (e.g. QC damping is decoherence-class on purpose), say how the system should interact and we will route that way.

## Reproduce

```powershell
cd "C:\Users\damia\Desktop\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_quantum.margin_vs_qpu
```
