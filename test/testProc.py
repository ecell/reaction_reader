def process(func):
    def declare(*args, **kwargs):
        def wrapper(reactants, products, effectors):
            class proccls(object):
                def __init__(self, *args, **kwargs):
                    self.args, self.kwargs = args, kwargs

                def __call__(self, x, t):
                    return func(x, t, reactants, products, effectors,
                                *self.args, **self.kwargs)

            return proccls(*args, **kwargs)
        return wrapper
    return declare

@process
def mass_action(x, t, reactants, products, effectors, *args, **kwargs):
    k, volume = args
    
    veloc = k * volume
    for r in reactants:
        coef = r['coef']
        value = x[r['id']] / volume
        while coef > 0:
            veloc *= value
            coef -= 1
    return veloc


with molecule_types:
    K1(phos(Y,pY))
    K2(phos(Y,pY))

with molecule_inits:
    K1(phos(Y))[60]
    K2(phos(Y))[60]

with reaction_rules:
    K1(phos(Y)) > K1(phos(pY)) | 2.0

    K2(phos(Y)) > K2(phos(pY)) | mass_action(2.0, 1.0)
