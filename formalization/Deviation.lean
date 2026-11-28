import Std
namespace Deviation
open Std Lean.Grind
variable {R I : Type} [CommRing R] [LE R] [LT R] [IsLinearOrder R] [LawfulOrderLT R] [OrderedRing R]

def total (w : I → R) (f : I → R) : List I → R
  | [] => 0
  | i::t => w i*f i+total w f t

omit [LE R] [LT R] [IsLinearOrder R] [LawfulOrderLT R] [OrderedRing R] in
theorem shift (xs : List I) (w f : I → R) (c : R) :
    total w (fun i => f i-c) xs = total w f xs - total w (fun _ => 1) xs*c := by
  induction xs with
  | nil => simp [total]; grind
  | cons i t ih => simp only [total,ih];grind

theorem upper (xs : List I) (w u v : I → R)
    (bound : ∀ i ∈ xs, 0 ≤ w i ∧ u i ≤ v i) : total w u xs ≤ total w v xs := by
  induction xs with
  | nil => exact Std.le_refl _
  | cons i t ih =>
    have head := bound i (by simp)
    have mul := OrderedRing.mul_le_mul_of_nonneg_left head.2 head.1
    have tail := ih (by grind)
    simp only [total];grind

theorem mass_nonneg (xs : List I) (w : I → R) (h : ∀ i ∈ xs, 0 ≤ w i) :
    0 ≤ total w (fun _ => 1) xs := by
  induction xs with
  | nil => simp [total]
  | cons i tail ih =>
    have head := h i (by simp)
    have rest := ih (by grind)
    simp only [total];grind

/-- The attainable envelope for compatible branch continuations. Its
interpretation as a scheduler uses the first-deviation pasting in the paper. -/
theorem envelope (xs : List I) (w v : I → R) (q h : R)
    (wpos : ∀ i ∈ xs, 0 ≤ w i) (normalize : q+total w (fun _ => 1) xs = 1) :
    (∀ (u : I → R) (t : R), h ≤ t → (∀ i ∈ xs, u i ≤ v i) →
      q*t+total w u xs-t ≤ total w (fun i => v i-h) xs) ∧
    q*h+total w v xs-h = total w (fun i => v i-h) xs := by
  have mass := mass_nonneg xs w wpos
  have qeq : q = 1-total w (fun _ => 1) xs := by grind
  rw [shift,qeq]
  constructor
  · intro u t ht hu
    have sumLe := upper xs w u v (by grind)
    have weighted := OrderedRing.mul_le_mul_of_nonneg_left ht mass
    grind
  · grind
end Deviation
#print axioms Deviation.envelope
