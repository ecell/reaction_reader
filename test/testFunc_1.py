#coding: utf-8
'''
  Example of user-defined function (MichaelisUniUni).

  - molecule inits
    S[60]
    P[0]
    C[60]

  - reaction rule
    S > P [C] | MichaelisUniUni(...)

  - parameters for function
    KmS = 100e-9
    KmP = 1.0
    KcF = 1.0
    KcR = 0.0
    volume = 1e-15

  - How to use user-defined function

  1. Add a call function to process/process.py .
     It is used to writing reaction rule in simulation file.
     It should return a list whose first element is str.  It is needed by
     process.FunctionMaker.make_functions() .

     >>
     def MichaelisUniUni(*args):
         return ["MichaelisUniUni", (args)]
     <<

  2. Add a function class to process/process.py .
     It should be derived class of FluxProcess class.
     __init__(), __call__(), and __str__() is required.

     >>
     def MichaelisMentenUniUniFluxProcess(FluxProcess):
         def __init__(self, KmS, KmP, KcF, KcR, 
                      volume, reactant, product, effectors):
             self.volume = volume
             ...

         def __call__(self, variale_array, time):
             ...
             return volocity

         def __str__(self):
             ...
     <<

  3. Add a condtion for user-defined function to 
     process.FunctionMaker.make_functions() .

     >>
     if k_name == 'MassAction':
         process = MassActionFluxProcess(...)

     # add following part
     elif k_name == 'MichaelisUniUni':
         process = MichaelisUniUniFluxProcess(...)

     else:
         ....
     <<
'''
#from func import *
from process.process import *

with molecule_types:
    S(a)
    P(a)
    C(a)

with molecule_inits:
    S(a) [60]
    P(a) [0]
    C(a) [60]

with reaction_rules:
    # MassAction
#    S(a) <_> P(a) [C(a)] | (MassAction(0.3), 0.3)

    # MichaelissUniUni(KmS, KmP, KcF, KcR, volume)
    S(a) > P(a) [C(a)] | MichaelisUniUni(100e-9, 1.0, 1.0, 0.0, 1e-15)

