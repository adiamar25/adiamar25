#################################################################
# FILE : math_print.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex9 2023
# DESCRIPTION: A simple program that make Rush Hour game
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################

from board import *
import re
from helper import *


class Game:
    """
    Add class description here
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API
        # implement your code and erase the "pass"
        self.__board = board

    def is_valid_input(self, input):
        if input == "!":
            return True

        possible_moves = self.__board.possible_moves()
        for move in possible_moves:
            if move[0] == input[0] and move[1] == input[-1]:
                return True
        return False

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        # implement your code and erase the "pass"
        print(self.__board)
        turn = input("Choose a car and a direction to move it: ")
        did_match = re.match('[A-Z],[lrud]', turn)
        while (turn != "!" and did_match == None
               or not self.is_valid_input(turn)):
            turn = input("Invalid input. Please try again: ")
            did_match = re.match('[A-Z],[lrud]', turn)
        if turn != "!":
            self.__board.move_car(turn[0], turn[-1])
            print(self.__board)
            return True
        return False

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        # implement your code and erase the "pass"
        to_continue = True

        # and to_continue:
        while (self.__board.cell_content(
                self.__board.target_location()) == None and to_continue):
            to_continue = self.__single_turn()
        if to_continue:
            print("You won!!!")
            return None


def is_legal_car(car_name, len, orientation):
    LEGAL_NAMES = "YBOGWR"
    if orientation != 0 and orientation != 1:
        return False
    elif car_name not in LEGAL_NAMES or (not (2 <= len <= 4)):
        return False

    return True


if __name__ == "__main__":
    # Your code here
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    # implement your code and erase the "pass"
    game_board = Board()
    cars_dict = load_json(sys.argv[1])

    for car in cars_dict.keys():
        if is_legal_car(car, cars_dict[car][0], cars_dict[car][2]):
            my_car = Car(car, cars_dict[car][0],
                         cars_dict[car][1], cars_dict[car][2])
            game_board.add_car(my_car)
    game = Game(game_board)
    game.play()
