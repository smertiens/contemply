#
# Contemply - A code generator that creates boilerplate files from templates
#
# Copyright (C) 2019  Sean Mertiens
# For more information on licensing see LICENSE file
#

from colorama import Style, Fore

__all__ = ['prompt']


def prompt(question, default='Yes'):
    correct = False
    ret = None
    while not correct:
        answer = input(Style.BRIGHT + '{0} '.format(question) + Fore.LIGHTYELLOW_EX + '[{0}]'.format(
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
