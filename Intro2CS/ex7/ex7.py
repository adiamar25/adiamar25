#################################################################
# FILE : math_print.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex7 2023
# DESCRIPTION: A not quite simple program that make some recursions
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################
import typing
from typing import List, Any
from ex7_helper import *


def mult(x: N, y: int) -> N:
    """ A function that gets two arguments: x, which can be int or float, 
        and y, which can only be int. the function calculates the value 
        of x product y using recursion, return the sum. 
        the function does that in O(n) notation. """
    # If one of the arguments is zero, return zero
    if x == 0 or y == 0:
        return 0
    # Else, return the sum of x plus (x*y)
    return add(x, mult(x, subtract_1(y)))


def is_even(n: int) -> bool:
    """ A function that gets an integer, 
        returns True if it even, False if it odd. """
    # If n is equal to zero, then n is even, so the function returns True
    if n == 0:
        return True
    # Else, the function calls itself, checks n-1
    return not is_even(subtract_1(n))


def log_mult(x: N, y: int) -> N:
    """ A function that gets two arguments: x, which can be int or float,
        and y, which cant be only int. the function returns the product x*y,
        and it does that using O(log(n)) notaion. """
    # If x or y are zero, then the product x*y = 0,
    # so the function returns 0
    if x == 0 or y == 0:
        return 0
    z: N = log_mult(x, divide_by_2(y))
    # If y is even number, then the function returns the sum of z+z,
    # which is ((x*y)/s)*2)
    if is_odd(y) == False:
        return add(z, z)
    # Else, the function returns the sum of z+z+x, which is also equal to x*y
    else:
        return add(x, add(z, z))


def power_check(mult_arg: int, x: int, b: int) -> bool:
    """ A helper function for us_power(), which recursivly call itself,
        with diffrent arguments, checks whether there is an exponent of b,
        such as b^n = x when we are not on the base cases. """
    if x <= mult_arg:
        if x == mult_arg:
            return True
        else:
            return False
    else:
        return power_check(log_mult(b, mult_arg), x, b)


def is_power(b: int, x: int) -> bool:
    """ A function that get two int arguments, return True whether exist an n
        such as b^n = x, False else. """
    # 1 is always a power of any number
    if x == 1:
        return True
    if b == 0 and x != 0:
        return False
    if b == 1 and x != 1:
        return False
    # If x is odd and b is even, or the oppsite, x is not a power of b
    elif is_odd(x) != is_odd(b):
        return False
    else:
        return power_check(log_mult(b, 1), x, b)


def reverse_string_helper(s: str, new_s: str, index: int) -> str:
    """ A helper function for reverse(), which get a string, an empty string, 
        and an index, and if the index is equal or greater than 0,
        the function append the last char of the string to the empty string, 
        which go longer. """
    if index >= 0:
        reversed_str = append_to_end(new_s, s[index])
        return reverse_string_helper(s, reversed_str, index - 1)
    return new_s


def reverse(s: str) -> str:
    """ A function that gets a string, and returns the reversed string 
        using recursion. """
    new_str = ""
    index = len(s) - 1
    return reverse_string_helper(s, new_str, index)


def play_hanoi(hanoi: Any, n: int, src: Any, dest: Any, temp: Any) -> Any:
    """ A function that simulate the hanoi game. we play the game
        if the disk number is greater then 0, and using recursion to place
        the disks by the ruls. """
    if n > 0:
        # Move n - 1 disks from src to temp
        play_hanoi(hanoi, n - 1, src, temp, dest)
        # Move the n disk from src to dest
        hanoi.move(src, dest)
        # Move the n - 1 disks from temp to dest
        play_hanoi(hanoi, n - 1, temp, dest, src)
        return None
    return None


def nums_1_helper(n: int, counter_ones: int) -> int:
    """ A helper function to number_of_ones(). it is recursively 
        call itself according the number of the digits in the integer 
        recieved. in addition, the function gets a counter, and it counts
        the number of 1 shows in each recursion call"""
    if n < 10:
        digit = n % 10
        if digit == 1:
            counter_ones += 1
            return counter_ones
        return counter_ones
    elif n == 10:
        counter_ones += 1
        return counter_ones
    else:
        digit = n % 10
        if digit == 1:
            counter_ones += 1
        return nums_1_helper(n // 10, counter_ones)


def number_of_ones(n: int) -> int:
    """ A function that get an integer, returns the number of times that the
        digit 1 showed in all the numbers from 1 to n(included). it's done
        by recursive call to itself, and calling to a helper function. """
    if n == 0:
        return 0
    return number_of_ones(n-1) + nums_1_helper(n, 0)


def index_compare(l1: List[int], l2: List[int], last_index: int) -> bool:
    if last_index == 0:
        if len(l1) > 0 and len(l2) > 0:
            if l1[0] == l2[0]:
                return True
            return False
        return False
    if last_index == len(l1)-1:
        if l1[last_index] != l2[last_index]:
            return False
        return index_compare(l1, l2, last_index-1)
    else:
        if last_index-1 >= 0:
            if l1[last_index-1] != l2[last_index-1]:
                return False
            return index_compare(l1, l2, last_index-1)
        return index_compare(l1, l2, last_index-1)


def compare_2d_lists_helper(l1_part: List[int], l2_part: List[int]) -> bool:
    if len(l1_part) != len(l2_part):
        return False
    return index_compare(l1_part, l2_part, len(l1_part)-1)


def compare_2d_lists(l1: List[List[int]], l2: List[List[int]]) -> bool:
    if len(l1) != len(l2):
        return False
    if len(l1) > 0 and len(l2) > 0:
        if (compare_2d_lists_helper(l1[0], l2[0])
                and compare_2d_lists_helper(l1[-1], l2[-1])):
            return True
        return False
    else:
        if len(l1) == 0 and len(l2) == 0:
            return True
        return False


def magic_list(n: int) -> List[Any]:
    """ A function which get an integer, returns a magic_list in the length
        of n, by calling the helper function. """
    return [] if n == 0 else magic_list(n-1) + [magic_list(n-1)]
