'''
L(r) + R(l,Y~U) + A(SH2) -> L(r!1).R(l!1,Y~U!2).A(SH2!2), k=0.1
L(r!1).R(l!1,Y~U!2).A(SH2!2) -> L(r) + R(l,Y~U) + A(SH2), k=0.3

Initial values:
L(r): 10000.0
R(l,d,Y~U): 5000.0
A(SH2,Y~U): 2000.0
'''

from func import *

with molecule_types:
     L(r)
#     R(l, d, Y(U))
     R(l, d, Y(U, P))
#     A(SH2, Y(U))
     A(SH2, Y(U, P))

with molecule_inits:
    L(r) [10000]
    R(l, d, Y(U)) [5000]
    A(SH2, Y(U)) [2000]

with reaction_rules:
#     L(r) + R(l, Y(U)) + A(SH2) > L(r[1]).R(l[1], Y(U)[2]).A(SH2[2]) [MassAction(.1)]
#     L(r[1]).R(l[1], Y(U)[2]).A(SH2[2]) > L(r) + R(l, Y(U)) + A(SH2) [MassAction(.3)]

#     L(r) + R(l, Y(U)) + A(SH2) <> L(r[1]).R(l[1], Y(U)[2]).A(SH2[2]) [L(r), A(SH2)]| MassAction2(.1, .3)
     L(r) + R(l, Y(U)) + A(SH2) <_> L(r[1]).R(l[1], Y(U)[2]).A(SH2[2]) [L(r), A(SH2)]| MassAction2(.1, .3)
