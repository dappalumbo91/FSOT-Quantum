/-
  Integer stamps for the formula catalog (this fold).
  Float identities live in Python runtime obligations Q-FORM-*.
-/

namespace FSOT.Quantum.Formulas

/-- Universal K · 10⁶ (rounded). Same as Fold.kMicro. -/
def kMicro : Nat := 420222

/-- Bubble-bleed fraction · 10⁶ (H0_global/67.4 − 1). -/
def bleedMilli : Nat := 15431

theorem kMicro_eq : kMicro = 420222 := rfl
theorem bleedMilli_eq : bleedMilli = 15431 := rfl

/-- Pin surface: K-micro and bleed-milli are the locked integers. -/
theorem formula_surface :
    kMicro = 420222 ∧ bleedMilli = 15431 := by
  refine ⟨kMicro_eq, bleedMilli_eq⟩

end FSOT.Quantum.Formulas
