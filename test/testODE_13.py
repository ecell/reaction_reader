'''
R(r2) + R(r1,r2) -> R(r2!1).R(r1!1,r2), k = 0.3
R(r2!1).R(r1!1,r2) -> R(r2) + R(r1,r2), k = 0.3

Initial values:
R(r1,r2): 10000.0
'''

from func import *

with molecule_types:
     R(r1, r2)

with reaction_rules:
     R(r2) + R(r1, r2) > R(r2[1]).R(r1[1], r2) [MassAction(0.1)]
     R(r2[1]).R(r1[1], r2) > R(r2) + R(r1, r2) [MassAction(0.3)]
