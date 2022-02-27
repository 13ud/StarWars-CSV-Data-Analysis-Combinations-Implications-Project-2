def join(headers1, sheet1, field1, headers2, sheet2, field2):
    """Input:
    headers1 - list of column headers from the first data sheet
    sheet1 - first data sheet contents, which is a list of rows or iter()
    where each row is a list of column values
    field1 - field name to join in the first datasheet
    headers2 - list of column headers from the second data sheet
    sheet2 - second data sheet contents or iter()
    field 2 - field name to join in the second datasheet

    Function merges lines from two files when the values in the field columns
    are the same. (the field column will then only appear once, not repeated).
    Can work for iterators as well as traditional list format for sheets """

    # Find the row index of the designated field columns, and remove the
    # repeating header in the headers2 list so as not to repeat the same column
    # After this, combine the two headers lists together to form the final
    # 'joined' headerslist for the final sheet
    index1 = headers1.index(field1)
    index2 = headers2.index(field2)
    headers2.pop(index2)
    result_header = headers1 + headers2

    # Convert the sheets into tuple to account for the possibility of
    # sheet input being an iterator, whilst not converting explicitly to a list
    sheet1 = tuple(sheet1)
    sheet2 = tuple(sheet2)

    # initialise final sheet part of output tuple, and magic number 'i'
    # to go through ALL of the sheet1 elements without using a second FOR loop
    # Then create an iterator of sheet1 using iter() function
    result_sheet = []
    sheet1index = 0
    rowiter1 = iter(sheet1)

    # While loop makes sure to go through ALL the values in the sheet1 iterator
    # WHEN StopIteration error shows up, it will be caught and pass this block
    while sheet1index < len(sheet1):
        try:
            rows1 = next(rowiter1)
            rowiter2 = iter(sheet2)
        except StopIteration:
            pass

        # Only for loop goes through ALL the values in the sheet2 iterator
        # paired with one sheet1 iterator value BEFORE sheet1 iterator goes to
        # next value. This block checks if the value in the designated field
        # columns are the same, and IF SO then joins the two rows together
        # WHEN StopIteration error shows up, it will pass this block
        for sheet2index in range(len(sheet2)):
            try:
                rows2 = next(rowiter2)
                if rows1[index1] == rows2[index2]:
                    rows2.pop(index2)
                    result_sheet.append(rows1 + rows2)
            except StopIteration:
                pass

        # After going through each pairing of a sheet1 value with all sheet2,
        # OR StopIteration error is caught and block is passed, the variable
        # sheet1index is increased by 1 to go to next sheet1 value pairings.
        sheet1index += 1

    return result_header, result_sheet



print(join(
["name","classification","language","homeworld"],
[["Hutt",     "gastropod","Huttese","Nal Hutta"],
 ["Sullustan","mammal",   "Sullutese","Sullust"]],
"homeworld",
["name",  "climate","gravity"],
[["Alderaan", "temperate", "1 standard"],
 ["Nal Hutta","temperate", "1 standard"],
 ["Sullust",  "superheted","1"]],
"name"))     # ---- end of function call ----

print(join(
["height","shape"],
[["200", "triangle"], ["100", "square"], ["450", "rectangle"], ["2", "something"]],
"shape",
["Name", "Num Sides", "Equal Sides"],
[["triangle", "3", "Y"], ["diamond", "4", "Y"], ["rectangle", "4", "Y"], ["square", "4", "Y"]],
"Name"))      # ---- end of function call ----


#check whether it works with iterators
print(join(['var'], iter([['Y'], ['X']]), 'var', ['var1', 'num'], iter([['X', '1'], ['Y', '2']]), 'var1'))
