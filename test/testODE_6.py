'''
L(r) + R(l) -> L(r!1).R(l!1), k = 0.1
L(r!1).R(l!1) -> L(r) + R(l), k = 0.3
R(Y~?) + A(SH2) -> R(Y~?!1).A(SH2!1), k = 0.2
R(Y~?!1).A(SH2!1) -> R(Y~?) + A(SH2), k = 0.4

Initial values:
L(r): 10000.0
R(l,d,Y~U): 5000.0
A(SH2,Y~U): 100.0
'''

from func import *

with molecule_types:
     L(r)
     R(l, d, Y(U))
     A(SH2, Y(U))

with reaction_rules:
     L(r) + R(l) > L(r[1]).R(l[1]) (.1, include_reactants(2, A))
     L(r[1]).R(l[1]) > L(r) + R(l) (.3, include_reactants(2, A))
     R(Y) + A(SH2) > R(Y[1]).A(SH2[1]) (.5, include_reactants(1, L))
     R(Y[1]).A(SH2[1]) > R(Y) + A(SH2) (.4, include_reactants(1, L))
