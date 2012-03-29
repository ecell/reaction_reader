# Avogadro's number
N_A = 6.0221367e+23


# def mass_action(*args, **kwargs):
#     # args is required to be (k, )
#     return ("mass_action", args, kwargs)

# def michaelis_uni_uni(*args, **kwargs):
#     # args is required to be (KmS, KmP, KcF, KcR, volume)
#     return ("michaelis_uni_uni", args, kwargs)

class RateRaw(object):
    def __init__(self, reactants, products, effectors, *args, **kwargs):
        self.args, self.kwargs = args, kwargs
        self.reactants, self.products, self.effectors = (
            reactants, products, effectors)
        self.func = None
            
    def __call__(self, x, t):
        return self.func(
            x, t, self.reactants, self.products, self.effectors, 
            *self.args, **self.kwargs)

    def name(self):
        return self.func.__name__ if self.func is not None else ''

    def __str__(self):
        retval = '%s(reactants=%s, products=%s, effectors=%s, ' % (
            self.name(), self.reactants, self.products, self.effectors)
        retval += 'args=%s, kwargs=%s)' % (
            self.args, self.kwargs)
        return retval
        
def rateraw(func):
    def wrapper(reactants, products, effectors, *args, **kwargs):
        raterawobj = RateRaw(reactants, products, effectors, *args, **kwargs)
        raterawobj.func = func
        return raterawobj
    return wrapper

def conc(x, sp):
    return x[sp['id']] / x[sp['vid']]

def molarconc(x, sp):
    return conc(x, xp) / N_A

def volume(x, sp):
    return x[sp['vid']]

@rateraw
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

@rateraw
def michaelis_menten(x, t, reactants, products, effectors, *args, **kwargs):
    k, Km, = args
    S = conc(x, reactants[0])
    E = conc(x, effectors[0])

    veloc = k * E * S / (Km + S)
    veloc *= volume(x, reactants[0])
    return veloc

@rateraw
def michaelis_uni_uni(x, t, reactants, products, effectors, *args, **kwargs):
    KmS, KmP, KcF, KcR = args

    S = conc(x, reactants[0])
    P = conc(x, products[0])
    E = conc(x, effectors[0])

    veloc = KcF * S - KcR * P
    veloc /= KmS * KmP + KmP * S + KmS * P
    veloc *= volume(x, reactants[0])
    return veloc
