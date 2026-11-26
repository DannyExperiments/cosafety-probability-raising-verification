"""Exact layered fixtures for the first-divergence optimizer and mass tie test."""
from fractions import Fraction as F
from itertools import product

# Each row schedules a or b. Outcome 0/1 remains on a possible designated
# path; at layer one these are two acceptable end states with different h.
# Outcome 2 is an off-path state. Residual maxima are stipulated (realizable
# using terminal chance branches and, for nonterminal states, the recurrence).
rows = [(F(a,2), F(b,2), F(2-a-b,2))
        for a in range(3) for b in range(3-a)]
pairs = list(product(rows, repeat=2))

def test(root, layer0, layer1, terminal):
    # terminal minimum equals maximum. State 2 in either layer is off-path.
    ac = [layer0, layer1]
    best = [max(sum(p*v for p,v in zip(r,terminal)) for r in a) for a in ac] + [F(0)]
    direct = verifier = False
    for j,h in enumerate(terminal[:2]):
        # Independent oracle: for each word, optimize the original effect
        # probability with the on-word continuation fixed at h.
        # For this layered setting the objective is multilinear in the two
        # action mixtures, so inspect pure corners. On equality require a
        # maximizing pure corner whose designated word has positive mass.
        for i in range(2):
            corners = []
            for p,r in product(root,ac[i]):
                chance = sum(p[z]*best[z] for z in range(3) if z != i)
                chance += p[i]*sum(r[z]*terminal[z] for z in range(3))
                corners.append((chance,p[i]*r[j]))
            if not any(q for value,q in corners):
                continue
            optimum = max(value for value,q in corners)
            direct |= optimum > h or (optimum == h and
                                      any(value==optimum and q for value,q in corners))
        # Verifier: eligible successor -> physical action, then compute
        # Bellman value and propagate only positive optimal equality arcs.
        cases = []
        for i in range(2):
            if not any(r[j] for r in ac[i]) or not any(p[i] for p in root):
                continue
            leaf = [(r[j] + sum(r[z]*(1+terminal[z]-h)
                                     for z in range(3) if z != j), bool(r[j]))
                    for r in ac[i]]
            v = max(w for w,q in leaf)
            live = any(w==v and q for w,q in leaf)
            for p in root:
                w = p[i]*v + sum(p[z]*(1+best[z]-h) for z in range(3) if z!=i)
                cases.append((w,bool(p[i]) and live))
        if cases:
            u = max(w for w,q in cases)
            verifier |= u > 1 or (u == 1 and any(w==u and q for w,q in cases))
    assert direct == verifier
    return direct

# The strict equality trap in the proof: action A has U=1 but no cylinder;
# action B has positive cylinder but U=3/4.
h=F(1,2)
values=(F(1), F(1,2) + F(1,2)*(1-h))
assert values == (F(1),F(3,4))
for denominator in range(1,40):
    q = F(1,denominator)
    assert (1-q)*values[0]+q*values[1] < 1

# Deterministic sampling of distinct fixtures over rational rows and values.
import random
rng=random.Random(890)
c=0
for _ in range(6600):
    a,b,r=(rng.choice(pairs) for _ in range(3))
    t=tuple(F(rng.randrange(5),4) for _ in range(3))
    c += test(r,a,b,t)
print("6600 exact layered trials agree; violations:", c)


def one_step_controls():
    """Direct conditional probability and independent verifier payoff agree."""
    h = F(1, 2)
    tested = 0
    for r in (F(1, 4), F(1, 2), F(3, 4)):
        a_bonus = 1 + r - h
        b_bonus = F(3, 4)
        relaxed = max(a_bonus, b_bonus)
        for numerator in range(17):
            share = F(numerator, 16)
            cylinder = share / 2
            original = (1 - share) * r + share / 4
            value = (1 - share) * a_bonus + share * b_bonus
            if cylinder:
                assert value == 1 + original - h
            assert value <= relaxed
            tested += 1
        assert relaxed == r + h or relaxed == b_bonus
    assert F(1, 2) * F(3, 4) + F(1, 2) / 4 == h
    print(f"Equality fixture: {tested} exact one-step mixtures agree.")


def cyclic_controls():
    """Check short words that revisit the designated node before completing."""
    h = F(1, 2)
    p = F(1, 2)
    count = 0
    for r, always_finish in product((F(1, 4), F(1, 2), F(3, 4)), (False, True)):
        b = F(1) if always_finish else F(3, 4)
        # L loops with probability p or moves to a state with effect chance r.
        # B ends immediately, either certainly or with a half chance of failure.
        best_effect = max(r, h if always_finish else h / 2)
        loop_fixed_point = 1 + r - h
        finish_l = 1 + p * best_effect + (1-p) * r - h
        u = max(b, loop_fixed_point, finish_l)
        assert u == max(b, p*u + (1-p)*(1+r-h), finish_l)
        witnesses = 0
        for visits in range(20):
            completion = p**visits * (1 if always_finish else F(1, 2))
            effect = (1 - p**visits)*r + p**visits * (h if always_finish else h/2)
            candidate = (1-p**visits) * loop_fixed_point + p**visits * b
            assert completion > 0 and candidate == 1 + effect - h
            witnesses += effect >= h
            count += 1
        assert bool(witnesses) == (u > 1 or (u == 1 and b == u))
    print(f"Cyclic controls: {count} exact words include equality with and without a positive witness.")


if __name__ == "__main__":
    one_step_controls()
    cyclic_controls()
