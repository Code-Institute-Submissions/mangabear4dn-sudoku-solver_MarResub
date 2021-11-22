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

def print_sudoku(sudoku):
    """
    Print the sudoku that is given to the function.
    Gets list(81)
    Values are printed as 9 x 9
      where filled values are numbers
      and missing values are 'X'.
    Returns None.
    """

    """
    Reference for using enumerate():
    https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
    Reference for printing without newline:
    https://stackoverflow.com/questions/493386/how-to-print-without-a-newline-or-space
    """
    for i, value in enumerate(sudoku):
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

handle_user()
