'''
L(r) + R(l) -> L(r!1).R(l!1), k = 0.1
L(r!1).R(l!1) -> L(r) + R(l), k = 0.3

Initial values:
L(r): 10000.0
R(l,d,Y~U): 5000.0
R(l,d,Y~P): 3000.0
'''

from func import *

with molecule_types:
     L(r)
     R(l, d, Y(U))
     R(l, d, Y(pU))

with molecule_inits:
    L(r) [10000]
    R(l, d, Y(U)) [5000]
    R(l, d, Y(pU)) [3000]

with reaction_rules:
#     L(r) + R(l) > L(r[1]).R(l[1]) [MassAction(.1)]
#     L(r[1]).R(l[1]) > L(r) + R(l) [MassAction(.3)]

     L(r) + R(l) <> L(r[1]).R(l[1]) | MassAction2(.1, .3)
