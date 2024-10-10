from board import *

if __name__ == '__main__':
    board = Board()
    cars = board.cars_list()
    for car in cars:
        board.add_car(car)
    print(board)
    """board.move_car("Y", "l")
    print(board)
    board.move_car("B", "u")
    print(board)
    board.move_car("R", "r")
    print(board)
    board.move_car("O", "d")
    print(board)
    board.move_car("R", "r")
    print(board)"""

    '''car1 = Car("Y", 3, (5, 3), 1)
    car2 = Car("B", 4, (0, 3), 0)
    l1 = car1.car_coordinates()
    print(l1)
    l2 = car2.car_coordinates()
    print(l2)'''
    # print(board.cars_list())
    #possible_moves = board.possible_moves()
    # board.cell_list()
    # print(board)
