with molecule_types:
    EGF(R)
    EGFR(L, CR1, Y1068 = (U, P))
    Grb2(SH2, SH3)
    Sos1(PxxP)
    Trash()

with molecule_inits:
    EGF(R) [0]
    EGFR(L, CR1, Y1068 = (U)) [1.8e5]
    Grb2(SH2, SH3) [1.5e5]
    Sos1(PxxP) [6.2e4]

with reaction_rules:
    # Ligand-receptor binding
    EGFR(L, CR1) + EGF(R) == EGFR(L[1], CR1).EGF(R[1]) | (9.0e7 / (6.02e23 * 1.0e-10), .06) #1,2
    # Receptor-aggregation
    EGFR(L[_], CR1) + EGFR(L[_], CR1) == EGFR(L[_], CR1[1]).EGFR(L[_], CR1[1]) | (1.0e7 / (6.02e23 * 3.0e-12), .06) #3,4
    # Transphosphorylation of EGFR by RTK
    EGFR(CR1[_], Y1068 = (U)) > EGFR(CR1[_], Y1068 = (P)) | .5 #5
    # Dephosphorylation
    EGFR(Y1068 = (P)) > EGFR(Y1068 = (U)) | 4.505 #6
    # Grb2 binding to pY1068
    EGFR(Y1068 = (P)) + Grb2(SH2) == EGFR(Y1068 =(P)[1]).Grb2(SH2[1]) | (1.5e6 / (6.02e23 * 3.0e-12), .05) #7,8
    # Grb2 binding to Sos1
    Grb2(SH3) + Sos1(PxxP) == Grb2(SH3[1]).Sos1(PxxP[1]) | (1.0e7 / (6.02e23 * 3.0e-12), .06) #9,10
    # Receptor dimer internalization/degradation
    EGF(R[1]).EGF(R[2]).EGFR(L[1], CR1[3]).EGFR(L[2], CR1[3]) > Trash() | .01 #11
 
