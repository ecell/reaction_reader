from func import *   #inport Mass Action file? 


with molecule_types:       #E-Cell4
    P6GL(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t),C6(f,t))
#ng#    FUM(C1_2(f,t),C1_2(f,t),C3_4(f,t),C3_4(f,t))
    P6GC(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t),C6(f,t))
    S7P(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t),C6(f,t),C7(f,t))
    G3P(C1(f,t),C2(f,t),C3(f,t))
    ACCOA(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t),C6(f,t),C7(f,t),C8(f,t),C9(f,t),C10(f,t),C11(f,t),C12(f,t),C13(f,t),C14(f,t),C15(f,t),C16(f,t),C17(f,t),C18(f,t),C19(f,t),C20(f,t),C21(f,t),C22(f,t),C23(f,t))
    CO2(C1(f,t))
    MAL(C1(f,t),C2(f,t),C3(f,t),C4(f,t))
    OAA(C1(f,t),C2(f,t),C3(f,t),C4(f,t))
    F6P(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t),C6(f,t))	
    XU5P(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t))	
    G2P(C1(f,t),C2(f,t),C3(f,t))	
    DHAP(C1(f,t),C2(f,t),C3(f,t))	
    R5P(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t))	
    SUCCOA(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t),C6(f,t),C7(f,t),C8(f,t),C9(f,t),C10(f,t),C11(f,t),C12(f,t),C13(f,t),C14(f,t),C15(f,t),C16(f,t),C17(f,t),C18(f,t),C19(f,t),C20(f,t),C21(f,t),C22(f,t),C23(f,t),C24(f,t),C25(f,t))	
    F16P(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t),C6(f,t))	
    COA(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t),C6(f,t),C7(f,t),C8(f,t),C9(f,t),C10(f,t),C11(f,t),C12(f,t),C13(f,t),C14(f,t),C15(f,t),C16(f,t),C17(f,t),C18(f,t),C19(f,t),C20(f,t),C21(f,t))	
    E4P(C1(f,t),C2(f,t),C3(f,t),C4(f,t))
    D13PG(C1(f,t),C2(f,t),C3(f,t))
    PYR(C1(f,t),C2(f,t),C3(f,t))
    PEP(C1(f,t),C2(f,t),C3(f,t))
    CIT(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t),C6(f,t))	
#ng#    SUC(C1_2(f,t),C1_2(f,t),C3_4(f,t),C3_4(f,t))	
    Ru5P(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t))	
    AKG(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t))	
    G6P(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t),C6(f,t))	
    GLU(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t),C6(f,t))
    T3P(C1(f,t),C2(f,t),C3(f,t))
    ICIT(C1(f,t),C2(f,t),C3(f,t),C4(f,t),C5(f,t),C6(f,t))
#    I()	               #?????????                           
#    NULL()	               #leak from the pathway??            



with molecule_inits:  #initial condition   #E-Cell4
    P6GL(C1(f),C2(f),C3(f),C4(f),C5(f),C6(f)) [0]
#ng#    FUM(C1_2(f),C1_2(f),C3_4(f),C3_4(f)) [0]
    P6GC(C1(f),C2(f),C3(f),C4(f),C5(f),C6(f)) [0]
    S7P(C1(f),C2(f),C3(f),C4(f),C5(f),C6(f),C7(f)) [0]
    G3P(C1(f),C2(f),C3(f)) [0]
    ACCOA(C1(f),C2(f),C3(f),C4(f),C5(f),C6(f),C7(f),C8(f),C9(f),C10(f),C11(f),C12(f),C13(f),C14(f),C15(f),C16(f),C17(f),C18(f),C19(f),C20(f),C21(f),C22(f),C23(f)) [0]
    CO2(C1(f)) [0]
    MAL(C1(f),C2(f),C3(f),C4(f)) [0]
    OAA(C1(f),C2(f),C3(f),C4(f)) [0]
    F6P(C1(f),C2(f),C3(f),C4(f),C5(f),C6(f)) [0]	
    XU5P(C1(f),C2(f),C3(f),C4(f),C5(f)) [0]	
    G2P(C1(f),C2(f),C3(f)) [0]	
    DHAP(C1(f),C2(f),C3(f)) [0]	
    R5P(C1(f),C2(f),C3(f),C4(f),C5(f)) [0]	
    SUCCOA(C1(f),C2(f),C3(f),C4(f),C5(f),C6(f),C7(f),C8(f),C9(f),C10(f),C11(f),C12(f),C13(f),C14(f),C15(f),C16(f),C17(f),C18(f),C19(f),C20(f),C21(f),C22(f),C23(f),C24(f),C25(f)) [0]	
    F16P(C1(f),C2(f),C3(f),C4(f),C5(f),C6(f)) [0]	
    COA(C1(f),C2(f),C3(f),C4(f),C5(f),C6(f),C7(f),C8(f),C9(f),C10(f),C11(f),C12(f),C13(f),C14(f),C15(f),C16(f),C17(f),C18(f),C19(f),C20(f),C21(f)) [0]	
    E4P(C1(f),C2(f),C3(f),C4(f)) [0]	
    D13PG(C1(f),C2(f),C3(f)) [0]	
    PYR(C1(f),C2(f),C3(f)) [0]	
    PEP(C1(f),C2(f),C3(f)) [0]	
    CIT(C1(f),C2(f),C3(f),C4(f),C5(f),C6(f)) [0]	
