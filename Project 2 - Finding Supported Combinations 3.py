from collections import defaultdict as d_dict
from itertools import combinations


def all_in(combinations, sequence):
    """ Helper function that creates combinations of valid (feature, value)
    tuples, in order to test it against the minimum support level later on """
    for element in combinations:
        if element not in sequence:
            return False
    return True


def get_supported_combinations(sheet, min_support):
    """ Inputs:
    sheet - a data sheet, consisting of a list of data rows of string values
    min_support - min. support for a combination to be included in output list

    Returns all combinations of (feature, value) which has a support above the
    given threshold input 'min_support' """

    # Initialise and create the dicts, total number of rows in sheet and
    # the lists which will be added/appended to respectively
    frequency_dict = d_dict(int)
    tuple_dict = d_dict(int)
    total_no_rows = len(sheet)
    listofcombs = []
    validlist = []
    validfeatures = []

    # Runs through the data in each row of the sheet
    # IF data is the special "NA" string, goes directly to next data, no change
    for rows in sheet:
        for data in rows:
            if data == "NA":
                continue


            # Otherwise, the frequency of the data is counted into a dict
            # and the tuple (row index, data) is stored in a separate dict too
            # These tuples are then stored in a list, where only unique tuples
            # in a sorted order are left in the list after using set method.
            else:
                frequency_dict[data] += 1
                tuple_dict[data] = (rows.index(data), data)
                listofcombs.append(tuple_dict[data])
                listofcombs = sorted(list(set(listofcombs)))

    # Iterates through each (list index, feature) tuple, and checks if its
    # Support fits within the minimum support range.
    # IF SO, the feature and its frequency is appended to the validlist
    # And JUST the feature is added to the validfeatures list
    for featuretuple in listofcombs:
        if frequency_dict[featuretuple[1]] / total_no_rows >= min_support:
            validlist.append(([featuretuple], frequency_dict[featuretuple[1]]))
            validfeatures.append(featuretuple[1])

    # Running through each row of the sheet and for combinations of min. size 2
    # the HELPER function 'all_in' is used to check if the combinations
    # are present within the rows. This is done for ALL feature combinations
    # If TRUE, the combination frequency is increased by 1
    for size in range(2, len(validfeatures) + 1):
        for comb in combinations(validfeatures, size):
            for rows in sheet:
                if all_in(comb, rows):
                    frequency_dict[comb] += 1

                    # Checks if the support of a combination is equal to or greater
            # than the min_support input.
            # IF SO, the combination of the tuples (row index, element)
            # are appended to the validlist, along with the comb. frequency
            if frequency_dict[comb] / total_no_rows >= min_support:
                combo = [tuple_dict[element] for element in comb]
                validlist.append((combo, frequency_dict[comb]))

                # After going through all the feature combinations of varying sizes,
    # the final validlist is sorted, and a tuple detailing the total_no_rows
    # is inserted at the start. This aligns with the question's set conditions
    validlist.sort()
    validlist.insert(0, ([], total_no_rows))
    return validlist


SHEET = [["small","blue","10"],["medium","green","20"],["medium","blue","10"],["medium","blue","30"]]

print(get_supported_combinations(SHEET,.8))
# [([], 4)]

print(get_supported_combinations(SHEET,.7))
# [([], 4), ([(0, 'medium')], 3), ([(1, 'blue')], 3)]

print(get_supported_combinations(SHEET,.5))
# [([], 4), ([(0, 'medium')], 3), ([(0, 'medium'), (1, 'blue')], 2), ([(1, 'blue')], 3), ([(1, 'blue'), (2, '10')], 2), ([(2, '10')], 2)]

print(get_supported_combinations(SHEET,.1))
# [([], 4), ([(0, 'medium')], 3), ([(0, 'medium'), (1, 'blue')], 2), ([(0, 'medium'), (1, 'blue'), (2, '10')], 1), ([(0, 'medium'), (1, 'blue'), (2, '30')], 1), ([(0, 'medium'), (1, 'green')], 1), ([(0, 'medium'), (1, 'green'), (2, '20')], 1), ([(0, 'medium'), (2, '10')], 1), ([(0, 'medium'), (2, '20')], 1), ([(0, 'medium'), (2, '30')], 1), ([(0, 'small')], 1), ([(0, 'small'), (1, 'blue')], 1), ([(0, 'small'), (1, 'blue'), (2, '10')], 1), ([(0, 'small'), (2, '10')], 1), ([(1, 'blue')], 3), ([(1, 'blue'), (2, '10')], 2), ([(1, 'blue'), (2, '30')], 1), ([(1, 'green')], 1), ([(1, 'green'), (2, '20')], 1), ([(2, '10')], 2), ([(2, '20')], 1), ([(2, '30')], 1)]

