import gspread
from google.oauth2.service_account import Credentials

"""Reference: CI video tutorials and materials for enabling APIs to access a google sheet"""
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('sudoku_solver')

# solver_log = SHEET.worksheet('solver_log')

# data = solver_log.get_all_values()

# print(data)

"""
For a sudoku 9x9 each filled value must be unique in it's row, column and quadrant to be correct.
To make checking uniqueness easier the following 3 tuples of indeces in the same row, column and quadrant 
will be used in iterations.
"""
rows = ((0, 1, 2, 3, 4, 5, 6, 7, 8), (9, 10, 11, 12, 13, 14, 15, 16, 17), 
        (18, 19, 20, 21, 22, 23, 24, 25, 26), (27, 28, 29, 30, 31, 32, 33, 34, 35), 
        (36, 37, 38, 39, 40, 41, 42, 43, 44), (45, 46, 47, 48, 49, 50, 51, 52, 53), 
        (54, 55, 56, 57, 58, 59, 60, 61, 62), (63, 64, 65, 66, 67, 68, 69, 70, 71), 
        (72, 73, 74, 75, 76, 77, 78, 79, 80))
cols = ((0, 9, 18, 27, 36, 45, 54, 63, 72), (1, 10, 19, 28, 37, 46, 55, 64, 73), 
        (2, 11, 20, 29, 38, 47, 56, 65, 74), (3, 12, 21, 30, 39, 48, 57, 66, 75), 
        (4, 13, 22, 31, 40, 49, 58, 67, 76), (5, 14, 23, 32, 41, 50, 59, 68, 77), 
        (6, 15, 24, 33, 42, 51, 60, 69, 78), (7, 16, 25, 34, 43, 52, 61, 70, 79), 
        (8, 17, 26, 35, 44, 53, 62, 71, 80))
quads = ((0, 1, 2, 9, 10, 11, 18, 19, 20), (3, 4, 5, 12, 13, 14, 21, 22, 23), 
         (6, 7, 8, 15, 16, 17, 24, 25, 26), (27, 28, 29, 36, 37, 38, 45, 46, 47), 
         (30, 31, 32, 39, 40, 41, 48, 49, 50), (33, 34, 35, 42, 43, 44, 51, 52, 53), 
         (54, 55, 56, 63, 64, 65, 72, 73, 74), (57, 58, 59, 66, 67, 68, 75, 76, 77), 
         (60, 61, 62, 69, 70, 71, 78, 79, 80))
relatives = (rows, cols, quads)

