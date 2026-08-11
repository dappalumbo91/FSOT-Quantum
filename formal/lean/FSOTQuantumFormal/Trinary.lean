/-
  FSOT-Quantum — Trinary spin model (Lean 4).

  Matches: FSOT-GPU Trinary.lean, Zig twin, fsot_lib.trinary
-/

namespace FSOT.Quantum

inductive Spin where
  | spinDown
  | superposed
  | spinUp
  deriving DecidableEq, Repr, Inhabited

def Spin.toInt : Spin → Int
  | .spinDown   => -1
  | .superposed => 0
  | .spinUp     => 1

def Spin.toBits : Spin → Nat
  | .spinDown   => 0
  | .superposed => 1
  | .spinUp     => 2

def Spin.ofBits? : Nat → Option Spin
  | 0 => some .spinDown
  | 1 => some .superposed
  | 2 => some .spinUp
  | _ => none

theorem Spin.roundtrip_bits (s : Spin) :
    Spin.ofBits? s.toBits = some s := by
  cases s <;> rfl

theorem Spin.toBits_le_two (s : Spin) : s.toBits ≤ 2 := by
  cases s <;> decide

def Spin.ofInt? : Int → Option Spin
  | -1 => some .spinDown
  | 0  => some .superposed
  | 1  => some .spinUp
  | _  => none

theorem Spin.roundtrip_int (s : Spin) :
    Spin.ofInt? s.toInt = some s := by
  cases s <;> rfl

/-- Valid pack codes are only {0,1,2}. -/
def validCode (n : Nat) : Prop := n ≤ 2

theorem toBits_valid (s : Spin) : validCode s.toBits := by
  cases s <;> simp [validCode, Spin.toBits]

def statesPerU64 : Nat := 32

theorem statesPerU64_eq : statesPerU64 = 32 := rfl

/-- Collapse threshold identity class: Θ = C_eff · P_var (runtime goldens).
    Formal surface carries the contract name; numeric equality is Python/Zig parity. -/
structure CollapseThresholdContract where
  formula : String := "C_eff * P_var"
  deriving Repr

end FSOT.Quantum
