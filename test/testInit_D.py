'''

'''

from func import *

with molecule_types:
    A(SH2, Y(U, P))
    B(a, c1(d, x, z))

with molecule_inits:
    A(SH2, Y(U)) [2000]
    B(a, c1(d))  [1000]

with reaction_rules:
    B(c1(d)) <_> B(c1(x)) | MassAction2(0.3, 0.1)
    B(c1(x)) <_> B(c1(z)) | (MassAction(0.3), 0.1)
    B(c1(z)) <_> B(c1(d)) | (0.3, 0.1)

    A(SH2) + B(a) <_> A(SH2[1]).B(a[1]) | 0.3

    A(Y(U)).B() > A(Y(P)).B() | 0.3
