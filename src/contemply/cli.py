#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from colorama import Style, Fore
import platform, sys

__all__ = ['prompt', 'user_input']


def user_input(prompt):
    """
    Wraoper for input() to handle coloring issues on windows

    :param str prompt: The text to prompt the user
    :return: The user's input
    :rtype: str
    """

    # On Python >= 3.5 colorama cannot properly replace ANSI characters in input-prompt
    # see here: https://github.com/tartley/colorama/issues/103
    # So we will print a separate prompt on the systems in question

    if platform.system() == 'Windows':
        pyver = sys.version_info

        if (pyver[0] == 3 and pyver[1] >= 5) or pyver[0] > 3:
            print(prompt)
            value = input('> ')
            return value

    value = input(prompt)
    return value


def prompt(question, default='Yes'):
    """
    Will ask the user a yes/no question

    :param str question: The question to ask
    :param str default: The default value if the user inputs nothing
    :return: True/False
    :rtype: bool
    """
    correct = False
    ret = None
    while not correct:
        answer = user_input(Style.BRIGHT + '{0} '.format(question) + Fore.LIGHTYELLOW_EX + '[{0}]'.format(
            default) + Fore.RESET + ': ' + Style.RESET_ALL)

        if answer == '':
            answer = default

        answer = answer.lower()
        if answer == 'y' or answer == 'yes':
            ret = True
            correct = True
        elif answer == 'n' or answer == 'no':
            ret = False
            correct = True
        else:
            print('Invalid answer')

    return ret
