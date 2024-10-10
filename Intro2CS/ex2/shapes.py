#################################################################
# FILE : shapes.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex2 2023
# DESCRIPTION: A simple program that calculates the area of some shapes.
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody							 	      
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################
import math
def shape_area():
    """ A function that gets a shape and measurements from
        the user and returns the value of its area. """
    user_shape = input("Choose shape (1=circle, 2=rectangle, 3=triangle): ")
    # Checks the user choice, and returns a area value according that
    if user_shape == "1":
        circle_radius = input()
        circle_area = math.pi * (float(circle_radius) ** 2)
        return circle_area
    elif user_shape == "2":
        sides_length = input()
        sides_width = input()
        rectangle_area = float(sides_length) * float(sides_width)
        return rectangle_area
    elif user_shape == "3":
        # The tringle is an equilateral triangle
        triangle_sides = input()
        triangle_area = ((3 ** 0.5) * (float(triangle_sides) ** 2)) / 4    
        return triangle_area 
    # Make sure the user inserted a valid number    
    else:
        return None
    