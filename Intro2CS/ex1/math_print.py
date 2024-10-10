#################################################################
# FILE : math_print.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex1 2023
# DESCRIPTION: A simple program that make some math calculuses
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody							 	      
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################

import math
def golden_ratio():  # a function that prints the golden ratio  
    print((1 + math.sqrt(5))/2)

def six_squared():   # a function that print the result of 6 square  
    print(6 ** 2)

def hypotenuse():    # a function that calculus the hypotenuse in a right triangle     
    print(math.sqrt((5 ** 2) + (12 ** 2)))

def pi():            # a function that prints the float pi
    print(math.pi)

def e():             # a function that prints the float e           
    print(math.e)

def squares_area():  # a function that prints the area of some squares   
    print((1 ** 2), (2 ** 2), (3 ** 2), (4 ** 2), (5 ** 2), 
          (6 ** 2), (7 ** 2), (8 ** 2), (9 ** 2), (10 ** 2))

if __name__ == "__main__" :
     golden_ratio()
     six_squared()
     hypotenuse()
     pi()
     e()
     squares_area()
