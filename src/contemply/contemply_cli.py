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
from contemply.preferences import PreferencesProvider
from contemply.storage import TemplateStorageManager


def storage_add(args, storage, preferences):
    try:
        storage.add_location(args.storage_name, args.storage_path)
        print(Fore.GREEN + '√' + Fore.RESET + ' New storage ' + Style.BRIGHT + '{0} (-> {1})'.format(
            args.storage_name, args.storage_path) +
              Style.RESET_ALL + ' has been added')
    except StorageException as e:
        print_error(str(e))


def storage_remove(args, storage, preferences):
    try:
        storage.remove_location(args.storage_name)
        print(Fore.GREEN + '√' + Fore.RESET + ' Storage ' + Style.BRIGHT + '{0}'.format(args.storage_name) +
              Style.RESET_ALL + ' has been deleted')
    except StorageException as e:
        print_error(str(e))


def storage_list(args, storage, preferences):
    try:
        for name, path in storage.list().items():
            print(Style.BRIGHT + name + Style.RESET_ALL + ' -> ' + path)

    except StorageException as e:
        print_error(str(e))


def template_parse(args, storage, preferences):
    if args.template_file.startswith('samples:'):
        file = get_builtin_template(args.template_file.split(':')[1])
    elif args.template_file.find('::') > 0:
        file = storage.resolve(args.template_file)
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


def get_argument_parser():
    parser = argparse.ArgumentParser(description="A code generator that creates boilerplate files from templates")
    subparsers = parser.add_subparsers()

    storage_add_parser = subparsers.add_parser('storage:add')
    storage_add_parser.add_argument('storage_name', type=str, metavar='NAME', help='The name of the new storage')
    storage_add_parser.add_argument('storage_path', type=str, metavar='PATH',
                                    help='The path the storage should point to')
    storage_add_parser.set_defaults(func=storage_add)

    storage_del_parser = subparsers.add_parser('storage:remove')
    storage_del_parser.add_argument('storage_name', type=str, metavar='NAME', help='The name of the storage to remove')
    storage_del_parser.set_defaults(func=storage_remove)

    storage_list_parser = subparsers.add_parser('storage:list')
    storage_list_parser.set_defaults(func=storage_list)

    template_parser = subparsers.add_parser('run')
    template_parser.add_argument('template_file', metavar='TEMPLATE', type=str,
                                 help='The template file you want to run')
    template_parser.add_argument("-p", "--print", help="Print output to console instead of creating a new file",
                                 action="store_true")
    template_parser.set_defaults(func=template_parse)

    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--no-header", help="If set  the header will not be printed", action="store_true")
    parser.add_argument('--version', action='version', version='%(prog)s {0}'.format(contemply.__version__))

    return parser


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
    subparsers = ['storage:add', 'storage:remove', 'storage:list', 'run']
    arguments = sys.argv
    # Preprocess arguments so the default subparser will be "run"
    if len(arguments) == 2:
        if arguments[1] not in subparsers:
            # add default subparser
            arguments = [arguments[0], 'run', arguments[1]]

    # remove script name
    arguments = arguments[1:]

    # Parse CLI args
    argument_parser = get_argument_parser()
    args = argument_parser.parse_args(arguments)
    preferences = PreferencesProvider()
    storage = TemplateStorageManager(preferences)

    if not args.no_header is True:
        header()

    if not hasattr(args, 'func'):
        argument_parser.print_help()
    else:
        args.func(args, storage, preferences)


if __name__ == '__main__':
    # Init colorama
    init()
    main()
