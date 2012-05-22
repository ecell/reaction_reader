========
Example
========

- Alphabets under each examples show the timing of corresponding process step.
- Arrows (->) show return value of process.
- $A means return value of step.A.

- operator precedence of Python
  1. call, getattr, getitem
  2. add
  3. or
  4. gt

--------------
MoleculeTypes
--------------

- egf(r)
    A BC

  A. AnyCallable.__init__(egf) -> AnyCallable
  B. AnyCallable.__init__(r) -> AnyCallable
  C. $A.__call__($B) -> PartialEntity(None, $B).__call__($B) -> RuleEntitySet

- egfr(Y = (U, P))
     A B    C  D E

  A. AnyCallable.__init__(egfr) -> AnyCallable
  B. AnyCallable.__init__(Y) -> AnyCallable
  C. AnyCallable.__init__(U) -> AnyCallable
  D. AnyCallable.__init__(P) -> AnyCallable
  E. $A.__call__($B = ($C, $D)) -> PartialEntity(None, $A).__call__($B = ($C, $D)) -> RuleEntitySet

--------------
MoleculeInits
--------------

- egf(r) [10]
    A BC    D

  A. AnyCallable.__init__(egf) -> AnyCallable
  B. AnyCallable.__init__(r) -> AnyCallable
  C. $A.__call__($B) -> PartialEntity(None, $A).__call__($B) -> RuleEntitySet
  D. $C.__getitem__(10) -> RuleEntitySet

- egfr(Y = U) [20]
     A B   CD    E

  A. AnyCallable.__init__(egfr) -> AnyCallable
  B. AnyCallable.__init__(Y) -> AnyCallable
  C. AnyCallable.__init__(U) -> AnyCallable
  D. $A.__call__($B = $C) -> PartialEntity(None, $A).__call__($B = $C) -> RuleEntitySet
  E. $D.__getitem__(20) -> RuleEntitySet

- egf(r[1]).egfr(l[1]) [30]
    A B  CD    E F  GH    I

  A. AnyCallable.__init__(egf) -> AnyCallable
  B. AnyCallable.__init__(r) -> AnyCallable
  C. $B.__getitem__(1) -> RuleEntityComponent
  D. $A.__call__($C) -> PartialEntity(None, $A).__call__($C) -> RuleEntitySet
  E. $D.__getattr__(egfr) -> PartialEntity
  F. AnyCallable.__init__(l) -> AnyCallable
  G. $F.__getitem__(1) -> RuleEntityComponent
  H. $E.__call__($G) -> RuleEntitySet
  I. $H.__getitem__(30) -> RuleEntitySet

- R(tf = P[1]).TF(d[1]) [40]
  A  B   C  DE  F G  HI    J

  A. AnyCallable.__init__(R) -> AnyCallable
  B. AnyCallable.__init__(tf) -> AnyCallable
  C. AnyCallable.__init__(P) -> AnyCallable
  D. $C.__getitem__(1) -> RuleEntityComponent
  E. $A.__call__($B = $D) -> PartialEntity(None, $A).__call__($B = $D) -> RuleEntitySet
  F. $E.__getattr__(TF) -> PartialEntity
  G. AnyCallable.__init__(d) -> AnyCallable
  H. $G.__getitem__(1) -> RuleEntityComponent
  I. $F.__call__($H) -> RuleEntitySet
  J. $I.__getitem__(40) -> RuleEntitySet

--------------
ReactionRules
--------------

- egf(r) > egfr(l) [egf(r)] | 0.1
    A BC L    D EF    G HIJ     K

  A. AnyCallable.__init__(egf) -> AnyCallable
  B. AnyCallable.__init__(r) -> AnyCallable
  C. $A.__call__($B) -> PartialEntity(None, $A).__call__($B) -> RuleEntitySet
  D. AnyCallable.__init__(egfr) -> AnyCallable
  E. AnyCallable.__init__(l) -> AnyCallable
  F. $D.__call__($E) -> PartialEntity(None, $D).__call__($E) -> RuleEntitySet
  G. AnyCallable.__init__(egf) -> AnyCallable
  H. AnyCallable.__init__(r) -> AnyCallable
  I. $G.__call__($H) -> PartialEntity(None, $G).__call__($H) -> RuleEntitySet
  J. $F.__getitem__($I) -> RuleEntitySet
  K. $J.__or__(0.1) -> $J.toRuleEntitySetList().__or__(0.1) -> RuleEntitySetList
  L. $C.__gt__($K) -> $C.toRuleEntitySetList().__gt__($K) -> Rule

