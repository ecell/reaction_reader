'''
R(d) + R(d) -> R(d!1).R(d!1) 
  include_reactants(1,L) and include_reactants(2,A), k=0.1
R(d!1).R(d!1) -> R(d) + R(d)
  include_products(1,L) and include_products(2,A), k=0.3

Initial values:
R(l,d,Y~U): 10000
L(r!1).R(l!1,d,Y~U): 5000
R(l,d,Y~U!1).A(SH2!1,Y~U): 3000
'''

from func import *

with molecule_types:
     L(r)
     R(l, d, Y(U))
     A(SH2, Y(U))

with reaction_rules:

     R(d) + R(d) > R(d[1]).R(d[1]) [michaelis_menten(.1)] [include_reactants(1, L)] [include_reactants(2, A)]
     R(d[1]).R(d[1]) > R(d) + R(d) [michaelis_menten(.3)] [include_products(1, L)] [include_products(2, A)]
