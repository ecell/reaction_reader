def michaelis_menten():
    pass

# Pythonic bionetgen section
with molecule_types:
    egf(r)
    Grb2(SH2,SH3)
    Shc(PTB, Y317(Y))
    Sos(dom)
    egfr(l,r,Y1068(Y),Y1148(Y))
    Grb2(SH2,SH3[1]).Sos(dom[1])

with reaction_rules:
    # Ligand-receptor binding
    egfr(l,r) + egf(r) <> egfr(l[1],r).egf(r[1]) [michaelis_menten]

    # Note changed multiplicity
    # Receptor-aggregation
    egfr(l[1],r) + egfr(l[2],r) <> egfr(l[1],r[3]).egfr(l[2],r[3]) [michaelis_menten]

    # Transphosphorylation of egfr by RTK
    egfr(r[1],Y1068(Y)) > egfr(r[1],Y1068(pY)) [michaelis_menten]
    egfr(r[1],Y1148(Y)) > egfr(r[1],Y1148(pY)) [michaelis_menten]
    
    #Dephosphorylayion
    egfr(Y1068(pY)) > egfr(Y1068(Y)) [michaelis_menten] 
    egfr(Y1148(pY)) > egfr(Y1148(Y)) [michaelis_menten] 
    
    # Shc transphosph
    egfr(r[2],Y1148(pY)[1]).Shc(PTB[1],Y317(Y)) > egfr(r[2],Y1148(pY)[1]).Shc(PTB[1],Y317(pY)) [michaelis_menten]
    Shc(PTB[1],Y317(pY)) > Shc(PTB[1],Y317(Y)) [michaelis_menten]
    
    # Y1068 activity
    egfr(Y1068(pY)) + Grb2(SH2,SH3)    <> egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3)    [michaelis_menten]
    egfr(Y1068(pY)) + Grb2(SH2,SH3[2]) <> egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3[2]) [michaelis_menten]
    egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3) + Sos(dom) <> egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3[2]).Sos(dom[2]) [michaelis_menten]
    
    # Y1148 activity
    egfr(Y1148(pY)) + Shc(PTB,Y317(Y))  <> egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(Y))  [michaelis_menten] 
    egfr(Y1148(pY)) + Shc(PTB,Y317(pY)) <> egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)) [michaelis_menten] 
    egfr(Y1148(pY)) + Shc(PTB,Y317(pY)[1]).Grb2(SH2[1],SH3) <> \
           egfr(Y1148(pY)[2]).Shc(PTB[2],Y317(pY)[1]).Grb2(SH2[1],SH3) [michaelis_menten]
    egfr(Y1148(pY)) + Shc(PTB,Y317(pY)[1]).Grb2(SH2[1],SH3[3]).Sos(dom[3]) <> \
           egfr(Y1148(pY)[2]).Shc(PTB[2],Y317(pY)[1]).Grb2(SH2[1],SH3[3]).Sos(dom[3]) [michaelis_menten]
    egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)) + Grb2(SH2,SH3) <> \
           egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)[2]).Grb2(SH2[2],SH3) [michaelis_menten]
    egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)) + Grb2(SH2,SH3[3]).Sos(dom[3]) <> \
           egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)[2]).Grb2(SH2[2],SH3[3]).Sos(dom[3]) [michaelis_menten]
    Shc(PTB[1],Y317(pY)[2]).Grb2(SH2[2],SH3) + Sos(dom) <> \
           Shc(PTB[1],Y317(pY)[2]).Grb2(SH2[2],SH3[3]).Sos(dom[3]) [michaelis_menten]
    
    # Cytosolic 
    Shc(PTB,Y317(pY)) + Grb2(SH2,SH3)    <> Shc(PTB,Y317(pY)[1]).Grb2(SH2[1],SH3)    [michaelis_menten] 
    Shc(PTB,Y317(pY)) + Grb2(SH2,SH3[2]) <> Shc(PTB,Y317(pY)[1]).Grb2(SH2[1],SH3[2]) [michaelis_menten] 
    Shc(PTB,Y317(pY)) > Shc(PTB,Y317(Y)) [michaelis_menten] 
    Grb2(SH2,SH3) + Sos(dom) <> Grb2(SH2,SH3[1]).Sos(dom[1]) [michaelis_menten]
    Shc(PTB,Y317(pY)[2]).Grb2(SH2[2],SH3) + Sos(dom) <> \
    Shc(PTB,Y317(pY)[2]).Grb2(SH2[2],SH3[3]).Sos(dom[3]) [michaelis_menten]
