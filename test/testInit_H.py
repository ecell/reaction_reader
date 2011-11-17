'''
pybngl.py 1.43 or later
'''

from func import *

with molecule_types:
    L(r)
    R(l, d, Y(U, P))
    A(SH2, Y(U, P))
    B(b)
    C(X(U, P))
    D(d(A, B))

with molecule_inits:
    L(r) [10000]
    R(l, d, Y(U)) [5000]
    R(l, d, Y(P)) [5000]
    A(SH2, Y(U)) [2000]
    D(d(A)) [1000]
    D(d(B)) [1000]
#    R(l, d[1], Y(U)).A(SH2, Y(U)[1]) [1000]

with reaction_rules:


#    L(r) + R(l, Y(U)) + A(SH2) <_> L(r[1]).R(l[1], Y(U)[2]).A(SH2[2]) | (0.1, 0.3) # loop?

#    L(r) + R(l, Y%1)   > L(r[1]).R(l[1], Y%1) | 0.3        # ok
#    L(r) + R(l)        > L(r[1]).R(l[1])      | 0.3        # ok ( same )
    L(r) + R(d, Y%1) <_> L(r[1]).R(d, Y[1]%1) | (0.1, 0.3) # ok!

#    L(r) <_> A(SH2, Y(U)) | 0.3, 0.3 # ok (after model.py changed)
#    L() <_> A() | 0.3                # ng

#    R(Y(U)) > C(X(U)) | 0.3 # ok
#    R(Y()) > C(X())   | 0.3 # ng (attribute does not specified?)
    R(Y%1) > C(X%1)   | 0.3 # ok!

#    R(Y%1) + R(Y%2) > C(X%1) + C(X%2) | 0.3 # ok!

#    R(Y(P)) + R(Y%32) + D(d%23) > C(X%1) + C(X%32) + D(d%23) | 0.3 # ok!

#    R(d, Y%1) + R(d, Y%2) > R(d[1], Y%1).R(d[1], Y%2) | MassAction(0.1, 0.3) # ok!


#    R(d[1]).A(Y(U)[1]) > R(d[1]).A(Y(U)[1]%2) [A]| 0.3 # ok
