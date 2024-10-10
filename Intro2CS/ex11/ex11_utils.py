#################################################################
# FILE : boggle.py
# WRITERS : Adi Amar, adi.amar1, 315244624,
#           Benjamin Teitler, benjamin.t, 328966346
# EXERCISE : intro2cs1 ex11 2023
# DESCRIPTION: A simple program that makes Boggle game by GUI
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################

#################################################################
############################ IMPORTS ############################
#################################################################

from typing import List, Tuple, Iterable, Optional
from datetime import datetime
import boggle_board_randomizer
from tree_dict import *
Board = List[List[str]]
Path = List[Tuple[int, int]]

#################################################################
############################# CODE ##############################
#################################################################


def is_valid_click(path, cor):
    """ Recieves the locaion of the new click, and if it is a legal move,
     then return the loction, otherwise returns an empty list"""
    if len(path) == 0:
        return [cor]
    last = path[len(path)-1]
    if abs(last[0]-cor[0]) <= 1 and abs(last[1]-cor[1]) <= 1 \
            and cor not in path:
        return [cor]
    return []


def check_duplicates(path):
    """ Checks if any coordinate appears more then once"""
    path_set = {p for p in path}
    return len(path_set) == len(path)


def in_board(cor, board):
    """ Checks if given location is in the boards boundries"""
    if cor[0] >= len(board) or cor[1] >= len(board[0]):
        return False
    return True


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """ Checks if the given path is legal, and if it is then return the word that it creates"""
    if path == []:
        return None
    word = str()
    if not check_duplicates(path):
        return None
    for i in range(len(path)-1):
        if not in_board(path[i], board):
            return None
        if abs(path[i][0]-path[i+1][0]) <= 1 and abs(path[i][1]-path[i+1][1]) <= 1:
            word += board[path[i][0]][path[i][1]]
        else:
            return None
    if not in_board(path[len(path)-1], board):
        return None
    word += board[path[len(path)-1][0]][path[len(path)-1][1]]
    if word in words:
        return word
    return None


def n_paths_helper(n, board, words, pos, path: List[tuple], tree):
    """ Helper for **find_length_n_paths()** """
    all_paths = []
    if tree.query(build_word(board, path)) == []:
        return []
    if len(path) == n:
        if is_valid_path(board, path, words) != None:
            return [path]
        return []
    if len(path) > n:
        return []
    heigth = len(board)
    length = len(board[0])
    row, col = pos
    for r in [-1, 0, 1]:
        for c in [-1, 0, 1]:
            new_row = row + r
            new_col = col + c
            if 0 <= new_row < heigth and 0 <= new_col < length and not (new_row, new_col) in path:
                all_paths += n_paths_helper(n, board, words,
                                            (new_row, new_col), path + [(new_row, new_col)], tree)
    return all_paths


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """ Returns all paths of words created with n steps"""
    tree = create_tree(words)
    all_options = []
    for r in range(len(board)):
        for c in range(len(board[r])):
            all_options += n_paths_helper(n, board,
                                          words, (r, c), [(r, c)], tree)
    return all_options


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """ Returns all words the length of n"""
    all_options = []
    tree = create_tree(words)
    for r in range(len(board)):
        for c in range(len(board[r])):
            all_options += n_words_helper(n, board,
                                          words, (r, c), [(r, c)], tree)
    return all_options


def build_word(board, path):
    """ Recieves path, and returns the word it builds"""
    word = str()
    for p in path:
        word += board[p[0]][p[1]]
    return word


def n_words_helper(n, board, words, pos, path, tree):
    """ Helper for **find_length_n_words()** """
    all_paths = []
    word = build_word(board, path)
    if tree.query(word) == []:
        return []
    if len(word) == n:
        if word in words:
            return [path]
        return []
    if len(word) > n:
        return []
    heigth = len(board)
    length = len(board[0])
    row, col = pos
    for r in [-1, 0, 1]:
        for c in [-1, 0, 1]:
            new_row = row + r
            new_col = col + c
            if 0 <= new_row < heigth and 0 <= new_col < length and not (new_row, new_col) in path:
                all_paths += n_words_helper(n, board, words,
                                            (new_row, new_col), path + [(new_row, new_col)], tree)
    return all_paths


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """ Returns the paths needed to put in to recieve the maximum score possible"""
    all_ways = []
    most_points = dict()
    tree = create_tree(words)
    for n in range(1, len(board)*len(board[0])+1):
        all_ways += find_length_n_paths(n, board, words)
    for way in all_ways:
        word = build_word(board, way)
        if word not in most_points.keys():
            most_points[word] = way
        elif len(most_points[word]) < len(way):
            most_points[word] = way
    return list(most_points.values())


def create_tree(words):
    """ Creates a tree of the given dictionary"""
    tree = Tree()
    for word in words:
        tree.insert(word)
    return tree
