from helper import *


class Car:
    """
    Add class description here
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # implement your code and erase the "pass"

        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation
        self.__cars_list = []

    def length(self):
        return self.__length

    def location(self):
        return self.__location

    def orientation(self):
        return self.__orientation

    def change_location(self, location):
        self.__location = location

    @staticmethod
    def make_car(cars, car):
        return Car(car, (cars[car])[0], (cars[car])[1], (cars[car])[-1])

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        # implement your code and erase the "pass"
        loc = self.location()
        length = self.length()
        orientation = self.orientation()
        coordinates_list = []
        for i in range(length):
            if orientation == 0:
                coordinates_list.append((loc[0]+i, loc[1]))
            else:
                coordinates_list.append((loc[0], loc[1]+i))

        return coordinates_list

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # implement your code and erase the "pass"
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.
        # implement your code and erase the "pass"
        length = self.length()
        orientation = self.orientation()
        loc = self.location()
        possible_moves = {}
        if orientation == 0:
            possible_moves['u'] = "cause the car to move up"
            possible_moves['d'] = "cause the car to move down"
        elif orientation == 1:
            possible_moves['l'] = "cause the car to move left"
            possible_moves['r'] = "cause the car to move right"

        return possible_moves

    def movement_requirements(self, move_key):
        """ 
        :param move_key: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').
        # implement your code and erase the "pass"
        required_cell = []
        length = self.length()
        loc = self.location()
        orientation = self.orientation()
        car_coordinates = self.car_coordinates()
        if move_key == "r" and orientation == 1:
            required_cell.append((loc[0], loc[1]+length))
        if move_key == "l" and orientation == 1:
            required_cell.append((loc[0], loc[1]-1))
        if move_key == "u" and orientation == 0:
            required_cell.append((loc[0]-1, loc[1]))
        if move_key == "d" and orientation == 0:
            required_cell.append((loc[0]+length, loc[1]))

        return required_cell

    def move(self, move_key):
        """ 
        :param move_key: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        # implement your code and erase the "pass"
        loc = self.__location
        poss_moves = self.possible_moves()
        if move_key in poss_moves.keys():
            if move_key == "r":
                self.__location = (loc[0], loc[-1]+1)
            if move_key == "l":
                self.__location = (loc[0], loc[-1]-1)
            if move_key == "u":
                self.__location = (loc[0]-1, loc[-1])
            if move_key == "d":
                self.__location = (loc[0]+1, loc[-1])
            return True
        return False

        # if move_key == "r":
        #  self.__location[-1] += 1
        # if move_key == "l":
        # self.__location[-1] -= 1
        # if move_key == "u":
        #  self.__location[0] -= 1
        # if move_key == "d":
        #self.__location[0] += 1

    def get_name(self):
        """
        :return: The name of this car.
        """
        # implement your code and erase the "pass"
        return self.__name
