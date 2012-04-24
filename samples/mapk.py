from ratelaw import ratelaw, conc, volume

@ratelaw
def my_mass_action(x, t, reactants, products, effectors, *args, **kwargs):
    k, = args
    
    veloc = k * volume(x, reactants[0])
    for r in reactants:
        coef = r['coef']
        value = conc(x, r)
        while coef > 0:
            veloc *= value
            coef -= 1
    return veloc

# world.volume = 1e-18
kf1, kd1, kcat1 = 6.7e-23, 0.02, 0.1
kf2, kd2, kcat2 = 2.5e-23, 0.02, 0.1
# krel = 1.0
 
with molecule_types:
    mapk(phos(YT, pYT, pYpT))
    kk(bs(on, off))
    # pp(bs(on, off))

with molecule_inits:
    mapk(phos(YT)) [600]
    kk(bs(on)) [60]
    # pp(bs(on)) [0]

with reaction_rules:
    mapk(phos(YT)) + kk(bs(on)) <_> mapk(phos(YT)[1]).kk(bs(on)[1]) | (kf1, kd1)
    # mapk(phos(YT)[1]).kk(bs[1]) > mapk(phos(pYT)) + kk(bs(off)) | kcat1
    # mapk(phos(YT)[1]).kk(bs[1]) > mapk(phos(pYT)) + kk(bs) | kcat1
    mapk(phos(YT)[1]).kk(bs[1]) > mapk(phos(pYT)) + kk(bs) | ('my_mass_action', (kcat1, ))

    mapk(phos(pYT)) + kk(bs(on)) <_> mapk(phos(pYT)[1]).kk(bs(on)[1]) | (kf2, kd2)
    # mapk(phos(pYT)[1]).kk(bs[1]) > mapk(phos(pYpT)) + kk(bs(off)) | kcat2
    mapk(phos(pYT)[1]).kk(bs[1]) > mapk(phos(pYpT)) + kk(bs) | kcat2

    # mapk(phos(pYpT)) + pp(bs(on)) <_> mapk(phos(pYpT)[1]).pp(bs(on)[1]) | (kf1, kd1)
    # mapk(phos(pYpT)[1]).pp(bs[1]) > mapk(phos(pYT)) + pp(bs(off)) | kcat1

    # mapk(phos(pYT)) + pp(bs(on)) <_> mapk(phos(pYT)[1]).pp(bs(on)[1]) | (kf2, kd2)
    # mapk(phos(pYT)[1]).pp(bs[1]) > mapk(phos(YT)) + pp(bs(off)) | kcat2

    # kk(bs(off)) > kk(bs(on)) | krel
    # pp(bs(off)) > pp(bs(on)) | krel