#ng#    SUC(C1_2(f),C1_2(f),C3_4(f),C3_4(f)) [0]	
    Ru5P(C1(f),C2(f),C3(f),C4(f),C5(f)) [0]	
    AKG(C1(f),C2(f),C3(f),C4(f),C5(f)) [0]	
    G6P(C1(f),C2(f),C3(f),C4(f),C5(f),C6(f)) [0]	
    GLU(C1(f),C2(f),C3(f),C4(f),C5(f),C6(f)) [0]	
    T3P(C1(f),C2(f),C3(f)) [0]	
    ICIT(C1(f),C2(f),C3(f),C4(f),C5(f),C6(f)) [0]	
#    I [1]	               #?????????                           
#    NULL [0]	               #leak from the pathway??            


with reaction_rules:    #E-cell4
    # HK
    GLU(C1%11,C2%12,C3%13,C4%14,C5%15,C6%16) > G6P(C1%11,C2%12,C3%13,C4%14,C5%15,C6%16) | MassAction(1.0)	#v_R00299

    # PGI
    G6P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > F6P(C1%1,C2%6,C3%2,C4%3,C5%4,C6%5) | MassAction(0.7)	 #v_R00771

    # PFK
    F6P(C1%11,C2%12,C3%13,C4%14,C5%15,C6%16) > F16P(C1%11,C2%12,C3%13,C4%14,C5%15,C6%16) | MassAction(0.85)	#v_R00756

    # FBA
    F16P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > DHAP(C1%5,C2%2,C3%6)+T3P(C1%4,C2%1,C3%3) | MassAction(0.85)	#v_R01068

    # TPI
#ng#    T3P(C1%1,C2%2,C3%3) <_> DHAP(C1%1,C2%2,C3%3) | MassAction2(0.15, 1.0)	#v_R01015_f, v_R01015_b

    # GAPDH
#ng#    T3P(C1%1,C2%2,C3%3) <_> D13PG(C1%2,C2%3,C3%1) | MassAction2(2.0, 0.25)	#v_R01061_f, v_R01061_b

    # PGK
#ng#    G3P(C1%11,C2%12,C3%13) <_> D13PG(C1%11,C2%12,C3%13) | MassAction2(2.0, 0.35)	#v_R01512_f, v_R01512_b

    # PGM
#ng#    G2P(C1%1,C2%2,C3%3) <_> G3P(C1%1,C2%2,C3%3) | MassAction2(0.35, 2.0)	#v_R01518_f, v_R01518_b

    # EN
