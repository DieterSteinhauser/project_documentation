Basics of Python Programming
====================================================

Hello! Welcome to Python!

The Python language is used for a variety of tasks, from statistical analysis, machine learning,
scripting, and much more. It is a Dynamically typed, interpreted language that gets its name from monty python.

Expressions
--------------------------

An expression in programming is the combination of values and operators without assignment. This can be done
with any number of constants or variables.

**For example:**

    .. code-block:: python
       :linenos:

       2 + 2

.. admonition:: Try it!

    Open the python console and preform calculations using the following operators. You can also see
    how it functions by reading `Chapter 3 of the Python Documentation. <https://docs.python.org/3/tutorial/introduction.html>`_



.. list-table:: Table of Arithmetic Operators
   :header-rows: 1

   * - Operator
     - Operation
     - Example
     - Result

   * - **
     - Exponent
     - 2 ** 3
     - 8

   * - %
     - Modulus/remainder
     - 22 % 8
     - 6

   * - //
     - Integer division/floored quotient
     - 22 // 8
     - 2

   * - /
     - Division
     - 22 / 8
     - 2.75

   * - \*
     - Multiplication
     - 3 * 5
     - 15

   * - \-
     - Subtraction
     - 5 - 2
     - 3

   * - \+
     - Addition
     - 2 + 2
     - 4



Variables and Assignment
--------------------------

Assigning values to variable name will create an environment variable.
Variable names must start with a letter and can have any combo of
letters, digits, and underscores. This is true for most languages.

    .. code-block:: python
       :linenos:

       # Assignment evaluates an expression seen on the right and stores the result in the variable.
        my_int = 2 + 2


.. admonition:: Assignment Operators

    It is also possible to perform an operation and assign a value in one statement if the input and output variable are
    the same.

   .. code-block:: python
       :linenos:

       my_int = 1
       my_int = my_int + 1  # Adds my_int and 1 and overwrites my_int. Value is now 2.
       my_int += 1          # Adds the right expression to my_int and assigns it to my_int. Value is now 3.


Naming Conventions
**************************

There are two main conventions of naming useful variables.
**CamelCase:** no spaces and the first letter of a word is capitalized.
**snake_case:** no capitals, all words are separated by underscores

Both have positives and negatives camel case looks weird if there are
single letter words or abbreviations that need to be capitalized.
CamelCase generally produces shorter length names.
snake_case is sort of the opposite, no problem with words but gets lengthy.

For Example:
    UFAESDataset vs uf_aes_dataset

.. tip:: One is not better than the other. The key to programming is staying consistent.

In python, classes generally follow the CamelCase convention, with every other object, variable, and function
being snake_case.

Data Representation
--------------------------

Data to a computer is stored as ones and zeros in the form of binary.
One digit of binary is called a **BIT**, 4 BITS are called a **NIBBLE**, and 8 BITS
are called a **BYTE**. Programmers think they're so funny.

While it is cool to understand binary, programming in binary is quite tedious.
Instead, we interpret Bytes of data to mean some other value.
This is done in a number of ways, but perhaps easiest to understand with an
integer (whole number).

22 = (10^1)*2 + (10^0)*2 = 20 + 2 = 22

In binary, each bit represents (2^n-1) where n is the position from right to
left. For example, take the nibble 0b1001:

0b1001 = (2^3)*1 + (2^2)*0 + (2^1)*0 + (2^0)*1 = 8 + 1 = 9

.. Note:: 0b is added to identify binary data.
    0b1001 can also be represented as 0b00001001, a full byte by adding four zeros in front.
    This is called padding.

Binary and Base-10 are not the only ways to represent a number, there is also
hexadecimal (hex) which is in base-16. Hex is useful for understanding certain
applications. It has values from 0 to 15 with A-F representing 10-15.


.. list-table:: Hex Conversion
   :header-rows: 1

   * - Hex
     - Decimal
   * - 0-9
     - 0-9
   * - A
     - 10
   * - B
     - 11
   * - C
     - 12
   * - D
     - 13
   * - E
     - 14
   * - F
     - 15


Why is this important?
**************************