"""
The index of each cell_relative is the same as the index in the sudoku so indeces can be used for both at the same time when iterating.
Coding was used to help generate the cell_relatives and then the cell index itself was removed manually from each line.
"""
cell_relatives = (
(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 27, 36, 45, 54, 63, 72), 
(0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 28, 37, 46, 55, 64, 73), 
(0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 29, 38, 47, 56, 65, 74), 
(0, 1, 2, 4, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 30, 39, 48, 57, 66, 75), 
(0, 1, 2, 3, 5, 6, 7, 8, 12, 13, 14, 21, 22, 23, 31, 40, 49, 58, 67, 76), 
(0, 1, 2, 3, 4, 6, 7, 8, 12, 13, 14, 21, 22, 23, 32, 41, 50, 59, 68, 77), 
(0, 1, 2, 3, 4, 5, 7, 8, 15, 16, 17, 24, 25, 26, 33, 42, 51, 60, 69, 78), 
(0, 1, 2, 3, 4, 5, 6, 8, 15, 16, 17, 24, 25, 26, 34, 43, 52, 61, 70, 79), 
(0, 1, 2, 3, 4, 5, 6, 7, 15, 16, 17, 24, 25, 26, 35, 44, 53, 62, 71, 80), 
(0, 1, 2, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 27, 36, 45, 54, 63, 72), 
(0, 1, 2, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 28, 37, 46, 55, 64, 73), 
(0, 1, 2, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 29, 38, 47, 56, 65, 74), 
(3, 4, 5, 9, 10, 11, 13, 14, 15, 16, 17, 21, 22, 23, 30, 39, 48, 57, 66, 75), 
(3, 4, 5, 9, 10, 11, 12, 14, 15, 16, 17, 21, 22, 23, 31, 40, 49, 58, 67, 76), 
(3, 4, 5, 9, 10, 11, 12, 13, 15, 16, 17, 21, 22, 23, 32, 41, 50, 59, 68, 77), 
(6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 24, 25, 26, 33, 42, 51, 60, 69, 78), 
(6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 24, 25, 26, 34, 43, 52, 61, 70, 79), 
(6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 24, 25, 26, 35, 44, 53, 62, 71, 80), 
(0, 1, 2, 9, 10, 11, 19, 20, 21, 22, 23, 24, 25, 26, 27, 36, 45, 54, 63, 72), 
(0, 1, 2, 9, 10, 11, 18, 20, 21, 22, 23, 24, 25, 26, 28, 37, 46, 55, 64, 73), 
(0, 1, 2, 9, 10, 11, 18, 19, 21, 22, 23, 24, 25, 26, 29, 38, 47, 56, 65, 74), 
(3, 4, 5, 12, 13, 14, 18, 19, 20, 22, 23, 24, 25, 26, 30, 39, 48, 57, 66, 75), 
(3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 23, 24, 25, 26, 31, 40, 49, 58, 67, 76), 
(3, 4, 5, 12, 13, 14, 18, 19, 20, 21, 22, 24, 25, 26, 32, 41, 50, 59, 68, 77), 
(6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 33, 42, 51, 60, 69, 78), 
(6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 34, 43, 52, 61, 70, 79), 
(6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 35, 44, 53, 62, 71, 80), 
(0, 9, 18, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 54, 63, 72), 
(1, 10, 19, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 55, 64, 73), 
(2, 11, 20, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 45, 46, 47, 56, 65, 74), 
(3, 12, 21, 27, 28, 29, 31, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 57, 66, 75), 
(4, 13, 22, 27, 28, 29, 30, 32, 33, 34, 35, 39, 40, 41, 48, 49, 50, 58, 67, 76), 
(5, 14, 23, 27, 28, 29, 30, 31, 33, 34, 35, 39, 40, 41, 48, 49, 50, 59, 68, 77), 
(6, 15, 24, 27, 28, 29, 30, 31, 32, 34, 35, 42, 43, 44, 51, 52, 53, 60, 69, 78), 
(7, 16, 25, 27, 28, 29, 30, 31, 32, 33, 35, 42, 43, 44, 51, 52, 53, 61, 70, 79), 
(8, 17, 26, 27, 28, 29, 30, 31, 32, 33, 34, 42, 43, 44, 51, 52, 53, 62, 71, 80), 
(0, 9, 18, 27, 28, 29, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 54, 63, 72), 
(1, 10, 19, 27, 28, 29, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 55, 64, 73), 
(2, 11, 20, 27, 28, 29, 36, 37, 39, 40, 41, 42, 43, 44, 45, 46, 47, 56, 65, 74), 
(3, 12, 21, 30, 31, 32, 36, 37, 38, 40, 41, 42, 43, 44, 48, 49, 50, 57, 66, 75), 
(4, 13, 22, 30, 31, 32, 36, 37, 38, 39, 41, 42, 43, 44, 48, 49, 50, 58, 67, 76), 
(5, 14, 23, 30, 31, 32, 36, 37, 38, 39, 40, 42, 43, 44, 48, 49, 50, 59, 68, 77), 
(6, 15, 24, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 51, 52, 53, 60, 69, 78), 
(7, 16, 25, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 51, 52, 53, 61, 70, 79), 
(8, 17, 26, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 51, 52, 53, 62, 71, 80), 
(0, 9, 18, 27, 28, 29, 36, 37, 38, 46, 47, 48, 49, 50, 51, 52, 53, 54, 63, 72), 
(1, 10, 19, 27, 28, 29, 36, 37, 38, 45, 47, 48, 49, 50, 51, 52, 53, 55, 64, 73), 
(2, 11, 20, 27, 28, 29, 36, 37, 38, 45, 46, 48, 49, 50, 51, 52, 53, 56, 65, 74), 
(3, 12, 21, 30, 31, 32, 39, 40, 41, 45, 46, 47, 49, 50, 51, 52, 53, 57, 66, 75), 
(4, 13, 22, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 50, 51, 52, 53, 58, 67, 76), 
(5, 14, 23, 30, 31, 32, 39, 40, 41, 45, 46, 47, 48, 49, 51, 52, 53, 59, 68, 77), 
(6, 15, 24, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53, 60, 69, 78), 
(7, 16, 25, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 61, 70, 79), 
(8, 17, 26, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 62, 71, 80), 
(0, 9, 18, 27, 36, 45, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74), 
(1, 10, 19, 28, 37, 46, 54, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74), 
(2, 11, 20, 29, 38, 47, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64, 65, 72, 73, 74), 
(3, 12, 21, 30, 39, 48, 54, 55, 56, 58, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77), 
(4, 13, 22, 31, 40, 49, 54, 55, 56, 57, 59, 60, 61, 62, 66, 67, 68, 75, 76, 77), 
(5, 14, 23, 32, 41, 50, 54, 55, 56, 57, 58, 60, 61, 62, 66, 67, 68, 75, 76, 77), 
(6, 15, 24, 33, 42, 51, 54, 55, 56, 57, 58, 59, 61, 62, 69, 70, 71, 78, 79, 80), 
(7, 16, 25, 34, 43, 52, 54, 55, 56, 57, 58, 59, 60, 62, 69, 70, 71, 78, 79, 80), 
(8, 17, 26, 35, 44, 53, 54, 55, 56, 57, 58, 59, 60, 61, 69, 70, 71, 78, 79, 80), 
(0, 9, 18, 27, 36, 45, 54, 55, 56, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74), 
(1, 10, 19, 28, 37, 46, 54, 55, 56, 63, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74), 
(2, 11, 20, 29, 38, 47, 54, 55, 56, 63, 64, 66, 67, 68, 69, 70, 71, 72, 73, 74), 
(3, 12, 21, 30, 39, 48, 57, 58, 59, 63, 64, 65, 67, 68, 69, 70, 71, 75, 76, 77), 
(4, 13, 22, 31, 40, 49, 57, 58, 59, 63, 64, 65, 66, 68, 69, 70, 71, 75, 76, 77), 
(5, 14, 23, 32, 41, 50, 57, 58, 59, 63, 64, 65, 66, 67, 69, 70, 71, 75, 76, 77), 
(6, 15, 24, 33, 42, 51, 60, 61, 62, 63, 64, 65, 66, 67, 68, 70, 71, 78, 79, 80), 
(7, 16, 25, 34, 43, 52, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 71, 78, 79, 80), 
(8, 17, 26, 35, 44, 53, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 78, 79, 80), 
(0, 9, 18, 27, 36, 45, 54, 55, 56, 63, 64, 65, 73, 74, 75, 76, 77, 78, 79, 80), 
(1, 10, 19, 28, 37, 46, 54, 55, 56, 63, 64, 65, 72, 74, 75, 76, 77, 78, 79, 80), 
(2, 11, 20, 29, 38, 47, 54, 55, 56, 63, 64, 65, 72, 73, 75, 76, 77, 78, 79, 80), 
(3, 12, 21, 30, 39, 48, 57, 58, 59, 66, 67, 68, 72, 73, 74, 76, 77, 78, 79, 80), 
(4, 13, 22, 31, 40, 49, 57, 58, 59, 66, 67, 68, 72, 73, 74, 75, 77, 78, 79, 80), 
(5, 14, 23, 32, 41, 50, 57, 58, 59, 66, 67, 68, 72, 73, 74, 75, 76, 78, 79, 80), 
(6, 15, 24, 33, 42, 51, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 79, 80), 
(7, 16, 25, 34, 43, 52, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 80), 
(8, 17, 26, 35, 44, 53, 60, 61, 62, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79))

