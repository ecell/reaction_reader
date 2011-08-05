'''
L(r) -> L(r) + R(l,d,Y~U), k = 0.1

Initial values:
L(r): 10000.0
R(l,d,Y~U): 0.0
'''

from func import *

with molecule_types:
     L(r)
     R(l, d, Y(U))

with reaction_rules:
     L(r) > L(r) + R(l, d, Y(U)) | MassAction(0.1)


