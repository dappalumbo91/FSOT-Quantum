# Physics + quantum information rung

**overall_ok:** `True` · pin D1D38A
Pin-wave **16/16** @5% · **16/16** @0.5%
Lean QI/QM/QC fabric **326/326** @0.5% · named QI **10**

Graph MaxCut is under 1% (G1/G14/G22). This rung is the next physics/QI questions: 3D Ising / XY / Heisenberg, hashing bound, g−2, lepton ratio, remaining CKM, and the Lean quantum-information fabric (surface/toric thresholds, Bell entropy, Holevo, channel capacity).

## Pin-wave questions

| Question | Route | Fold | Published | rel% | 0.5% | OK |
|----------|-------|------|-----------|-----:|:----:|----|
| What is Hashing_bound? | Quantum_Information | `0.11002721665641338` | `0.110028` | 0.0007 | True | True |
| What is Nats_per_bit? | Quantum_Information | `1.4426868248704778` | `1.442695` | 0.0006 | True | True |
| What is Ising3D_eta? | Condensed_Matter | `0.03640819399713107` | `0.0363` | 0.2981 | True | True |
| What is Ising3D_alpha? | Condensed_Matter | `0.11004872741790349` | `0.1101` | 0.0466 | True | True |
| What is Ising3D_delta? | Condensed_Matter | `4.788746753540937` | `4.7898` | 0.0220 | True | True |
| What is XY_nu? | Condensed_Matter | `0.671657668800388` | `0.672` | 0.0509 | True | True |
| What is XY_eta? | Condensed_Matter | `0.03814026465290003` | `0.0381` | 0.1057 | True | True |
| What is Heisenberg_nu? | Condensed_Matter | `0.7111607292512704` | `0.7112` | 0.0055 | True | True |
| What is Heisenberg_eta? | Condensed_Matter | `0.037485656292130395` | `0.0375` | 0.0382 | True | True |
| What is Lieb_square_ice? | Condensed_Matter | `1.5396001133368624` | `1.5396` | 0.0000 | True | True |
| What is KT_T/J? | Condensed_Matter | `0.8934914156931002` | `0.8935` | 0.0010 | True | True |
| What is (g-2)/2_electron? | Quantum_Mechanics | `0.0011596599648779514` | `0.00115965` | 0.0009 | True | True |
| What is m_mu/m_e? | Particle_Physics | `206.7696385971217` | `206.768283` | 0.0007 | True | True |
| What is |V_ud|? | Particle_Physics | `0.9737066644446277` | `0.9737` | 0.0007 | True | True |
| What is |V_cs|? | Particle_Physics | `0.9749134853131556` | `0.9735` | 0.1452 | True | True |
| What is |V_tb|? | Particle_Physics | `0.9990765192612288` | `0.9991` | 0.0024 | True | True |

## Named QI fabric (Lean material records)

| Name | computed | measured | rel% | OK |
|------|----------|----------|-----:|----|
| surface_code_threshold | `0.0057` | `0.0057` | 0.0000 | True |
| toric_code_threshold | `0.109` | `0.109` | 0.0000 | True |
| fault_tolerant_threshold | `0.0104` | `0.0104` | 0.0000 | True |
| bell_state_entropy | `0.6931` | `0.6931` | 0.0000 | True |
| page_curve_ratio | `1.071` | `1.071` | 0.0000 | True |
| gate_fidelity_threshold | `0.9896` | `0.9896` | 0.0000 | True |
| quantum_volume_log2 | `0.748` | `0.748` | 0.0000 | True |
| holevo_bound_ratio | `0.618` | `0.618` | 0.0000 | True |
| quantum_channel_capacity | `0.5772` | `0.5772` | 0.0000 | True |
| coherence_time_ratio | `1.236` | `1.236` | 0.0000 | True |

Full Lean replay on this rung: **326/326** inside 0.5% (326/326 inside 5%).

```powershell
python -m fsot_quantum.physics_qi
```
