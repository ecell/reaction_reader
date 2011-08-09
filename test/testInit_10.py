'''
L(r) + R(l) -> L(r!1).R(l!1), k = 0.1
L(r) + R(l,Y~U) -> L(r!1).R(l!1,Y~U), k = 0.1
L(r!1).R(l!1) -> L(r) + R(l), k = 0.3

Initial values:
L(r): 10000.0
R(l,d,Y~U): 10000.0
'''

from func import *

with molecule_types:
     L(r)
     R(l, d, Y(U))
     A(SH2, Y(U))

with molecule_inits:
    L(r) [10000]
    R(l, d, Y(U)) [10000]

with reaction_rules:
     L(r) + R(l) > L(r[1]).R(l[1])|MassAction(0.1)
     L(r) + R(l, Y(U)) > L(r[1]).R(l[1], Y(U)) |MassAction(0.1)
     L(r[1]).R(l[1]) > L(r) + R(l) |MassAction(0.3)