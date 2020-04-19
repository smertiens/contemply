#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019-2020  Sean Mertiens
# For more information on licensing see LICENSE file
#

def bar(args, ctx):
    print('This %s!' % args[0])

def newstyle_bar(args):
    print('This %s!' % args[0])