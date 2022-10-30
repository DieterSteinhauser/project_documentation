# ---------------------------------------------------------
#                          NOTES
# ---------------------------------------------------------

# ---------------------------------------------------------
#                         INCLUDES
# ---------------------------------------------------------

# ---------------------------------------------------------
#                         METHODS
# ---------------------------------------------------------


def fizzbuzz(max_index):
    """
    Method that implements the fizzbuzz problem

    :param max_index: the maximum of the for loop for fizzbuzz.
    :type max_index: int
    :return: Prints max_index amount of statements in the console.
    :rtype: None
    """
    triggers = {3: 'Fizz', 5: 'Buzz'}

    for index in range(1, max_index):
        return_str = ''

        for trigger, value in triggers.items():
            if index % trigger == 0:
                return_str += value

        if return_str == '':
            return_str = index

        print(return_str)

# ---------------------------------------------------------
#                          MAIN
# ---------------------------------------------------------


if __name__ == "__main__":
    number = int(input("Enter a maximum number for fizzbuzz."))
    fizzbuzz(number)

# ---------------------------------------------------------
#                       END OF FILE
# ---------------------------------------------------------
