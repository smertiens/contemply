.. _functions:

Functions
=========

String functions
****************

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
    :param search: A string or a string variable or a list of strings to search for
    :param str replace: A string or a string variable
    :return: The edited string
    :rtype: str


Filesystem Functions
********************

.. py:function:: makeFolders(path, [, mode])

    Recursively creates all folders in path.

    :param str path: The path that should be created. All paths are relative to the current working directory. Trying to access
            upstream folders will result in a SecurityError.
    :param str mode: The file mode. Only available on systems that support it (Linux/OSX). If mode is omitted, the default
            setting of the python os.makedir() function applies (0777)


Misc Functions
**************

.. py:function:: echo(message)

    Prints a message to the console.

    :param str message: The message to print

