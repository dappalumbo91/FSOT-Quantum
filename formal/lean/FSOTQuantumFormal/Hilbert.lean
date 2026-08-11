/-
  FSOT-Quantum — Hilbert fragment contracts (Lean 4).
  Runtime twin: fsot_quantum/hilbert.py, circuit_library.py, qft_shor.py
-/

namespace FSOT.Quantum.Hilbert

/-- Number of amplitudes for n qubits. -/
def ampDim (n : Nat) : Nat := 2 ^ n

theorem ampDim_zero : ampDim 0 = 1 := by native_decide
theorem ampDim_one : ampDim 1 = 2 := by native_decide
theorem ampDim_two : ampDim 2 = 4 := by native_decide
theorem ampDim_three : ampDim 3 = 8 := by native_decide

theorem ampDim_mono (n : Nat) : ampDim n ≤ ampDim (n + 1) := by
  simp [ampDim]
  exact Nat.pow_le_pow_right (by decide : 0 < 2) (Nat.le_succ n)

theorem bell_dim : ampDim 2 = 4 := ampDim_two
theorem ghz3_dim : ampDim 3 = 8 := ampDim_three
theorem ampDim_twelve : ampDim 12 = 4096 := by native_decide

/-- Alias used by surface stamp. -/
def dim (n : Nat) : Nat := ampDim n
theorem dim_twelve : dim 12 = 4096 := ampDim_twelve

structure QFTRegister where
  nQubits : Nat
  deriving Repr

def qftDim (q : QFTRegister) : Nat := ampDim q.nQubits

theorem qftDim_eq (n : Nat) : qftDim ⟨n⟩ = 2 ^ n := rfl

end FSOT.Quantum.Hilbert
