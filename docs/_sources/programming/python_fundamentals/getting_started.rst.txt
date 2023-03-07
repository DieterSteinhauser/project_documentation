Getting Started with Python
====================================================

Make sure to install `Python <https://www.python.org/downloads/>`_ on your computer, preferably version 3.7  or later.
You'll also want a development environment (IDE) to write and debug code. For beginners, I'd recommend `PyCharm <https://www.jetbrains.com/pycharm/download/#section=windows>`_
and for more advanced users, try using `VScode <https://code.visualstudio.com/Download>`_. Alongside these, you may
want to install `Notepad++ <https://notepad-plus-plus.org/downloads/>`_ to add another tool to your toolbox of editing
files and programs.

.. warning:: You may use notepad or whatever text editor you choose, but know that errors will be much harder
    to detect without a proper development environment. The hardest to detect being Tabs vs Spaces. If you
    use a mixture of tabs and spaces in python, your code will not run. Python much prefers spaces and IDE's
    make the TAB key enter four spaces by default to avoid this issue.

You can run python without any of these tools by using the ``python`` command in the terminal.
This can be used to run a specific script using a command like ``python  c:\folder\with\code\run_me.py`` or simply
opening the python console with ``python`` This is useful for testing small snippets of code. The same can be done
with the IDLE application.

.. Note:: If your application of python is for statistics and graphing, similar to use of R or Matlab, you may want to
    consider using `Jupyter Notebooks <https://jupyter.org/install>`_. Jupyter allows for sectioning of code for
    creating graphs and tables inline with markdown sections, allowing you to export your work as a neatly formed PDF.

Once Python and an IDE is installed, go to the terminal and run ``python -m pip install --upgrade pip``
to update the pip package manager. If not already installed with your version of python, download pip by running
``python get-pip.py`` in the terminal and attempt the previous command.

.. Note:: Pip is a useful tool to extend the functionality of python with packages. Once installed, python packages can be
    installed as needed by writing ``pip install <desired_package>``. We will revisit specific packages at a later point.

After installing the package manager, go ahead and install these packages:
``python -m pip install numpy scipy ipython jupyter lxml openpyxl pylint pytest pandas matplotlib seaborn paramiko requests sphinx sphinx_rtd_theme``


.. Note:: If you copied the DefaultProject folder and are using it for your new project,
    there is a requirements.txt file in the project. you can run ``pip install -r requirements.txt`` to download
    every package specified in the file. Installing the requirements.txt file is a common practice if you are hopping
    onto an existing project and need to setup your environment.

Great! Now your environment is setup! If you have interest in setting up documentation for your project, advance to
the :ref:`Using Sphinx Documentation Tools` page.

****************************************
Further Reading
****************************************

* `Python Documentation <https://docs.python.org/3/>`_
* `PIP Documentation <https://pip.pypa.io/en/stable/>`_
* `Automate the Boring Stuff by Al Sweigart <https://automatetheboringstuff.com/>`_
* `Free Python Books <https://pythonbooks.org/free-books/>`_
* `Python Anti-Patterns <https://docs.quantifiedcode.com/python-anti-patterns/>`_




