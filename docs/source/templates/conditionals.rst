Conditionals
============

Contemply supports if/elseif/else constructs to customize template output based on user input.

.. code-block:: contemply

    #::
    bool_var = True

    if bool_var
        echo('bool_var is True')
    endif


You can check for different conditions using **elseif** and provide a default with **else**:

.. code-block:: contemply

    #::
    fruit = ask("What's your favourite fruit?")

    if fruit == "banana"
        echo("Oh, it's yellow!")
    elseif fruit == "apple"
        echo("Looks like an apple!")
    elseif fruit == "kiwi"
        echo("Yummy!")
    else
        echo("I don't know this one!")
    endif
