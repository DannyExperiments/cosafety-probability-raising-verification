# Problem and proof outline

Given an explicit finite rational MDP, a deterministic Rabin effect automaton and a DFA accepting exactly the minimal good prefixes of a co-safety cause, check condition (coS). For every such word and every scheduler giving it positive probability, conditioning on it must strictly raise the effect probability. [Source](https://lmcs.episciences.org/12897/pdf#page=60)

## First deviation

Read both monitors in the MDP product. For a fixed word and prefix action distributions, partition the remaining mass by its first deviation. A scheduler can minimize the effect probability after the designated completion and maximize it after each deviation. Full histories allow these choices even after states merge. The maximum gap is the sum of each deviation probability times its continuation maximum minus the endpoint minimum.

## Deciding all feasible words

For each possible endpoint minimum, keep designated support paths reaching a matching terminal without an earlier accepting prefix. Pay one on completion and one plus the continuation maximum minus the endpoint minimum on deviation. All payments are nonnegative. Exact reachability optimization handles an auxiliary choice of designated successor, including zero immediate probability for that successor. At value below one, no violating word exists. At value above one, a finite truncation and small positive perturbation witness a violation. At equality, a word witnesses failure precisely when it follows Bellman-tight positive-support edges to a terminal. This is a graph reachability check.

The number of thresholds, product sizes and exact reachability programs are polynomial. [Complete proof](../paper/manuscript.pdf)
