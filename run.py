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
rows = (0, 1, 2, 3, 4, 5, 6, 7, 8), (9, 10, 11, 12, 13, 14, 15, 16, 17), (18, 19, 20, 21, 22, 23, 24, 25, 26), (27, 28, 29, 30, 31, 32, 33, 34, 35), (36, 37, 38, 39, 40, 41, 42, 43, 44), (45, 46, 47, 48, 49, 50, 51, 52, 53), (54, 55, 56, 57, 58, 59, 60, 61, 62), (63, 64, 65, 66, 67, 68, 69, 70, 71), (72, 73, 74, 75, 76, 77, 78, 79, 80)
cols = (0, 9, 18, 27, 36, 45, 54, 63, 72), (1, 10, 19, 28, 37, 46, 55, 64, 73), (2, 11, 20, 29, 38, 47, 56, 65, 74), (3, 12, 21, 30, 39, 48, 57, 66, 75), (4, 13, 22, 31, 40, 49, 58, 67, 76), (5, 14, 23, 32, 41, 50, 59, 68, 77), (6, 15, 24, 33, 42, 51, 60, 69, 78), (7, 16, 25, 34, 43, 52, 61, 70, 79), (8, 17, 26, 35, 44, 53, 62, 71, 80)
quads = (0, 1, 2, 9, 10, 11, 18, 19, 20), (3, 4, 5, 12, 13, 14, 21, 22, 23), (6, 7, 8, 15, 16, 17, 24, 25, 26), (27, 28, 29, 36, 37, 38, 45, 46, 47), (30, 31, 32, 39, 40, 41, 48, 49, 50), (33, 34, 35, 42, 43, 44, 51, 52, 53), (54, 55, 56, 63, 64, 65, 72, 73, 74), (57, 58, 59, 66, 67, 68, 75, 76, 77), (60, 61, 62, 69, 70, 71, 78, 79, 80)

def get_sudoku():
    """
    Get unfinished sudoku input from user.
    Input should be a string of 81 char 
      where 1,2,3,4,5,6,7,8,9 are filled values in the sudoku
      and any other char is a missing value in the sudoku.
    Returns list(81) -sudoku in a form of a list with the lenght of 81
      where int values 1,2,3,4,5,6,7,8,9 are filled values in the sudoku
      and a set(1,2,3,4,5,6,7,8,9) is inserted in place of any missing missing value in the sudoku.
    """
    print("Please input a sudoku as a string (no spaces) of 81 characters\n")
    print("Numbers 1,2,3,4,5,6,7,8,9 are the filled values and other symbols are missing values")
    input_sudoku = input("Sudoku: \n")

    print(len(input_sudoku))

    # Later delete
    input_sudoku = "ieb3k7s5h40a3n5f2l7g5m7e4n96f5ieb3k7s5h40a3n5f2l7g5m7e4n96f5heu635972b6492hdtvep5"

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

    #for s in sudoku:
        #print(s)

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
    if cell_content in {'1', '2', '3', '4', '5', '6', '7', '8', '9'}:
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

def fill_last_value(sudoku):
    """
    Replace any missing sudoku value with the last remaining value in it's set if the set has only one value left in it.
    Gets list(81)
    Returns list(81) and a boolean made_changes
    """

def fill_unique_value(sudoku):
    """
    Replace any missing sudoku value with one of the values in it's set 
      if that value doesn't repeat in any of the sets of missing values related to it (same row, column, quadrant)
      after all the filled values are cleared (clear_filled).
    Gets list(81)
    Returns list(81) and a boolean made_changes
    """

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

    print_sudoku(locations)

    """Change location to input"""

    input_cell_code = input('Please enter the XX code to the cell you want to change the value for: ')

    if input_cell_code in locations:
        cell_index = locations.index(input_cell_code)
        print(cell_index)
        input_new_cell_value = input(f'Please enter the new value for the cell\n {input_cell_code}: ')
        while len(input_new_cell_value) > 1:
            print("The value must be a nuber between 1 and 9 for filled cell or any one other character for unfilled cell!")
            print("Please try again!\n")
            
            input_new_cell_value = input(f'Please enter the new value for the cell\n {input_cell_code}: ')

        old_value = sudoku[cell_index]
        sudoku[cell_index] = input_new_cell_value
        print(f'{old_value} -> {sudoku[cell_index]}')

        print_sudoku(sudoku)

    else:
        replace_cell(sudoku)

    return locations

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
    sudoku = get_sudoku()

    #replace_grid = replace_cell(sudoku)

    print(sudoku)

handle_user()
