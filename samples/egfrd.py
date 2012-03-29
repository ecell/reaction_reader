#from param import *

with molecule_types:
    egf(r)
    Grb2(SH2,SH3)
    Shc(PTB, Y317(Y, pY))
    Sos(dom)
    egfr(l,r,Y1068(Y, pY),Y1148(Y, pY))

with molecule_inits:
    egf(r) [1.2e6]
    egfr(l,r,Y1068(Y),Y1148(Y)) [1.8e5]
    Grb2(SH2,SH3) [1.0e5]
    Shc(PTB, Y317(Y)) [2.7e5]
    Sos(dom) [1.3e4]
    Grb2(SH2,SH3[1]).Sos(dom[1]) [4.9e4]

with reaction_rules:
    # Ligand-receptor binding
    egfr(l,r) + egf(r) <_> egfr(l[1],r).egf(r[1]) | (1.667e-06, .06)

    # Receptor-aggregation
    egfr(l[1],r) + egfr(l[2],r) <_> egfr(l[1],r[3]).egfr(l[2],r[3]) | (5.556e-06, .1)

    # Transphosphorylation of egfr by RTK
    egfr(r[1],Y1068(Y)) > egfr(r[1],Y1068(pY)) | .5
    egfr(r[1],Y1148(Y)) > egfr(r[1],Y1148(pY)) | .5

    #Dephosphorylayion
    egfr(Y1068(pY)) > egfr(Y1068(Y)) | 4.505
    egfr(Y1148(pY)) > egfr(Y1148(Y)) | 4.505

    # Shc transphosph
    egfr(r[2],Y1148(pY)[1]).Shc(PTB[1],Y317(Y)) > egfr(r[2],Y1148(pY)[1]).Shc(PTB[1],Y317(pY)) | 3
    Shc(PTB[1],Y317(pY)) > Shc(PTB[1],Y317(Y)) | .03

    # Y1068 activity
    egfr(Y1068(pY)) + Grb2(SH2,SH3) <_> egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3) | (8.333e-07, .05)
    egfr(Y1068(pY)) + Grb2(SH2,SH3[2]) <_> egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3[2]) | (1.25e-06, .03)
    egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3) + Sos(dom) <_> egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3[2]).Sos(dom[2]) | (5.556e-06, .06)

    # Y1148 activity
    egfr(Y1148(pY)) + Shc(PTB,Y317(Y)) <_> egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(Y)) | (2.5e-05, .6)
    egfr(Y1148(pY)) + Shc(PTB,Y317(pY)) <_> egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)) | (2.5e-07, .3)
    egfr(Y1148(pY)) + Shc(PTB,Y317(pY)[1]).Grb2(SH2[1],SH3) <_> \
           egfr(Y1148(pY)[2]).Shc(PTB[2],Y317(pY)[1]).Grb2(SH2[1],SH3) | (2.5e-07, .3)
    egfr(Y1148(pY)) + Shc(PTB,Y317(pY)[1]).Grb2(SH2[1],SH3[3]).Sos(dom[3]) <_> \
           egfr(Y1148(pY)[2]).Shc(PTB[2],Y317(pY)[1]).Grb2(SH2[1],SH3[3]).Sos(dom[3]) | (6.667e-08, .12)

    egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)) + Grb2(SH2,SH3) <_> \
           egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)[2]).Grb2(SH2[2],SH3) | (1.667e-06, .1)

    egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)) + Grb2(SH2,SH3[3]).Sos(dom[3]) <_> \
           egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)[2]).Grb2(SH2[2],SH3[3]).Sos(dom[3]) | (5e-06, .0429)

    Shc(PTB[1],Y317(pY)[2]).Grb2(SH2[2],SH3) + Sos(dom) <_> \
           Shc(PTB[1],Y317(pY)[2]).Grb2(SH2[2],SH3[3]).Sos(dom[3]) | (5.556e-06, 0.0214)

    # Cytosolic
    Shc(PTB,Y317(pY)) + Grb2(SH2,SH3)    <_> Shc(PTB,Y317(pY)[1]).Grb2(SH2[1],SH3)    | (1.667e-06, .01)
    Shc(PTB,Y317(pY)) + Grb2(SH2,SH3[2]) <_> Shc(PTB,Y317(pY)[1]).Grb2(SH2[1],SH3[2]) | (1.167e-05, .1)
    Shc(PTB,Y317(pY)) > Shc(PTB,Y317(Y)) | .005
    Grb2(SH2,SH3) + Sos(dom) <_> Grb2(SH2,SH3[1]).Sos(dom[1]) | (5.556e-08, .0015)
    Shc(PTB,Y317(pY)[2]).Grb2(SH2[2],SH3) + Sos(dom) <_> Shc(PTB,Y317(pY)[2]).Grb2(SH2[2],SH3[3]).Sos(dom[3]) | (1.667e-05, .064)
