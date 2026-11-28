# Claims and evidence

| Claim | Evidence |
| --- | --- |
| Matches published coS condition | Definition 6.11 and §6.2.1, with explicit minimal-prefix DFA and Rabin DRA. |
| Exact maximum gap for a fixed word | Paper §2. Switch to continuation maxima after a first deviation and to the minimum after completion. |
| Deterministic polynomial-time verification | Paper §3. Product, reachability LP and positive-tight-arc graph. |
| Equality diagnosis | Paper §4, rotating worked example and offline explorer. |
| Finite replay | 6,600 exact layered trials, 51 one-step mixtures and 120 cyclic words. |

## Lean verification

For finitely many first-deviation parts with nonnegative masses and total probability one including the designated word, Lean proves the gap upper bound from the maximal continuation values and its exact equality at those values and the minimal designated value. The scheduler pasting and automaton algorithm remain in the paper. [Source and replay](formalization/README.md)
