from model.model import *

def michaelis_menten(a=None):
    return float(a)

def MassAction(a=None):
    return float(a)

def include_reactants(a=None, b=None):
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
