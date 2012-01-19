from func import *

with molecule_types:
    FUM(C1_2(MW12,MW13),C1_2(MW12,MW13),C3_4(MW12,MW13),C3_4(MW12,MW13))
    SUC(C1_2(MW12,MW13),C1_2(MW12,MW13),C3_4(MW12,MW13),C3_4(MW12,MW13))
    MAL(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13))

with molecule_inits:
    FUM(C1_2(MW12),C1_2(MW12),C3_4(MW12),C3_4(MW12)) [0]
    FUM(C1_2(MW13),C1_2(MW12),C3_4(MW12),C3_4(MW12)) [0]
    SUC(C1_2(MW12),C1_2(MW12),C3_4(MW12),C3_4(MW12)) [0]
    MAL(C1(MW12),C2(MW12),C3(MW12),C4(MW12)) [0]

with reaction_rules:
    # R00412
    SUC(C1_2%1,C1_2%2,C3_4%3,C3_4%4) > FUM(C1_2%1,C1_2%2,C3_4%3,C3_4%4) | 0.1
    # R01082
    FUM(C1_2%2,C1_2%1,C3_4%4,C3_4%3) > MAL(C1%1,C2%2,C3%3,C4%4) | 0.2