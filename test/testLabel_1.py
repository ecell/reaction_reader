#from func import *
from process.process import *

with molecule_types:
    P6GL(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13),C6(MW12,MW13))
    GLU(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13),C6(MW12,MW13))
    G6P(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13),C6(MW12,MW13))
    F6P(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13),C6(MW12,MW13))
    F16P(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13),C6(MW12,MW13))
    DHAP(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13))
    T3P(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13))
    D13PG(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13))
    G2P(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13))
    G3P(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13))
    PEP(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13))
    PYR(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13))
    CO2(C1(MW12,MW13))
    OAA(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13))
    COA(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13),C6(MW12,MW13),C7(MW12,MW13),C8(MW12,MW13),C9(MW12,MW13),C10(MW12,MW13),C11(MW12,MW13),C12(MW12,MW13),C13(MW12,MW13),C14(MW12,MW13),C15(MW12,MW13),C16(MW12,MW13),C17(MW12,MW13),C18(MW12,MW13),C19(MW12,MW13),C20(MW12,MW13),C21(MW12,MW13))
    ACCOA(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13),C6(MW12,MW13),C7(MW12,MW13),C8(MW12,MW13),C9(MW12,MW13),C10(MW12,MW13),C11(MW12,MW13),C12(MW12,MW13),C13(MW12,MW13),C14(MW12,MW13),C15(MW12,MW13),C16(MW12,MW13),C17(MW12,MW13),C18(MW12,MW13),C19(MW12,MW13),C20(MW12,MW13),C21(MW12,MW13),C22(MW12,MW13),C23(MW12,MW13))
    CIT(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13),C6(MW12,MW13))
    ICIT(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13),C6(MW12,MW13))
    SUCCOA(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13),C6(MW12,MW13),C7(MW12,MW13),C8(MW12,MW13),C9(MW12,MW13),C10(MW12,MW13),C11(MW12,MW13),C12(MW12,MW13),C13(MW12,MW13),C14(MW12,MW13),C15(MW12,MW13),C16(MW12,MW13),C17(MW12,MW13),C18(MW12,MW13),C19(MW12,MW13),C20(MW12,MW13),C21(MW12,MW13),C22(MW12,MW13),C23(MW12,MW13),C24(MW12,MW13),C25(MW12,MW13))
    AKG(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13))
    MAL(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13))
    P6GC(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13),C6(MW12,MW13))
    Ru5P(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13))
    XU5P(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13))
    R5P(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13))
    S7P(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13),C5(MW12,MW13),C6(MW12,MW13),C7(MW12,MW13))
    E4P(C1(MW12,MW13),C2(MW12,MW13),C3(MW12,MW13),C4(MW12,MW13))
    EXCELL(hoge)
    I(foo)

with molecule_inits:
    P6GL(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12)) [0]
    GLU(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12)) [0]
#    GLU(C1(C13),C2(C13),C3(C13),C4(C13),C5(C13),C6(C13)) [5000]
    G6P(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12)) [0]
    F6P(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12)) [0]
    F16P(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12)) [0]
    DHAP(C1(MW12),C2(MW12),C3(MW12)) [0]
    T3P(C1(MW12),C2(MW12),C3(MW12)) [0]
    D13PG(C1(MW12),C2(MW12),C3(MW12)) [0]
    G2P(C1(MW12),C2(MW12),C3(MW12)) [0]
    G3P(C1(MW12),C2(MW12),C3(MW12)) [0]
    PEP(C1(MW12),C2(MW12),C3(MW12)) [0]
    PYR(C1(MW12),C2(MW12),C3(MW12)) [0]
    CO2(C1(MW12)) [0]
    OAA(C1(MW12),C2(MW12),C3(MW12),C4(MW12)) [0]
    COA(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12),C7(MW12),C8(MW12),C9(MW12),C10(MW12),C11(MW12),C12(MW12),C13(MW12),C14(MW12),C15(MW12),C16(MW12),C17(MW12),C18(MW12),C19(MW12),C20(MW12),C21(MW12)) [0]
    ACCOA(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12),C7(MW12),C8(MW12),C9(MW12),C10(MW12),C11(MW12),C12(MW12),C13(MW12),C14(MW12),C15(MW12),C16(MW12),C17(MW12),C18(MW12),C19(MW12),C20(MW12),C21(MW12),C22(MW12),C23(MW12)) [0]
    CIT(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12)) [0]
    ICIT(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12)) [0]
    AKG(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12)) [0]
    SUCCOA(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12),C7(MW12),C8(MW12),C9(MW12),C10(MW12),C11(MW12),C12(MW12),C13(MW12),C14(MW12),C15(MW12),C16(MW12),C17(MW12),C18(MW12),C19(MW12),C20(MW12),C21(MW12),C22(MW12),C23(MW12),C24(MW12),C25(MW12)) [0]
    MAL(C1(MW12),C2(MW12),C3(MW12),C4(MW12)) [0]
    P6GC(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12)) [0]
    Ru5P(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12)) [0]
    XU5P(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12)) [0]
    R5P(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12)) [0]
    S7P(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12),C7(MW12)) [0]
    E4P(C1(MW12),C2(MW12),C3(MW12),C4(MW12)) [0]
    
    EXCELL(hoge) [0]
    I(foo) [100]

