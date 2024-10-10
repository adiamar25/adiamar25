from car import *
from board import *
from game import *
import sys


class Car1(Car):
    def car_coordinates(self):
        return [(5, 1), (5, 2)]


class Car2(Car):
    def movement_requirements(self, move_key):
        return [(2, 0), (7, 0)]


class Car3(Car):
    def car_coordinates(self):
        return [(5, 0), (7, 0), (6, 0)]


class Car4(Car):
    def possible_moves(self):
        return {"aa": ""}

    def movement_requirements(self, move_key):
        return [(1, 3)]


class Board1(Board):
    def target_location(self):
        return 5, 5


def test_move_car():
    _car = Car1("R", 2, (0, 0), 0)
    b = Board()
    b.add_car(_car)
    b.move_car("R", "d")
    assert b.cell_content((5, 1)) == b.cell_content((5, 2)) == "R"


def test_move_req():
    _car = Car2("R", 2, (0, 0), 0)
    b = Board()
    b.add_car(_car)
    assert not b.possible_moves()
    assert not b.move_car("R", "d")


def test_coords():
    _car = Car3("R", 3, (0, 0), 0)
    b = Board()
    assert not b.add_car(_car)


def test_possible_moves():
    _car = Car4("R", 2, (1, 1), 0)
    car1 = Car4("O", 7, (6, 0), 1)
    b = Board()
    b.add_car(_car)
    b.add_car(car1)
    assert len(b.possible_moves()) == 2
    assert all(m[1] == "aa" for m in b.possible_moves())


def test_target():
    def input(*args):
        assert False

    sys.modules["builtins"].input = input
    b = Board1()
    _game = Game(b)
    b.add_car(Car("R", 3, (5, 3), 1))
    _game.play()


def test_name():
    inputs = ["!", "P,r"]

    def input(*args):
        if not inputs:
            assert False
        else:
            return inputs.pop()

    sys.modules["builtins"].input = input
    _car = Car("P", 5, (0, 0), 1)
    b = Board()
    assert b.add_car(_car)
    _game = Game(b)
    _game.play()
    assert not b.cell_content((0, 5))
