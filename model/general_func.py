# for the internal state
STATE_UNSPECIFIED = -1
STATE_UNSPECIFIED_STRING = '?'

# for binding state
BINDING_UNSPECIFIED = -1
BINDING_SPECIFIED = 1
BINDING_NONE = 0
BINDING_UNSPECIFIED_STRING = '?'
BINDING_ANY = 2
BINDING_ANY_STRING = '+'

# Constants for the condition of reaction rule.
REACTANTS = 1
PRODUCTS = 2

from Correspondence import *

def create_correspondence_list(pairs):
    '''
    Creates a list of correspondences from given pairs.

    pairs: List of pairs.
    '''
    cp_pairs = list(pairs)
    cp_pairs.sort()

    # Creates the lists of pairs for each first entity.
    pair_lists = []
    cur_pair = None
    cur_list = []
    for i, pair in enumerate(cp_pairs):
        if i == 0:
            cur_pair = pair
        else:
            if not pair.has_equal_first_element(cur_pair):
                pair_lists.append(cur_list)
                cur_list = []
                cur_pair = pair
        cur_list.append(pair)
    if len(cur_list):
        pair_lists.append(cur_list)

    combination_lists = []
    for i, pair_list in enumerate(pair_lists):
        if i == 0:
            for pair in pair_list:
                combination_lists.append([pair])
        else:
            comb_lists_new = []
            for comb in combination_lists:
                for pair in pair_list:
                    exists = False
                    for el in comb:
                        if el.has_equal_second_element(pair):
                            exists = True
                            break
                    if exists:
                        continue
                    list_new = list(comb) + [pair]
                    comb_lists_new.append(list_new)
            combination_lists = comb_lists_new

    correspondence_list = []
    for comb in combination_lists:
        c = Correspondence()
        for pair in comb:
            c.add_pair(pair)
        correspondence_list.append(c)

    return correspondence_list


