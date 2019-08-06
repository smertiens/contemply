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
- Create a src-folder with a subfolder for our package and the __init__.py file (if the user wants that)

You can find the complete template in the samples-folder:
https://github.com/smertiens/contemply/blob/develop/src/contemply/samples/pypackage.pytpl


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

    #::
    pkg_name_clean = replace(pkg_name, " ", "-")
    description = ask("Describe your package in a few words:")

.. warning:: You will see, that each code block in this tutorial starts with '#::', this is only necessary for the
        syntax highlighting to work. You only need to set it once, see :ref:`commandblocks` for details.

Let's give our new template a test drive. Open a terminal and navigate to the folder where you have saved the template,
and run it by entering:

::

    contemply run mytemplate.pytpl

Instead of mytemplate.pytpl you have to use your template name of course. In this example, the template has a "pytpl"
extension, in fact you can use any kind of filename or extension or even no extension for your templates. Contemply
doesn't care. If we have done everything correctly, you will be asked for a package name version, your name and a package
description.

**Task:**: Try checking your package's clean name for proper string replacement by echoing "pkg_name_clean".

Now that everything seems to work, we also want to allow our user to choose the initial status of the pip package.
Since there are predefined values for
this property we show the options as a list to choose from. We can also see that Contemply supports simple lists (see
:ref:`lists` for details). The :py:func:`choose` function will then get the chosen option from the user.
The last line in this code blocks asks the user, whether a src-folder should be created using :py:func:`yesno`.

.. code-block:: contemply

    #::
    status = ["1 - Planning", "2 - Pre-Alpha", "3 - Alpha", "4 - Beta", "5 - Production/Stable"]
    pkg_status = choose("What is the status of your package?", status)
    create_src_folder = yesno('Create source folder?', 'yes')

Before we put everything together we will ask the user about required packages. Since we can not be sure about
the number of packages that should be added, we will use :ref:`whileloops` to add multiple dependencies until the
user enters an empty string.


.. code-block:: contemply

    #::
    requirements = []
    echo("You can add required packages now. Hit enter to finish this step.")
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

First of all we will create the setup.py file and the README.md. We will use multifile syntax to write the all the lines
to the correct files (see :ref:`multifile` for details). Note that you can insert variables by prepending a $.

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

    #::
    >> "README.md"
        -> "# $pkg_name"
        -> "$description"
    <<

In this example you can also see, that there are several ways to add content to a file. If you want to stay within a
command block, use the "->" operator followed by a string to add the string contents as a new line to the current file.
If you write content outside of command blocks, they will automatically be added to the current file.
If no file is specified, Contemply will ask for a filename to write to after running the template.

To create the requirements.txt file (which is basically one required package per line) we use :ref:`forloops` to iterate
over every element in our requirements list. Note that the $-syntax for variables does not only work on content lines
but also inside of most string parameters (like :py:func:`makeFolders`).
We also use an if-clause to check, wether we should create a src-folder.

.. code-block:: contemply

    #::
    >> "requirements.txt"
    for req in requirements
        -> "$req"
    endfor
    <<

    #% Last thing to do: create source folder
    if create_src_folder
        makeFolders("src/$pkg_name_clean")

        #% and write empty init file
        >> "src/$pkg_name_clean/__init__.py"
            -> ""
        <<
    endif



Use Storage to gain quick access to your template
-------------------------------------------------

Take a look at :ref:`storage` to find out how to access your templates in a quick and easy way.