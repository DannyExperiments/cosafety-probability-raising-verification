# Lean verification

For finitely many first-deviation parts with nonnegative masses and total probability one including the designated word, Lean proves the gap upper bound from the maximal continuation values and its exact equality at those values and the minimal designated value. The scheduler pasting and automaton algorithm remain in the paper.

The checked declaration is `Deviation.envelope`. [Source](Deviation.lean) · [Pinned CI](../.github/workflows/lean.yml)

```sh
lean -DwarningAsError=true formalization/Deviation.lean
```

CI compares the compiler output with the committed axiom report.
