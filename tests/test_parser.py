#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from contemply.parser import *


def test_new_parser():
    text = '#: test = "hello world"\n #: echoX(test)'

    parser = TemplateParser()
    parser.parse_file('/Users/mephisto/python_projects/contemply/samples/color.pytpl')