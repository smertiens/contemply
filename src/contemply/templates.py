from contemply.storage import get_secure_path
import contemply.cli as cli
from colorama import Fore, Style
import os

class TemplateContext:

    def __init__(self):
        self.output = '@file'
        self.filename = ''
        self.content = []
    
    def flush(self):
        
        if self.output == '@console':
            
            target_file = self.filename

            if target_file == '':
                target_file = '(No filename specified)'

            print(Fore.CYAN + target_file + ': ' + Fore.RESET)

            for line in self.content:
                print('\t' + line)

        
        elif self.output == '@file':
            
            while self.filename == '':
                print('No filename was specified for the template. Please enter one now:')
                self.filename = cli.user_input('Filename: ')

            path = get_secure_path(os.getcwd(), self.filename)
            disp_path = path.replace(os.getcwd(), '')

            overwrite = True
            if os.path.exists(path):
                overwrite = cli.prompt('A file with the name {0} already exists. Overwrite?'.format(disp_path))

            if overwrite:
                with open(path, 'w') as f:
                    f.write('\n'.join(self.content))

                print(Fore.GREEN + '√' + Fore.RESET + ' File ' + Style.BRIGHT + '{0}'.format(disp_path) +
                        Style.RESET_ALL + ' has been created')

        elif self.output == '@null':
            return