Every language has different use of bytes for data by default. Understanding bits and bytes of data will
enable you to use bitwise operators, potentially creating more efficient code.

Since python is a dynamic language, bit and byte operations are less prevalent and data allocated to variables can
change as needed. Python will interpret how much is needed based on the context.

.. list-table:: Table of Bitwise Operators
   :header-rows: 1

   * - Operator
     - Operation
     - Example
     - Result

   * - &
     - AND
     - 2 & 3
     - 2

   * - |
     - OR
     - 2 | 3
     - 3

   * - ~
     - NOT
     - ~2
     - -3

   * - ^
     - XOR
     - 2 ^ 3
     - 1

   * - >>
     - Shift Right
     - 4 >> 1
     - 2

   * - <<
     - Shift Left
     - 4 << 1
     - 8


Data Types
--------------------------

Traditionally speaking, all languages use these data types or
extensions of them:

.. list-table:: Table of Data Types
   :header-rows: 1

   * - Name
     - Use
     - Example
     - Size

   * - String
     - Alphanumeric characters
     - 'hello world'
     - Byte/character

   * - Integer
     - Whole numbers
     - 22
     - usually 4 bytes

   * - Float
     - Number with a decimal point
     - 3.1415
     - 4 bytes

   * - Character
     - Single alphanumeric character
     - 'D'
     - 1 byte

   * - Boolean
     - Representing logical values
     - TRUE, FALSE
     - 1-2 bytes

   * - None
     - represents absence
     - None
     - NA

What do I mean by extensions? well lets say an integer was one byte
that would give me 256 possible values, but what if my number is 300?
data types sometimes have shorter and longer versions of themselves to
account for this issue.

An Integer is traditionally 4 bytes, so:

A short int would be 2 bytes

A long int would be 4 bytes

A long long int would be 8 bytes