#ng#    G2P(C1%1,C2%2,C3%3) <_> PEP(C1%1,C2%2,C3%3) | MassAction2(2.0, 0.35)	#v_R00658_f, v_R00658_b

    # PK
    PEP(C1%11,C2%12,C3%13) > PYR(C1%11,C2%12,C3%13) | MassAction(1.27)	#v_R00200

    # PPC
    PEP(C1%1,C2%2,C3%4)+CO2(C1%3) > OAA(C1%1,C2%2,C3%3,C4%4) | MassAction(0.97)	#v_R00345

    # PPK
    OAA(C1%11,C2%12,C3%13,C4%14) > PEP(C1%11,C2%12,C3%14)+CO2(C1%13) | MassAction(0.66)	#v_R00341

    # PDH
    PYR(C1%1,C2%2,C3%3)+COA(C1%4,C2%5,C3%6,C4%7,C5%8,C6%9,C7%10,C8%11,C9%12,C10%13,C11%14,C12%15,C13%16,C14%17,C15%18,C16%19,C17%20,C18%21,C19%22,C20%23,C21%24) > ACCOA(C1%1,C2%4,C3%5,C4%6,C5%7,C6%8,C7%9,C8%10,C9%11,C10%12,C11%13,C12%2,C13%14,C14%15,C15%16,C16%17,C17%18,C18%19,C19%20,C20%21,C21%22,C22%23,C23%24)+CO2(C1%3) | MassAction(1.09)	#v_R00210

    # CIT1P
    ACCOA(C1%2,C2%7,C3%8,C4%9,C5%10,C6%11,C7%12,C8%13,C9%14,C10%15,C11%16,C12%4,C13%17,C14%18,C15%19,C16%20,C17%21,C18%22,C19%23,C20%24,C21%25,C22%26,C23%27)+OAA(C1%1,C2%6,C3%3,C4%5) > CIT(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6)+COA(C1%7,C2%8,C3%9,C4%10,C5%11,C6%12,C7%13,C8%14,C9%15,C10%16,C11%17,C12%18,C13%19,C14%20,C15%21,C16%22,C17%23,C18%24,C19%25,C20%26,C21%27) | MassAction(0.89)	#v_R00351

    # CS
    CIT(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) <_> ICIT(C1%2,C2%6,C3%4,C4%1,C5%5,C6%3) | MassAction2(1.0, 0.11)	#v_R01324_f, v_R01324_b

    # IDH
    ICIT(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > AKG(C1%2,C2%1,C3%4,C4%3,C5%6)+CO2(C1%5) | MassAction(0.89)	#v_R00267

    # AKGDH
    AKG(C1%4,C2%3,C3%16,C4%15,C5%26)+COA(C1%2,C2%1,C3%5,C4%6,C5%7,C6%8,C7%9,C8%10,C9%11,C10%12,C11%13,C12%14,C13%17,C14%18,C15%19,C16%20,C17%21,C18%22,C19%23,C20%24,C21%25) > SUCCOA(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6,C7%7,C8%8,C9%9,C10%10,C11%11,C12%12,C13%13,C14%14,C15%15,C16%16,C17%17,C18%18,C19%19,C20%20,C21%21,C22%22,C23%23,C24%24,C25%25)+CO2(C1%26) | MassAction(0.8)	#v_R01197

    # ST
    SUCCOA(C1%16,C2%15,C3%12,C4%11,C5%17,C6%18,C7%19,C8%20,C9%21,C10%22,C11%23,C12%24,C13%25,C14%26,C15%14,C16%13,C17%27,C18%28,C19%29,C20%30,C21%31,C22%32,C23%33,C24%34,C25%35) > SUC(C1_2%11,C1_2%12,C3_4%13,C3_4%14)+COA(C1%15,C2%16,C3%17,C4%18,C5%19,C6%20,C7%21,C8%22,C9%23,C10%24,C11%25,C12%26,C13%27,C14%28,C15%29,C16%30,C17%31,C18%32,C19%33,C20%34,C21%35) | MassAction(0.8)	#v_R00405

    # SDH
#ng#    SUC(C1_2%1,C1_2%2,C3_4%3,C3_4%4) > FUM(C1_2%1,C1_2%2,C3_4%3,C3_4%4) | MassAction(0.8)	#v_R00412

    # FUM
#ng#    FUM(C1_2%2,C1_2%1,C3_4%4,C3_4%3) > MAL(C1%1,C2%2,C3%3,C4%4) | MassAction(0.8)	#v_R01082

    # MDH
    MAL(C1%1,C2%2,C3%3,C4%4) > OAA(C1%1,C2%2,C3%3,C4%4)	| MassAction(0.72) #v_R00342

    # MEZ
    MAL(C1%1,C2%2,C3%3,C4%4) > PYR(C1%1,C2%2,C3%4)+CO2(C1%3) | MassAction(0.07)	#v_R00214

    # G6PDH
    G6P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > P6GL(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) | MassAction(0.29)	#v_R00835

    # 6PGLase
    P6GL(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > P6GC(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) | MassAction(0.29)	#v_R02035

    # 6PGODH
    P6GC(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6) > Ru5P(C1%5,C2%1,C3%4,C4%2,C5%3)+CO2(C1%6) | MassAction(0.29)	#v_R01528

    # X5PI
#ng#    Ru5P(C1%1,C2%2,C3%3,C4%4,C5%5) <_> XU5P(C1%1,C2%2,C3%3,C4%4,C5%5) | MassAction2(0.30, 0.20)	#v_R01529_f, v_R01529_b

    # R5PI
#ng#    R5P(C1%1,C2%2,C3%3,C4%4,C5%5) <_> Ru5P(C1%5,C2%1,C3%4,C4%2,C5%3) | MassAction2(0.20, 0.30)	#v_R01056_f, v_R01056_b

    # TK1
    S7P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6,C7%7)+T3P(C1%8,C2%9,C3%10) <_> R5P(C1%2,C2%4,C3%6,C4%7,C5%5)+XU5P(C1%1,C2%9,C3%3,C4%10,C5%8) | MassAction2(0.18, 0.09)	#v_R01641_f, v_R01641_b

    # TA
    S7P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6,C7%7)+T3P(C1%8,C2%9,C3%10) <_> E4P(C1%7,C2%2,C3%6,C4%4)+F6P(C1%9,C2%1,C3%10,C4%8,C5%5,C6%3) | MassAction2(0.18, 0.09)	#v_R01827_f, v_R01827_b

    # TK2
    F6P(C1%1,C2%2,C3%3,C4%4,C5%5,C6%6)+T3P(C1%7,C2%8,C3%9) <_> E4P(C1%5,C2%1,C3%4,C4%3)+XU5P(C1%2,C2%8,C3%6,C4%9,C5%7) | MassAction2(0.06, 0.12)	#v_R01067_f, v_R01067_b

    # Leak_G6P
