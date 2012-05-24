with molecule_types:
#    A(a1 = (U, A1), a2 = (U, A2), a3 = (U, A3))
#    B(b = (a, b, 0, 1))
#    C(C)
#    D(d, d1 = (0, 1), d2 = (0, 1), d3 = (0, 1))
#    E(e)

    egf(r)
    egfr(l, d, Y = (U, P))
#    egfl(l, d[1], X = A, Y = P[1], XX=Axs[3], YY=True, a=a)
    egfl(l, d, Y, XX, X = (A, d), YY=(YY, d), a=(a, d))

    A(a=(P, Y))
    B(b)
    C(c)
    D(d)
    E(e)
    F(f)
    G(g)
    
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

    B(b[1]).A(a=Y[1]) [30]
    A(a=Y[1]).B(b[1]) [30]
    B(b) [10]
    A(a=P) [20]

    egf(r[1]).egfr(l, d, Y = U[1]) [100]

    egf(r[1]).egfr(l[1], d, Y = U) [160]
    egf(r) [160]
    egfl(l, d[1], Y[2], XX[3], X = A, YY=YY, a=a).egf(r[1]).egf(r[2]).egf(r[3]) [140]
#    eg(a=U).egfr(l, d[1], X = A, Y = P[1], XX=Axs[3], YY=True, a=a).eg(a) [140]
    egfr(l, d, Y = U) [120]
    egf(r[1]).egfr(l[1], d[2], Y = U).egf(r[2]) [100]
    pass

with reaction_rules:
    A(a) > B(b) [C(c), C(c)] | 2.1
#    A(a) > B(b) [C(c).C(c)] | 2.2
#    A(a) > B(b) [C(c), C(c)]| 2.3
#    A(a) > B(b) [C(c).C(c), C(c)]| 2.4
#    A(a) > B(b) [C(c), C(c).C(c)]| 2.5
#    A(a) > B(b) [C(c)] | 1.1
    A(a) > B(b).B(b) [C(c)] | 1.2
    A(a) > B(b) + B(b).B(b) [C(c)] | 1.3
    A(a) + B(b).C(c) > D(d)| 0.1
    A(a).A(a) + B(b).C(c) > D(d) | 0.2
    A(a) + A(a).A(a) + B(b).C(c) > D(d)| 0.3

#    egfr(l, d[1], X = A, Y = P[1], XX=Axs[3], YY=True, a=a).eg(a) > A(a) | 0.1
    A(a=P[1]).B(b[1]) > G(g) | 0.1
    A(a) > G(g[1]).B(b[1]) | 0.2
    A(a).B(b) > G(g) | 0.3
    A(a).B(b) > G(g).B(b) | 0.4

    A(a) + B(b) > C(c) [A(a[1]).B(b[1])] | 1.1
    A(a) > B(b) + C(c) [A(a[1]).B(b[1])] | 1.2

    A(a) > B(b) + C(c).D(d) [A(a[1]).B(b[1]), A(a), A(a).B(b).C(c)]| 1.3
    A(a).B(b) > D(d).E(e).F(f) + G(g)| 2.1

#    A(a).B(b) > D(d).E(e).F(f) + G(g) | 2.1
    A(a) + B(b) + C(c) > D(d) + E(e).F(f) [A(a).B(b)] | 2.2

    A(a[1]).B(b[1]) > D(d).E(e).F(f) + G(g) [C(c), C(c)] | 2.1
    A(a) + A(a=P[1]).B(b[1]) + A(a) + A(a).B(b) > D(d).E(e).F(f) + G(g) | 2.1

    egf(r) + egfr(l) > egf(r[1]).egfr(l[1]) [egf(r)] | mm(k, k)

