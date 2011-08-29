'''
L(r) + R(l) -> L(r!1).R(l!1), k = 0.1
L(r!1).R(l!1) -> L(r) + R(l), k = 0.3

Initial values:
L(r): 10000.0
R(l,d,Y~U): 10000.0
'''

from func import *

with molecule_types:
    L(r)
#    R(l, d, Y(U))
    R(l, d, Y(U, P))
    A(a)
    B(b)

with molecule_inits:
    L(r) [10000]
    R(l, d, Y(U)) [10000]

with reaction_rules:
#    L(r) + R(l) < A(a) > L(r[1]).R(l[1]) [A(a), B(b)] | (0.1, 0.3)
#    L(r[1]).R(l[1])<_>  L(r) + R(l) [A(a), B(b)] | (0.1, 0.3)

#    L(r) + R(l) > L(r[1]).R(l[1]) > L(r[1]).R(l[1]) [A(a), B(b)] | (0.1, 0.3)

    L(r) + R(l) <_> L(r[1]).R(l[1]) [A(a), B(b)] | (0.1, 0.3)

#    L(r) + R(l) > L(r[1]).R(l[1]) | 0.1
