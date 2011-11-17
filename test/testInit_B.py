'''

'''

from func import *

with molecule_types:
    L(r)
    R(l, d, Y(U, P))
    A(SH2, Y(U, P))
#    B(b)

with molecule_inits:
    L(r) [10000]
    R(l, d, Y(U)) [5000]
    A(SH2, Y(U)) [2000]

with reaction_rules:
    L(r) + R(l, Y(U)) + A(SH2) <_> L(r[1]).R(l[1], Y(U)[2]).A(SH2[2]) | (1.1, 0.3)

    R(Y(U)) <_> R(Y(P)) | 1.3, 0.3