with reaction_rules:
    # R00299
    GLU(C1%11,C2%12,C3%13,C4%14,C5%15,C6%16) > G6P(C1%11,C2%12,C3%13,C4%14,C5%15,C6%16) | 0.3
    # R00771
    G6P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > F6P(C1%1,C2%6,C3%2,C4%3,C5%4,C6%5) | 0.7
    # R00756
    F6P(C1%11,C2%12,C3%13,C4%14,C5%15,C6%16) > F16P(C1%11,C2%12,C3%13,C4%14,C5%15,C6%16) | 0.85
    # R01068
    F16P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > DHAP(C1%5,C2%2,C3%6)+T3P(C1%4,C2%1,C3%3) | 0.85
    # R01015
    T3P(C1%1,C2%2,C3%3) <_> DHAP(C1%1,C2%2,C3%3) | (0.15, 1.0)
    # R01061
    T3P(C1%1,C2%2,C3%3) <_> D13PG(C1%2,C2%3,C3%1) | (2.0, 0.25)
    # R01512
    G3P(C1%11,C2%12,C3%13) <_> D13PG(C1%11,C2%12,C3%13)	| (2.0, 0.35)
    # R01518
    G2P(C1%1,C2%2,C3%3) <_> G3P(C1%1,C2%2,C3%3)	| (0.35, 2.0)
    # R00658
    G2P(C1%1,C2%2,C3%3) <_> PEP(C1%1,C2%2,C3%3)	| (2.0, 0.35)
    # R00200
    PEP(C1%11,C2%12,C3%13) > PYR(C1%11,C2%12,C3%13) | 1.27
    # R00345
    PEP(C1%1,C2%2,C3%4)+CO2(C1%3) > OAA(C1%1,C2%2,C3%3,C4%4) | 0.97
    # R00341
    OAA(C1%11,C2%12,C3%13,C4%14) > PEP(C1%11,C2%12,C3%14)+CO2(C1%13) | 0.66
    # R00210
    PYR(C1%1,C2%2,C3%3)+COA(C1%4,C2%5,C3%6,C4%7,C5%8,C6%9,C7%10,C8%11,C9%12,C10%13,C11%14,C12%15,C13%16,C14%17,C15%18,C16%19,C17%20,C18%21,C19%22,C20%23,C21%24) > ACCOA(C1%1,C2%4,C3%5,C4%6,C5%7,C6%8,C7%9,C8%10,C9%11,C10%12,C11%13,C12%2,C13%14,C14%15,C15%16,C16%17,C17%18,C18%19,C19%20,C20%21,C21%22,C22%23,C23%24)+CO2(C1%3) | 1.09
    # R00351
    ACCOA(C1%2,C2%7,C3%8,C4%9,C5%10,C6%11,C7%12,C8%13,C9%14,C10%15,C11%16,C12%4,C13%17,C14%18,C15%19,C16%20,C17%21,C18%22,C19%23,C20%24,C21%25,C22%26,C23%27)+OAA(C1%1,C2%6,C3%3,C4%5) > CIT(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6)+COA(C1%7,C2%8,C3%9,C4%10,C5%11,C6%12,C7%13,C8%14,C9%15,C10%16,C11%17,C12%18,C13%19,C14%20,C15%21,C16%22,C17%23,C18%24,C19%25,C20%26,C21%27) | 0.89
    # R01324
    CIT(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) <_> ICIT(C1%2,C2%6,C3%4,C4%1,C5%5,C6%3) | (1.0, 0.11)
    # R00267
    ICIT(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > AKG(C1%2,C2%1,C3%4,C4%3,C5%6)+CO2(C1%5) | 0.89
    # R01197
    AKG(C1%4,C2%3,C3%16,C4%15,C5%26)+COA(C1%2,C2%1,C3%5,C4%6,C5%7,C6%8,C7%9,C8%10,C9%11,C10%12,C11%13,C12%14,C13%17,C14%18,C15%19,C16%20,C17%21,C18%22,C19%23,C20%24,C21%25) > SUCCOA(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6,C7%7,C8%8,C9%9,C10%10,C11%11,C12%12,C13%13,C14%14,C15%15,C16%16,C17%17,C18%18,C19%19,C20%20,C21%21,C22%22,C23%23,C24%24,C25%25)+CO2(C1%26) | 0.8
    # R00342
    MAL(C1%1,C2%2,C3%3,C4%4) > OAA(C1%1,C2%2,C3%3,C4%4) | 0.72
    # R00214
    MAL(C1%1,C2%2,C3%3,C4%4) > PYR(C1%1,C2%2,C3%4)+CO2(C1%3) | 0.07
    # R00835
    G6P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > P6GL(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) | 0.29
    # R02035
    P6GL(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > P6GC(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) | 0.29
    # R01528
    P6GC(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > Ru5P(C1%5,C2%1,C3%4,C4%2,C5%3)+CO2(C1%6) | 0.29
    # R01529
    Ru5P(C1%1,C2%2,C3%3,C4%4,C5%5) <_> XU5P(C1%1,C2%2,C3%3,C4%4,C5%5) | (0.30, 0.20)
    # R01056
    R5P(C1%1,C2%2,C3%3,C4%4,C5%5) <_> Ru5P(C1%5,C2%1,C3%4,C4%2,C5%3) | (0.20, 0.30)
    # R01641
    S7P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6,C7%7)+T3P(C1%8,C2%9,C3%10) <_> R5P(C1%2,C2%4,C3%6,C4%7,C5%5)+XU5P(C1%1,C2%9,C3%3,C4%10,C5%8) | (0.18, 0.09)
    # R01827
    S7P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6,C7%7)+T3P(C1%8,C2%9,C3%10) <_> E4P(C1%7,C2%2,C3%6,C4%4)+F6P(C1%9,C2%1,C3%10,C4%8,C5%5,C6%3) | (0.18, 0.09)
    # R01067
    F6P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6)+T3P(C1%7,C2%8,C3%9) <_> E4P(C1%5,C2%1,C3%4,C4%3)+XU5P(C1%2,C2%8,C3%6,C4%9,C5%7) | (0.06, 0.12)
    # excrete
    G6P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > EXCELL(hoge) | 0.01
    F6P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > EXCELL(hoge) | 0.01
    T3P(C1%1,C2%2,C3%3) > EXCELL(hoge) | 0.01
    G3P(C1%1,C2%2,C3%3) > EXCELL(hoge) | 0.1
    PEP(C1%1,C2%2,C3%3) > EXCELL(hoge) | 0.06
    PYR(C1%1,C2%2,C3%3) > EXCELL(hoge) | 0.26
    ACCOA(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6,C7%7,C8%8,C9%9,C10%10,C11%11,C12%12,C13%13,C14%14,C15%15,C16%16,C17%17,C18%18,C19%19,C20%20,C21%21,C22%22,C23%23) > EXCELL(hoge) | 0.2
    Ru5P(C1%1,C2%2,C3%3,C4%4,C5%5) > EXCELL(hoge) | 0.04
    E4P(C1%1,C2%2,C3%3,C4%4) > EXCELL(hoge) | 0.03
    OAA(C1%1,C2%2,C3%3,C4%4) > EXCELL(hoge) | 0.14
    AKG(C1%1,C2%2,C3%3,C4%4,C5%5) > EXCELL(hoge) | 0.1

    #G6P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > P6GL(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) | 0.29

    I(foo) > I(foo) + GLU(C1(MW12),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12)) | 1
#    I(foo) > I(foo) + GLU(C1(MW13),C2(MW12),C3(MW12),C4(MW12),C5(MW12),C6(MW12)) | 0
    I(foo) > I(foo) + GLU(C1(MW13),C2(MW13),C3(MW13),C4(MW13),C5(MW13),C6(MW13)) | 0
