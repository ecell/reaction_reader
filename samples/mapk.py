from numpy import pi, inf
from ratelaw import ratelaw, conc, volume, N_A

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

k1 = 0.027e+9 / (N_A * 1000)
k2 = 1.35
k3 = 1.5
k4 = 0.056e+9 / (N_A * 1000)
k5 = 1.73
k6 = 15.0

sigma, D, Nkk = 5e-9, 2e-12, 30
# sigma = 5e-9

kD = 4 * pi * sigma * D

if kD < inf:
    kon1, koff1, kf1 = k1 * kD / (k1 + kD), k2 * kD / (k1 + kD), k3
    kon2, koff2, kf2 = k4 * kD / (k4 + kD), k5 * kD / (k4 + kD), k6
else:
    kon1, koff1, kf1 = k1, k2, k3
    kon2, koff2, kf2 = k4, k5, k6

tau_rel = 1e-3
krel = 0.69314718055994529 / tau_rel
# krel = inf

with molecule_types:
    mapk(phos=(YT, pYT, pYpT))
    kk(bs=(on, off))
    pp(bs=(on, off))

with molecule_inits:
    mapk(phos=YT) [120]
    kk(bs=on) [Nkk]
    pp(bs=on) [60 - Nkk]

with reaction_rules:
    mapk(phos=YT) + kk(bs=on) == mapk(phos=YT[1]).kk(bs=on[1]) \
        | (kon1, koff1)
    mapk(phos=YT[1]).kk(bs=on[1]) \
        > mapk(phos=pYT) + kk(bs=(off if krel < inf else on)) | kf1

    mapk(phos=pYT) + kk(bs=on) == mapk(phos=pYT[1]).kk(bs=on[1]) \
        | (kon2, koff2)
    mapk(phos=pYT[1]).kk(bs=on[1]) \
        > mapk(phos=pYpT) + kk(bs=(off if krel < inf else on)) | kf2

    mapk(phos=pYpT) + pp(bs=on) == mapk(phos=pYpT[1]).pp(bs=on[1]) \
        | (kon1, koff1)
    mapk(phos=pYpT[1]).pp(bs=on[1]) \
        > mapk(phos=pYT) + pp(bs=(off if krel < inf else on)) | kf1

    mapk(phos=pYT) + pp(bs=on) == mapk(phos=pYT[1]).pp(bs=on[1]) \
        | (kon2, koff2)
    mapk(phos=pYT[1]).pp(bs=on[1]) \
        > mapk(phos=YT) + pp(bs=(off if krel < inf else on)) | kf2

    if krel < inf:
        kk(bs=off) > kk(bs=on) | krel
        pp(bs=off) > pp(bs=on) | krel
