.. _templatefunctions:

Template functions
==================

Interactivity
*************

.. py:function:: ask(prompt)

    This function will prompt the user for a string value.

    :param str prompt: The question to ask the user, a space is automatically added to the end of the string, if
                        none exists.
    :return: The user's answer as a string

.. py:function:: choose(prompt, choices)

    This function will provide the user with a list of numbered choices. The user can then input the number
    of the item he chooses.

    :param str prompt: The text of the question
    :param list choices: A list of strings that the user can choose from.
    :return: The text of the selected choice as string

    Example:

        ::

            #: color = choose('What is your favourite color?', ['red', 'green', 'blue'])
            #: echo('Ah, your favourite color is $color.')


        this will result in:

        ::

            What is your favourite color?
            1. red
            2. green
            3. blue
            Your choice: 2
            Ah, your favourite color is green.


.. py:function:: yesno(prompt, [default = Yes])

    This function asks the user a yes/no question. The function accepts "yes"/"y" and "no"/"n" as input and is
    case-insensitive.

    :param str prompt: The text of the question
    :param str default: The default answer (used when the user enters nothing), either: "yes" or "no".
    :return: True/False depending on the users answer

    Example:

    ::

        #: add_hw = yesno('Do you want to add Hello World to your file?', 'No')

        #: if add_hw == True
        Hello World
        #: endif


    this will result in:

    ::

        Do you want to add Hello World to your file? [No]: Yes

        Hello World


Other Template functions
************************

.. py:function:: setOutput(filename)

    Sets the name of the outputfile. If no outputfile is set, the user will be prompted to enter a filename.

    :param str filename: The name of the file (may contain variables). Either absolute or relative to the current directory


String functions
================

.. py:function:: uppercase(string)

    Converts string to uppercase.

    :param str string: A string or a string variable


.. py:function:: lowercase(string)

    Converts string to lowercase.

    :param str string: A string or a string variable


.. py:function:: capitalize(string)

    Capitalizes string.

    :param str string: A string or a string variable


.. py:function:: contains(string, search)

    Returns True if "string" contains "search".

    :param str string: A string or a string variable
    :param str search: A string or a string variable
    :rtype: boolean


.. py:function:: replace(string, search, replace)

    Replaces all occurences of "search" in "string" with "replace".

    :param str string: A string or a string variable
    :param str search: A string or a string variable
    :param str replace: A string or a string variable
    :return: The edited string
    :rtype: str



Built in functions
==================

.. py:function:: size(thing)

    Returns the size of a thing. If the first argument is a string the function will return the strings length,
    if it is a list it will return the number of items in the list.

    :param any thing: A list or a string
    :returns: Length or number of elements
    :rtype: int

.. py:function:: echo(message)

    Prints a message to the console.

    :param str message: The message to print

.. py:function:: env(name)

    Returns the value of an environment variable

    :param str name: The name of the variable
    :return: The variables value

    Example:

    ::

        #: username = env("USER")
        #: echo ("Hello $username!")

.. py:function:: exit()

    Exits contemply and stops template processing
