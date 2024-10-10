#################################################################
# FILE : battleship.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex4 2023
# DESCRIPTION: A program that run the "battleship" game
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################


import helper
import copy


def init_board(rows, columns):
    """A function that initiate the board. 
       it gets two parameters of rows and columns, 
       and make nested list which presents the game board"""
    game_board = []
    for i in range(rows):
        inner_list = []
        for j in range(columns):
            inner_list.append(helper.WATER)
        game_board.append(inner_list)
    return game_board


def cell_loc(name):
    """A function that get a string contains a coordinate from the user, 
       in the following order: a letter presents the column number, 
       and a number presents the row number. for example: "B7", and returns
       a tuple coordinate contains the suitable indexes in the opposite order.
       in the current example: (6, 1). the function gets only upper letters.
       if the input invalid, the function returns None. """
    if helper.is_int((name[-1:0:-1])) and (name[0]).isupper():
        coordinate_tuple = (int(name[1:])-1, ord(name[0])-65)
    return coordinate_tuple


def check_input(name):
    """A function that checks whether the user input is valid. """
    if helper.is_int((name[-1:0:-1])) and (name[0]).isupper():
        if (ord(name[0]) - 65 >= helper.NUM_COLUMNS or
                int(name[1:]) > helper.NUM_ROWS or int(name[1:]) <= 0):
            return False
        else:
            return True
    else:
        return False


def valid_ship(board, size, loc):
    """A function that get three parameters: a board, a size of a ship,
       and a location, and returns a boolian variable which tells whether 
       we can put this ship in the board or not. """
    if loc == None:
        return False
    if loc[0] < 0:
        return False
    if loc[0] + size <= len(board) and loc[-1] <= len(board[0]):
        for i in range(loc[0], loc[0]+size):
            if board[i][loc[-1]] != helper.WATER:
                return False
        return True
    else:
        return False


def put_ships_in_board(board, tuple_index, ship_size):
    """A function that put ship in a certain size 
       in a givven location on the board. """
    counter = 0
    for lst in board[tuple_index[0]:]:
        if counter < ship_size:
            lst[tuple_index[-1]] = helper.SHIP
            counter += 1
    return board


def create_player_board(rows, columns, ship_sizes):
    """A function which gets a row number, a columns nujmber and a ship size, 
       and put the ships in a location supplied by the user. """
    game_board = init_board(rows, columns)
    ship_num = 0
    while ship_num < len(ship_sizes):
        helper.print_board(game_board)
        input_size = helper.get_input("Please select location"
                                      " to place your ship: ")
        while not check_input(input_size.upper()):
            input_size = helper.get_input("Invalid location."
                                          " Please pick another one: ")
        input_coordinate = cell_loc(input_size.upper())
        while not valid_ship(game_board, ship_sizes[ship_num],
                             input_coordinate):
            helper.print_board(game_board)
            new_input_size = helper.get_input("Please select a valid"
                                              " location: ")
            while not check_input(new_input_size.upper()):
                new_input_size = helper.get_input("Please select a valid"
                                                  " location: ")
            input_coordinate = cell_loc(new_input_size.upper())
        game_board = put_ships_in_board(game_board,
                                        (input_coordinate[0],
                                         input_coordinate[-1]),
                                        ship_sizes[ship_num])
        ship_num += 1
    return game_board


def fire_torpedo(board, loc):
    """A function that gets a board and a specific location to bomb. 
       if there was water in the given location, the function changes it to 
       HIT_WATER or HIT_SHIP, the necessary one. """
    if loc[0] < len(board) and loc[-1] < len(board[0]):
        if board[loc[0]][loc[-1]] == helper.WATER:
            board[loc[0]][loc[-1]] = helper.HIT_WATER
        if board[loc[0]][loc[-1]] == helper.SHIP:
            board[loc[0]][loc[-1]] = helper.HIT_SHIP
    else:
        return board
    return board


def possible_locs_ships(board, ship_size):
    """A function that get a board and an hypothetic ship 
       size to put in the board, returns a set of possible 
       location to place the ship. """
    locations_list = []
    rows_number = len(board)
    columns_number = len(board[0])
    for i in range(rows_number):
        for j in range(columns_number):
            if valid_ship(board, ship_size, (i, j)):
                locations_list.append((i, j))
    locations_set = set(locations_list)
    return locations_set


def possible_bomb_locs(board):
    """A function that get a board, returns a set of possible 
       location to send the bomb. the locations are those which 
       contains water for the viewer. """
    possible_locs = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if (board[i][j] != helper.HIT_WATER and
                    board[i][j] != helper.HIT_SHIP):
                possible_locs.append((i, j))
    return set(possible_locs)


def is_ships_in_board(board):
    """A function that checks whether there are stil ships in 
       a given board or not. retunrns a boolian variable. """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == helper.SHIP:
                return True
    return False


