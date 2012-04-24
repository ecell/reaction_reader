import types

# Avogadro's number
N_A = 6.0221367e+23


# def mass_action(*args, **kwargs):
#     # args is required to be (k, )
#     return ("mass_action", args, kwargs)

# def michaelis_uni_uni(*args, **kwargs):
#     # args is required to be (KmS, KmP, KcF, KcR, volume)
#     return ("michaelis_uni_uni", args, kwargs)

class RateLaw(object):
    def __init__(self, reactants, products, effectors, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
        self.reactants, self.products, self.effectors = (
            reactants, products, effectors)
            
    def __call__(self, x, t):
        return 0.0

    def name(self):
        return self.__class__.__name__

    def __str__(self):
        retval = '%s(reactants=%s, products=%s, effectors=%s, ' % (
            self.name(), self.reactants, self.products, self.effectors)
        retval += 'args=%s, kwargs=%s)' % (
            self.args, self.kwargs)
        return retval

def ratelaw(func):
    class DecoratedRateLaw(RateLaw):
        def __init__(self, reactants, products, effectors, *args, **kwargs):
            super(DecoratedRateLaw, self).__init__(
                reactants, products, effectors, *args, **kwargs)
            self.func = func
                
        def __call__(self, x, t):
            return self.func(
                x, t, self.reactants, self.products, self.effectors, 
                *self.args, **self.kwargs)
    
        def name(self):
            return self.func.__name__
    
    return DecoratedRateLaw

def load_ratelaws(module, module_name=None):
    if type(module) is types.ModuleType:
        if module_name is None:
            module_name = '%s.' % (module.__name__)
        namespace = module.__dict__
    elif issubclass(type(module), dict):
        if module_name is None:
            module_name = ''
        namespace = module
    else:
        return {}

    ratelaws = {}
    for key, value in namespace.items():
        if type(value) is type and issubclass(value, RateLaw):
            ratelaws['%s%s' % (module_name, key)] = value
    return ratelaws

def conc(x, sp):
    return x[sp['id']] / x[sp['vid']]

def molarconc(x, sp):
    return conc(x, xp) / N_A

def volume(x, sp):
    return x[sp['vid']]

@ratelaw
def mass_action(x, t, reactants, products, effectors, *args, **kwargs):
    k, = args
    
    veloc = k * volume(x, reactants[0])
    for r in reactants:
        coef = r['coef']
        value = conc(x, r)
        while coef > 0:
            veloc *= value
            coef -= 1
    return veloc

@ratelaw
def michaelis_menten(x, t, reactants, products, effectors, *args, **kwargs):
    k, Km, = args
    S = conc(x, reactants[0])
    E = sum([conc(x, effector) for effector in effectors])

    veloc = k * E * S / (Km + S)
    veloc *= volume(x, reactants[0])
    return veloc

@ratelaw
def michaelis_uni_uni(x, t, reactants, products, effectors, *args, **kwargs):
    KmS, KmP, KcF, KcR = args

    S = conc(x, reactants[0])
    P = conc(x, products[0])
    E = sum([conc(x, effector) for effector in effectors])

    veloc = KcF * S - KcR * P
    veloc /= KmS * KmP + KmP * S + KmS * P
    veloc *= volume(x, reactants[0])
    return veloc
