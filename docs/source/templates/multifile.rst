.. _multifile:

Creating multiple files
=======================

Using file blocks
*****************

Contemply allows you to create multiple files from one single template file using a simple syntax.
The content of a file lives inside a **file block**. All content lines within this block will be written
to the specified file. You can start a file block like this:

.. code-block:: contemply

    #: >> "myfile.txt"

    The content for my file.
    Also this second line.


If you want to start another file block, you have to **close the previous one** before.

.. code-block:: contemply

    #: >> "myfile.txt"
    The content for my file.
    #: <<

    #: >> "another_file.txt"
    This content goes to another_file.txt
    #: <<

If you only write to one file (and only have one file block), you don't need to close it.

When specifying the same file block more than once, the second set of lines will simply be appended to the file.

.. code-block:: contemply

    #: >> "myfile.txt"
    The content for my file.
    #: <<

    #: >> "another_file.txt"
    This content goes to another_file.txt
    #: <<

    #: >> "myfile.txt"
    This line will be appended at the end of the file.
    #: <<

Create missing folders in filepath
----------------------------------

You can tell Contemply to create all missing folders in the filepath you are writting to. To do so, simply set the first
parameter of the file block to "True". By default missing folders are not created and trying to write the file to a
folder that does not exist will result in an error.

.. code-block:: contemply

    #: >> "/foo/bar/myfile.txt", True
    The folders "foo" and "bar" will be created if they don't exist.
    #: <<


Default output
**************

You don't need to use file blocks. Any output that is created outside of a fileblock, will also be saved. In this case
Contemply will prompt the user for a filename.

::

    This line will go to the default output. The user will be prompted for a filename.

    #: >> "another_file.txt"
    This content goes to another_file.txt
    #: <<

    This line will also go to the default output.


