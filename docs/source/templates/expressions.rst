.. _expressions:

Expressions
===========

Arithmetic expressions
**********************

At the moment Contempyl only supports arithmetic expressions with two operands, meant for counting up indices or anything
similar. In future releases more complex expressions might be supported.
You can use the usual operators to do addition, subtraction, division and multiplication.

::

    #::
    result = 50 - 10
    result = 25 + 25
    result = 50 / 2
    result = 2 * 22

Comparisons
***********

You can do simple comparisons, usually used in if-clauses and while-loops. Contemply comparisons (as arithmetic expressions)
do not support parentheses at the moment.

::

    #::
    if 20 > 10:
        echo('Thought so')
    endif

=========   =====================
Operator    Comment
=========   =====================
==          Equals
!=          Not equals
<           Smaller than
>           Greater than
<=          Smaller or equal to
>=          Greator or equal to
=========   =====================