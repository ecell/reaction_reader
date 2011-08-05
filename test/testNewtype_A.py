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
    R(l, d, Y(U))
    A(a)
    B(b)

with reaction_rules:
#    L(r) + R(l) > L(r[1]).R(l[1]) | MassAction(0.1)
#    L(r[1]).R(l[1]) > L(r) + R(l) | 0.3
#    L(r) + R(l, d) + A(a) > L(r[1]).R(l[1], d[2]).A(a[2]) | (0.1)
#    L(r[1]).R(l[1], d[2]).A(a[2]) > L(r) + R(l, d) + A(a) | 0.3

#    L(r[1]).R(l[1], d[2]).A(a[2]) <> L(r) + R(l,d) + A(a) | (0.1, 0.3)

#    L(r) + R(l) > L(r[1]).R(l[1]) [A(a[1]).B(b[1])] | MassAction(0.1)
#    L(r[1]).R(l[1]) > L(r) + R(l) [A(a[1]).B(b[1])] | 0.3
#    L(r) + R(l, d) + A(a) > L(r[1]).R(l[1], d[2]).A(a[2]) [A(a[1]), B(b[1])] | (0.1)
#    L(r[1]).R(l[1], d[2]).A(a[2]) > L(r) + R(l, d) + A(a) [A(a[1]), B(b[1])] | 0.3

#    L(r) + R(l) <> L(r[1]).R(l[1]) [A(a[1]).B(b[1])] | (MassAction(0.1), MassAction(0.3))
#    L(r) + R(l, d) + A(a) <> L(r[1]).R(l[1], d[2]).A(a[2]) [A(a[1]), B(b[1])] | (0.1, 0.3)


