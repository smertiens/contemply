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


Content lines
*************
By default Contemply will ignore all other lines in your file  not starting with '#:' or '#%' and just hand them
through to your templates output. These are your **content lines**. Contemply will replace variables in them though.
To insert a variable in a content line prefix it with '$'.

Example:

::

    #% First we will define a variable
    #: var = "Hello world!"
    #% now we add it to a content line:

    def say_hello():
        print("$var")

