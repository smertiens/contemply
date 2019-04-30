#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import argparse, os
from contemply.parser import *
from colorama import init, Fore

init()


def print_error(msg):
    print(Fore.RED + '{0}'.format(msg))


def header():
    print('*' * 40)
    print('*' + 'Contemply {0}'.format(contemply.__version__).center(38) + '*')
    print('*' * 40)


def main():
    header()

    # Parse CLI args
    parser = argparse.ArgumentParser(description="A code generator that creates boilerplate files from templates")

    parser.add_argument('template_file', metavar='template_file', type=str,
                        help='The template file you want to run')

    args = parser.parse_args()

    file = os.path.realpath(args.template_file)

    if not os.path.exists(file):
        print('I could not find that file')
        quit(1)

    parser = TemplateParser()

    try:
        parser.parse_file(file)
    except ParserException as e:
        print_error(e)


if __name__ == '__main__':
    main()
