import World
import Simulator

import pybngl


if __name__ == '__main__':
    # reaction_reader$ PYTHONPATH=$PYTHONPATH:. python test/test_mapk.py

    filename = 'samples/mapk.py'

    parser = pybngl.Pybngl()
    m, seed_species = parser.parse_model(filename)
    reaction_results = parser.generate_reaction_network(m, seed_species)
    # reaction_results = parser.generate_reaction_network(
    #     m, seed_species, rulefilename='test/mapk.txt')

    w = pybngl.create_world(m, seed_species)
    simulator = Simulator.ODESimulator(m, w, reaction_results)

    simulator.run(60 * 60)
    data = simulator.get_logged_data().T
    
    import matplotlib.pylab as plt

    t = data[0] / 60
    plt.plot(t, data[1] + data[3], 'b-', label='mapk(phos(YT))')
    plt.plot(t, data[4] + data[5], 'g-', label='mapk(phos(pYT))')
    # plt.plot(t, data[4] + data[5] + data[6], 'g--', label='mapk(phos(pYT))')
    plt.plot(t, data[6], 'r-', label='mapk(phos(pYpT))')
    plt.legend(loc='best', shadow=True)
    plt.xlim(t[0], t[-1])
    plt.xlabel('Time (min)')
    plt.show()
