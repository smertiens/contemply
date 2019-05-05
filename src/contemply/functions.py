#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#
from colorama import Fore, Style
from contemply.exceptions import *
import contemply.cli as cli
import os

"""
Built in functions
"""


def ask(args, ctx):
    """
    Call in inside your template as: **ask(prompt)**

    :param prompt: The text of the question

    This function will prompt the user for a string value.
    """
    if len(args) != 1:
        raise SyntaxError("Function ask() needs exactly 1 argument", ctx)

    answer = input(Style.BRIGHT + args[0] + Style.RESET_ALL)
    return answer


def choose(args, ctx):
    """
    Call inside your template as: choose(prompt, choices)

    :param prompt: The text of the question
    :param choices: A list of strings that the user can choose from. The selected string will be saved to
                    variable name

    This function will provide the user with a list of numbered choices. The user can then input the number
    of the item he chooses.

    Example:

    ::

        #: choose('What is your favourite color?', ['red', 'green', 'blue'], 'color')
        #: echo('Ah, your favourite color is $color.')


    this will result in:

    ::

        What is your favourite color?
        1. red
        2. green
        3. blue
        Your choice: 2
        Ah, your favourite color is green.


    """
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
    """
    Call inside your template as: choose(prompt, [default = Yes])

    :param prompt: The text of the question
    :param defautl: The default value that is returned when the user has entered nothing. If this argument is not
                    given, the default value will be 'Yes'.

    This function will ask the user a yes/no question. The answer is saved to variable_name as boolean.
    Accepted user inputs are: "yes", "Yes", "y" / "no", "No", "n"

    Example:

    ::

        #: addhw = yesno('Do you want to add Hello World to your file?', 'No')

        #: if addhw == True
        Hello World
        #: endif


    this will result in:

    ::

        Do you want to add Hello World to your file? [No]: Yes

        Hello World

    """
    default = 'Yes'

    if len(args) < 1:
        raise SyntaxError("Function yesno() needs at least 1 argument")
    elif len(args) == 2:
        default = args[1]
    else:
        raise SyntaxError("Function yesno() expects not more than 2 arguments.")

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
