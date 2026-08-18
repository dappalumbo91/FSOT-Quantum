# Probability as FSOT multiverse branching

**overall_ok:** `True` · **19/19** · pin D1D38A **not edited**

Probability here is not a Born-rule add-on and not a free parameter. It is the **branch density** of exhaustive folds of \(S=K(T_1+T_2+T_3)\).

Genetics already has the trinary: \(+1\) and \(-1\) are collapsed observations (`trit_not` of each other). \(0\) is superposed (homologs disagree — do not average the two collapses).

## Three folds of one spin

| Trit | Fold | How |
|------|------|-----|
| \(+1\) | collapsed up | `observed=True`, domain \(\delta\psi\) |
| \(-1\) | collapsed down | `observed=True`, \(\delta\psi+\pi\) (`trit_not`) |
| \(0\) | superposed | `observed=False` |

Density of a fold is \(|S|\) of that evaluation, then normalize. A measurement that insists on a collapse renormalizes the two observed folds. The \(0\)-trit stays a third world, not noise.

## Live spin branches

| Domain | \(D_{\mathrm{eff}}\) | \(S_{+1}\) | \(S_{-1}\) | \(S_0\) | \(w_{+1}\) | \(w_{-1}\) | \(w_0\) | collapsed \(+1/-1\) |
|--------|---------------------:|-----------:|-----------:|--------:|--------:|--------:|------:|--------------------:|
| Quantum_Mechanics | 6 | `0.955506` | `-4.312160` | `-0.656021` | 0.1613 | 0.7280 | 0.1107 | 0.1814 / 0.8186 |
| Quantum_Computing | 11 | `0.336015` | `1.699232` | `-0.147673` | 0.1539 | 0.7784 | 0.0676 | 0.1651 / 0.8349 |
| Quantum_Optics | 11 | `0.408171` | `0.583430` | `-0.294047` | 0.3175 | 0.4538 | 0.2287 | 0.4116 / 0.5884 |
| Particle_Physics | 5 | `0.950413` | `-4.267134` | `-0.645781` | 0.1621 | 0.7278 | 0.1101 | 0.1822 / 0.8178 |

Living table \(S(\mathrm{QM})=+0.9555\) **is** the \(+1\) fold. Collapsed QM densities are **0.1814 / 0.8186**, not a postulated \(1/2\). The T1 look-cosine alone *is* balanced (\(|f_1|=|f_-1|=0.497364\)) — that is the observer-factor lemma, not the full trit_not pair.

## How this maps the usual rules

| Usual talk | FSOT |
|------------|------|
| \(P=\#\text{wanted}/\#\text{possible}\) | density of named folds / all folds of that event |
| Theoretical \(1/6\) die | arity of 6 indistinguishable exclusive faces |
| Theoretical fair coin | arity 2 **or** look-cosine lemma — not the QM trit_not pair |
| Independent | product of branch densities (separate spins) |
| Dependent | remaining exclusive set, renormalize |
| Mutually exclusive | \(+1\) and \(-1\) of one spin; weights sum to 1 |
| Law of large numbers | \(\varphi\)-walk of many copies settles to the seed densities |
| Empirical | same densities, counted |
| Subjective | not used. No personal coefficient. |
| Born \(\|\psi\|^2\) | **not added**. Weights are \(\|S\|\). |

## Checks

| ID | Question | OK |
|----|----------|:--:|
| `pin_S_QM_plus` | Is the +1 QM fold the living table S(QM)? | True |
| `partition_Quantum_Mechanics` | Do |S| branch weights on Quantum_Mechanics sum to 1? | True |
| `partition_Quantum_Computing` | Do |S| branch weights on Quantum_Computing sum to 1? | True |
| `partition_Quantum_Optics` | Do |S| branch weights on Quantum_Optics sum to 1? | True |
| `partition_Particle_Physics` | Do |S| branch weights on Particle_Physics sum to 1? | True |
| `collapsed_partition_Quantum_Mechanics` | Do collapsed |S| weights on Quantum_Mechanics sum to 1? | True |
| `collapsed_partition_Quantum_Computing` | Do collapsed |S| weights on Quantum_Computing sum to 1? | True |
| `collapsed_partition_Quantum_Optics` | Do collapsed |S| weights on Quantum_Optics sum to 1? | True |
| `collapsed_partition_Particle_Physics` | Do collapsed |S| weights on Particle_Physics sum to 1? | True |
| `look_cosine_half` | Is the T1 look-cosine π-shift balanced (|f+|=|f-|)? | True |
| `full_scalar_not_born_half` | Is the full-scalar trit_not pair different from a Born 1/2? | True |
| `die_arity_6` | Fair die: six indistinguishable exclusive faces? | True |
| `coin_arity_2` | Fair coin as two indistinguishable faces? | True |
| `independent_plus_plus` | Independent: two QM +1 collapses (product of densities)? | True |
| `dependent_two_aces` | Dependent: P(ace then ace) from remaining exclusive set? | True |
| `mutex_plus_minus` | Mutually exclusive: +1 and -1 of one QM spin? | True |
| `lln_qm_collapsed` | LLN: 10000 φ-walk copies settle to collapsed |S|? | True |
| `superposition_own_fold` | Is the 0-trit a distinct unobserved fold (weight > 0)? | True |
| `pin_untouched` | Were only pin seeds used? | True |

## What we did not do

- Did not post a Born rule or square a wavefunction.
- Did not invent a coefficient to crawl collapsed QM to \(1/2\).
- Did not treat a die as six QM phases (that would be the wrong object).
- Did not average \(+1\) and \(-1\) to make the \(0\)-trit.
- Did not touch `vendor/fsot_compute.py`.

```powershell
python -m fsot_quantum.probability_branch
```
