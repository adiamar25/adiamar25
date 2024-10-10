#################################################################
# FILE : largest_and_smallest.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex2 2023
# DESCRIPTION: A simple program that returns the maximum value
#              and the minimum value of a given numbers set.
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody							 	      
# WEB PAGES I USED: None
# NOTES: i chose two inputs for the check_largest_and_smallest function.
#        the first one because i wanted check whether the
#        "largest_and_smallest" function works well even if all the
#        numbers are equals, although there is no distincted max or min
#        value. i chose the other test to check whether the function 
#        react well to negative numbers as well.
#################################################################
def largest_and_smallest(num1, num2, num3):
    """ A function that gets three numbers
        and return the largest num, then the smallest num. """
    biggest_num = num1
    smallest_num = num1
    # Checks if num1 is really the biggest number, or some other number
    if num2 > num1:    
        biggest_num = num2
        if num3 > num2:
            biggest_num = num3
    elif num3 > num1:
        biggest_num = num3
        # Checks if num1 is really the smallest number, or some other number
    if num2 < num1:   
        smallest_num = num2
        if num3 < num2:
            smallest_num = num3
    elif num3 < num1:
        smallest_num = num3
        
    return biggest_num, smallest_num

def check_largest_and_smallest():
    counter = 0
    max_val, min_val = largest_and_smallest(17, 1, 6)
    if max_val == 17 and min_val == 1:
        counter += 1
    max_val, min_val = largest_and_smallest(1, 17, 6)
    if max_val == 17 and min_val == 1:
        counter += 1  
    max_val, min_val = largest_and_smallest(1, 1, 2)
    if max_val == 2 and min_val == 1:
        counter += 1
    max_val, min_val = largest_and_smallest(17, 17, 17)
    if max_val == 17 and min_val == 17:
        counter += 1
    max_val, min_val = largest_and_smallest(-15, -14, 0)
    if max_val == 0 and min_val == -15:
        counter += 1
    if counter == 5:
        return True
    return False


    
    


        
        