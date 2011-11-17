'''

'''

from func import *

with molecule_types:
    A(SH2, Y(U, P))
#    B(c1(d, x), c2(d, x), c3(d, x), c4(d, x), c5(d, x), c6(d, x))
    B(a, c1(d, x), c2(d, x), c3(d, x))

with molecule_inits:
    A(SH2, Y(U)) [2000]
#    B(c1(d), c2(d), c3(d), c4(d, x), c5(d, x), c6(d, x)) [1000]
    B(a, c1(d), c2(d), c3(d)) [1000]

with reaction_rules:
    B(c1(d)) <_> B(c1(x)) [A(SH2)] | MassAction2(0.3, 0.1)
    B(c2(d)) <_> B(c2(x)) [A(SH2)] | (MassAction(0.3), 0.1)
    B(c3(d)) <_> B(c3(x)) [A(SH2)] | (0.3, 0.1)
#    B(c4(d)) <_> B(c4(x))          | MassAction2(0.3, 0.1)
#    B(c5(d)) <_> B(c5(x))          | (MassAction(0.3), 0.1)
#    B(c6(d)) <_> B(c6(x))          | (0.3, 0.1)

    A(SH2) + B(a) <_> A(SH2[1]).B(a[1]) | 0.3

    A(Y(U)).B() > A(Y(P)).B() | 0.3
