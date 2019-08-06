Variables
=========

You can assign a value to variable using the assignment operator (=).
There are no scopes in Contemply, so your variable is accessible throughout your template.
Variable names must start with a letter and may contain alphanumeric characters and the underscore (_).

Numbers
*******

Contemply only support integer numbers at the moment.

.. code-block:: contemply

    #: answer = 42

For *very* simple arithmetics take a look at :ref:`expressions`.


Strings
*******

You can use both double quotes (") or single quotes (') to define a string in Contemply. If you use on of them, the other
one can then be used inside the string. At the moment escaping characters is not supported.

.. code-block:: contemply

    #::
    my_string = "Hello World"

    #% same as:
    my_string = 'Hello World'

    #% you can use quotes inside your string:
    my_string = "He said 'Hello World'."
    my_string = 'He said "Hello World".'


.. _lists:

Lists
*****

Lists in Contemply have zero-based integer keys. The can be created using square brackets.

.. code-block:: contemply

    #::
    my_list = ['item 1', 'item 2']
    empty_list = []

    echo(my_list[0])
    #% will echo: "item 1"


To add an item to a list, you can use the **add operator (+=)**.

.. code-block:: contemply

    #::
    my_list = ['item 1', 'item 2']
    echo(my_list)
    #% will echo: ['item 1', 'item 2']

    my_list += 'item 3'
    echo(my_list)
    #% will echo: ['item 1', 'item 2', 'item 3']


Although lists can itself have lists as items, child lists cannot be accessed directly (e.g. as my_list[0][0]) at
the moment, but they can be used in a for loop:

.. code-block:: contemply

    #::
    my_list = []
    my_list += ['inner item 1', 'inner item 2']
    my_list += ['inner item 3', 'inner item 4']

    for sublist in my_list
        echo(sublist[0])
    endfor



Boolean
*******

Boolean values are the reserved keywords **True** / **False**.

.. code-block:: contemply

    #: my_bool = True