def get_sudoku():
    """
    Get unfinished sudoku input from user and make changes necessary for the solving of it.
    Input should be a string of 81 char 
      where 1,2,3,4,5,6,7,8,9 are filled values in the sudoku
      and any other char is a missing value in the sudoku.
    Returns list(81) -sudoku in a form of a list with the lenght of 81
      where int values 1,2,3,4,5,6,7,8,9 are filled values in the sudoku
      and a set(1,2,3,4,5,6,7,8,9) is inserted in place of any missing missing value in the sudoku.
    """
    print("Please input a sudoku as a string (no spaces) of 81 characters!\n")
    print("Numbers 1,2,3,4,5,6,7,8,9 are the filled values and any other symbols are missing values.")
    input_sudoku = input("Sudoku: \n")

    # Later delete
    # random/error in sudoku
    # input_sudoku = "ieb3k7s5h40a3n5f2l7g5m7e4n96f5ieb3k7s5h40a3n5f2l7g5m7e4n96f5heu635972b6492hdtvep5"
    # solvable
    input_sudoku = "1f6gft8h5dddr1hhhh3kk8h5dd7gg93h16ggt6hhhhh9rrr49h25dd5kk6h3cc9kkkk5jjjj6t7ddd2w3"
    # unique
    # input_sudoku = "1263498h5dddr1hhhh3kk8h5dd7gg93h16ggt6hhhhh9rrr49h25dd5kk6h3cc9kkkk5jjjj6t7ddd2w3"

    if len(input_sudoku) == 81:
        print_sudoku(input_sudoku)
    else:
        print("\n\nInput is not a string of 81 charachters!")
        print("Try again...\n")
        get_sudoku()

    sudoku = []
    for s in input_sudoku:
        if s in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            sudoku.append(int(s))
        else:
            sudoku.append({1, 2, 3, 4, 5, 6, 7, 8, 9})

    return sudoku

