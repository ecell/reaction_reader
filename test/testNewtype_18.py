'''
R(Y~U!1).A(SH2!1) -> A(SH2), k = 0.1

Initial values:
R(l,d,Y~U!1).A(SH2!1,Y~U): 10000.0
L(r!1).R(l!1,d,Y~U!2).A(SH2!2,Y~U): 10000.0
'''

from func import *

with molecule_types:
     L(r)
     R(l, d, Y(U))
     A(SH2, Y(U))

with reaction_rules:
     R(Y(U)[1]).A(SH2[1]) > A(SH2) | MassAction(0.1)

