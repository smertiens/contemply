#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import argparse, os, logging
from contemply.parser import *
from colorama import Fore, init

# Init colorama
init()


def print_error(msg):
    print(Fore.RED + '{0}'.format(msg))


def header():
    print('*' * 40)
    print('*' + 'Contemply {0}'.format(contemply.__version__).center(38) + '*')
    print('*' * 40)


def main():
    # Parse CLI args
    parser = argparse.ArgumentParser(description="A code generator that creates boilerplate files from templates")

    parser.add_argument('template_file', metavar='template_file', type=str,
                        help='The template file you want to run')
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-p", "--print", help="Print output to console instead of creating a new file",
                        action="store_true")
    parser.add_argument("--header", type=bool, help="If set to False, the header will not be printed", default=True)

    args = parser.parse_args()

    if args.header is True:
        header()

    file = os.path.realpath(args.template_file)

    if not os.path.exists(file):
        print('I could not find that file')
        quit(1)

    parser = TemplateParser()

    # set up parser
    if args.verbose is True:
        parser.get_logger().setLevel(logging.DEBUG)
    else:
        parser.get_logger().setLevel(logging.INFO)

    if args.print is True:
        parser.set_outputmode(TemplateParser.OUTPUTMODE_CONSOLE)

    try:
        parser.parse_file(file)
    except ParserException as e:
        print_error(e)


if __name__ == '__main__':
    main()
