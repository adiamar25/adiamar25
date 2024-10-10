#################################################################
# FILE : calculate_mathematical_expression.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex2 2023
# DESCRIPTION: A simple program that make some math calculuses
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody							 	      
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################
def calculate_mathematical_expression(num1, num2, math_operator):
    """ A function that gets to numbers and a math operator in string type,
        and return a value according to the math operator it gets. """
    # Checks if the function got an illeagal math operator
    if math_operator not in "+-*:":   
        return None    
    if math_operator == "+":
        return num1 + num2
    elif math_operator == "*":
        return num1 * num2
    elif math_operator == "-":
        return num1 - num2
    elif math_operator == ":":
        # Make sure we don't divide by zero
        if int(num2) == 0:             
            return None
        return num1 / num2
    
def calculate_from_string(math_expression):
    """ A function that gets a string which contains a math expression,
        and return the sum of this expression. """
    first_num, math_oper, sec_num = math_expression.split()
    return calculate_mathematical_expression(float(first_num),
                                             float(sec_num), math_oper)
    
