.. _getstarted:

Get started with Contemply
==========================

This quick tutorial will guide you through writing a simple Contemply template.


Build a template for a PyPi package
***********************************

In this tutorial, we will create a template for a PyPi package project. First let's take a look at what out
template should do:

- Create a setup.py with some basic information like package name and version
- Create a README file
- Create a requirements.txt file so we have all our dependencies
- Create a src-folder with a subfolder for our package and the __init__.py file


Get the necessary information from the user
-------------------------------------------

Before creating files and folders, we will collect all necessary information from the user.

.. code-block:: contemply

    #::
    echo("Welcome, let's start creating our package!")

    pkg_name = ask("What is the name of your package?")
    pkg_version = ask("What is the version of your package?")
    author_name = ask("What is the package author's name?")

As you can see, :py:func:`echo` let's you output a message to the console. We use it here, to greet the user.
The next thre lines make use of the :py:func:`ask` function to retrieve information from the user.
"Ask" will simply show an input prompt with a message and return the user's input as a string.

Before continuing, we will reformat the user input. We will create a valid package name by replacing spaces with a
dash using the :py:func:`replace` function. Of course more reformatting will be necessary in a real world case, take
a look at Contemply's string functions for more ways of manipulating strings.

We will also use the ask-function again to prompt the user for a short package description.

.. code-block:: contemply

    pkg_name_clean = replace(pkg_name, " ", "-")
    description = ask("Describe your package in a few words:")

Describe

.. code-block:: contemply

    status = ["1 - Planning", "2 - Pre-Alpha", "3 - Alpha", "4 - Beta", "5 - Production/Stable"]
    pkg_status = choose("What is the status of your package?", status)


Describe


.. code-block:: contemply

    requirements = []
    while True
        answer = ask("Name of the required package:")
        if answer == ""
            break
        else
            requirements += answer
        endif
    endwhile
    #::


Create all files and folders
----------------------------

.. code-block:: contemply

    #: >> "setup.py"
    import setuptools

    with open('README.md', 'r') as fh:
        long_description = fh.read()

    requirements = []
    with open('requirements.txt', 'r') as fh:
        for line in fh:
            requirements.append(line)

    setuptools.setup(
        name='$pkg_name_clean',
        version='$pkg_version',
        packages=setuptools.find_packages('src'),
        package_dir={'': 'src'},
        classifiers=[
            '$pkg_status'
        ],

        author='$author_name'
    )
    #: <<

    #: >> "README.md"
    # $pkg_name
    $description
    #: >>

    #: >> "requirements.txt"
    #: for req in requirements
    $req
    #: endfor
    #: >>

    #% Last thing to do: create source folder
    #: makeFolders("src/$pkg_name_clean")

    #% and write empty init file
    #: >> "src/$pkg_name_clean/__init__.py"

    #: <<


Use Storage to gain quick access to our template
------------------------------------------------

