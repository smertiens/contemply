Template Syntax
===============

Contemply templates consist of a text single file. It contains all information necessary to create
your files and folders. 
Contemply templates can be created and edited with every texteditor.

Basic template structure
************************

A template consists of two basic things, a **section header** and the **file template** itself.
If you want to create more than one file in your template (e.g. a boilerplate index.html and a default CSS file)
you will need a section header for every file you want to create.
Let's take a closer look at these two basic building blocks:

Section header
--------------

A Contemply template file **must** start with a section header on the first line.
The basic form is:

.. code-block::
    
    --- Contemply

    content of your section header...

    ---

The section header is the right place to:

- Define the filename of your output files
- Collect data from your users to fill the template with
- Create additional folders

Everything that is not a valid expression inside the section header will  be printed to the 
console. Empty lines will be ignored. If you want to print an empty line to the console, write 
a single dot "."

.. code-block::

    --- Contemply
    
    Welcome to our code generator!

    There is no blank line above this one in the console.
    .
    .
    Above this line there are two blank lines in the console.


If you want to comment out a line inside a section header, use the "-" sign.


.. code-block::

    --- Contemply
    
    Welcome to our code generator!

    - I am a comment and will be ignored.


Define a filename to write to
-----------------------------

You do not need to define a filename to which your template is saved. By default, Contemply will prompt you for 
a filename after every section in your template.
Sometimes you might be interested in naming your output in a special way, e.g. when creating a python package. 
In this case your package will not work if there is no \_\_init\_\_.py file.

You can set a fixed filename using the **Filename** property inside the section header:

.. code-block::
    
    --- Contemply
    
    Filename is "setup.py"

    --
    This line will be saved in setup.py

Files (and folders) can only be created relative to the current directory.

.. code-block::
    
    --- Contemply
    
    Output is "@console"

    --
    This line will be output to the console.


There are a number of different values for **Output**:

.. list-table:: Values for outputfile
    :header-rows: 1

    * - Option
      - Description
    * - @file
      - Write to a file (either set by **Filename** or ask the user for it)
    * - @console
      - Output to the console (mentions the filename if one is set (see above))
    * - @null
      - No output at all (used in unit tests sometimes)


Change the default output channel
---------------------------------

By default Contemply will save your template to a file. In some cases you might want to choose
a different output, e.g. for debugging your templates. The output channel can be set using the
**Output** property inside a section header.




Template content
----------------

Everything outside of a section header is treated as template an potentially copied to your outputfile.
You cannot use the user input syntax as mentioned above here, user input has to be handled in the section header.
You can of course use conditionals, loops and call functions. See the respective sections of this documentation
to learn how to use all of these elements.


Get user input
**************



All user input functions can only be used inside a section header (first collect all data, then
put it inside our template).


Ask the user for string input
-----------------------------

To prompt the user for string input, we need a text to display with the input prompt 
and a variable name in which we want to save the users answer.

.. code-block::

    --- Contemply
    
    user_name: "What is your name? "

    ---

Notice that instead of "=" we use the ":" operator. This will trigger an input prompt.


Ask the user for a list of strings
----------------------------------

Sometimes we want to use a list of items in the template. For example to loop over a list 
of files to include. This can be done by adding the loop operator "..." after the line with
the prompt. This will ask the user for input until he enters an empty string (that is: simply presses
return). Remember to indent the loop operator "...".

.. code-block::

    --- Contemply

    favourite_animals: "Tell me all your favourite animals! "
        ...

    ---


Let the user choose from a list of items
----------------------------------------

If you want the user to choose from a predefined list of elements, you can use the list operator (-)
after the prompt.

.. code-block::

    --- Contemply

    color: "What's your favourite color?"
        - Red
        - Green
        - Blue

    ---


Use variables
*************

Apart from assigning user input to variables, you can also create them yourself.

Define variables yourself
-------------------------

If you want to define a variable yourself, simply use the assignment operator ("=").

.. code-block::

    --- Contemply

    color: "Red"
    number: 129
    floating_number: 44.9

    ---

Insert variables 
----------------

You can insert variable values using their names and wrapping them inside "§". To change the start and end markers for
variable replacement see :ref:`markers`.

.. code-block::

    --- Contemply

    version: "1.0.0"
    
    ---
    # My Python App
    # Version: § version §

    print('Hello!')

If you are using variables as part of an expression (e.g. in conditionals, see following section), you do not need to 
wrap them in §.


Conditionals
************

You can use conditionals to output only certain parts of your template depending on e.g. user input.
Contemply's new parser does not use the usual if/else language constructs but tries to use a shorter syntax.
That way it's a bit easier to viusally separate content and template commands.

An if-block in Contemply starts end ends with **?**. The question mark must appear at the beginning of the line.

.. code-block::

    --- Contemply

    output_header: "Enter 'yes' to add a file header: "
    
    ---
    ? output_header == 'yes'
    # My Python App
    # Version: § version §
    ?

    print('Hello!')

You can also check for a number of conditions just like in a classical if-else if construct.
A line starting with **??** is interpreted as "else if".

.. code-block::

    --- Contemply

    output_header: "Enter 'yes' to add a file header: "
    
    ---
    ? output_header == 'yes'
    # My Python App
    # Version: § version §
    ?? output_header == 'maybe'
    # My Python App (just one line)
    ?

    print('Hello!')

If you use **??** without a condition it is interpreted as an **else**.

.. code-block::

    --- Contemply

    output_header: "Enter 'yes' to add a file header: "
    
    ---
    ? output_header == 'yes'
    # My Python App
    # Version: § version §
    ??
    # No header needed :(
    ?

    print('Hello!')


Loops
*****

You can loop over a list of items with the loop operator "...".
Contemply loops work like a **foreach** loop, where the current list element is
available via a variable.

.. code-block::

    --- Contemply
    
    favourite_animals: "Tell me all your favourite animals! "
        ...
    
    ---
    <p>Favourite animals:</p>
    <ul>
    ... favourite_animals -> animal
    <li>§ animal §</li>
    ...
    </ul>


Functions
*********

You can use a number of different functions. For a list of available functions see :ref:`functions`.
To execute a function, start the line with **!**. This works in section headers and in your template' content.

.. code-block::

    --- Contemply
    
    ! makeFolders('new_folder_1')

    ---
    We need another folder!

    ! makeFolders('new_folder_2')

If you want to use functions as part of expressions, you do not need to use the **!** operator:

.. code-block::

    ? lowercase('YES') == 'yes'
    Hello World
    ?

Use functions as filters for variables
--------------------------------------

You can append one or more functions to your variables. The functions will be processed from left to right.

.. code-block::

    --- Contemply
    
    var = "WoRLd!"
    
    ---

    Hello § var ! lowercase ! capitalize §

**Notice** The function will only receive one argument (the input value). If the function requires more than one argument
it might fail


Additional settings
*******************

.. _markers:

Change start-/endmarkers
-------------------------

The default start- and endmarkers for wrapping variables in Contemply is "§". Usually this default setting will
work well with most programing languages/documents.
They can still be changed inside a section header:

.. code-block::

    --- Contemply
    
    StartMarker is "$"
    EndMarker is "#"

    foo = "world"
    
    ---

    Hello $ foo #!