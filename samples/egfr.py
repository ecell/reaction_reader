with molecule_types:
#    A(a1 = (U, A1), a2 = (U, A2), a3 = (U, A3))
#    B(b = (a, b, 0, 1))
#    C(C)
#    D(d, d1 = (0, 1), d2 = (0, 1), d3 = (0, 1))
#    E(e)
    egf(r)
    egfr(l, d, Y = (U, P))

with molecule_inits:
#    E(e) [500]
#    D(d, d1 = 0, d2 = 0, d3 = 1) [420]
#    D(d, d1 = 1, d2 = 1, d3 = 0) [440]
#    A(a1 = U, a3 = A3, a2 = U) [300]
#    C(C) [200]
#    B(b = a) [610]
#    B(b = b) [620]
#    B(b = 0) [630]
#    B(b = 1) [640]
    egf(r) [160]
    egfr(l, d, Y = P) [140]
    egfr(l, d, Y = U) [120]
    egf(r[1]).egfr(l[1], d, Y = U) [100]

with reaction_rules:
    egf(r) > egfr(l) | 0.1
#    egf(r) + egfr(l) > egf(r[1]).egfr(l[1]) [egf(r)] | mm(k, k)

