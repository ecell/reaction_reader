'''
KmS = 100e-9
KmP = 1.0
KcF = 1.0
KcR = 0.0
S<_>P[C]| michaelis_uni_uni(...)
S[60]
P[0]
C[60]

'''
# from rateraws import *

# def michaelis_uni_uni(*args, **kwargs):
#     # args is required to be (KmS, KmP, KcF, KcR, volume)
#     return ("michaelis_uni_uni", args, kwargs)

with molecule_types:
    S(a)
    P(a)
    C(a)

with molecule_inits:
    S(a) [60 / 6.02e+23]
    P(a) [0]
    C(a) [60 / 6.02e+23]

with reaction_rules:
    # michaelis_uni_uni(KmS, KmP, KcF, KcR)
    S(a) > P(a) [C(a)] | ('michaelis_uni_uni', (100e-9, 1.0, 1.0, 0.0))
    # S(a) > P(a) [C(a)] | michaelis_uni_uni(100e-9, 1.0, 1.0, 0.0)
    # S(a) > P(a) [C(a)] | 0.4
