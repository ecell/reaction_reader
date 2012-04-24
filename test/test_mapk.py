import numpy
import re

import World
import Simulator

import pybngl
import ratelaw


def get_indices(species_list, expr):
    return [i for i in range(len(species_list)) 
            if re.compile(expr).search(species_list[i].str_simple())]

def singlerun(filename, params):
    parser = pybngl.Pybngl()
    parser.namespace.newcls.tmp_list = []
    parser.namespace.newcls.global_list = []

    m, seed_species, namespace = parser.parse_model(filename, params=params)
    reaction_results = parser.generate_reaction_network(m, seed_species)

    ratelaws = ratelaw.load_ratelaws(namespace)

    w = pybngl.create_world(m, seed_species)
    w.volume = 1e-18
    simulator = Simulator.ODESimulator(
        m, w, reaction_results, ratelaws=ratelaws)

    simulator.run(60 * 60 * 100)
    data = simulator.get_logged_data().T
    return data, simulator.get_species()

def run(filename, params):
    expr_list = ['phos\(YT\)', 'phos\(pYT\)', 'phos\(pYpT\)']

    Nkk_list = range(1, 60) # numpy.arange(1, 60, dtype=int)
    return_val = []
    for Nkk in Nkk_list:
        params.update(dict(Nkk=Nkk))
        data, species_list = singlerun(filename, params)
        y = []
        for expr in expr_list:
            indices = get_indices(species_list, expr)
            y.append(sum([data[idx + 1][-1] for idx in indices])) 
        return_val.append(y)

    return numpy.array(Nkk_list), numpy.array(return_val).T


if __name__ == '__main__':
    # reaction_reader$ PYTHONPATH=$PYTHONPATH:. python test/test_mapk.py

    import matplotlib.pylab as plt
    import matplotlib as mpl


    filename = 'samples/mapk.py'

    colors = ['b', 'g', 'r', 'c', 'y', 'k']

    D_list = [0.06e-12, 0.25e-12, 1.0e-12, 4e-12]
    for i, D in enumerate(D_list):
        x, y = run(filename, dict(D=D))

        x = x / (60.0 - x)
        y = y / 120.0

        c = colors[i]
        plt.semilogx(x, y[2], 'o-', color=c, markeredgecolor=c, markerfacecolor=c, label=r'$%g\mathrm{\mu m^2/s}$' % (D * 1e+12))

    plt.xlabel('[KK]/[P]')
    plt.legend(loc='best', shadow=True)
    plt.show()
