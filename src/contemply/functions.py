#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import os

import contemply.cli as cli
from colorama import Style, Fore
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
    print(Fore.YELLOW + 'This function is deprecated and WILL NOT work. See "Creating multiple files" in the docs' + Fore.RESET)
    #check_function_args(['setOutput', 'str'], args)
    #ctx.set_outputfile(args[0])


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
    check_function_args(['replace', 'str', 'str, list', 'str'], args)
    search = args[1] if isinstance(args[1], list) else [args[1]]
    result = args[0]

    for item in search:
        result = result.replace(item, args[2])

    return result


# Misc functions working on types

def size(args, ctx):
    check_function_args(['size', '*str,list'], args)

    return len(args[0])


# Filesystem functions

def makeFolders(args, ctx):
    check_function_args(['makeFolders', 'str', '*str'], args)
    path = get_secure_path(os.getcwd(), ctx.process_variables(args[0]))

    if len(args) == 2:
        mode = int(args[1], 8)
        os.makedirs(path, mode)
    else:
        os.makedirs(path)

    print(Fore.GREEN + '√' + Fore.RESET + ' Folder ' + Style.BRIGHT + '{0}'.format(ctx.process_variables(args[0])) +
          Style.RESET_ALL + ' has been created')
