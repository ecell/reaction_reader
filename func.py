from model.model import *
#from model.model import IncludingEntityCondition

def michaelis_menten(a=None):
#    print '*** michaelis_menten(',a,') is called ***'
    return float(a)

def MassAction(a=None):
    return float(a)

def MassAction2(a=None, b=None):
    return a, b

def include_reactants(a=None, b=None):
#    print '*** include_reactants(', a, ',', b._key, ') is called ***'
    d = EntityType(b._key)
    d.__name=b._key
    c = IncludingEntityCondition(REACTANTS, int(a), d)
    return c

def include_products(a=None, b=None):
    d = EntityType(b._key)
    d.__name=b._key
    c = IncludingEntityCondition(PRODUCTS, int(a), d)
    return c

def exclude_reactants(a=None, b=None):
    return NotCondition(include_reactants(a, b))

def exclude_products(a=None, b=None):
    return NotCondition(include_products(a, b))