def is_input_valid(sudoku):
    """
    Check if the input has enough filled values to try solving it
    Gets list(81)
    Returns a boolean
    """

def display_unfilled_cell(cell_content):
    """
    Display unfilled cell as -
    Gets cell content
    Returns cell content if filled or - if unfilled
    """
    cell_content = str(cell_content)
    if len(cell_content) == 1 and cell_content in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        return cell_content
    elif len(cell_content) == 2:
        # len is 2 only when a sudoku code XX map is generated
        return cell_content
    else:
        return '-'

def print_sudoku(sudoku):
    """
    Print the sudoku that is given to the function.
    Gets list(81)
    Values are printed as 9 x 9
      where filled values are numbers
      and missing values are '-'.
    Returns None.
    """

    """
    Reference for using enumerate():
    https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
    Reference for printing without newline:
    https://stackoverflow.com/questions/493386/how-to-print-without-a-newline-or-space
    """
    for i, value in enumerate(sudoku):
        value = display_unfilled_cell(sudoku[i])
        if ((i+1) % 27) == 0:
            print(value, '\n')
        elif ((i+1) % 9) == 0:
            print(value, end='\n')
        elif ((i+1) % 3) == 0:
            print(value, end='   ')
        else:
            print(value, end=' ') 
    print('\n')

def clear_filled(sudoku):
    """
    Clear already filled values from related sets for missing values.
    If the value is in the same row, column of quadrant it gets popped from the set.
    Gets list(81)
    Returns list(81) and a boolean made_changes
    """

    made_changes = False
    ind = 0
    for value in sudoku:
        if value not in range(1, 10):
            
            filled_values = {sudoku[rel_ind] for rels in relatives for relative_field in rels if ind in relative_field for rel_ind in relative_field if sudoku[rel_ind] in range(1, 10)}
            """
            filled_values = set()
            for rels in relatives: # rows, cols, quads
                for relative_field in rels: # like each row in rows
                    if ind in relative_field: # if the index is in the row
                        for rel_ind in relative_field: # for each value in row
                            if sudoku[rel_ind] in range(1, 10): # if it is filled
                                filled_values.add(sudoku[rel_ind])
            """
            if value != filled_values:
                value.difference_update(filled_values)
                # print(ind, value)
                made_changes = True
        ind += 1
    return sudoku, made_changes

def fill_last_value(sudoku):
    """
    Replace any missing sudoku value with the last remaining value in it's set if the set has only one value left in it.
    Gets list(81)
    Returns list(81) and a boolean made_changes
    """
    made_changes = False
    ind = 0
    for cell in sudoku:
        if cell not in range(1, 10):
            if len(cell) == 1:
                sudoku[ind] = cell.pop()
                made_changes = True
        ind += 1

    return sudoku, made_changes

