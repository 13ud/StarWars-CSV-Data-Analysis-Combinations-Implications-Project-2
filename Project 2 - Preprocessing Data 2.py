def rep_number_quantiles(numlist, k):
    """ Inputs:
    numlist - list of specific column number values found in sheet
    k - number of quantiles to create for numbers present in relevant column

    Helper function that initialises quartile start and end boundaries,
    and calculates initial jth interval value, rounding it to allow
    indexing of list.This while loop block continues UNTIL the quartile end
    updates to or greater than the length of the list of column numbers,
    returning an updated numlist filled with the representing numbers. """

    quartile_start, quartile_end = 0, 0
    j = round(len(numlist) / (2 * k))
    while quartile_end < len(numlist):
        quartile_end += (len(numlist)) / k

        # Max() makes sure the index value does not go below 0
        # Calculates the representative number for the jth interval, and
        # Assigns the value to all the numbers within the quantile range
        max_value = max(j - 1, 0)
        rep_number = numlist[int(max_value)][0]
        minvalue = min(len(numlist), round(quartile_end))
        for i in range(quartile_start, minvalue):
            numlist[i][0] = rep_number

        # Updates the start boundary of the quartile, and the j interval
        quartile_start = minvalue
        j += len(numlist) / k

    return numlist


def preprocess(sheet, k):
    """ Inputs:
    sheet - a data sheet, consisting of a list of data rows of string values
    k - number of quantiles / maximum number of unique values after processing
    Returns a sheet that has been modified by replacing all proper names with
    their first letters, removing all characters coming after a number and
    converting the list of numbers to k or less unique representative numbers
    """

    # Initialise lists, which will store information OR lists of column info
    numindexeslist = []
    listofnuminfolists = []
    listofjustnumberlists = []

    # Goes through each string value in each row
    for row in sheet:
        for string in row:

            # IF the string contains a number in the beginning,
            # It updates this value with JUST the number by splitting string
            # and returning the first element of the split list.
            # It also remembers this index by adding to a list, used later
            if string[0] in '-0123456789':
                index = row.index(string)
                row[index] = string.split()[0]
                numindexeslist.append(index)


            # Replaces all proper names with JUST their first letters,
            # where proper letter is a string with UPPER then LOWERCASE letter
            elif string[0].isupper() and string.upper() != string:
                index = row.index(string)
                row[index] = string[0]

    # Removes any duplicate indexes in the list, STILL leaving it as a list
    numindexeslist = list(set(numindexeslist))

    # Goes through the elements of the stored indexes list where numbers were
    # present, and initialises new list AFTER every index is gone through.
    for nindex in numindexeslist:
        newinfolist = []
        just_numberslist = []

        # Goes through the elements of each row, checking the indexes where
        # numbers are present, and stores a tuple of the element's information.
        # Specifically formatted as: (element, row number, index number in row)
        # FOR EACH COLUMN, a list is then appended to the listofnumberlists.
        for row in sheet:
            rowindex = row.index(row[nindex])
            if row[nindex][0] in '-0123456789':
                newinfolist.append([row[nindex], sheet.index(row), rowindex])
                just_numberslist.append(row[nindex])
        listofnuminfolists.append(sorted(newinfolist))
        listofjustnumberlists.append(list(set(just_numberslist)))

    # Goes through the number and its index info in the 'listofnumberlists',
    # checking if the number of unique values is greater than 'k'.
    # IF NOT, the block will directly go to the next list of column values
    for listindex in range(len(listofnuminfolists)):
        numlist = listofnuminfolists[listindex]
        justnumlist = listofjustnumberlists[listindex]
        if len(justnumlist) <= k:
            continue

        # Helper function updates list with representative numbers in quartiles
        updatednumlist = rep_number_quantiles(numlist, k)

        # Goes through the indexinfo within the lists of each number in the
        # numlist, and directly reassigns the value to the sheet.
        # IF the original value is NOT a number as defined in the question,
        # then it will NOT be updated (e.x. if "NA", etc)
        for indexinfo in updatednumlist:
            if str(sheet[indexinfo[1]][indexinfo[2]])[0] in '-0123456789':
                sheet[indexinfo[1]][indexinfo[2]] = str(indexinfo[0])

    return sheet


print(preprocess(
[['Earth',  '10', 'blue', '100.0 years'],
 ['Mars',   '11', 'red',  '250.0 years'],
 ['Venus',  '12', 'yellow', '300.0 years'],
 ['Pluto',  '13', 'white', '270.0 months'],
 ['Mercury','14', 'gray',   '300.0 days'],
 ['Jupiter', '15', 'white, orange, brown and red', '280.0 days']],  3
))

# [['E', '10', 'blue', '100.0'], ['M', '10', 'red', '100.0'], ['V', '12', 'yellow', '300.0'], ['P', '12', 'white', '270.0'], ['M', '14', 'gray', '300.0'], ['J', '14', 'white, orange, brown and red', '270.0']]

print(preprocess([['US','1'],['The U.S.','2'],['the U.S.','3'],['1. The U.S.','NA'],['2. the U.S.','7']], 2))
# [['US', '1'], ['T', '1'], ['the U.S.', '3'], ['1.', 'NA'], ['2.', '3']]

print(preprocess([['-1 is minus 1','1 is one'],['-2 is minus 2','1 is one'],['-3 is minus 3','1 is one'],['-4 is minus 4','1 is one'],['-5 is minus 5','1 is one'],['-6 is minus 6','5 is five']], 2))
# [['-2', '1'], ['-2', '1'], ['-2', '1'], ['-5', '1'], ['-5', '1'], ['-5', '5']]







