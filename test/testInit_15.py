'''
L(r) + R(l,d,Y~U) -> R(l,d,Y~U), k = 0.1

Initial values:
L(r): 10000.0
R(l,d,Y~U): 10000.0
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
     R(l, d, Y(U)) [10000]

with reaction_rules:
     L(r) + R(l, d, Y(U)) > R(l, d, Y(U)) | MassAction(0.1)


