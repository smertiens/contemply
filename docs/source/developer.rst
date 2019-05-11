Adding Contemply to your application
====================================

You can easily add Contemply as a code generator to your application.
Take a look at this example:

.. code-block:: python

    from contemply.parser import *

    parser = TemplateParser()
    output = parser.parse_file('my_template.pytpl')


TemplateParser Reference
************************

.. autoclass:: contemply.parser.TemplateParser
    :members:

TemplateContext Reference
*************************

Using the TemplateContext, you can inject your own variables into your templates.

.. code-block:: python

    from contemply.parser import *

    parser = TemplateParser()
    ctx = parser.get_template_context()
    ctx.set('my_value', 'Hello world')

    output = parser.parse_file('my_template.pytpl')


.. autoclass:: contemply.parser.TemplateContext
    :members: