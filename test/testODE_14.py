'''
Based on a sample file:
http://vcell.org/bionetgen/models/icsb2009-sample.bngl

rule_text = 'L(r) + R(l,d) -> L(r!1).R(l!1,d)'
rule_text = 'L(r!1).R(l!1,d) -> L(r) + R(l,d)'
rule_text = 'R(l!+,d) + R(l!+,d) -> R(l!+,d!2).R(l!+,d!2)'
rule_text = 'R(l!+,d!2).R(l!+,d!2) -> R(l!+,d) + R(l!+,d)'
rule_text = 'R(d!+,Y~U) -> R(d!+,Y~P)'
rule_text = 'R(Y~P) -> R(Y~U)'
rule_text = 'R(Y~P) + A(SH2) -> R(Y~P!1).A(SH2!1)'
rule_text = 'R(Y~P!1).A(SH2!1) -> R(Y~P) + A(SH2)'
rule_text = 'A(Y~U).A() -> A(Y~P).A()'
rule_text = 'A(Y~P) -> A(Y~U)'

'''

from func import *

with molecule_types:
     L(r)
     R(l, d, Y(U))
     A(SH2, Y(U))

with reaction_rules:
     L(r) + R(l, d) > L(r[1]).R(l[1], d) [MassAction(0.01)]
     L(r[1]).R(l[1], d) > L(r) + R(l, d) [MassAction(1.)]
     R(l[1], d) + R(l[2], d) > R(l[1], d[3]).R(l[2], d[3]) [MassAction(1.)]
     R(l[1], d[2]).R(l[3], d[2]) > R(l[1], d) + R(l[2], d) [MassAction(1.)]
     R(d[1], Y(U)) > R(d[1], Y(pU)) [MassAction(10.)]
     R(Y(pU)) > R(Y(U)) [MassAction(5.)]
     R(Y(pU)) + A(SH2) > R(Y(pU)[1]).A(SH2[1]) [MassAction(0.1)]
     R(Y(pU)[1]).A(SH2[1]) > R(Y(pU)) + A(SH2) [MassAction(0.1)]
     A(Y(U)).A() > A(Y(pU)).A() [MassAction(10.)]
     A(Y(pU)) > A(Y(U)) [MassAction(5.)]
