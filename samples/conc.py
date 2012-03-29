'''
KmS = 100e-9
KmP = 1.0
KcF = 1.0
KcR = 0.0
S<_>P[C]| MichaelisUniUni(...)
S[60]
P[0]
C[60]

'''
from rate_functions import *

with molecule_types:
    S(a)
    P(a)
    C(a)

with molecule_inits:
    S(a) [60 / 6.02e+23]
    P(a) [0]
    C(a) [60 / 6.02e+23]

with reaction_rules:
    # MichaelissUniUni(KmS, KmP, KcF, KcR, volume)
    S(a) > P(a) [C(a)] | MichaelisUniUni(100e-9, 1.0, 1.0, 0.0, 1e-15)
#    S(a) > P(a) [C(a)] | 0.4


