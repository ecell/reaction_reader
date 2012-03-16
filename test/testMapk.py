# from func import *

# kf1, kd1, kcat1 = 1.0, 1.0, 1.0
# kf2, kd2, kcat2 = 1.0, 1.0, 1.0
# krel = 1.0
 
with molecule_types:
    mapk(phos(YT, pYT, pYpT))
    kk(bs(on, off))
    pp(bs(on, off))

with molecule_inits:
    mapk(phos(YT)) [60]
    kk(bs(on)) [60]
    pp(bs(on)) [60]

with reaction_rules:
    mapk(phos(YT)) + kk(bs(on)) <_> mapk(phos(YT)[1]).kk(bs(on)[1]) | (kf1, kd1)
    mapk(phos(YT)[1]).kk(bs[1]) > mapk(phos(pYT)) + kk(bs(off)) | kcat1

    mapk(phos(pYT)) + kk(bs(on)) <_> mapk(phos(pYT)[1]).kk(bs(on)[1]) | (kf2, kd2)
    mapk(phos(pYT)[1]).kk(bs[1]) > mapk(phos(pYpT)) + kk(bs(off)) | kcat2

    mapk(phos(pYpT)) + pp(bs(on)) <_> mapk(phos(pYpT)[1]).pp(bs(on)[1]) | (kf1, kd1)
    mapk(phos(pYpT)[1]).pp(bs[1]) > mapk(phos(pYT)) + pp(bs(off)) | kcat1

    mapk(phos(pYT)) + pp(bs(on)) <_> mapk(phos(pYT)[1]).pp(bs(on)[1]) | (kf2, kd2)
    mapk(phos(pYT)[1]).pp(bs[1]) > mapk(phos(YT)) + pp(bs(off)) | kcat2

    kk(bs(off)) > kk(bs(on)) | krel
    pp(bs(off)) > pp(bs(on)) | krel
