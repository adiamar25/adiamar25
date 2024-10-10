#################################################################
# FILE : math_print.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex1 2023
# DESCRIPTION: A simple program that make some math calculuses
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################

########################### IMPORTS ###############################
from typing import List, Tuple, Set, Optional, Any

########################### CODE ##################################

# We define the types of a partial picture and a constraint (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    """ PARAM1: picture, represented by 2D list.
        PARAM2: row, represented by an integer
        PARAM3: col, represented by an integer.
        the function returns the max value of seen cells from a 
        given coordinate (n, m) by considering the unknown coordinates
        as white. """
    if picture[row][col] == 0:
        return 0
    counter = 0
    for col_ind in range(col, len(picture[0])):
        if picture[row][col_ind] != 0:
            counter += 1
        else:
            break
    for col_ind in range(col-1, -1, -1):
        if picture[row][col_ind] != 0:
            counter += 1
        else:
            break
    for row_ind in range(row+1, len(picture)):
        if picture[row_ind][col] != 0:
            counter += 1
        else:
            break
    for row_ind in range(row-1, -1, -1):
        if picture[row_ind][col] != 0:
            counter += 1
        else:
            break
    return counter


def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    """ PARAM1: picture, represented by 2D list.
        PARAM2: row, represented by an integer
        PARAM3: col, represented by an integer.
        the function returns the min value of seen cells from a 
        given coordinate (n, m) by considering the unknown coordinates
        as black. """
    if picture[row][col] == 0 or picture[row][col] == -1:
        return 0
    counter = 0
    for col_ind in range(col, len(picture[0])):
        if picture[row][col_ind] == 1:
            counter += 1
        else:
            break
    for col_ind in range(col-1, -1, -1):
        if picture[row][col_ind] == 1:
            counter += 1
        else:
            break
    for row_ind in range(row+1, len(picture)):
        if picture[row_ind][col] == 1:
            counter += 1
        else:
            break
    for row_ind in range(row-1, -1, -1):
        if picture[row_ind][col] == 1:
            counter += 1
        else:
            break
    return counter


def check_constraints(picture: Picture, constraints_set: Set[Constraint]) -> int:
    """ PARAM1: picture, represented by 2D list.
        PARAM2: constraints_set, a set of tuples representing a 
        coordinate and the number of cells that seen from it. 
        the function returns 0 if at least one constrain broke, 
        1 if no constrain broke for sure, and 2 if we 
        can"t detemine certainly. """
    constraints_exact_counter = 0
    constraint_violated = 0
    for constraint in constraints_set:
        max_seen = max_seen_cells(picture, constraint[0], constraint[1])
        min_seen = min_seen_cells(picture, constraint[0], constraint[1])
        if max_seen == min_seen and min_seen == constraint[-1]:
            constraints_exact_counter += 1
        elif min_seen <= constraint[-1] <= max_seen:
            pass
        else:
            constraint_violated += 1
    if constraints_exact_counter == len(constraints_set):
        return 1
    elif constraint_violated >= 1:
        return 0
    else:
        return 2


def create_image(n: int, m: int, constraints_set):
    """ PARAM1: n, integer that represent the number of rows.
        PARAM2: m, integer that represent the number of columns.
        PARAM3: constraints_set, a set of tuples representing a 
        coordinate and the number of cells that seen from it.
        The function returns a 2D list that represent the image, and 
        puts in some constrains that we know for sure the image takes. """
    image = []
    for i in range(n):
        inner_list = []
        for j in range(m):
            inner_list.append(-1)
        image.append(inner_list)
    for constrain in constraints_set:
        if constrain[-1] == 0:
            image[constrain[0]][constrain[1]] = 0
        else:
            image[constrain[0]][constrain[1]] = 1

    return image


def ok_to_place(image, value, constarints_set, row, col):
    """ PARAM1: image, represnted by 2D list.
        PARAM2: value, an integer that is 1 or 0.
        PARAM3: constraints_set, a set of tuples representing a 
        coordinate and the number of cells that seen from it.
        PARAM4: row, an integer. 
        PARAM5: col, an integer. 
        The function returns False whether there was at least one 
        constrain that broke, True else. """
    image[row][col] = value
    if check_constraints(image, constarints_set) == 0:
        return False
    return True


def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[Picture]:
    """ PARAM1: constraints_set, a set of tuples representing a 
        coordinate and the number of cells that seen from it.
        PARAM2: row, an integer. 
        PARAM3: col, an integer.
        The function returns one possible solution of the puzzle, 
        using the helper function. """
    res: List = []
    image = create_image(n, m, constraints_set)
    picture = _puzzle_helper(constraints_set, image, 0, res)
    print(picture)
    if picture == None:
        return picture
    return picture[0]


def _puzzle_helper(constraints_set, image, ind, result_list: List[Any]):
    """ PARAM1: constraints_set, a set of tuples representing a 
        coordinate and the number of cells that seen from it.
        PARAM2: image, represented by 2D list. 
        PARAM3: ind, an index that is an integer between 0 to n*m.
        PARAM4: result_list, a list that gets the solution of the puzzle.
        The function returns the results_list"""
    if ind == len(image) * len(image[0]):
        result_list.append(image[:])
        return

    row = ind // len(image[0])
    col = ind % len(image[0])

    if image[row][col] == 1 or image[row][col] == 0:
        _puzzle_helper(constraints_set, image, ind+1, result_list)
        if check_constraints(image, constraints_set) == 1:
            return result_list
        return

    for value in range(2):
        if ok_to_place(image[:], value, constraints_set, row, col):
            image[row][col] = value
            _puzzle_helper(constraints_set, image, ind+1, result_list)
            if check_constraints(image, constraints_set) == 1:
                return result_list
    image[row][col] = -1


def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) -> int:
    """ PARAM1: constraints_set, a set of tuples representing a 
        coordinate and the number of cells that seen from it.
        PARAM2: n, an integer. 
        PARAM3: m, an integer.
        The function returns the number of possible solutions of the puzzle, 
        using the helper function. """
    image = create_image(n, m, constraints_set)
    return _how_many_solutions_helper(constraints_set, image, 0)


def _how_many_solutions_helper(constraints_set, image, ind):
    """ PARAM1: constraints_set, a set of tuples representing a 
        coordinate and the number of cells that seen from it.
        PARAM2: image, represented by 2D list. 
        PARAM3: ind, an index that is an integer between 0 to n*m.
        The function returns counter, the number of possible solutions. """
    if ind == len(image) * len(image[0]):
        return 1

    row = ind // len(image[0])
    col = ind % len(image[0])

    if image[row][col] == 1 or image[row][col] == 0:
        _how_many_solutions_helper(constraints_set, image, ind+1)

    counter = 0
    for value in range(2):
        if ok_to_place(image, value, constraints_set, row, col):
            image[row][col] = value
            counter += _how_many_solutions_helper(
                constraints_set, image, ind+1)
        image[row][col] = -1
    return counter


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    pass
