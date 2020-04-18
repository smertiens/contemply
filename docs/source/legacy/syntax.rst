Template file syntax
====================

You can build a Contemply template from any file, you simply add questions as a comment and replace
parts of your file with a variable.

Templates are processed line-by-line and there are three different types of lines: **command lines**, **content
lines** and **comment lines**. Let's start with the latter one.

Comment lines
*************

The start with **#%**. These lines are ignored and **removed from your templates output**. They are meant to
comment out Contemply commands (since you usually don't want them to be part of your template's output).
Note: Normal python comments (starting with '#') are not removed of course and will be part of the template's
output.


Command lines
*************

These lines start with **#:** and this is where the magic happens. Following '#:' you can enter any
Contemply expression, one per line. The command line syntax is very similar to Python or other templating
languages. Take a look at the README file or the samples folder in the GitHub Repo to see how it works.
You can also take a look at :ref:`templatefunctions`.

.. _commandblocks:

Command blocks
--------------

If you have a many command lines in a row, you can use **#::** to toggle a **commmand block**. All lines in
this block are treated as command lines, sou don't have to start every line with '#:'.

Example:


.. code-block:: contemply

    #% Demo of a command block
    #::
        echo('Line 1')
        echo('Line 2')
    #::


Content lines
*************

By default Contemply will ignore all other lines in your file  not starting with '#:' or '#%' and just hand them
through to your templates output. These are your **content lines**. Contemply will replace variables in them though.
To insert a variable in a content line prefix it with '$'.

Example:

.. code-block:: contemply

    #% First we will define a variable
    #: var = "Hello world!"
    #% now we add it to a content line:

    def say_hello():
        print("$var")


Indentation
***********

You can indent lines **inside command blocks** as you like, but the block delimiters (#::) must be at the beginning of the line.
As you can see from the script examples in the docs, indentation can increase readability.
If you are using commandlines, the line **has to start with #:**. After that you can again indent as you like.

.. code-block:: contemply

    #::
        if True
            echo('You can indent command blocks')
        endif
    #::

    #:         echo('Command lines must start with #:')


