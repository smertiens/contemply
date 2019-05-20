Variables
=========

You can assign a value to variable using the assignment operator (=).
There are no scopes in Contemply, so your variable is accessible throughout your template.
Variable names must start with a letter and may contain alphanumeric characters and the underscore (_).

Numbers
*******

Contemply only support integer numbers at the moment.

::

    #: answer = 42

For *very* simple arithmetics take a look at :ref:`expressions`.


Strings
*******

You can use both double quotes (") or single quotes (') to define a string in Contemply. If you use on of them, the other
one can then be used inside the string. At the moment escaping characters is not supported.

::

    #::
    my_string = "Hello World"

    #% same as:
    my_string = 'Hello World'

    #% you can use quotes inside your string:
    my_string = "He said 'Hello World'."
    my_string = 'He said "Hello World".'


Lists
*****

Lists in Contemply are one-dimensional and have zero-based integer keys. The can be created using square brackets.

::

    #::
    my_list = ['item 1', 'item 2']
    empty_list = []

    echo(my_list[0])
    #% will echo: "item 1"


To add an item to a list, you can use the **add operator (+=)**.

::

    #::
    my_list = ['item 1', 'item 2']
    echo(my_list)
    #% will echo: ['item 1', 'item 2']

    my_list += 'item 3'
    echo(my_list)
    #% will echo: ['item 1', 'item 2', 'item 3']


Boolean
*******

Boolean values are the reserved keywords **True** / **False**.

::

    #: my_bool = True