def fill_unique_value(sudoku):
    """
    Replace any missing sudoku value with one of the values in it's set 
      if that value doesn't repeat in any of the sets of missing values related to it (same row, column, quadrant)
      after all the filled values are cleared (clear_filled).
    Gets list(81)
    Returns list(81) and a boolean made_changes
    """
    made_changes = False
    ind = 0
    for value in sudoku:
        print(f"ind: {ind}")
        if type(value) is set:
            for rels in relatives: # rows, cols, quads
                present_rel_values = {} # dictionary will be easier to iterate later
                for relative_field in rels: # like each row in rows
                    if ind in relative_field: # if the index is in the row
                        for rel_ind in relative_field: # for each value in row
                            present_rel_values[str(rel_ind)] = sudoku[rel_ind]
                present_rel_values_list = list(present_rel_values.values())
                present_rel_keys_list = list(present_rel_values.keys())
            
                #print(present_rel_values_list)
                #print(list(present_rel_values.keys()))

                i = 0
                for rel_val in present_rel_values_list:
                    if rel_val in range(1, 10): # filled value
                        pass
                    i += 1
        ind += 1

        sudoku, made_changes = fill_last_value(sudoku)
    return sudoku, made_changes

def is_valid(sudoku):
    """
    Check if all values are unique in the same row, column and quadrant.
    Gets list(81)
    Returns a boolean
    """

def is_solved(sudoku):
    """
    Check if the sudoku list(81) 
      is solved (meaning has only int values between 1 and 9) and 
      is valid (unique values in each row, column and quadrant).
    Gets list(81)
    Returns a boolean
    """

def replace_cell(sudoku):
    """
    Replace the content of one cell.
    Gets list(81)
    Returns list(81) and a boolean made_changes
    """

    """Create locations map"""
    locations = []
    for ind in range(81):
        if ind < 10:
            locations.append('0' + str(ind))
        else:
            locations.append(str(ind))

    print("This is the code (XX) map for the sudoku: \n")
    print_sudoku(locations)

    """Replace value of location with input"""
    made_changes = True

    input_cell_code = input('Please enter the XX code to the cell you want to change the value for: ')

    if input_cell_code in locations:
        cell_index = locations.index(input_cell_code)
        old_value = sudoku[cell_index]
        print(f"Current {input_cell_code} value is: {old_value}")
        input_new_cell_value = input(f'Please enter the new value for the cell\n {input_cell_code}: ')
        while len(input_new_cell_value) > 1:
            print("The value must be a number between 1 and 9 for filled cell or any one other character for unfilled cell!")
            print("Please try again!\n")
            
            input_new_cell_value = input(f'Please enter the new value for the cell\n {input_cell_code}: ')

        sudoku[cell_index] = int(input_new_cell_value)
        if str(old_value) == str(sudoku[cell_index]):
            print(f"You entered the same value: {old_value}")
            made_changes = False
        else: 
            print(f'{old_value} -> {sudoku[cell_index]}')

        print("Your sudoku currently: \n")
        print_sudoku(sudoku)

    else:
        replace_cell(sudoku)

    return [sudoku, made_changes]

def handle_unsolvable(sudoku):
    """
    Handle a sudoku the program cannot finish solving.
    Gets list(81)
    Returns None
    """

