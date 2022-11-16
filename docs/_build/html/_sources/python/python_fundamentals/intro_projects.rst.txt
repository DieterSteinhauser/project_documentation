Novice and Introductory Projects
====================================================

Hello World
--------------------------

All programmers start off with two simple words: 'Hello World!'

This is a nice and friendly introduction to the programming environment and language. We can make python say this by
doing the following in the python console.

.. code-block:: python
   :linenos:

      print("Hello World!")

We can improve upon this by creating a function. This function will do the following:

.. automodule:: src.python_fundamentals.hello_world
   :members:



For this assignment do the following:

- Create a method that implements the function described above.
- Have your program say hello to the world.
- have your program ask who you are.
- have your program say hello to you directly.


Solution
*********
:ref:`Hello World Solution`


Weight Calculator
--------------------------

Have the terminal ask how the mass of an object on earth in kilograms. Then calculate how much it would weigh
on all planets in the solar system and the moon. Have the program nicely print the results.

Consider creating a method with the following functionality to streamline the process.

.. automodule:: src.python_fundamentals.weight_calculator
   :members:



.. list-table:: Gravitational Force on Different Planets
   :header-rows: 1

   * - Name
     - Gravitational Force (G)

   * - Mercury
     - 0.38

   * - Venus
     - 0.9

   * - Earth
     - 1

   * - Moon
     - 0.17

   * - Mars
     - 0.38

   * - Jupiter
     - 2.53

   * - Saturn
     - 1.07

   * - Uranus
     - 0.89

   * - Neptune
     - 1.14



Solution
*********
:ref:`Weight Calculator Solution`



Fibonacci Sequence
--------------------------

Create a function that implements the fibonacci sequence to a number specified by the user.
Have your program ask the user how many numbers they wish to calculate and print a list of the numbers.

The fibonacci sequence is as follows:

.. math:: 0, 1, 1, 2, 3, 5, 8, ....

Which can be represented as:

.. math:: F(n) = F(n-1) + F(n-2)

|

The following methods could be implemented to return the fibonacci sequence.


.. automodule:: src.python_fundamentals.fibonacci
   :members:

.. note:: You may choose to implement the fibonacci method using recursion, a function that calls itself. This is
   one of many ways to handle this. It is not required to implement a recursive function, but you may find it easier to
   understand.

Solution
*********
:ref:`Fibonacci Sequence Solution`


Fizz Buzz
--------------------------

Implement the common fizz buzz programming question.
Have a program that asks the user for a maximum number for the fizz buzz loop.

- Iterate through a loop from 1 to a maximum number.
- For each number divisible by three, print 'Fizz'
- For each number divisible by five, print 'Buzz'
- For each number divisible by both three and five, print 'FizzBuzz'
- Otherwise print the index of the loop.


.. automodule:: src.python_fundamentals.fizzbuzz
   :members:

Solution
*********
:ref:`Fizz Buzz Solution`

