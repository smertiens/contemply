#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#
from colorama import Fore, Style
import os

"""
Built in functions
"""


def ask(args, ctx):
    """
    Call in inside your template as: **ask(prompt, variable_name)**

    :param prompt: The text of the question
    :param variable_name: The variable to save the answer to

    This function will prompt the user for a string value and save it to variable_name.
    To access the user input later in your template, simply insert the variable: $variable_name
    """
    if len(args) < 2:
        raise SyntaxError("Function needs exactly 2 argument")

    answer = input(Style.BRIGHT + args[0] + Style.RESET_ALL)
    ctx.set(args[1], answer)


def choose(args, ctx):
    """
    Call inside your template as: choose(prompt, choices, variable_name)

    :param prompt: The text of the question
    :param choices: A list of strings that the user can choose from. The selected string will be saved to
                    variable name
    :param variable_name: The variable to save the answer to

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
    if len(args) < 3:
        raise SyntaxError("Function needs exactly 2 argument")

    if not isinstance(args[1], list):
        raise SyntaxError("Expected list at position 2")

    varname = args[2]
    choices = args[1]
    prompt = args[0]
    print(prompt)
    for i, line in enumerate(choices):
        print('{0}. {1}'.format(i + 1, line))

    correct = False
    while not correct:
        answer = input(Style.BRIGHT + 'Your choice: ' + Style.RESET_ALL)

        if answer.isnumeric() and int(answer) in range(1, len(choices) + 1):
            correct = True
        else:
            print('Invalid choice')

    ctx.set(varname, choices[int(answer) - 1])


def yesno(args, ctx):
    """
    Call inside your template as: choose(prompt, variable_name, [default = Yes])

    :param prompt: The text of the question
    :param variable_name: The variable to save the answer to
    :param defautl: The default value that is returned when the user has entered nothing. If this argument is not
                    given, the default value will be 'Yes'.

    This function will ask the user a yes/no question. The answer is saved to variable_name as boolean.
    Accepted user inputs are: "yes", "Yes", "y" / "no", "No", "n"

    Example:

    ::

        #: yesno('Do you want to add Hello World to your file?', 'addhw', 'No')

        #: if addhw == True
        Hello World
        #: endif


    this will result in:

    ::

        Do you want to add Hello World to your file? [No]: Yes

        Hello World

    """
    if len(args) < 2:
        raise SyntaxError("Function needs at least 1 argument")

    prompt = args[0]
    varname = args[1]
    default = 'Yes'

    if len(args) > 2:
        default = args[2].capitalize()

    correct = False
    ret = None
    while not correct:
        answer = input(Style.BRIGHT + '{0} '.format(prompt) + Fore.LIGHTYELLOW_EX + '[{0}]'.format(
            default) + Fore.RESET + ': ' + Style.RESET_ALL)

        if answer == '':
            answer = default

        if answer == 'y' or answer == 'yes' or answer == 'Yes':
            ret = True
            correct = True
        elif answer == 'n' or answer == 'no' or answer == 'No':
            ret = False
            correct = True
        else:
            print('Invalid answer')

    ctx.set(varname, ret)


def env(args, ctx):
    if len(args) < 1:
        raise SyntaxError("Function needs at exactly 1 argument")

    return os.environ[args[0]]


def echo(args, ctx):
    if len(args) == 0:
        raise SyntaxError("Function needs exactly 1 argument")
    print(args[0])
    print(ctx.process_variables(args[0]))


def output(args, ctx):
    if len(args) == 0:
        raise SyntaxError("Function needs exactly 1 argument")

    ctx.set_outputfile(args[0])
