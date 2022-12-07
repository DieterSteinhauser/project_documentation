Using Sphinx Documentation Tools
====================================================

Sphinx is a tool that allows for automatic generation of documentation. It uses ReStructured Text files or
Markdown to create 'outlines' for documents, which then get interpreted into HTML or PDF files. In fact, you're
looking at generated Sphinx documentation right now!

.. note:: If you copied this DefaultProject folder and ran the requirements.txt, all you have to do is change
    directories to the docs folder (``cd docs``) in the terminal, then build the output files using a command such
    as ``make html``. You can make other formats of files, such as PDF, EPUB, and more!

If you are doing a fresh install of sphinx, you'll have to do a ``pip install sphinx`` create a docs folder in your
project folder (``mkdir docs``), change to the docs directory (``cd docs``) and run ``sphinx-quickstart``.

Follow the documentation creation prompts. defaults will be shown as '[y]' or '[n]'. Once this is done, you'll want
to build the documentation by running ``make html``. Do this any time you want to update the documentation.
Now in the build folder is the starter HTML pages.

****************************************
Customization
****************************************

**I recommend the following edits to the conf.py file:**

To have sphinx access folders outside the documentation folder, you'll have to change the path a bit. In my setup, I
have something like the following folder structure.

ProjectFolder
    - source_code
        * hello_world.py
    - docs
        * build
            - doctrees
            -  html
        * conf.py
        * makefile
        * make.bat
        * index.rst
        * learning_python.rst
        * getting_started.rst
        * using_sphinx.rst
        * hello_world.rst
    - venv
    - requirements.txt

To have documentation be generated based on python code in the src directory, I need to have sphinx
access the 'source_code' folder. To do this, we are going to do the following to change the sys.path to add the project
folder. This effectively changes the scope of sphinx from '../../ProjectFolder/docs' to '../../ProjectFolder'.

.. code-block:: python
   :linenos:

    # If extensions (or modules to document with autodoc) are in another directory,
    # add these directories to sys.path here. If the directory is relative to the
    # documentation root, use os.path.abspath to make it absolute, like shown here.
    #
    import os
    import sys
    if os.path.abspath('..') not in sys.path:
        sys.path.insert(0, os.path.abspath('..'))  # '..' moves up one folder, much like 'cd ..'

    print(sys.path)  # prints the sys.path for debugging


To automate you documentation creation, it's useful to have some to have these the autodoc and auto-section-label
extensions. I added some other things to my conf.py but these are the most important.

.. code-block:: python
   :linenos:

    # -- General configuration ---------------------------------------------------

    # Add any Sphinx extension module names here, as strings. They can be
    # extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
    # ones.
    extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosectionlabel', 'sphinx.ext.napoleon',
                'sphinx.ext.coverage', 'sphinx.ext.extlinks']

Finally, to further customize the look of the output files, I recommend looking into `sphinx themes <https://sphinx-themes.org/>`_.
Personally I choose the 'read the docs' theme. This was included in the pip install given in
:ref:`Getting Started with Python` and can be customized with the following.


.. code-block:: python
   :linenos:


    # -- Options for HTML output -------------------------------------------------

        # The theme to use for HTML and HTML Help pages.  See the documentation for
        # a list of builtin themes.
        #
        html_theme = 'sphinx_rtd_theme'

        # Add any paths that contain custom static files (such as style sheets) here,
        # relative to this directory. They are copied after the builtin static files,
        # so a file named "default.css" will overwrite the builtin "default.css".
        html_static_path = ['_static']


        # extra options for the read the docs theme.
        html_theme_options = {
            'analytics_id': 'G-XXXXXXXXXX',  # Provided by Google in your dashboard
            'analytics_anonymize_ip': False,
            'logo_only': False,
            'display_version': True,
            'prev_next_buttons_location': 'bottom',
            'style_external_links': False,
            'vcs_pageview_mode': '',
            'style_nav_header_background': 'seaborn',
            # Toc options
            'collapse_navigation': True,
            'sticky_navigation': True,
            'navigation_depth': 4,
            'includehidden': True,
            'titles_only': False
        }

****************************************
Further Reading
****************************************

* `Sphinx Tutorial <https://www.sphinx-doc.org/en/master/tutorial/index.html>`_
* `Sphinx Autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_
* `ReStructured Text Quick Reference <https://docutils.sourceforge.io/docs/user/rst/quickref.html#internal-hyperlink-targets>`_
* `ReStructured Text Cheat Sheet  <https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html#include-other-rst-files-with-the-toctree-directive>`_

