Developer Documentation
=======================

Using the parser API
********************

.. warning:: Since version 1.1 the TemplateParser class can be found in the "frontend"-module.

You can easily add Contemply as a code generator to your application.
Take a look at this example:

.. code-block:: python

    from contemply.frontend import TemplateParser

    parser = TemplateParser()
    output = parser.parse_file('my_template.pytpl')


Using the TemplateContext, you can inject your own variables into your templates.


.. code-block:: python

    from contemply.frontend import TemplateParser

    parser = TemplateParser()
    ctx = parser.get_template_context()
    ctx.set('my_value', 'Hello world')

    output = parser.parse_file('my_template.pytpl')



TemplateParser Reference
************************

.. autoclass:: contemply.frontend.TemplateParser
    :members:

TemplateContext Reference
*************************

.. autoclass:: contemply.frontend.TemplateContext
    :members: