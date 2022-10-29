# ---------------------------------------------------------
#                          NOTES
# ---------------------------------------------------------

# ---------------------------------------------------------
#                         INCLUDES
# ---------------------------------------------------------

# ---------------------------------------------------------
#                         METHODS
# ---------------------------------------------------------


def say_hello(target='World'):
    """
    Python method that says hello to a target

    :param target: A target to direct your greeting. Defaults to 'World' if target is not specified
    :type target: str
    :return: Prints 'Hello World!' in the console.
    :rtype: None
    """
    print(f"Hello {target}!")
    return None


# ---------------------------------------------------------
#                          MAIN
# ---------------------------------------------------------


if __name__ == "__main__":
    say_hello()
    name = input("Who do I have the pleasure of speaking to?")
    say_hello(name)

# ---------------------------------------------------------
#                       END OF FILE
# ---------------------------------------------------------
