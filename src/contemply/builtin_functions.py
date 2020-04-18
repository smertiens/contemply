import os

from contemply.util import check_function_args
from colorama import Style, Fore
from contemply.storage import get_secure_path
from contemply.util import check_function_args

def echo(args):
    check_function_args(['echo', 'str'], args)
    print(args[0])

# String functions

def uppercase(args):
    check_function_args(['uppercase', 'str'], args)
    return args[0].upper()


def lowercase(args):
    check_function_args(['lowercase', 'str'], args)
    return args[0].lower()


def capitalize(args):
    check_function_args(['capitalize', 'str'], args)
    return args[0].capitalize()


def contains(args):
    check_function_args(['contains', 'str', 'str'], args)
    return args[1] in args[0]


def replace(args):
    check_function_args(['replace', 'str', 'str, list', 'str'], args)
    search = args[1] if isinstance(args[1], list) else [args[1]]
    result = args[0]

    for item in search:
        result = result.replace(item, args[2])

    return result

# Filesystem functions

def makeFolders(args):
    check_function_args(['makeFolders', 'str', '*str'], args)
    path = get_secure_path(os.getcwd(), args[0])

    if len(args) == 2:
        mode = int(args[1], 8)
        os.makedirs(path, mode)
    else:
        os.makedirs(path)

    print(Fore.GREEN + '√' + Fore.RESET + ' Folder ' + Style.BRIGHT + '{0}'.format(args[0]) +
          Style.RESET_ALL + ' has been created')
