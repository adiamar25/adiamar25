#################################################################
# FILE : ex3.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex3 2023
# DESCRIPTION: A simple program that make some vector calculuses
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################

def input_list():
    """ A function that gets input of numbers from the user, and return
        a list which contains all those numbers, and also their sum.
        The function stops when the user insert an empty string"""
    num_string_from_user = input()
    # The list which the function returns
    input_list = []
    # A variable intended to calculate the sum of all
    # the numbers inserted by the user
    counter = 0
    # A loop that works while the user does not inserts an empty string,
    # and update the input list accordingly
    while num_string_from_user != "":
        # Converting the string inputed by the user to float type
        num_string_from_user = float(num_string_from_user)
        input_list.append(num_string_from_user)
        counter += num_string_from_user
        num_string_from_user = input()
    # Checks whether the user insertd an empty string in his first chance.
    # If he did, returns the list: [0]
    if len(input_list) == 0:
        input_list.append(0)
        return input_list
    input_list.append(counter)
    return input_list


def inner_product(vec_1, vec_2):
    """ A function that get two vectors, represented by lists, 
        returns the sum of their standart inner product"""
    # Checks whether the length of the two vectors inputed is not equal,
    # and returns None accordingly
    if len(vec_1) != len(vec_2):
        return None
    # Returns 0 if the length of both vectors is 0
    if len(vec_1) == 0 and len(vec_2) == 0:
        return 0
    # In the next couple of lines, the function calculate the product of
    # every numbers of both vectors that has the same index,
    # returns the sum of all that products
    counter = 0
    for index in range(len(vec_1)):
        curr_sum = vec_1[index] * vec_2[index]
        counter += curr_sum
    return counter


def sequence_monotonicity(sequence):
    """ A that gets a list of numbers, and checks if it answer
        one or more of the sequences monotonicity requirements"""
    bool_list = [None, None, None, None]
    # Checks whether the sequence is in accending order
    for index in range(1, len(sequence)):
        if sequence[index] < sequence[index - 1]:
            bool_list[0] = False
    if bool_list[0] != False:
        bool_list[0] = True
    # Checks whether the sequence is in completely accending order
    for index in range(1, len(sequence)):
        if sequence[index] <= sequence[index - 1]:
            bool_list[1] = False
    if bool_list[1] != False:
        bool_list[1] = True
    # Checks whether the sequence is in declining order
    for index in range(1, len(sequence)):
        if sequence[index - 1] < sequence[index]:
            bool_list[2] = False
    if bool_list[2] != False:
        bool_list[2] = True
    # Checks whether the sequence is in completely declining order
    for index in range(1, len(sequence)):
        if sequence[index - 1] <= sequence[index]:
            bool_list[3] = False
    if bool_list[3] != False:
        bool_list[3] = True
    return bool_list


def monotonicity_inverse(def_bool):
    """ A function that gets a list contains four boolian variables, 
    and returns an example of sequence which answer the terms
    of the "sequence_monotonicity" function """
    # An example for accending ordered sequence
    if def_bool == [True, False, False, False]:
        return [1, 1, 2, 3]
    # An example for declining ordered sequence
    if def_bool == [False, False, True, False]:
        return [6, 5, 4, 4]
    # An example for completely accending ordered sequence
    if def_bool == [True, True, False, False]:
        return [1, 2, 3, 4]
    # An example for completely declining ordered sequence
    if def_bool == [False, False, True, True]:
        return [6, 5, 4, 3]
    # An example for a sequence which is not declining nor accending
    if def_bool == [False, False, False, False]:
        return [1, 4, 2, 2]
    if def_bool == [True, False, True, False]:
        return [4, 4, 4, 4]
    return None


def convolve(math):
    """ A function which gets a list of lists, represents a matrix,
        and returns a convolve matrix, also represnted by list of lists. """
    # Checks whether the list which got from the user is empty
    if len(math) == 0:
        return None
    # Defining a list in which we insert the convolve matrix
    convolve_list = []
    # Here we set variables that simulate start and end indexes which
    # helps us to run over the matrix in 3x3 squares
    start_row = 0
    end_row = 3
    start_column = 0
    end_column = 3
    # Defining a while loops which promotes the start and end values
    # while there left at list three rows and columns in the matrix
    while len(math) - start_row >= 3:
        # Defining a list in which we insert the rows of the convolve matrix
        inner_list = []
        while len(math[0]) - start_column >= 3:
            # Setting a counter which calculate the total value in every
            # 3x3 matrix. finnaly, we insert the counter to "inner_list"
            counter = 0
            # Defining a for loops which helps us to run over
            # the matrix's rows and columns by approaching its indexes
            for i in range(start_row, end_row):
                for j in range(start_column, end_column):
                    # Adds the number in the i row and the
                    # j column in the matrix to counter
                    math_i_j = math[i][j]
                    counter += math_i_j
            inner_list.append(counter)
            # Promoting the star and end variables indexes
            start_column += 1
            end_column += 1
        # Inserting a row to the convolve matrix
        convolve_list.append(inner_list)
        start_row += 1
        end_row += 1
        # Going back to default start and end indexes
        start_column = 0
        end_column = 3
    return convolve_list


def sum_of_vectors(vec_lst):
    """ A function that gets a list contains a lists of number,
        which represent vectors, and returns the suitable vector sum """
    # Checks if the vectors list is empty
    if not bool(vec_lst):
        return None
    # The next couple of lines are using two for loops in order to
    # approach the elements in the inner lists by their indexes, then
    # inserting the sum of each iteration in sum_list
    sum_list = []
    for i in range(len(vec_lst[0])):
        counter = 0
        for j in range(len(vec_lst)):
            counter += vec_lst[j][i]
        sum_list.append(counter)
    return sum_list


def num_of_orthogonal(vectors):
    """ A function that gets a list of vectors, represented by lists, and
        cheks for all the possible vector couples whether they orthogonal """
    couples_num = 0
    i = 1
    for vector1 in vectors:
        # Uses while and for loops to run over all the vectors but vector1,
        # by using a changed index
        while i < len(vectors):
            for vector2 in vectors[i:]:
                # Calls the "inner_product" function we defined earlier,
                # in order to calculate the inner product of every two vectors
                check_if_orthogonal = inner_product(vector1, vector2)
                # Checks if the inner product is equal to 0
                if check_if_orthogonal == 0:
                    couples_num += 1
            i += 1
            break
    return couples_num


print(num_of_orthogonal([[1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 0, 0]]))
