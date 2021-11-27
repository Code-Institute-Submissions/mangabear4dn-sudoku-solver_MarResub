"""
This is module of sudoku solver.
"""
import time
"""
For a sudoku 9x9 each filled value must be unique
in it's row, column and quadrant to be correct.
To make checking uniqueness easier the following 3 tuples of indeces
in the same row, column and quadrant
will be used in iterations.
"""
rows = ((0, 1, 2, 3, 4, 5, 6, 7, 8),
        (9, 10, 11, 12, 13, 14, 15, 16, 17),
        (18, 19, 20, 21, 22, 23, 24, 25, 26),
        (27, 28, 29, 30, 31, 32, 33, 34, 35),
        (36, 37, 38, 39, 40, 41, 42, 43, 44),
        (45, 46, 47, 48, 49, 50, 51, 52, 53),
        (54, 55, 56, 57, 58, 59, 60, 61, 62),
        (63, 64, 65, 66, 67, 68, 69, 70, 71),
        (72, 73, 74, 75, 76, 77, 78, 79, 80))
cols = ((0, 9, 18, 27, 36, 45, 54, 63, 72),
        (1, 10, 19, 28, 37, 46, 55, 64, 73),
        (2, 11, 20, 29, 38, 47, 56, 65, 74),
        (3, 12, 21, 30, 39, 48, 57, 66, 75),
        (4, 13, 22, 31, 40, 49, 58, 67, 76),
        (5, 14, 23, 32, 41, 50, 59, 68, 77),
        (6, 15, 24, 33, 42, 51, 60, 69, 78),
        (7, 16, 25, 34, 43, 52, 61, 70, 79),
        (8, 17, 26, 35, 44, 53, 62, 71, 80))
quads = ((0, 1, 2, 9, 10, 11, 18, 19, 20),
         (3, 4, 5, 12, 13, 14, 21, 22, 23),
         (6, 7, 8, 15, 16, 17, 24, 25, 26),
         (27, 28, 29, 36, 37, 38, 45, 46, 47),
         (30, 31, 32, 39, 40, 41, 48, 49, 50),
         (33, 34, 35, 42, 43, 44, 51, 52, 53),
         (54, 55, 56, 63, 64, 65, 72, 73, 74),
         (57, 58, 59, 66, 67, 68, 75, 76, 77),
         (60, 61, 62, 69, 70, 71, 78, 79, 80))
relatives = (rows, cols, quads)
"""
The index of each cell_relative is the same as the index in the sudoku
so indeces can be used for both at the same time when iterating.
Coding was used to help generate the cell_relatives and
then the cell index itself was removed manually from each line.
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
    Get unfinished sudoku input from user and make changes necessary for
    the solving of it.
    Input should be a string of 81 char
      where 1,2,3,4,5,6,7,8,9 are filled values in the sudoku
      and any other char is a missing value in the sudoku.
    Returns list(81) -sudoku in a form of a list with the lenght of 81
      where int values 1,2,3,4,5,6,7,8,9 are filled values in the sudoku
      and a set(1,2,3,4,5,6,7,8,9) is inserted in place of any missing missing
      value in the sudoku.
    """
    print("Please input a sudoku as a string (no spaces) of 81 characters!\n")
    print("Numbers 1,2,3,4,5,6,7,8,9 are the filled values")
    print("and any other symbols are missing values.")
    input_sudoku = input("Sudoku: \n")

    if len(input_sudoku) < 1:
        print("No sudoku received!")
        print("Goodbye!")
        quit()

    # For testing
    # random/error in sudoku
    # input_sudoku = "ieb3k7s5h40a3n5f2l7g5m7e4n96f5ieb3k7s5h40a3n5f2l7g5m7e4n96f5heu635972b6492hdtvep5"
    # solvable
    # input_sudoku = "1f6gft8h5dddr1hhhh3kk8h5dd7gg93h16ggt6hhhhh9rrr49h25dd5kk6h3cc9kkkk5jjjj6t7ddd2w3"
    # unique
    # input_sudoku = "1263498h5dddr1hhhh3kk8h5dd7gg93h16ggt6hhhhh9rrr49h25dd5kk6h3cc9kkkk5jjjj6t7ddd2w3"
    # solved
    # input_sudoku = "176239845485716932392845167759381624261574398834962571548623719923157486617498253"
    # not enough int
    # input_sudoku = "1fegftrhhdddrghhhh3kkkhgdd7ggujhkyggtyhhhhh9rrrj9hj5ddlkkehtccjkkkkfjjjj6tlddd2w3"

    if len(input_sudoku) == 81:
        if is_input_valid(input_sudoku):
            print_sudoku(input_sudoku)
        else:
            print("\n\nInput doesn't have enough filled in values!")
            print("Try again...\n")
            get_sudoku()
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
    Check if the input has enough filled values to try solving it.
    Enetered sudoku should have at least 17 filled cells.
    Reference:
    https://www.quora.com/What-is-the-minimum-number-of-numbers-needed-on-a-standard-9x9-Sudoku-for-it-to-still-be-solvable
    Gets list(81)
    Returns a boolean
    """
    int_counter = 0
    for cell in sudoku:
        if cell in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
            int_counter += 1
    if int_counter > 16:
        return True
    else:
        return False


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
    Returns list(81)
    """
    ind = 0
    for value in sudoku:
        if value in range(1, 10):
            for i in cell_relatives[ind]:
                if sudoku[i] not in range(1, 10) and value in sudoku[i]:
                    sudoku[i].remove(value)
        ind += 1
    return sudoku


