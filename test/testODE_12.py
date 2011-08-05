'''
R(d) + R(d) -> R(d!1).R(d!1), k=0.1
R(d!1).R(d!1) -> R(d) + R(d), k=0.3

Initial values:
R(l,d,Y~U): 10000
'''

from func import *

with molecule_types:
     R(l, d, Y(U))

with reaction_rules:
     R(d) + R(d) > R(d[1]).R(d[1]) [MassAction(0.1)]
     R(d[1]).R(d[1]) > R(d) + R(d) [MassAction(0.3)]

