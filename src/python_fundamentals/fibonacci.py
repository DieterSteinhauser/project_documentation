# ---------------------------------------------------------
#                          NOTES
# ---------------------------------------------------------

# ---------------------------------------------------------
#                         INCLUDES
# ---------------------------------------------------------

# ---------------------------------------------------------
#                         METHODS
# ---------------------------------------------------------

sequence = {0: 0, 1: 1}


def fibonacci_of(index):
    """Calculates the fibonacci number of a given index"""

    # if we have already computed this index, return it.
    if index in sequence:
        return sequence[index]

    # Compute and store the Fibonacci number recursively
    sequence[index] = fibonacci_of(index - 1) + fibonacci_of(index - 2)
    return sequence[index]


def fibonacci_list(max_index):
    """
    Method that implements the fibonacci sequence to a given value

    :param max_index: the maximum of the for loop for fizzbuzz.
    :type max_index: int
    :return: Creates a list of max_index fibonacci numbers.
    :rtype: list
    """
    return [fibonacci_of(index) for index in range(max_index)]

# ---------------------------------------------------------
#                          MAIN
# ---------------------------------------------------------


if __name__ == "__main__":
    number = int(input("Enter a maximum number for a fibonacci sequence."))
    fibo_list = fibonacci_list(number)
    print(fibo_list)


# ---------------------------------------------------------
#                       END OF FILE
# ---------------------------------------------------------
