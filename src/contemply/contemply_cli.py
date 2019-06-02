#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

import click
from colorama import Fore, init
from contemply import samples
from contemply.parser import *
from contemply.preferences import PreferencesProvider
from contemply.storage import TemplateStorageManager


class CLIContext:

    def __init__(self):
        self.preferences = PreferencesProvider()
        self.storage = TemplateStorageManager(self.preferences)
        self.verbose = False


def header(ret_header = False):
    h = '\n'.join([
        '*' * 40,
        '*' + 'Contemply {0}'.format(contemply.__version__).center(38) + '*',
        '*' * 40,
        ''
    ])

    if ret_header:
        return h
    else:
        print(h)

def print_error(msg):
    print(Fore.RED + '{0}'.format(msg) + Fore.RESET)


def get_builtin_template(name):
    """
    Retrieves one of the sample templates
    :param str name: Builtin template name (from samples folder)
    :return: The absolute path to the template file
    """
    if not name.endswith('.pytpl'):
        name += '.pytpl'

    path = os.path.realpath(os.path.join(os.path.dirname(samples.__file__), name))
    return path


@click.group(invoke_without_command=False)
@click.pass_context
def cli(ctx):
    ctx.obj = CLIContext()

@cli.command()
@click.option('--no-header', type=bool, is_flag=True, help='Do not show application header')
@click.option('--verbose', '-v', type=click.BOOL, is_flag=True, help='Increase verbosity')
@click.option('--print', '-p', 'print_out', type=click.BOOL, is_flag=True, help='Show template output in terminal')
@click.argument('template_file')
@click.pass_context
def run(ctx, no_header, verbose, print_out, template_file):
    """
    Runs a template.

    You can either enter the path to a file as TEMPLATE_FILE or run a template from storage, by prefixing the template
    file with the storage name followed by ::, for example:

        contemply my_storage::my_template.pytpl.

    Contemply also provides a number of builtin sample templates, for example try this one:

        contemply samples:class
    """
    if no_header is not True:
        header()

    storage = ctx.obj.storage

    if template_file.startswith('samples:'):
        file = get_builtin_template(template_file.split(':')[1])
    elif template_file.find('::') > 0:
        file = storage.resolve(template_file)
    else:
        file = os.path.realpath(template_file)

    if not os.path.exists(file):
        print_error('Template "{0}" not found.'.format(file))
        sys.exit()

    parser = TemplateParser()

    # set up parser
    if verbose is True:
        parser.get_logger().setLevel(logging.DEBUG)
    else:
        parser.get_logger().setLevel(logging.INFO)

    if print_out is True:
        parser.set_output_mode(TemplateParser.OUTPUTMODE_CONSOLE)

    try:
        parser.parse_file(file)
    except ParserError as e:
        print_error(e)
    except KeyboardInterrupt:
        print('\nGoodbye.')
        sys.exit()


@cli.command()
@click.pass_context
def version(ctx):
    """
    Shows the current version and exits.
    """
    print('Contemply version {0}'.format(contemply.__version__))


@cli.command('storage:list')
@click.pass_context
def storage_list(ctx):
    """
    Lists all existing storage locations.
    """
    storage = ctx.obj.storage

    try:
        for name, path in storage.list().items():
            print(Style.BRIGHT + name + Style.RESET_ALL + ' -> ' + path)

    except StorageException as e:
        print_error(str(e))

@cli.command('storage:show')
@click.argument('storage_name')
@click.pass_context
def storage_show(ctx, storage_name):
    """
    Show all templates in an existing storage location.
    """

    storage = ctx.obj.storage

    try:
        tpls = storage.show(storage_name)

        print('Showing templates in ' + Style.BRIGHT + storage_name + Style.RESET_ALL + ':\n')

        for path in tpls:
            print('- ' + os.path.basename(path))

        print('\nFound {} templates.'.format(len(tpls)))

    except StorageException as e:
        print_error(str(e))


@cli.command('storage:add')
@click.argument('name')
@click.argument('path')
@click.pass_context
def storage_add(ctx, name, path):
    """
    Adds a new storage location
    """

    storage = ctx.obj.storage

    try:
        storage.add_location(name, path)
        print(Fore.GREEN + '√' + Fore.RESET + ' New storage ' + Style.BRIGHT + '{0} (-> {1})'.format(
            name, os.path.realpath(path)) +
              Style.RESET_ALL + ' has been added')
    except StorageException as e:
        print_error(str(e))


@cli.command('storage:remove')
@click.argument('name')
@click.pass_context
def storage_remove(ctx, name):
    """
    Removes an existing storage location
    """
    storage = ctx.obj.storage

    try:
        storage.remove_location(name)
        print(Fore.GREEN + '√' + Fore.RESET + ' Storage ' + Style.BRIGHT + '{0}'.format(name) +
              Style.RESET_ALL + ' has been removed')
    except StorageException as e:
        print_error(str(e))


def main():
    # Init colorama
    init()
    cli()


if __name__ == '__main__':
    main()
