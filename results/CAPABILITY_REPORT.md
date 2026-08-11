# FSOT-QC Capability Report

**overall_ok:** `True`
**device:** `cuda`
**algorithms:** 16/16 (100.0%)
**gpu_parallel_all_ok:** `True`
**wall_s:** `1.6012`
**Θ:** `0.9174663774653723`

## Algorithms

| Name | OK | Expected | Got |
|------|----|----------|-----|
| deutsch_jozsa_n4 | True | `constant` | `constant` |
| deutsch_jozsa_n4 | True | `constant` | `constant` |
| deutsch_jozsa_n4 | True | `balanced` | `balanced` |
| deutsch_jozsa_n8 | True | `balanced` | `balanced` |
| bernstein_vazirani_n4 | True | `[1, 0, 1, 1]` | `[1, 0, 1, 1]` |
| bernstein_vazirani_n8 | True | `[1, 1, 0, 0, 1, 0, 1, 1]` | `[1, 1, 0, 0, 1, 0, 1, 1]` |
| bernstein_vazirani_n12 | True | `[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]` | `[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]` |
| grover_search_N16 | True | `7` | `7` |
| grover_search_N64 | True | `41` | `41` |
| grover_search_N256 | True | `200` | `200` |
| grover_search_N1024 | True | `777` | `777` |
| bell_correlation | True | `1.0` | `1.0` |
| phase_class_estimation | True | `{'class_QM': 'emergence', 'class_QC': 'damping'}` | `{'S_QM': 0.9555063001027194, 'S_QC': -0.14767310363368633, 'class_QM': 'emergence', 'class_QC': 'damping'}` |
| ising_n6 | True | `-6` | `-6` |
| ising_n5 | True | `-3` | `-3` |
| qft_role_phase_rotation | True | `{'shape': [32, 64], 'finite': True}` | `{'shape': [32, 64], 'finite': True, 'device': 'cuda'}` |

## GPU parallel

- **pack_stress:** ok=True device=cuda detail=`{'groups': 32768, 'trits': 1048576, 'seconds': 0.005619100062176585, 'roundtrip_ok': True, 'device': 'cuda'}`
- **grover_batch:** ok=True device=cuda detail=`{'batch': 256, 'n_items': 512, 'correct': 256, 'accuracy': 1.0, 'seconds': 0.0027884000446647406, 'instances_per_sec': 91808.92120907271, 'device': 'cuda'}`
- **bv_batch:** ok=True device=cuda detail=`{'batch': 128, 'n': 8, 'correct': 128, 'accuracy': 1.0, 'seconds': 0.0002647999208420515, 'device': 'cuda', 'note': 'parity oracle f(x)=s·x — exact recover on basis probes'}`
- **consensus_batch:** ok=True device=cuda detail=`{'batch': 16, 'seq': 48, 'dim': 48, 'out_shape': [16, 48, 48], 'seconds': 0.057294400059618056, 'finite': True, 'device': 'cuda'}`

## Goal

FSOT quantum capability on GPU/CPU — answers without quantum hardware infrastructure; parallel interface = GPU

