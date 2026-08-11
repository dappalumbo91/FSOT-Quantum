/-
  FSOT-Quantum pack contracts (Lean 4).

  Runtime: fsot_lib.trinary.pack_u64 / unpack_u64
  Codes {0,1,2}, 32 per UInt64, 2 bits each.
-/

import FSOTQuantumFormal.Trinary

namespace FSOT.Quantum

/-- Abstract 32-trit packed word (carrier UInt64). -/
structure Packed32 where
  raw : UInt64
  deriving Repr

/-- Bit width per trit. -/
def bitsPerTrit : Nat := 2

theorem bitsPerTrit_eq : bitsPerTrit = 2 := rfl

/-- Capacity: 64 / 2 = 32. -/
theorem pack_capacity :
    statesPerU64 * bitsPerTrit = 64 := by
  native_decide

/-- Illegal pack code 3 is not a Spin. -/
theorem ofBits_three_none : Spin.ofBits? 3 = none := by
  rfl

/-- Encoding injectivity on Spin. -/
theorem toBits_injective (a b : Spin) (h : a.toBits = b.toBits) : a = b := by
  cases a <;> cases b <;> simp [Spin.toBits] at h <;> try rfl
  all_goals cases h

end FSOT.Quantum