- egf(r)  > egf(r) + egf(r) [egf(r)] | 0.2
    A BC  P   D EF N   G HI    J KLM     O

  A. AnyCallable.__init__(egf) -> AnyCallable
  B. AnyCallable.__init__(r) -> AnyCallable
  C. $A.__call__($B) -> PartialEntity(None, $A).__call__($B) -> RuleEntitySet
  D. AnyCallable.__init__(egf) -> AnyCallable
  E. AnyCallable.__init__(r) -> AnyCallable
  F. $D.__call__($E) -> PartialEntity(None, $D).__call__($E) -> RuleEntitySet
  G. AnyCallable.__init__(egf) -> AnyCallable
  H. AnyCallable.__init__(r) -> AnyCallable
  I. $G.__call__($H) -> PartialEntity(None, $G).__call__($H) -> RuleEntitySet
  J. AnyCallable.__init__(egf) -> AnyCallable
  K. AnyCallable.__init__(r) -> AnyCallable
  L. $J.__call__($K) -> PartialEntity(None, $J).__call__($K) -> RuleEntitySet
  M. $I.__getitem__($L) -> RuleEntitySet
  N. $F.__add__($M) -> $F.toRuleEntitySetList().__add__($M) -> RuleEntitySetList
  O. $N.__or__(0.2) -> RuleEntitySetList
  P. $C.__gt__($O) -> $C.toRuleEntitySetList().__gt__($O) -> Rule

- egf(r) + egf(r, l) + egf(r) > egf(r[1]).egf(r[1], l[2]).egf(r[2]) | 0.3
    A BC H   D E  FG L   I JK b   M N  OP   Q R  S  T  UV   W X  YZ     a

  A. AnyCallable.__init__(egf) -> AnyCallable
  B. AnyCallable.__init__(r) -> AnyCallable
  C. $A.__call__($B) -> PartialEntity(None, $A).__call__($B) -> RuleEntitySet
  D. AnyCallable.__init__(egf) -> AnyCallable
  E. AnyCallable.__init__(r) -> AnyCallable
  F. AnyCallable.__init__(l) -> AnyCallable
  G. $D.__call__($E, $F) -> PartialEntity(None, $D).__call__($E, $F) -> RuleEntitySet
  H. $C.__add__($G) -> $C.toRuleEntitySetList().__add__($G) -> RuleEntitySetList
  I. AnyCallable.__init__(egf) -> AnyCallable
  J. AnyCallable.__init__(r) -> AnyCallable
  K. $I.__call__($J) -> PartialEntity(None, $I).__call__($J) -> RuleEntitySet
  L. $H.__add__($K) -> RuleEntitySetList
  M. AnyCallable.__init__(egf) -> AnyCallable
  N. AnyCallable.__init__(r) -> AnyCallable
  O. $N.__getitem__(1) -> RuleEntityComponent
  P. $M.__call__($O) -> PartialEntity(None, $M).__call__($O) -> RuleEntitySet
  Q. $P.__getattr__(egf) -> PartialEntity
  R. AnyCallable.__init__(r) -> AnyCallable
  S. $R.__getitem__(1) -> RuleEntityComponent
  T. AnyCallable.__init__(l) -> AnyCallable
  U. $T.__getitem__(2) -> RuleEntityComponent
  V. $Q.__call__($S, $U) -> RuleEntitySet
  W. AnyCallable.__init__(egf) -> AnyCallable
  X. AnyCallable.__init__(r) -> AnyCallable
  Y. $X.__getitem__(2) -> RuleEntityComponent
  Z. $W.__call__($Y) -> RuleEntitySet
  a. $Z.__or__(0.3) -> $a.toRuleEntitySetList().__or__(0.3) -> RuleEntitySetList
  b. $L.__add__($a) -> $Rule
