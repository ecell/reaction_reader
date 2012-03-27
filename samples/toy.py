from func import *

with molecule_types:
    S(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13))
    X1(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13))
    X2(C1(MW12,MW13),C2(MW12,MW13))
    P(C1(MW12,MW13),C2(MW12,MW13))
    C(C1(MW12,MW13))
    I(foo)

with molecule_inits:
    S(C1(MW12),C2(MW12),C3(MW12)) [1.0]
    X1(C1(MW12),C2(MW12),C3(MW12)) [1.0]
    X2(C1(MW12),C2(MW12)) [1.0]
    P(C1(MW12),C2(MW12)) [0.0]
    C(C1(MW12)) [0.0]
    I(foo) [1]

with reaction_rules:
    S(C1%1,C2%2,C3%3) > X1(C1%1,C2%2,C3%3) | 0.01
    X1(C1%1,C2%2,C3%3) > X2(C1%1,C2%2) + C(C1%3) | 0.003
    X1(C1%1,C2%2,C3%3) > X2(C1%2,C2%3) + C(C1%1) | 0.007
    X2(C1%1,C2%2) > P(C1%1,C2%2) | 0.01
    
    # vi_S
    I(foo) > I(foo) + S(C1(MW12),C2(MW12),C3(MW12)) | 1.0
    I(foo) > I(foo) + S(C1(MW13),C2(MW13),C3(MW12)) | 0.0
