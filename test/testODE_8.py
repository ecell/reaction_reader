'''
L(r) + R() -> L(r!1).R(l!1), k = 0.1
L(r!1).R(l!1) -> L(r) + R(l), k = 0.3

Initial values:
L(r): 10000.0
R(l,d,Y~U): 5000.0
L(r!1).R(l!1,d,Y~U): 2000
'''

from func import *

with molecule_types:
     L(r)
     R(l, d, Y(U))
     A(SH2, Y(U))

with reaction_rules:
     L(r) + R() > L(r[1]).R(l[1]) [MassAction(0.1)]
     L(r[1]).R(l[1]) > L(r) + R(l) [MassAction(0.3)]
