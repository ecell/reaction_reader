''' 
    Test script for GillespieSolver
    
    This script input following chemical reactions.

    X <-> Y     (Kon = 0.5, Koff = 0.2)
    2X <-> Z    (Kon = 0.4, Koff = 0.2)
    X + Y <-> 2X    (Kon = 0.3 Koff = 0.5)
'''
import numpy as np
import GillespieSolver

'''
import sys
print "Wating for debug. Press Ctrl + D"
for line in sys.stdin:
    print line
'''


chem_dict = dict([('X', 0), ('Y', 1), ('Z', 2), ('W', 3)])
world = np.array([1000, 1000, 1000, 1000], np.int32)  # X, Y, Z, W


gs = GillespieSolver.GillespieSolver()
# Reaction 1
r1 = gs.reaction_add()
gs.reaction_add_substance(r1, chem_dict['X'], 1)
gs.reaction_add_product(r1, chem_dict['Y'], 1)
gs.reaction_set_kinetic_parameter(r1, 0.5)

# Reaction 2
r2 = gs.reaction_add()
gs.reaction_add_substance(r2, chem_dict['Y'], 1)
gs.reaction_add_product(r2, chem_dict['X'], 1)
gs.reaction_set_kinetic_parameter(r2, 0.2)

# Reaction 3
r3 = gs.reaction_add()
gs.reaction_add_substance(r3, chem_dict['X'], 2)
gs.reaction_add_product(r3, chem_dict['Z'], 1)
gs.reaction_set_kinetic_parameter(r3, 0.4)

# Reaction 4
r4 = gs.reaction_add()
gs.reaction_add_substance(r4, chem_dict['Z'], 1)
gs.reaction_add_product(r4, chem_dict['X'], 2)
gs.reaction_set_kinetic_parameter(r4, 0.2)

# Reaction 5
r5 = gs.reaction_add()
gs.reaction_add_substance(r5, chem_dict['X'], 1)
gs.reaction_add_substance(r5, chem_dict['W'], 1);
gs.reaction_add_product(r5, chem_dict['X'], 2);
gs.reaction_set_kinetic_parameter(r5, 0.3);

# Reaction 6
r6 = gs.reaction_add();
gs.reaction_add_substance(r6, chem_dict['X'], 2);
gs.reaction_add_product(r6, chem_dict['X'], 1);
gs.reaction_add_product(r6, chem_dict['W'], 1);
gs.reaction_set_kinetic_parameter(r6, 0.5);

gs.set_current_state(world)
gs.duration(9.0)

world_after_10_seconds = np.empty( len(world), np.int32 )
gs.get_current_state(world_after_10_seconds)

print world_after_10_seconds