def handle_user():
    """
    Handle interactions with the user and call functions to solve the sudoku.
    """
    rrr = []
    for i in range(81):
        r_set = set()
        if i == 0:
            r_set = list(rows[0])
        elif i / 9 < 1:
            r_set = list(rows[0])
            #print(i, ' - 0')
        elif i / 9 < 2:
            r_set = list(rows[1])
            #print(i, ' - 1')
        elif i / 9 < 3:
            r_set = list(rows[2])
            #print(i, ' - 2')
        elif i / 9 < 4:
            r_set = list(rows[3])
            #print(i, ' - 3')
        elif i / 9 < 5:
            r_set = list(rows[4])
            #print(i, ' - 4')
        elif i / 9 < 6:
            r_set = list(rows[5])
            #print(i, ' - 5')
        elif i / 9 < 7:
            r_set = list(rows[6])
            #print(i, ' - 6')
        elif i / 9 < 8:
            r_set = list(rows[7])
            #print(i, ' - 7')
        elif i / 9 < 9:
            r_set = list(rows[8])
            #print(i, ' - 8')
        rrr.append(r_set)
        #print(type(rrr[i]))
    for i in range(81):
        c_set = set()
        if i == 0:
            c_set = list(cols[0])
        elif i % 9 < 1:
            c_set = list(cols[0])
            print(i, ' - 0')
        elif i % 9 < 2:
            c_set = list(cols[1])
            print(i, ' - 1')
        elif i % 9 < 3:
            c_set = list(cols[2])
            print(i, ' - 2')
        elif i % 9 < 4:
            c_set = list(cols[3])
            print(i, ' - 3')
        elif i % 9 < 5:
            c_set = list(cols[4])
            print(i, ' - 4')
        elif i % 9 < 6:
            c_set = list(cols[5])
            print(i, ' - 5')
        elif i % 9 < 7:
            c_set = list(cols[6])
            print(i, ' - 6')
        elif i % 9 < 8:
            c_set = list(cols[7])
            print(i, ' - 7')
        elif i % 9 < 9:
            c_set = list(cols[8])
            print(i, ' - 8')
        #rrr.append(c_set)
        for cc in c_set:
            rrr[i].append(cc)
    for i in range(81):
        q_set = set()
        if i in quads[0]:
            q_set = list(quads[0])
            print(i, ' - 0')
        elif i in quads[1]:
            q_set = list(quads[1])
            print(i, ' - 1')
        elif i in quads[2]:
            q_set = list(quads[2])
            print(i, ' - 2')
        elif i in quads[3]:
            q_set = list(quads[3])
            print(i, ' - 3')
        elif i in quads[4]:
            q_set = list(quads[4])
            print(i, ' - 4')
        elif i in quads[5]:
            q_set = list(quads[5])
            print(i, ' - 5')
        elif i in quads[6]:
            q_set = list(quads[6])
            print(i, ' - 6')
        elif i in quads[7]:
            q_set = list(quads[7])
            print(i, ' - 7')
        elif i in quads[8]:
            q_set = list(quads[8])
            print(i, ' - 8')
        #rrr.append(c_set)
        for qq in q_set:
            rrr[i].append(qq)
    print("cell_relatives = (")
    ind = 0
    for i in rrr:
        i.remove(i.index(ind))
        i = tuple(set(i))
        ind += 1
        
        print(i, ", ", sep = "")
    print(")")

    quit()
    print("Hello friend!")
    print("This is your Sudoku Solver!")
    sudoku = get_sudoku()

    print("Do you want to make any changes to it?")
    print("\n\n(Yes) press 'y' !\n(No. Let's continue!) press any key besides 'y' and 'q' ! \n(Quit) press'q' !\n")
    to_change_smth = input("Make changes: ")
    if to_change_smth.lower() == 'y':
        while to_change_smth.lower() == 'y':
            replace_grid = replace_cell(sudoku)
            to_change_smth = input("To make more changes press 'y': ")
    elif to_change_smth.lower() == 'q':
        print("Goodbye!")
        quit()

    # to keep record of the input sudoku
    sudoku_at_the_start = sudoku

    print("Do you want this program to try to solve it?")
    print("\n(Yes) press any key besides 'n' and 'q' ! \n(No) press 'n' ! \n(Quit) press 'q' !")
    to_solve = input('Solve sudoku: ')
    if to_solve.lower() == 'n':
        print("Ok. Not solving sudoku!")
        # hint the cell instead?
        print("Goodbye!")
        quit()
    elif to_solve.lower() == 'q':
        print("Goodbye!")
        quit()

    made_changes = True
    i=0
    while made_changes and i<100:
        sudoku, made_changes = clear_filled(sudoku)
        sudoku, made_changes = fill_last_value(sudoku)
        sudoku, made_changes = fill_unique_value(sudoku)
        i += 1

    print(made_changes)

    #for 'unsolved after solving' sudoku ofer to make a change to cells again

    print_sudoku(sudoku)

handle_user()
