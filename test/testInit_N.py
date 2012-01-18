'''

'''

#from func import *

with molecule_types:
    L1(a(_0,_1), b(_0,_1))
    L2(c(_0,_1), d(_0,_1), e(_0,_1))
    R1(o(_0,_1))
    R2(p(_0,_1), q(_0,_1), r(_0,_1), s(_0,_1))
    M(x(_0,_1), y(_0,_1))
    N(z(_0,_1), w(_0,_1))
    A(a2)
    B()
    C(c1, c1)

with molecule_inits:
    L1(a(_0), b(_0))        [10]
    L1(a(_0), b(_1))        [20]
#    L2(c(_0), d(_0), e(_0)) [30]
#    R1(o(_1))               [40]
#    A(a2)                   [50]
#    B()                     [60]
#    C(c1, c1)                [70]

with reaction_rules:

#    NG #1 : useless rule is generated (L(0,0)>L(0,0))
#    L1(a%1, b%2) > L1(a%2, b%1) | 0.3

#    NG #3 : %1(label of first R1) is overlapped by %2(label of second R1)
#    R1(o(_0)) <_> R1(o(_1)) | 0.1
#    R1(o%1) + R1(o%2) + L1(a%3, b%4) > R2(p%1, q%2, r%3, s%4) | 0.3

#    NG #4 : reaction is not created.
#    A(a2) > B() | 0.3

#    NG #5 : not concrete
#    A(a2) + L1(a%1) <_> A(a2[1]).L1(a[1]%1) | (0.1, 0.2)

#    NG #6 : components with same name
#    C(c1, c1) + A(a2) > C(c1[1], c1).A(a2[1]) | 0.3



#    OK #0
#    L1(a(_0),b(_0))+L2(c(_0),d(_0),e(_0))>L1(a(_1),b(_1))+L2(c(_1),d(_1),e(_1)) | 0.3

#    OK #1
#    L1(a%1) > R1(o%1) | 0.3

#    OK #2
#    L1(b%1) > R1(o%1) | 0.3

#    OK #3
#    L1(b%1) > R1(o%1) | 0.3
#    L1(a%1, b%2) <_> M(x%1, y%2) | 0.3
#    M(x%1, y%2) <_> N(z%1, w%2)  | 0.3

#    OK #4
#    L1(a%1, b%2) + A(a2) > M(x%1, y%2) | 0.3
#    R1(o%1) + L1(a%2, b%3) > L2(c%1, d%2, e%3) | 0.3
#    L1(a%1, b%2) + L2(c%3, d%4, e%5) > R1(o%1) | 0.1
#    R2(p%1, q%2, r%3, s%4) > L2(c%1, d%2, e%4) | 0.3

#    OK #5
#    L1(a%1,b%2)+L2(c(_0),d(_0),e(_0))<_>L1(a%2,b%1)+L2(c(_1),d(_1),e(_1)) | 0.3
#    L2(c%1, d%2, e%3) <_> L1(a%1, b%2) + R1(o%3) | 0.3
#    L1(a%1, b%2) + L2(c%3, d%4, e%5) <_> R1(o%1) + R2(p%2, q%3, r%4, s%5) | 0.1

#    OK #6
#    L1(a(_0), b(_0)) <_> L1(a(_1), b(_1)) | 0.1
#    L1(a%1) > R1(o%1) | 0.3

#    OK #7
#    R1(o%1) > B() | 0.3

#    OK #8
#    A(a2) + R1(o%1) <_> A(a2[1]).R1(o[1]%1) | (0.1, 0.1)
#    R1(o(_0)) <_> R1(o(_1)) | (0.2, 0.3)

#    OK #9
#    A(a2) + L1(a%1, b%2) <_> A(a2[1]).L1(a[1]%1, b%2) | (0.1, 0.2)
#    L1(a(_0)) > L1(a(_1)) | 0.2

#    OK #10 : by disabling concreteness check
#    A(a2) > A(a2) + L1(a(_0), b(_0)) | 0.1
#    A(a2) > A(a2) + L1(a(_0), b(_1)) | 0.2
#    L1(a%1, b%2) + R1(o%3) > L2(c%1, d%2, e%3) | 0.3
#    L2(c%1, d%2, e%3) > L1(a%3, b%2) | 0.4

#    OK #11 : multiple generateion (L1(0,0)>R1(0)) (small different)
    L1(a%1) > R1(o%1) | 0.3
    L1(b%1) > R1(o%1) | 0.7
    # L1(a(_0),b(_0)) > R1(o(_0)) | 1.0
    # L1(a(_0),b(_1)) > R1(o(_0)) | 0.3
    # L1(a(_0),b(_1)) > R1(o(_1)) | 0.7
