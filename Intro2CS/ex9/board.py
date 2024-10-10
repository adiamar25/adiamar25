from helper import *
from car import *
import sys


class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """

    def __init__(self):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # implement your code and erase the "pass"
        self.__length = 7
        self.__board_list = []
        self.__cars = []
        self.__winning_coordinate = (self.__length//2, self.__length)
        self.__fill_board()

    def __fill_board(self):
        for row in range(self.__length):
            inner_list = []
            for col in range(self.__length):
                inner_list.append("_")
                if row == self.__length//2 and col == self.__length - 1:
                    inner_list.append("_")
            self.__board_list.append(inner_list)

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable representation
        # of the board for printing, but may not assume details about it.
        # implement your code and erase the "pass"
        game_board = ""
        for list in self.__board_list:
            for string in list:
                game_board += string
            game_board += '\n'

        return game_board

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        # implement your code and erase the "pass"
        coordinates_list = []
        for row in range(self.__length):
            for col in range(self.__length):
                coordinates_list.append((row, col))
        coordinates_list.append((self.__length//2, self.__length))

        return coordinates_list

    def check_bounds(self, car):
        moves = []
        car_coordinates = car.car_coordinates()
        length = len(car_coordinates)
        car_possible_moves = car.possible_moves()
        loc = car_coordinates[0]
        for item in car_possible_moves.keys():
            if item == "u" or item == "d":
                orientation = 0
                if 0 < loc[orientation]:
                    if (self.cell_content((loc[0]-1, loc[1]))) == None:
                        direction = "u"
                        description = "The car can move up"
                        moves.append((car.get_name(), direction, description))
                if loc[orientation] + length < self.__length:
                    if (self.cell_content((loc[0] + length, loc[1]))) == None:
                        direction = "d"
                        description = "The car can move down"
                        moves.append((car.get_name(), direction, description))
            else:
                orientation = 1
                if 0 < loc[orientation]:  # up, left
                    if (self.cell_content((loc[0], loc[1]-1))) == None:
                        direction = "l"
                        description = "The car can move left"
                        moves.append((car.get_name(), direction, description))
                if loc[0] != self.__length//2:
                    if loc[orientation] + length < self.__length:
                        if ((self.cell_content
                             ((loc[0], loc[1] + length))) == None):
                            direction = "r"
                            description = "The car can move right"
                            moves.append(
                                (car.get_name(), direction, description))
                else:
                    if loc[orientation] + length <= self.__length:
                        if ((self.cell_content(
                                (loc[0], loc[1] + car.length()))) == None):
                            direction = "r"
                            description = "The car can move right"
                            moves.append(
                                (car.get_name(), direction, description))

        return moves

    def is_car_in_board(self, car):
        name = car.get_name()
        name = name
        for row_ind in range(len(self.__board_list)):
            for col_ind in range(len(self.__board_list[0])):
                if self.__board_list[row_ind][col_ind] == name:
                    return True
        return False

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,move_key,description)
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        # implement your code and erase the "pass"
        moves_list = []
        for car in self.__cars:
            if self.is_car_in_board(car):
                moves_list += self.check_bounds(car)

        return moves_list

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        # implement your code and erase the "pass"
        return self.__winning_coordinate

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        # implement your code and erase the "pass"
        if self.__board_list[coordinate[0]][coordinate[1]] == '_':
            return None
        return self.__board_list[coordinate[0]][coordinate[1]]
        # for car in self.__cars:
        #     car_coordinates = car.car_coordinates()
        #     if coordinate in car_coordinates:
        #         return car.get_name()
        # return None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"
        # self.__cars.append(car)
        coordinates = car.car_coordinates()
        for coor in coordinates:
            if coor not in self.cell_list():
                return False
            if self.cell_content(coor) != None:
                return False
        self.__cars.append(car)
        for coordinate in coordinates:
            self.__board_list[coordinate[0]
                              ][coordinate[1]] = car.get_name()
        return True

    def place_car(self, car, orientation, move_key):
        """
        A function that actualy moves the car on the board.
        We call it from the move_car() function.
        """
        car_coordinates = car.car_coordinates()
        length = len(car_coordinates)
        loc = car_coordinates[0]
        name = car.get_name()
        # for i in range(length):
        if orientation == 0:
            if move_key == "u":
                self.__board_list[loc[0]+length-1][loc[1]] = "_"
                self.__board_list[loc[0]-1][loc[1]] = name
            else:
                self.__board_list[loc[0]][loc[1]] = "_"
                self.__board_list[loc[0]+length][loc[1]] = name
        else:
            if move_key == "r":
                self.__board_list[loc[0]][loc[1]] = "_"
                self.__board_list[loc[0]][loc[1]+length] = name
            else:
                self.__board_list[loc[0]][loc[1]+length-1] = "_"
                self.__board_list[loc[0]][loc[1]-1] = name

    def move_car(self, name, move_key):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param move_key: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        # implement your code and erase the "pass"
        for car in self.__cars:
            if car.get_name() == name:
                moves_list = self.possible_moves()
                for move in moves_list:
                    if move[0] == name and move[1] == move_key:
                        orientation = 0
                        if move[1] in "rl":
                            orientation = 1
                        # car.move(move_key)
                        self.place_car(car, orientation, move[1])
                        car.move(move_key)
                        return True

        return False
