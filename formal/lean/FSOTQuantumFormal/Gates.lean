/-
  FSOT-Quantum gate algebra (Lean 4).

  Runtime twin: fsot_quantum/gates.py
  No complex amplitudes; trinary ops only.
-/

import FSOTQuantumFormal.Trinary

namespace FSOT.Quantum

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

theorem pair_superposed_left (t : Spin) : pair .superposed t = .superposed := by
  cases t <;> rfl

theorem pair_superposed_right (s : Spin) : pair s .superposed = .superposed := by
  cases s <;> rfl

def consensus : Spin → Spin → Spin
  | a, b => if a = b then a else .superposed

theorem consensus_refl (s : Spin) : consensus s s = s := by
  simp [consensus]

theorem consensus_disagree :
    consensus .spinUp .spinDown = .superposed := by
  simp [consensus]

/-- CX-analog: control up flips target; super → super; down holds. -/
def cxTarget (c t : Spin) : Spin :=
  match c with
  | .superposed => .superposed
  | .spinUp => neg t
  | .spinDown => t

theorem cx_control_up_flips (t : Spin) : cxTarget .spinUp t = neg t := by
  rfl

theorem cx_control_down_holds (t : Spin) : cxTarget .spinDown t = t := by
  rfl

theorem cx_control_super_super (t : Spin) : cxTarget .superposed t = .superposed := by
  rfl

/-- CCX: both controls up → flip target; either super → super; else hold. -/
def ccxTarget (c1 c2 t : Spin) : Spin :=
  match c1, c2 with
  | .spinUp, .spinUp => neg t
  | .superposed, _ => .superposed
  | _, .superposed => .superposed
  | _, _ => t

theorem ccx_both_up (t : Spin) : ccxTarget .spinUp .spinUp t = neg t := by
  rfl

end FSOT.Quantum
