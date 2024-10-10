#################################################################
# FILE : hello_turtle.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex1 2023
# DESCRIPTION: A simple program that draw a fleet of two ships to the screen
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody							 	      
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################

import turtle
def draw_triangle():  # This function draw a triangle
    turtle.forward(45)
    turtle.right(120)
    turtle.forward(45)
    turtle.right(120)
    turtle.forward(45)
    turtle.right(120)
 
def draw_sail():      # This function draw a sail
    turtle.left(90)
    turtle.forward(50)
    turtle.right(150)
    draw_triangle()
    turtle.right(30)
    turtle.up()
    turtle.forward(50)
    turtle.down()
    turtle.left(90)

def draw_ship():       #This function draw a ship
    turtle.forward(50)
    draw_sail()
    turtle.forward(50)
    draw_sail()
    turtle.forward(50)
    draw_sail()
    turtle.forward(50)
    turtle.right(120)
    turtle.forward(20)
    turtle.right(60)
    turtle.forward(180)
    turtle.right(60)
    turtle.forward(20)

def draw_fleet():      # This function draw a fleet   
    draw_ship()
    turtle.left(60)
    turtle.up()
    turtle.forward(300)
    turtle.down()
    turtle.right(180)
    draw_ship()
    turtle.right(120)
    turtle.up()
    turtle.forward(300)


if __name__ == "__main__" :
    draw_fleet()
    turtle.done
    



