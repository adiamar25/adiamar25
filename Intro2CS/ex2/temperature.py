#################################################################
# FILE : temperature.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex2 2023
# DESCRIPTION: A simple program that checks the value of some
#              days temperature regarding to some specific day.
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody							 	      
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################
def is_vormir_safe(min_temp, day1_temp, day2_temp, day3_temp):
    """ A function that gets a minimum temperature value and another three
        temperature values, and checks whether or not at least two values
        are greater than the minimum value. """
    counter = 0
    if day1_temp > min_temp:
        counter += 1
    if day2_temp > min_temp:
        counter += 1
    if day3_temp > min_temp:
        counter += 1
    if counter >= 2:
        return True
    return False