def fill_last_value(sudoku):
    """
    Replace any missing sudoku value with the last remaining value in it's set if the set has only one value left in it.
    Gets list(81)
    Returns list(81)
    """
    ind = 0
    for cell in sudoku:
        if cell not in range(1, 10):
            if len(cell) == 1:
                value = cell.copy().pop()
                if is_valid(sudoku, ind, value):
                    sudoku[ind] = cell.pop()
        ind += 1

    return sudoku


def fill_unique_value(sudoku):
    """
    Replace any missing sudoku value with one of the values in it's set
      if that value doesn't repeat in any of the sets of
      the missing values related to it (same row, column, quadrant),
      after all the filled values are cleared (clear_filled).
    Gets list(81)
    Returns list(81)
    """
    ind = 0
    for cell_group in cell_relatives:
        if sudoku[ind] not in range(1, 10):
            for related_range in relatives:
                # make a list of values possible in the range
                values = []
                for rel in related_range:
                    if ind in rel:
                        for cell in rel:
                            if sudoku[cell] not in range(1, 10):
                                for val in sudoku[cell]:
                                    values.append(val)
                # look for a unique value in the made list
                unique_values = []
                for val in values:
                    if values.count(val) == 1:
                        unique_values.append(val)
                # look for the location of unique value if any found and replace it
                if len(unique_values) > 0:
                    unique_value = unique_values[0]
                    valid_uniqueness = is_valid(sudoku, ind, unique_value)
                    if valid_uniqueness:
                        sudoku[ind] = unique_value
                        return sudoku
        ind += 1
    return sudoku


def is_valid(sudoku, ind, value):
    """
    Check if all values are unique in the same row, column and quadrant.
    Only function that prints full sudoku while solving is in progress.
    Gets list(81), index of cell and 1-9 value to validate for this cell
    Returns a boolean
    """
    for cell in cell_relatives[ind]:
        if sudoku[cell] == value:
            return False
    if ind < 10:
        print(f"\n0{ind} <- {value}")
    else:
        print(f"\n{ind} <- {value}")
    print_sudoku(sudoku)
    return True


def is_solved(sudoku):
    """
    Check if the sudoku list(81)
      is solved (meaning has only int values between 1 and 9) and
      is valid (unique values in each row, column and quadrant).
    Gets list(81)
    Returns a boolean
    """
    for cell in sudoku:
        if cell not in range(1, 10):
            return False
    for cell_group in cell_relatives:
        cell_set = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        cell_filled_with = []
        for cell in cell_group:
            cell_filled_with.append(sudoku[cell])
        if cell_set.sort() != cell_filled_with.sort():
            return False
    return True


def make_locations_map():
    """
    Create a visual map to use when asking user about a specific cell
    Return list with locations names
    """
    locations = []
    for ind in range(81):
        if ind < 10:
            locations.append('0' + str(ind))
        else:
            locations.append(str(ind))

    print("This is the code (XX) map for the sudoku: \n")
    print_sudoku(locations)
    return locations


