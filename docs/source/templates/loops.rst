Using loops
===========

You can use loops to repeat certain parts of your template. For an example take a look at the class-sample-template:
https://github.com/smertiens/contemply/blob/develop/src/contemply/samples/class.pytpl

.. _whileloops:

While loops
***********

A while loop will take a condition and will run as long as the condition is True.

.. code-block:: contemply

    #::
    num = 0

    while num < 5
        echo ("Number $num")
        num = num + 1
    endwhile
    #::


You can also use the **break** statement to end the loop at any time.

.. code-block:: contemply

    #::
    num = 0
    while True
        if num == 5
            break
        endif

        echo ("Number $num")
        num = num + 1
    endwhile
    #::

.. _forloops:

For loops
*********

With for loops you can iterate over a list.

.. code-block:: contemply

    #::
    shopping_list = ['eggs', 'milk', 'cheese']

    for item in shopping_list
        echo("We need $item!")
    endfor
    #::


You can use **break** to end a for loop ahead of time.
