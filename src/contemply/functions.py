#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import os

import contemply.cli as cli
from colorama import Style
from contemply.exceptions import *

"""
Built in functions
"""


def ask(args, ctx):
    if len(args) != 1:
        raise SyntaxError("Function ask() needs exactly 1 argument", ctx)

    prompt = args[0]
    if prompt[-1] != ' ':
        prompt = prompt + ' '

    answer = input(Style.BRIGHT + prompt + Style.RESET_ALL)
    return answer


def choose(args, ctx):
    if len(args) != 2:
        raise SyntaxError("Function choose() needs exactly 2 arguments", ctx)

    if not isinstance(args[1], list):
        raise SyntaxError("Expected list at position 2", ctx)

    choices = args[1]
    prompt = args[0]
    print(Style.BRIGHT + prompt + Style.RESET_ALL)
    for i, line in enumerate(choices):
        print('{0}. {1}'.format(i + 1, line))

    correct = False
    answer = 0
    while not correct:
        answer = input(Style.BRIGHT + 'Your choice: ' + Style.RESET_ALL)

        if answer.isnumeric() and int(answer) in range(1, len(choices) + 1):
            correct = True
        else:
            print('Invalid choice')

    return choices[int(answer) - 1]


def yesno(args, ctx):
    if len(args) < 1:
        raise SyntaxError("Function yesno() needs at least 1 argument", ctx)
    elif len(args) > 2:
        raise SyntaxError("Function yesno() expects not more than 2 arguments.", ctx)

    default = 'Yes' if len(args) != 2 else args[1]

    return cli.prompt(args[0], default)


def env(args, ctx):
    if len(args) != 1:
        raise SyntaxError("Function env() needs at exactly 1 argument", ctx)

    return os.environ[args[0]]


def echo(args, ctx):
    if len(args) == 0:
        raise SyntaxError("Function echo() needs exactly 1 argument", ctx)

    print(ctx.process_variables(args[0]))


def setOutput(args, ctx):
    if len(args) == 0:
        raise SyntaxError("Function output() needs exactly 1 argument", ctx)

    ctx.set_outputfile(args[0])
