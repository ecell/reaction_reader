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
#    C(c(0))
    B(b)
    D(Y(U, P))

with molecule_inits:
#    L(r) = 10000
    L(r) [10000]
    R(l, d, Y(U)) [10000]
    A(a) [1000]

with reaction_rules:
#    L(r) + R(l) < A(a) > L(r[1]).R(l[1]) [A(a), B(b)] | (0.1, 0.3)
#    L(r[1]).R(l[1])<_>  L(r) + R(l) [A(a), B(b)] | (0.1, 0.3)

#    L(r) + R(l) > L(r[1]).R(l[1]) > L(r[1]).R(l[1]) [A(a), B(b)] | (0.1, 0.3)

#    L(r) + R(l) <_> L(r[1]).R(l[1]) [A(a), B(b)] | (0.1, 0.3)
#    R(d) + A(a) <_> A(a[1]).R(d[1])              | (0.1, 0.3)
    L(r) + R(l) > L(r[1]).R(l[1]) [A(a), B(b)] | 0.1
    R(Y(U)) > R(Y(P))                          | 0.1
#    R(l, d, Y%1) > D(Y%1)                          | 0.1

#    L(r) + R(l) > L(r[1]).R(l[1]) | 0.1
