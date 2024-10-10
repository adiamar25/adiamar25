#################################################################
# FILE : quadratic_equation.py
# WRITER : Adi Amar , adi.amar1 , 315244624
# EXERCISE : intro2cs1 ex2 2023
# DESCRIPTION: A simple program that solves quadratic equations.
# STUDENTS I DISCUSSED THE EXERCISE WITH: Nobody							 	      
# WEB PAGES I USED: None
# NOTES: Nothing special
#################################################################
def quadratic_equation(a, b, c):
    """ A function that gets three numbers represents coefficients
        and solves the suitable quadratic equation. """
    x1 = (-b + ((b**2) - 4*a*c)**0.5) / (2*a)
    x2 = (-b - ((b**2) - 4*a*c)**0.5) / (2*a)
    if type(x1) == float and type(x2) == float:
        if x1 != x2:
            return x1, x2
        return x1, None
    elif type(x1) == float and type(x2) != float:
        return x1, None
    elif type(x1) != float and type(x2) == float:
        return None, x2
    elif type(x1) != float and type(x2) != float:
        return None, None
    
def quadratic_equation_user_input():
    """ A function that gets coefficients from the user, 
    prints the solutions number of the suitable quadratic equation
    and the solutions themselves. """
    user_coefficients = input("Insert coefficients a, b, and c: ")
    # saving the coefficients inserted by the user into a variables
    a, b, c = user_coefficients.split()  
    a = float(a)
    b = float(b)
    c = float(c)
    if a == 0:
        print("The parameter 'a' may not equal 0")
    else:
        # Calling the quadratic_equation function
        # and save the solution into variables
        equation_sol1, equation_sol2 = quadratic_equation(a, b, c) 
        # The next couple lines checks how many solution the equation has
        if equation_sol1 == None and equation_sol2 != None:
            print("The equation has 1 solution:", equation_sol2)
        elif equation_sol2 == None and equation_sol1 != None:
            print("The equation has 1 solution:", equation_sol1)
        elif equation_sol1 == None and equation_sol2 == None:
            print("The equation has no solutions")
        else:
            print("The equation has 2 solutions:",
                  equation_sol1, "and", equation_sol2)
            
