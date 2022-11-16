# ---------------------------------------------------------
#                          NOTES
# ---------------------------------------------------------

# ---------------------------------------------------------
#                         INCLUDES
# ---------------------------------------------------------

# ---------------------------------------------------------
#                         METHODS
# ---------------------------------------------------------

def factorial(number):
    """
    Calculates the factorial of a given number.

    :param number: integer that the user wants the factorial of.
    :type number: int
    :return: integer of the resulting factorial.
    :rtype: int
    """

    return_val = 1
    if number > 1:
        return_val = number * factorial(number - 1)

    return return_val

# ---------------------------------------------------------
#                          MAIN
# ---------------------------------------------------------


if __name__ == "__main__":
    num_user = input("Enter a number to compute a factorial")
    result = factorial(int(num_user))
    print(result)

# ---------------------------------------------------------
#                       END OF FILE
# ---------------------------------------------------------
