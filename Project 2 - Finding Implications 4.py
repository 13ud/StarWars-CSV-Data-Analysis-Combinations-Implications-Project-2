import csv
from reference import *
from itertools import combinations, permutations
from collections import defaultdict as d_dict


def sort_byorder_comblists(validlist, all_featureslist):
    """ Inputs:
    validlist - list of tuplefs consisting of (lift, antecedent, subsequent)
    all_featureslist - list of (antecedent, subsequent) feature combinations

    Helper function that returns a validlist that is sorted by
    the lift in decreasing order. In the case of a lift metric tie,
    this function sorts by order of combination in feature_comb_freq list """

    # Applied to sort by order of combination list IF List value is TIED*
    list_order = []
    check_unique_list = []
    for tuples in validlist:
        ant = tuples[1][0]
        sub = tuples[2]
        ant_sub = [ant, sub]

        # Checks if the (antecedent, subsequent) pairing (in a specific order)
        # Is present in the initial comb_freq list input via all_featureslist.
        # If SO AND this is the FIRST Time this (ant, sub) pairing is checked,
        # Then an additional value 'comb_index' is added to 2nd tuple position
        # to aid sorting by order of combination found
        if (sorted(ant_sub) in all_featureslist
                and ant_sub not in check_unique_list):
            check_unique_list.append(ant_sub)
            comb_index = 10 - all_featureslist.index(sorted(ant_sub))
            list_order.append((tuples[0], comb_index, tuples[1], tuples[2]))

    return sorted(list_order, reverse=True)


def find_implications(feature_comb_freq, max_out_len):
    """ Inputs:
    feature_comb_freq - the list of (combination, frequency) tuples where
    combination is a list of (feature, value) tuples. (comb. may be empty)
    max_out_len - the maximum list length in output

    Returns all possible implications for a given list of "feature = value"
    combinations, with the calculated lift metric. This uses antecedent and
    subsequent relationships, where empty subsequents are NOT tested """

    # This accounts for the corner cases where either the combination list
    # ONLY consists of an empty list, or ONE feature,
    # OR max_out_len is equal to 0, and returns an empty list.
    if len(feature_comb_freq) <= 1 or max_out_len == 0:
        return []

    if len(feature_comb_freq) == 2:
        return [(1, feature_comb_freq[1][0], [])]

    # Initialise lists, dicts and calculate the total data number for the sheet
    validlist = []
    singlefeatureslist = []
    all_featureslist = []
    asjoint_list = []
    total_no_of_rows = feature_comb_freq[0][1]
    frequency_dict = d_dict(int).copy()

    # Iterates through the feature_comb tuples excluding the first tuple
    # which contains ([], total_no_rows), and assigns the 1st part as a feature
    # and the 2nd as the frequency of the tuple.
    for tuples in feature_comb_freq[1:]:
        features, freq = tuples

        # This accounts for a feature_comb where there is more than one feature
        # IF SO, appended to all_featureslist containing all feature_comb
        # If only 1 feature, frequency is added to dict
        if len(features) > 1:
            all_featureslist.append(features)

            # Sorting is applied so that the same antecedent but in a different
            # order (i.e. permutations) will register the same frequency output
            frequency_dict[tuple(sorted(features, reverse=True))] = freq

        else:
            frequency_dict[features[0]] = freq
            singlefeatureslist.append(features)
            all_featureslist.append(features)

    # Creates and iterates through the permutations of the single features,
    # Leaving one untouched feature for the single subsequent tuple later on
    # The antecedent is assigned as the first element of the perm list created
    # and a copy of singlefeatureslist is made for every iteration to find sub
    for perm in permutations(singlefeatureslist, len(singlefeatureslist) - 1):
        remainingfeature = singlefeatureslist.copy()
        antecedent = perm[0][0]

        # Iterates through each feature in the perm and removes the feature
        # and assigns the remaining as the subsequent for this iteration
        for feature in perm:
            remainingfeature.remove(feature)
        subsequent = remainingfeature[0][0]

        # Combines the ant- and subsequent features to create the asjoint value
        # AND assigns a permutation version which is sorted a specific way
        # that allows the searching of the frequency_dict later on
        asjoint = tuple((antecedent, subsequent))
        perm_asjoint = tuple(sorted(asjoint, reverse=True))

        # Checks if the antecedent, subsequent joint combination is present
        # in the original list or has not been checked yet.
        # IF NOT for either, then this (ant, sub) pairing is ignored.
        # Note: The second condition makes sure repeated asjoints are ignored
        if (frequency_dict[perm_asjoint] == 0
                or asjoint in asjoint_list):
            continue
        asjoint_list.append(asjoint)

        # Calculates the epsilon value, the support, confidence and lift metric
        epsilon = 1 / total_no_of_rows
        support_subsq = frequency_dict[tuple(subsequent)] / total_no_of_rows
        conf_implc = frequency_dict[perm_asjoint] / frequency_dict[antecedent]
        lift = (1 + epsilon - support_subsq) / (1 + epsilon - conf_implc)

        # Adds tuple of (lift, ant, sub) to the validlist
        validlist.append((float(f'{lift:.3g}'), [antecedent], subsequent))

    # Uses HELPER function to sort elements in list by order of combination
    # found in the original list input. This is to meet set design conditions
    # After doing so, the comb_index value is 'removed', and the tuple pairing
    # (list, ant, sub) is appended to the finallist in order, to be returned.
    list_order = sort_byorder_comblists(validlist, all_featureslist)
    finallist = [(tuples[0], tuples[2], tuples[3]) for tuples in list_order]

    return finallist[:max_out_len]

print(find_implications([([], 40), ([(7, "normal")], 4), ([(9, "good")], 8), ([(7, "normal"), (9, "good")], 2)], 100))
# [(1.57, [(7, 'normal')], (9, 'good')), (1.19, [(9, 'good')], (7, 'normal'))]

print(find_implications([([], 4), ([(0, "7")], 2), ([(0, "7"), (2, "3")], 2), ([(1, "2")], 3), ([(1, "2"), (2, "3")], 3), ([(2, "3")], 4)], 100))
# [(1.0, [(2, '3')], (0, '7')), (1.0, [(0, '7')], (2, '3')), (1.0, [(2, '3')], (1, '2')), (1.0, [(1, '2')], (2, '3'))]

print(find_implications([([], 3), ([(1,"A")], 2), ([(1, "A"), (2, "B")], 2), ([(1, "B")], 1), ([(1, "B"), (2, "D")], 1), ([(2,"B")], 2), ([(2, "D")], 1)], 2))
# [(3.0, [(2, 'D')], (1, 'B')), (3.0, [(1, 'B')], (2, 'D'))]

print(find_implications([([], 3), ([(1,"A")], 2), ([(1, "A"), (2, "B")], 2), ([(1, "B")], 1), ([(1, "B"), (2, "D")], 1), ([(2,"B")], 2), ([(2, "D")], 1)], 20))
# [(3.0, [(2, 'D')], (1, 'B')), (3.0, [(1, 'B')], (2, 'D')), (2.0, [(2, 'B')], (1, 'A')), (2.0, [(1, 'A')], (2, 'B'))]
