# import inspect
import sys

# Avogadro's number
# N_A = 6.0221367e+23


def MassAction(*args):
    # args is required to be (k, )
    return ["MassAction", args]

def MichaelisUniUni(*args):
    # args is required to be (KmS, KmP, KcF, KcR, volume)
    return ["MichaelisUniUni", args]

class FluxProcess(object):
    # def conc(self, sp):
    #     '''returns values of species in sp_list which has species idx
    #     '''
    #     # return [va[i] for i in sp_list]
    #     # (args, varargs, varkw, locals) = inspect.getargvalues(frame)
    #     va = inspect.getargvalues(
    #         inspect.stack()[2][0]).locals['variable_array']
    #     return va[sp['id']]

    def exit_with_message(self, msg=None):
        if msg is not None:
            sys.stdout.write('%s\n' % msg)
        sys.exit()

class MassActionFluxProcess(FluxProcess):
    def __init__(self, reactants, products, effectors, args, kwargs):
        # self.reactants, self.products, self.effectors = (
        #     reactants, products, effectors)
        self.reactants = reactants

        self.k_value, = args

    def __call__(self, variable_array, time):
        velocity = self.k_value * variable_array[self.reactants[0]['vid']]
        for r in self.reactants:
            coef = r['coef']
            value = variable_array[r['id']] / variable_array[r['vid']]
            while coef > 0:
                velocity *= value
                coef -= 1
        return velocity

    def __str__(self):
        retval = 'MassActionFluxProcess('
        retval += 'k=%f, ' % (self.k_value)
        retval += 'reactants=%s' % self.reactants
        retval += ')'
        return retval

class MichaelisUniUniFluxProcess(FluxProcess):
    def __init__(self, reactants, products, effectors, args, kwargs):
        self.reactants, self.products, self.effectors = (
            reactants, products, effectors)

        self.KmS, self.KmP, self.KcF, self.KcR, self.volume = args

        # Get Species' name
        # print [x.str_simple() for x in self.species.values()]
        # for i, v in enumerate(species): print i+1, species[v].str_simple()

        # Get Reactors' name
        # print [i.str_simple() for i in effectors]

        if len(self.reactants) != 1 or len(self.products) != 1:
            self.exit_with_message(
                "the numbers of reactants and products must be 1.")

    def __call__(self, variable_array, time):
        # for i, v in enumerate(self.species):
        #     print self.species[v].str_simple(), variable_array[i]
        # def molar_conc(sp):
        #     """${3:function documentation}"""
        #     n = self.conc(sp)
        #     conc_v = n / self.volume
        #     mol_conc = conc_v / N_A
        #     return mol_conc

        S = variable_array[self.reactants[0]['id']] / self.volume
        P = variable_array[self.products[0]['id']] / self.volume
        E = variable_array[self.effectors[0]['id']] / self.volume

        # velocity = self.KcF * E * S / (self.KmS + S)
        velocity = self.KcF * S - self.KcR * P
        velocity /= self.KmS * self.KmP + self.KmP * S + self.KmS * P
        velocity *= self.volume
        return velocity

    def __str__(self):
        retval = 'MichaelisUniUniFluxProcess('
        retval += 'KmS=%f, KmP=%f, KcF=%f, KcR=%f, volume=%f, ' % (
            self.KmS, self.KmP, self.KcF, self.KcR, self.volume)
        retval += 'reactants=%s, ' % self.reactants
        retval += 'products=%s, ' % self.products
        retval += 'effectors=%s' % self.effectos
        retval += ')'
        return retval