def create_computer_board(board):
    """A function that create a board for the computer, 
       using possible_locs_ships, put_ship_in_board functions
       we made earlier, choose_ship_location from helper.py. """
    ships_in_pc_board = 0
    while ships_in_pc_board < len(helper.SHIP_SIZES):
        ships_locs_set = possible_locs_ships(board,
                                             helper.SHIP_SIZES
                                             [ships_in_pc_board])
        chosen_location = helper.choose_ship_location(board,
                                                      helper.SHIP_SIZES
                                                      [ships_in_pc_board],
                                                      ships_locs_set)
        board = put_ships_in_board(board,
                                   chosen_location,
                                   helper.SHIP_SIZES
                                   [ships_in_pc_board])
        ships_in_pc_board += 1
    return board


def change_hidden_board(computer_board, hidden_pc_board, loc_to_bomb):
    """ A function that gets 2 boards, the hidden one and the its full origin, 
        and edits the hidden one according to the bombs thrown at the 
        origin board. """
    if computer_board[loc_to_bomb[0]][loc_to_bomb[-1]] == helper.HIT_WATER:
        hidden_pc_board[loc_to_bomb[0]][loc_to_bomb[-1]] = helper.HIT_WATER
    if computer_board[loc_to_bomb[0]][loc_to_bomb[-1]] == helper.HIT_SHIP:
        hidden_pc_board[loc_to_bomb[0]][loc_to_bomb[-1]] = helper.HIT_SHIP
    return hidden_pc_board


def who_won(player_board, computer_board):
    """ A function which determine wo wins according to the amount 
       of ships left in each board. a player that all his ships attacked 
       is the loser one. the function returns a string contains a message 
       about the winner and whether to play another game. """
    game_over_msg = "The game is over.\n"
    plr_won_msg = "Player won!!!\n"
    pc_won_msg = "Computer won!!!\n"
    draw_msg = "Draw!\n"
    another_game = "Would you like to play another game?\n"
    answer = "response 'Y' or 'N': "
    if (is_ships_in_board(computer_board) and
            not is_ships_in_board(player_board)):
        helper.print_board(player_board, computer_board)
        winner = game_over_msg + pc_won_msg + another_game + answer
        return winner
    elif (is_ships_in_board(player_board) and
          not is_ships_in_board(computer_board)):
        helper.print_board(player_board, computer_board)
        winner = game_over_msg + plr_won_msg + another_game + answer
        return winner
    else:
        helper.print_board(player_board, computer_board)
        winner = game_over_msg + draw_msg + another_game + answer
        return winner


def rematch(answer):
    """ A function that gets an input from the user, 
       and starting a new game accordingly by activate 
       main() function again. """
    while answer != "N" and answer != "Y":
        answer = helper.get_input("Please insert a valid answer:"
                                  " 'Y' or 'N': ")
    if answer == "Y":
        main()
    else:
        pass


def main():
    """ The main function of the program. in here we run the game, 
        and managing the turns. we calls all the other function of this
        file here, and some of the relevants of helper.py function. """
    player_board = create_player_board(helper.NUM_ROWS, helper.NUM_COLUMNS,
                                       list(helper.SHIP_SIZES))
    computer_board = init_board(helper.NUM_ROWS, helper.NUM_COLUMNS)
    hidden_pc_board = copy.deepcopy(computer_board)
    hidden_player_board = copy.deepcopy(computer_board)
    computer_board = create_computer_board(computer_board)
    while (is_ships_in_board(player_board) and
           is_ships_in_board(computer_board)):
        helper.print_board(player_board, hidden_pc_board)
        loc_to_bomb = helper.get_input("Please insert location to bomb: ")
        while not check_input(loc_to_bomb.upper()):
            loc_to_bomb = helper.get_input("Invalid location. Try again: ")
        loc_to_bomb = cell_loc(loc_to_bomb.upper())
        while ((hidden_pc_board[loc_to_bomb[0]]
                               [loc_to_bomb[-1]] != helper.WATER)):
            loc_to_bomb = helper.get_input("Invalid location. Try again: ")
            while not check_input(loc_to_bomb.upper()):
                loc_to_bomb = helper.get_input("Invalid location."
                                               " Try again: ")
            loc_to_bomb = cell_loc(loc_to_bomb.upper())
        computer_board = fire_torpedo(computer_board, loc_to_bomb)
        hidden_pc_board = change_hidden_board(computer_board,
                                              hidden_pc_board,
                                              loc_to_bomb)
        loc_to_bomb_player = possible_bomb_locs(player_board)
        pc_attack_loc = helper.choose_torpedo_target(
            hidden_player_board, loc_to_bomb_player)
        player_board = fire_torpedo(player_board, pc_attack_loc)
        hidden_player_board = change_hidden_board(player_board,
                                                  hidden_player_board,
                                                  pc_attack_loc)
    the_winner = who_won(player_board, computer_board)
    another_game = helper.get_input(the_winner)
    rematch(another_game)
    return None


if __name__ == "__main__":
    main()
