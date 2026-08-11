/-
  FSOT-Quantum — Hilbert fragment contracts (Lean 4).

  Runtime twin: fsot_quantum/hilbert.py, qft_shor.py
  We formalize discrete structure: qubit count, amplitude dimension 2^n,
  and QFT size. Continuous unitarity is runtime-normalized.
-/

namespace FSOT.Quantum.Hilbert

/-- Number of amplitudes for n qubits. -/
def dim (n : Nat) : Nat := 2 ^ n

theorem dim_zero : dim 0 = 1 := by native_decide
theorem dim_one : dim 1 = 2 := by native_decide
theorem dim_two : dim 2 = 4 := by native_decide
theorem dim_three : dim 3 = 8 := by native_decide

theorem dim_mono (n : Nat) : dim n ≤ dim (n + 1) := by
  simp [dim]
  exact Nat.pow_le_pow_right (by decide : 0 < 2) (Nat.le_succ n)

/-- Bell state lives in dim 4. -/
theorem bell_dim : dim 2 = 4 := dim_two

/-- GHZ-3 lives in dim 8. -/
theorem ghz3_dim : dim 3 = 8 := dim_three

/-- Circuit library max n=12 → 4096 amplitudes. -/
theorem dim_twelve : dim 12 = 4096 := by native_decide

/-- QFT size matches register. -/
structure QFTRegister where
  n : Nat
  deriving Repr

def QFTRegister.dim (q : QFTRegister) : Nat := dim q.n

theorem qft_reg_dim (n : Nat) : (QFTRegister.mk n).dim = 2 ^ n := rfl

end FSOT.Quantum.Hilbert
