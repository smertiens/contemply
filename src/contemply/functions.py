#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import os

import contemply.cli as cli
from colorama import Style
from contemply.storage import get_secure_path
from contemply.util import check_function_args

"""
Built in functions
"""

# Interactive functions

def ask(args, ctx):
    check_function_args(['ask', 'str'], args)

    prompt = args[0]
    if prompt[-1] != ' ':
        prompt = prompt + ' '

    answer = cli.user_input(Style.BRIGHT + prompt + Style.RESET_ALL)
    return answer


def choose(args, ctx):
    check_function_args(['choose', 'str', 'list'], args)

    choices = args[1]
    prompt = args[0]
    print(Style.BRIGHT + prompt + Style.RESET_ALL)
    for i, line in enumerate(choices):
        print('{0}. {1}'.format(i + 1, line))

    correct = False
    answer = 0
    while not correct:
        answer = cli.user_input(Style.BRIGHT + 'Your choice: ' + Style.RESET_ALL)

        if answer.isnumeric() and int(answer) in range(1, len(choices) + 1):
            correct = True
        else:
            print('Invalid choice')

    return choices[int(answer) - 1]


def yesno(args, ctx):
    check_function_args(['yesno', 'str', '*str'], args)
    default = 'Yes' if len(args) != 2 else args[1]

    return cli.prompt(args[0], default)


# Other template functions

def setOutput(args, ctx):
    check_function_args(['setOutput', 'str'], args)
    path = get_secure_path(os.getcwd(), args[0])
    ctx.set_outputfile(path)


# Other functions

def env(args, ctx):
    check_function_args(['env', 'str'], args)
    return os.environ[args[0]]


def echo(args, ctx):
    check_function_args(['echo', 'str'], args)
    print(ctx.process_variables(str(args[0])))


# String functions

def uppercase(args, ctx):
    check_function_args(['uppercase', 'str'], args)
    return args[0].upper()

def lowercase(args, ctx):
    check_function_args(['lowercase', 'str'], args)
    return args[0].lower()

def capitalize(args, ctx):
    check_function_args(['capitalize', 'str'], args)
    return args[0].capitalize()

def contains(args, ctx):
    check_function_args(['contains', 'str', 'str'], args)
    return args[1] in args[0]

def replace(args, ctx):
    check_function_args(['replace', 'str', 'str', 'str'], args)
    return args[0].replace(args[1], args[2])

# Misc functions working on types

def size(args, ctx):
    check_function_args(['size','*str,list'], args)

    return len(args[0])