8 bytes sounds like a meal to me. (I'm sorry, bad joke).

A Double is a 64bit/8byte floating point value.It is called a double because the added 4 bytes,
creating a 'double precision floating point' value.

.. note:: All decimal numbers use `IEEE 754 <https://en.wikipedia.org/wiki/IEEE_754/>`_ floating point since digital
    computers don't naturally understand fractions. Cool stuff if you want a rabbit hole.

Strings
--------------------------
Strings are also an array of characters, and can be treated as such for taking only parts of a string.
However, python has more sophisticated methods of augmenting a string that may be more explicit as to the operation.

.. seealso:: I won't go in complete detail as to how strings can be used, so look at
    `Python's Documentation on Strings. <https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str>`_

Strings have may ways to be formatted, and can use both single and double quotes. when trying to use the literal single
or double quotes, you can 'escape' with an escape character.


.. list-table:: Built In Python Data Structures
   :header-rows: 1

   * - Name
     - Use
   * - \'
     - Single Quote
   * - \"
     - double Quote
   * - \\
     - backslash
   * - \n
     - New Line
   * - \r
     - Carriage Return
   * - \t
     - Tab
   * - \f
     - Form Feed
   * - \o
     - Octal Value
   * - \x
     - Hex Value


.. tip:: The easiest way to compose strings is by using a formatted string by
    adding a prefix f to a string declaration. For example:

    .. code-block:: python
       :linenos:

       bacon_count = 4
       breakfast = f"We have {bacon_count} strips of bacon."


Type Casting
--------------------------

Some types of data need to be cast to another type of data for proper functionality of code. Type casting is done by
enclosing an expression within parentheses, preceded by a type. For example:

.. code-block:: python
   :linenos:

   spam = float(3)    # spam will evaluate to 3.0
   eggs = int(4.6)    # eggs will be rounded down to 4, regardless of the decimal.
   breakfast = "Breakfast is " + str(eggs) + " eggs."

Comments
--------------------------

.. Note:: **Comments** are a way to describe the functionality and purpose of your code.
    the best comments explain why the code functions, and good comments explain what the code does.

.. code-block:: python
   :linenos:

   # lines that start with a pound sign are comments
   # commented out code is a very common way to debug without loss of work

Logic and Flow Control
--------------------------

All programs run off of logic provided by the developer. this is done using a variety of methods, but the most
common is if, else logic, for loops, and while loops.

.. list-table:: Table of Logical and Comparison Operators
   :header-rows: 1

   * - Operator
     - Operation
     - Example
     - Result

   * - ==
     - Equal to
     - 2 == 3
     - False

   * - !=
     - Not equal to
     - 2 != 3
     - True

   * - >
     - Greater than
     - 2 > 3
     - False

   * - >=
     - Greater than or equal to
     - 2 >= 3
     - False

   * - <
     - Less than
     - 2 < 3
     - True

   * - <=
     - Less than or equal to
     - 2 <= 3
     - True

   * - and
     - True if both are true
     - True and False
     - False

   * - or
     - True if one is true
     - True or False
     - False

   * - not
     - Negate result
     - not(False)
     - True

   * - is
     - True if both are the same object
     - False is False
     - True

   * - in
     - True if value found in sequence
     - 5 in [4, 5, 6, 7]
     - True


If statements evaluate the logic of a statement and execute commands based on the result. Else-if Statements (elif) can
be inserted within logic to check more parameters.

.. code-block:: python
   :linenos:

   x = 5
   elements = [4, 5, 6, 7]

   if x in elements:
       print(f'found {x} in {elements}!')
   else:
       print(f'{x} was not found in {elements}')

Iteration is best done using for or while loops, depending on the task. While loops find better usage for continuous
iteration until there is a break point reached.

.. code-block:: python
   :linenos:

   # index based loops use the range key
   for index in range(10):
       print(index)

   # while loop that does the same thing
   index = 0
   while(index < 10):
       print(index)
       index += 1

   # for each based loops iterate a data structure
   elements = [4, 5, 6, 7]
   for element in elements:
       print(element)

.. seealso:: There are more logical statements for evaluating program operations in
    `Python Documentation CH4: Flow Control <https://docs.python.org/3/tutorial/controlflow.html>`_ to learn about more
    specific operations.

Functions and Methods
--------------------------

Functions and methods are synonymous in that they are a call to a piece of code and can be defined in the following
ways:

.. code-block:: python
   :linenos:

    # function anatomy
    def function_structure(input1: type_suggestion, input2......) -> Return_type_suggestion:
    """
        Docstring of the Function, Defines what it does and what it's inputs/outputs are.
        :param input1: define input1
        :type input1: input1 type
        :return: define the return of the function
        :rtype: return type

    """
        return_val = 1
        # some code that does something
        return return_val


    # --------------------------
    # A function with no inputs or outputs
    def do_nothing():
    """A method that does nothing, taking no inputs or outputs."""
        pass


    # --------------------------
    # documentation best practice function
    def add(a: int, b: int) -> int:
    """Add two integers together.
       :param a: integer A.
       :type a: int
       :param b: integer B.
       :type b: int
       :return: a summation of integer A and B.
       :rtype: int
    """
        sum = a + b
        return sum



    # --------------------------
    # valid function with no documentation
    def subtract(a, b):
        return a - b



    # --------------------------
    # Execution of above functions
    x = 5
    y = 3
    add(x, y)
    subtract(x, y)

.. attention:: Indentation is critical in python as function boundaries are based on indentation level.

Functions provide inputs and outputs as needed. Type hints for the inputs and outputs are possible but not required in
python, they're more like type suggestions. Docstrings of a function are also not required, but a best practice, and work
well with :ref:`Using Sphinx Documentation Tools`. It is also a best practice to have a return statement for each function
but is also not necessary unless the function is returning a value.

.. note:: Anytime some name has parentheses following it, it is recognized as a function call in python.

Data Structures
--------------------------

The following are referred to as data structures, something that is a
container for data. Everything in python is an object/data structure, even the previously mentioned data types.



.. list-table:: Built In Python Data Structures
   :header-rows: 1

   * - Name
     - Use
     - Example
     - Mutable

   * - bool
     - Boolean logical value
     - TRUE, FALSE
     - NO

   * - int
     - integer numbers
     - 22
     - NO

   * - float
     - floating point number
     - 3.1415
     - NO

   * - String
     - Alphanumeric character string
     - 'hello world'
     - NO

   * - list
     - sequence of objects
     - [1, 2, 3, 3]
     - YES

   * - tuple
     - sequence of objects
     - (1, 2, 3, 3)
     - NO

   * - dict
     - dictionary/map of associated objects
     - {'apple': 'red', 'banana': 'yellow'}
     - YES

   * - set
     - unordered set of distinct objects
     - [1, 2, 3]
     - YES

   * - frozenset
     - unordered set of distinct objects
     - [1, 2, 3]
     - NO


What is Mutability?
***********************

An object that is **mutable** is one that can be edited in some way without assignment. An **immutable** object
cannot be changed without assignment. The most common immutable objects are integers and strings. For example:

.. code-block:: python
    :linenos:

    foo = 4                # 4 is assigned to variable foo
    foo + 1                # evaluates to 5, but foo remains 4 without assignment
    print(foo)
    bar = 3                # 3 is assigned to variable bar
    bar = foo + bar        # 7 is assigned ot the variable bar
    print(bar)
    my_list = [foo, bar]   # list of [4, 3] assigned to my_list
    baz = 2                # 2 is assigned to variable baz
    my_list.append(baz)    # My_list was appended as it is mutable, and is now [4, 3, 2]
    print(my_list)


.. seealso:: I highly recommend looking at the `Python Documentation CH5: Built-in Data Structures <https://docs.python.org/3/tutorial/datastructures.html>`_
    to understand the ways data structures can be utilized.


.. admonition:: Try it!

    Open the python console and try using some data structures. You can also see
    how some function by reading the later parts in
    `Chapter 3 of the Python Documentation. <https://docs.python.org/3/tutorial/introduction.html>`_


Modules
--------------------------

Modules are extensions on your program that you can add to interact with packages or other python code that you've created.
Imports of modules allow for cleaner code and expand functionality past the standard python library. You may import
modules if a few different ways:

.. code-block:: python
   :linenos:

   import os                           # direct import, calls would require the name, e.g. os.path()
   from fibo import fib, fib2          # import specific functions
   from math import *                  # imports all methods from the module, this can be troublesome.
   import numpy as np                  # imports numpy module but renames the call to np. e.g. np.array()
   from \path\to\my\module import add  # import function from a local module, good for segmenting code.

There are many useful libraries but this should get you started.


General Use
*******************************
- os
- sys
- path
- pprint

Higher Level Programming
*******************************************
- datalclasses
- collections
- re
- sphinx
- typing
- csv
- json
- requests

Math, Statistics, and Plotting
*******************************
- scipy
- pandas
- statistics
- matplotlib
- sympy
- seaborn
- numpy

Machine Learning/Image Processing
***********************************
- tensorflow
- pytorch
- opencv Python

Command Line Interface
*******************************
- typer
- argparse
- click

Graphical User Interface
*******************************
- pysfml
- tkinter
- kivy

Input and Output
--------------------------

Input and Output (IO) is a key pillar of all programming. Dataset interaction and user interaction are pertinent for
most programs. for simple command line IO, consider the following example:

.. code-block:: python
   :linenos:

   print('What is your name?')
   name = input()
   print(f'Nice to meet you {name}!')

   # same as above, but the input can print the question string.
   name = input('What is your name?')
   print(f'Nice to meet you {name}!')

You can also interact with files on the computer by doing the following:

.. code-block:: python
   :linenos:

   # puts contents of the data into memory under the variable read_data
   with open('path\to\file.txt', 'r', encoding="utf-8") as f:
       read_data = f.read()

   # writes contents of the data to disk
   with open("path\to\test.txt",'w',encoding = 'utf-8') as f:
       f.write("my first line\n")
       f.write("This file\n\n")
       f.write("has three lines\n")

   # append contents of the data to disk
   with open("path\to\test.txt",'a',encoding = 'utf-8') as f:
       f.write("Now it has four lines\n")

.. tip:: I highly recommend csv and json modules for writing to those file types. The general structure of reading/writing
    is the same, with the benefit of nicely formatted code. Pandas is also a useful module as it can further automate
    file IO.

.. seealso:: For more information on python inputs and outputs checkout
    `Python Documentation CH7: Input and Output. <https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files>`_