#    G6P() > NULL() | MassAction(0.01)	#v_vs_G6P

    # Leak_F6P
#    F6P() > NULL() | MassAction(0.01)	#v_vs_F6P

    # Leak_T3P
#    T3P() > NULL() | MassAction(0.01)	#v_vs_T3P

    # Leak_G3P1
#    G3P() > NULL() | MassAction(0.1)	#v_vs_G3P

    # Leak_PEP
#    PEP() > NULL() | MassAction(0.06)	#v_vs_PEP

    # Leak_PYR
#    PYR() > NULL() | MassAction(0.26)	#v_vs_PYR

    # Leak_ACCOA
#    ACCOA() > NULL() | MassAction(0.2)	#v_vs_ACCOA

    # Leak_Ru5P
#    Ru5P() > NULL() | MassAction(0.04)	#v_vs_Ru5P

    # Leak_E4P
#    E4P() > NULL() | MassAction(0.03)	#v_vs_E4P

    # Leak_OAA
#    OAA() > NULL() | MassAction(0.14)	#v_vs_OAA

    # Leak_AKG
#    AKG() > NULL() | MassAction(0.1)	#v_vs_AKG

    # GLU
#    I > I + GLU(C1~0,C2~0,C3~0,C4~0,C5~0,C6~0) | MassAction(1)	#v_vi_GLU_unlabeled
#    I > I + GLU(C1~1,C2~0,C3~0,C4~0,C5~0,C6~0) | MassAction(f)	#v_vi_GLU_labeled
    #I -> I + GLU(C1~1,C2~1,C3~1,C4~1,C5~1,C6~1)	v_vi_GLU_labeled

#ng#    I() > I() + GLU(C1(0),C2(0),C3(0),C4(0),C5(0),C6(0)) | MassAction(1)	#v_vi_GLU_unlabeled
#ng#    I() > I() + GLU(C1(1),C2(0),C3(0),C4(0),C5(0),C6(0)) | MassAction(0)	#v_vi_GLU_labeled



#with observables:              #define output elements
#    Molecules P6GL P6GL()      #output name is "P6GL" include any condition P6GL(-"P6GL()") 
#    Molecules FUM FUM()
#    Molecules P6GC P6GC()
#    Molecules S7P S7P()
#    Molecules G3P G3P()
#    Molecules ACCOA ACCOA()
#    Molecules CO2 CO2()
#    Molecules MAL MAL()
#    Molecules OAA OAA()
#    Molecules F6P F6P()
#    Molecules XU5P XU5P()
#    Molecules G2P G2P()
#    Molecules DHAP DHAP()
#    Molecules R5P R5P()
#    Molecules SUCCOA SUCCOA()
#    Molecules F16P F16P()
#    Molecules COA COA()
#    Molecules E4P E4P()
#    Molecules D13PG D13PG()
#    Molecules PYR PYR()
#    Molecules PEP PEP()
#    Molecules CIT CIT()
#    Molecules SUC SUC()
#    Molecules Ru5P Ru5P()
#    Molecules AKG AKG()
#    Molecules G6P G6P()
#    Molecules GLU GLU()
#    Molecules T3P T3P()
#    Molecules ICIT ICIT()
