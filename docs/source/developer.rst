Developer Documentation
=======================

Parser API
**********

You can easily add Contemply as a code generator to your application.

.. code-block:: python

    from contemply.parser import Parser

    parser = Parser()

    # Parse a file
    parser.parse_file('my_template.pytpl')

    # Alternatively: Parse a string
    parser.parse_string('---Contemply')

    parser.run()


Using the legacy parser API (DEPRECATED!)
*****************************************

.. warning:: This version of the API is deprecated!

You can easily add Contemply as a code generator to your application.
Take a look at this example:

.. code-block:: python

    from contemply.legacy.frontend import TemplateParser

    parser = TemplateParser()
    output = parser.parse_file('my_template.pytpl')


Using the TemplateContext, you can inject your own variables into your templates.


.. code-block:: python

    from contemply.legacy.frontend import TemplateParser

    parser = TemplateParser()
    ctx = parser.get_template_context()
    ctx.set('my_value', 'Hello world')

    output = parser.parse_file('my_template.pytpl')
