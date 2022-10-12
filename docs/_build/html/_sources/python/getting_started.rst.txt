Getting Started with Python
====================================================

Make sure to install `Python <https://www.python.org/downloads/>`_ on your computer, preferably version 3.7  or later.
You'll also want a development environment (IDE) to write and debug code. For beginners, I'd recommend `PyCharm <https://www.jetbrains.com/pycharm/download/#section=windows>`_
and for more advanced users, try using `VScode <https://code.visualstudio.com/Download>`_. Alongside these, you may
want to install `Notepad++ <https://notepad-plus-plus.org/downloads/>`_ to add another tool to your toolbox of editing
files and programs.

.. Note:: If your application of python is for statistics and graphing, similar to use of R or Matlab, you may want to
    consider using `Jupyter Notebooks <https://jupyter.org/install>`_. Jupyter allows for sectioning of code for
    creating graphs and tables inline with markdown sections, allowing you to export your work as a neatly formed PDF.

Once Python and an IDE is installed, go to the terminal and run ``python -m pip install --upgrade pip``
to update the pip package manager. If not already installed with your version of python, download pip by running
``python get-pip.py`` in the terminal and attempt the previous command.

.. Note:: Pip is a useful tool to extend the functionality of python with packages. Once installed, python packages can be
    installed as needed by writing ``pip install <desired_package>``. We will revisit packages at a later point.

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

* `Python Anti-Patterns <https://docs.quantifiedcode.com/python-anti-patterns/>`_



