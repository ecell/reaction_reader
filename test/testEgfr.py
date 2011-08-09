from func import *

with molecule_types:
    egf(r)
    Grb2(SH2,SH3)
    Shc(PTB, Y317(Y))
    Sos(dom)
    egfr(l,r,Y1068(Y),Y1148(Y))
    Grb2(SH2,SH3[1]).Sos(dom[1])

with molecule_inits:
    egf(r) [1.2e6]
    egfr(l,r,Y1068(Y),Y1148(Y)) [1.8e5]
    Grb2(SH2,SH3) [1.0e5]
    Shc(PTB, Y317(Y)) [2.7e5]
    Sos(dom) [1.3e4]
    Grb2(SH2,SH3[1]).Sos(dom[1]) [4.9e4]

with reaction_rules:
    # Ligand-receptor binding
    egfr(l,r) + egf(r) <> egfr(l[1],r).egf(r[1]) | MassAction2(1.667e-06, .06)

    #egfr(l,r) + egf(r) <> egfr(l[1],r).egf(r[1]) [MassAction, (.1, )]
    #egfr(l,r) + egf(r) <> egfr(l[1],r).egf(r[1]) [egfr(l,r), egf(r)], MassAction, {"Vmax": 1.0, "Km": 2.0}
    #        [MassAction(effector= [egfr(l,r), egf(r)], params={"Vmax": 1.0, "Km": 2.0})]

    # Note changed multiplicity
    # Receptor-aggregation
    #egfr(l[1],r) + egfr(l[2],r) <> egfr(l[1],r[3]).egfr(l[2],r[3]) [MassAction(.1)]
    egfr(l[1],r) + egfr(l[2],r) <> egfr(l[1],r[3]).egfr(l[2],r[3]) | MassAction2(5.556e-06, .1)

    # Transphosphorylation of egfr by RTK
    egfr(r[1],Y1068(Y)) > egfr(r[1],Y1068(pY)) | MassAction(.5)
    egfr(r[1],Y1148(Y)) > egfr(r[1],Y1148(pY)) | MassAction(.5)

    #Dephosphorylayion
    egfr(Y1068(pY)) > egfr(Y1068(Y)) | MassAction(4.505)
    egfr(Y1148(pY)) > egfr(Y1148(Y)) | MassAction(4.505)

    # Shc transphosph
    egfr(r[2],Y1148(pY)[1]).Shc(PTB[1],Y317(Y)) > egfr(r[2],Y1148(pY)[1]).Shc(PTB[1],Y317(pY)) | MassAction(3)
    Shc(PTB[1],Y317(pY)) > Shc(PTB[1],Y317(Y)) | MassAction(.03)

    # Y1068 activity
    egfr(Y1068(pY)) + Grb2(SH2,SH3) <> egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3) | MassAction2(8.333e-07, .05)
    egfr(Y1068(pY)) + Grb2(SH2,SH3[2]) <> egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3[2]) | MassAction2(1.25e-06, .03)
    egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3) + Sos(dom) <> egfr(Y1068(pY)[1]).Grb2(SH2[1],SH3[2]).Sos(dom[2]) | MassAction2(5.556e-06, .06)

    # Y1148 activity
    egfr(Y1148(pY)) + Shc(PTB,Y317(Y)) <> egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(Y)) | MassAction2(2.5e-05, .6)
    egfr(Y1148(pY)) + Shc(PTB,Y317(pY)) <> egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)) | MassAction2(2.5e-07, .3)
    egfr(Y1148(pY)) + Shc(PTB,Y317(pY)[1]).Grb2(SH2[1],SH3) <> \
           egfr(Y1148(pY)[2]).Shc(PTB[2],Y317(pY)[1]).Grb2(SH2[1],SH3) | MassAction2(2.5e-07, .3)
    egfr(Y1148(pY)) + Shc(PTB,Y317(pY)[1]).Grb2(SH2[1],SH3[3]).Sos(dom[3]) <> \
           egfr(Y1148(pY)[2]).Shc(PTB[2],Y317(pY)[1]).Grb2(SH2[1],SH3[3]).Sos(dom[3]) | MassAction2(6.667e-08, .12)

    egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)) + Grb2(SH2,SH3) <> \
           egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)[2]).Grb2(SH2[2],SH3) | MassAction2(1.667e-06, .1)

    egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)) + Grb2(SH2,SH3[3]).Sos(dom[3]) <> \
           egfr(Y1148(pY)[1]).Shc(PTB[1],Y317(pY)[2]).Grb2(SH2[2],SH3[3]).Sos(dom[3]) | MassAction2(5e-06, .0429)

    Shc(PTB[1],Y317(pY)[2]).Grb2(SH2[2],SH3) + Sos(dom) <> \
           Shc(PTB[1],Y317(pY)[2]).Grb2(SH2[2],SH3[3]).Sos(dom[3]) | MassAction2(5.556e-06, 0.0214)

    # Cytosolic
    Shc(PTB,Y317(pY)) + Grb2(SH2,SH3)    <> Shc(PTB,Y317(pY)[1]).Grb2(SH2[1],SH3)    | MassAction2(1.667e-06, .01)
    Shc(PTB,Y317(pY)) + Grb2(SH2,SH3[2]) <> Shc(PTB,Y317(pY)[1]).Grb2(SH2[1],SH3[2]) | MassAction2(1.167e-05, .1)
    Shc(PTB,Y317(pY)) > Shc(PTB,Y317(Y)) | MassAction(.005)
    Grb2(SH2,SH3) + Sos(dom) <> Grb2(SH2,SH3[1]).Sos(dom[1]) | MassAction2(5.556e-08, .0015)
    Shc(PTB,Y317(pY)[2]).Grb2(SH2[2],SH3) + Sos(dom) <> \
    Shc(PTB,Y317(pY)[2]).Grb2(SH2[2],SH3[3]).Sos(dom[3]) | MassAction2(1.667e-05, .064)
