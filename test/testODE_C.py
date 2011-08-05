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
     R(l, d, Y(U))
     A(SH2, Y(U))

with reaction_rules:



#     L(r)   + R(l) > L(r[1]).R(l[1])   [MassAction(.1)]
#     A(SH2) + R(d) > A(SH2[1]).R(d[1]) [MassAction(.1)] [include_reactants(2, L)]
#     L(r[1]).R(l[1])   > L(r)   + R(l) [MassAction(.1)]
#     A(SH2[1]).R(d[1]) > A(SH2) + R(d) [MassAction(.1)] [include_products(2, L)]

     L(r)   + R(l) <> L(r[1]).R(l[1])   [MassAction(.1)]
#     A(SH2) + R(d) <> A(SH2[1]).R(d[1]) [MassAction(.1)] [exclude_reactants(2, L)]
#     R(d) + A(SH2) <> R(d[1]).A(SH2[1]) [MassAction(.1)] [include_reactants(1, L)]

     R(d) + A(SH2) <> R(d[1]).A(SH2[1]) [MassAction(.1)] [include_reactants(1, L)] [exclude_reactants(2, R)]
