# Welcome to Sudoku Solver
## Purpose 
The purpose of the sudoku solver is to be a usefull tool to help solve sudoku puzzles. I personally find this tool usefull because I like solving the sudoku puzzles. So I created this project for personal use in times of need.

## Input

The main input of this program is the sudoku itself.
Sudoku traditionally of 9x9 dimentions and divided in 9 squeres of 3x3 dimentions. Each 3x3 square (quadrant), row and column can have only unique values in range from 1 till 9.
This program takes only this kind of sudoku for solving.

![Sudoku](assets/images/sudoku.png)

## Testing with different kinds of inputs for sudoku:

### Sudoku input is too short
![Too short](assets/images/too_short.png)

After entering an input that is too short:
* shows message that the input is not 81 characters long
* let's make the input for sudoku again

 - CORRECT response to the situation

### Sudoku input is too long
![Too long](assets/images/too_long.png)

After entering an input that is too long:
* shows message that the input is not 81 characters long
* let's make the input for sudoku again

 - CORRECT response to the situation


### Sudoku input doesn't have enough integers for solving it.
![Not enough integers](assets/images/not_enough_integers.png)

After enetring an input of 81 charachters and with less than 17 integers:
* shows a message that the input didn't have enough integer values (filled in values)
* let's you make the input of sudoku again
 - CORRECT response


### Enter pressed without entering a sudoku
![No input](assets/images/no_input.png)

If enter is pressed without inputing a string:
* shows a message that no sudoku was input
* quits program
 - CORRECT response to the situation


### Error in input
![Error in input](assets/images/error1.png)

If sudoku is entered with already existing error in it - the same value is filled in in the same row column or quadrant.
* takes it as a valid input for now
* asks if user wants to change any cell that was entered
 - CORRECT response
 - In the future sudoku solver could be updated to catch this as an error but because of the constraints it was left as an feature to add later not as an error of the program.


## Testing with different kinds of inputs for modifying the input sudoku:

### Cell value change after sudoku input
![Change cell value](assets/images/change_cell_value.png)

If entered 'y' to change a cell value:
* a map is displayed to help name the field to change the value of
* let's make an input for the cell code XX
  * if entered a correct code - shows current value
  * if entered an incorrect code - shows map agai to enter the code for the cell again

 - CORRECT response to the situation

### Cell value change after sudoku input
![Change cell value](assets/images/change_cell_value.png)

If entered 'y' to change a cell value:
* a map is displayed to help name the field to change the value of
* let's make an input for the cell code XX
  * if entered a correct code - shows current value
  * if entered an incorrect code - shows map again to enter the code for the cell again

 - CORRECT response to the situation

### Offers to solve sudoku
![Offers to solve](assets/images/to_solve.png)

If the sudoku input was succesfull and user has finished making changes to the cells if user wished to make any:
* offers to solve sudoku if user wishes to solve it
* based on next input:
  * continues to solve
  * offers to hint a cell if 'n' 
  * quits program if 'q'

 - CORRECT response to the situation


### If solver cannot solve the sudoku
![Unsolved sudoku](assets/images/unsolved.png)

If the sudoku solver couln't reach a solved sudoku:
* offers to hint cells of the sudoku if user wishes to get a hint from the solver
* based on next input:
  * asks for a cell code to deliver a hint for
  * shows what the unsolved sudoku was and offers to solve another sudoku if 'n'
  * shows what the unsolved sudoku was and quits program if 'q'

 - CORRECT response to the situation


### If solver can solve the sudoku
![Solved sudoku](assets/images/solved.png)

If the sudoku solver could reach a solved sudoku:
* it prints out the process of filling each cell out and the sudoku after each new filled cell. In the end it mention that the user can see the steps by scrolling back
* offers to solve another

 - CORRECT response to the situation

## Deployment

Welcome mangabear4dn,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **August 17, 2021**

## Reminders

* Your code must be placed in the `run.py` file
* Your dependencies must be placed in the `requirements.txt` file
* Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

-----
Happy coding!

## Credits
* w3schools information on data types and methods
* Mentor suggestions
* CI lessons
* stackoverflow for more concrete solutions (references in the code)
* other materials on the processes (reference in the code)