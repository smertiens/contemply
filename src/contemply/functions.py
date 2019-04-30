#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

"""
Built in functions
"""


def ask(args, ctx):
    """
    Call in inside your template as: **ask(prompt, variable_name)**

    :param prompt: The text of the question
    :param variable_name: The variable name to save the answer to
    """
    if len(args) < 2:
        raise SyntaxError("Function needs exactly 2 argument")

    answer = input(args[0])
    ctx.set(args[1], answer)


def choose(args, ctx):
    if len(args) < 3:
        raise SyntaxError("Function needs exactly 2 argument")

    if not isinstance(args[1], list):
        raise SyntaxError("Expected list at position 2")

    choices = args[1]
    prompt = args[0]
    print(prompt)
    for i, line in enumerate(choices):
        print('{0}. {1}'.format(i + 1, line))

    # add quit option
    print(print('{0}. {1}'.format(len(choices) + 1, 'Cancel')))

    correct = False
    while not correct:
        answer = input('Your choice: ')

        if answer.isnumeric() and int(answer) in range(1, len(choices) + 1):
            correct = True
        elif int(answer) == len(args[1]) + 1:
            quit()
        else:
            print('Invalid choice')

    ctx.set(prompt, choices[int(answer) - 1])


def yesno(args, ctx):
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
        answer = input('{0} [{1}]: '.format(prompt, default))

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


def echo(args, ctx):
    if len(args) == 0:
        raise SyntaxError("Function needs exactly 1 argument")

    print(args[0])


def output(args, ctx):

    if len(args) == 0:
        raise SyntaxError("Function needs exactly 1 argument")

    ctx.set_outputfile(args[0])