/-
  FSOT-Quantum — Trinary spin model for bare-metal quantum pathway.

  Spins:
    spinDown   = -1
    superposed =  0
    spinUp     = +1

  Pack codes match FSOT-GPU Trinary.lean: 0 / 1 / 2.
  Theory authority: FSOT-2.1-Lean pin D1D38A.
-/

namespace FSOT.Quantum

inductive Spin
  | spinDown
  | superposed
  | spinUp
  deriving DecidableEq, Repr

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

theorem Spin.roundtrip (s : Spin) : Spin.ofBits? s.toBits = some s := by
  cases s <;> rfl

def neg : Spin → Spin
  | .spinDown   => .spinUp
  | .superposed => .superposed
  | .spinUp     => .spinDown

theorem neg_involutive (s : Spin) : neg (neg s) = s := by
  cases s <;> rfl

def pair : Spin → Spin → Spin
  | .superposed, _ => .superposed
  | _, .superposed => .superposed
  | .spinUp, .spinUp => .spinUp
  | .spinDown, .spinDown => .spinUp
  | .spinUp, .spinDown => .spinDown
  | .spinDown, .spinUp => .spinDown

def consensus : Spin → Spin → Spin
  | a, b => if a = b then a else .superposed

/-- States per UInt64 at 2 bits / spin. -/
def statesPerU64 : Nat := 32

theorem statesPerU64_eq : statesPerU64 = 32 := rfl

end FSOT.Quantum