def replace_cell(sudoku):
    """
    Replace the content of one cell.
    Gets list(81)
    Returns list(81)
    """

    """Create locations map"""
    locations = make_locations_map()

    """Replace value of location with input"""
    input_cell_code = input('Please enter the XX code to the cell you want to change the value for: \n')

    if input_cell_code in locations:
        cell_index = locations.index(input_cell_code)
        old_value = sudoku[cell_index]
        print(f"Current {input_cell_code} value is: {old_value}")
        input_new_cell_value = input(f'Please enter the new value for the cell\n {input_cell_code}: \n')
        while len(input_new_cell_value) > 1:
            print("The value must be a number between 1 and 9 for filled cell or any one other character for unfilled cell!")
            print("Please try again!\n")
            input_new_cell_value = input(f"Please enter the new value for the cell\n {input_cell_code}: \n")
        if input_new_cell_value not in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
            input_new_cell_value = (1, 2, 3, 4, 5, 6, 7, 8, 9)
        else:
            sudoku[cell_index] = int(input_new_cell_value)
        if str(old_value) == str(sudoku[cell_index]):
            print(f"You entered the same value: {old_value}")
        else:
            print(f'{old_value} -> {sudoku[cell_index]}')

        print("Your sudoku currently: \n")
        print_sudoku(sudoku)

    else:
        replace_cell(sudoku)

    return sudoku


def handle_user():
    """
    Handle interactions with the user and call functions to solve the sudoku.
    """
    print("\n\n\nHello friend!")
    print("This is your Sudoku Solver!")
    sudoku = get_sudoku()

    print("Do you want to make any changes to it?")
    print("\n\n(Yes) press 'y' !\n(No. Let's continue!) press any key besides 'y' and 'q' ! \n(Quit) press'q' !\n")
    to_change_smth = input("Make changes: \n")
    if to_change_smth.lower() == 'y':
        while to_change_smth.lower() == 'y':
            sudoku = replace_cell(sudoku)
            to_change_smth = input("To make more changes press 'y': \n")
    elif to_change_smth.lower() == 'q':
        print("Goodbye!")
        quit()
    sudoku_at_the_start = sudoku

    print("Do you want this program to try to solve it?")
    print("\n(Yes) press any key besides 'n' and 'q' ! \n(No) press 'n' ! \n(Quit) press 'q' !")
    to_solve = input('Solve sudoku: \n')
    if to_solve.lower() == 'n':
        print("Ok. Not solving sudoku!")
    elif to_solve.lower() == 'q':
        print("Goodbye!")
        quit()
    else:
        """
        Add time out to solving so it doesn't go on forever if unable to solve.
        Reference:
        https://stackoverflow.com/questions/13293269/how-would-i-stop-a-while-loop-after-n-amount-of-time
        """
        print("Solving...")
        # 10 seconds to solve or break loop
        timeout = time.time() + 10
        while not is_solved(sudoku):
            sudoku = clear_filled(sudoku)
            sudoku = fill_last_value(sudoku)
            sudoku = fill_unique_value(sudoku)
            if time.time() > timeout:
                break
    if not is_solved(sudoku) or to_solve.lower() == 'n':
        print("Oh No! Sudoku solver couldn't solve this sudoku either! :(")
        print("Would you like a hint?")

        to_hint = input("Hint? (press 'y') : \n")
        if to_hint.lower() == 'y':
            while to_hint.lower() == 'y':
                sudoku = clear_filled(sudoku)
                locations = make_locations_map()
                input_cell_code = input('Please enter the XX code to the cell you want a hint for: \n')
                if input_cell_code in locations:
                    cell_index = locations.index(input_cell_code)
                    print(f"{input_cell_code} : {sudoku[cell_index]}")
                else:
                    print(f" {input_cell_code} is not on locations map!")
                to_hint = input("Hint? (press 'y') : \n")
        else:
            print("OK. Better luck next time!")
        print("\n\nThis is the sudoku you entered: \n")
        print_sudoku(sudoku_at_the_start)
        print("\nBetter luck next time!")
    else:
        print("\n\nFinal result: \n")
        print_sudoku(sudoku)
        print("\nExcellent!")
        print("To see the order in which Sudoku Solver found the solution")
        print(" - please, scroll back^^^")

    another = input("\nWould you like to solve another? (press 'y') : \n")
    if another.lower() == 'y':
        print("\nRestarting Sudoku Solver...")
        handle_user()
    else:
        print("Goodbye!")
        quit()


handle_user()
