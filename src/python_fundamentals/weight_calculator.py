# ---------------------------------------------------------
#                          NOTES
# ---------------------------------------------------------

# ---------------------------------------------------------
#                         INCLUDES
# ---------------------------------------------------------

# ---------------------------------------------------------
#                         METHODS
# ---------------------------------------------------------

planet_forces = {'Mercury': 0.38,
                 'Venus': 0.9,
                 'Earth': 1,
                 'Moon': 0.17,
                 'Mars': 0.38,
                 'Jupiter': 2.53,
                 'Saturn': 1.07,
                 'Uranus': 0.89,
                 'Neptune': 1.14
                 }


def print_weights(mass: float) -> None:
    """
    Print the weights of the object on each planet for a given mass.

    :param mass: mass of the object
    :type mass: float
    :return: Prints weights on each of the planets and moon.
    :rtype: None
    """
    print('This is your weight on each planet:')
    for planet, force in planet_forces.items():
        print(f'{planet}: {round(force*mass, 2)}Kg')

# ---------------------------------------------------------
#                          MAIN
# ---------------------------------------------------------


if __name__ == "__main__":
    user_mass = input("Enter a mass in kilograms")
    print_weights(float(user_mass))

# ---------------------------------------------------------
#                       END OF FILE
# ---------------------------------------------------------
