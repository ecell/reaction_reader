from func import *

with molecule_types:
    GLU()

with molecule_inits:
    GLU() [10000]

with reaction_rules:
    GLU(C1%11,C2%12,C3%13,C4%14,C5%15,C6%16) <_> G6P(C1%11,C2%12,C3%13,C4%14,C5%15,C6%16)
