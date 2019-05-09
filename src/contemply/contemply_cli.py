#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import argparse, os, logging, sys
from contemply.parser import *
from contemply import samples
from colorama import Fore, init

# Init colorama
init()


def print_error(msg):
    print(Fore.RED + '{0}'.format(msg))


def header():
    print('*' * 40)
    print('*' + 'Contemply {0}'.format(contemply.__version__).center(38) + '*')
    print('*' * 40)
    print('')


def get_builtin_template(name):
    if not name.endswith('.pytpl'):
        name += '.pytpl'

    path = os.path.realpath(os.path.join(os.path.dirname(samples.__file__), name))
    return path


def main():
    # Parse CLI args
    parser = argparse.ArgumentParser(description="A code generator that creates boilerplate files from templates",
                                     )

    parser.add_argument('template_file', metavar='template_file', type=str,
                        help='The template file you want to run')
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-p", "--print", help="Print output to console instead of creating a new file",
                        action="store_true")
    parser.add_argument("--no-header", help="If set  the header will not be printed", action="store_true")
    parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(contemply.__version__))

    args = parser.parse_args()

    if not args.no_header is True:
        header()

    if args.template_file.startswith('samples:'):
        file = get_builtin_template(args.template_file.split(':')[1])
    else:
        file = os.path.realpath(args.template_file)

    if not os.path.exists(file):
        print_error('Template "{0}" not found.'.format(file))
        sys.exit()

    parser = TemplateParser()

    # set up parser
    if args.verbose is True:
        parser.get_logger().setLevel(logging.DEBUG)
    else:
        parser.get_logger().setLevel(logging.INFO)

    if args.print is True:
        parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)

    try:
        parser.parse_file(file)
    except ParserError as e:
        print_error(e)
    except KeyboardInterrupt:
        print('\nGoodbye.')
        sys.exit()


if __name__ == '__main__':
    main()
