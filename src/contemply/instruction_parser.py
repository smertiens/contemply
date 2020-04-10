from contemply import cli
import re

class InstructionParser:

    def __init__(self):
        self.data = {}
        self.current_line = 0
        self.lines = []

        self.re_prompt = re.compile(r'^(\w+)\:[ ]?(.*)$')
        self.re_option = re.compile(r'^(?:\t| +)\- (.*)$')

    def parse(self, text: str) -> dict:

        self.lines = text.splitlines()
        
        while(self.current_line < len(self.lines)):
            if (self.line_is_prompt()):
                if (self.line_is_option(1)):
                    self.process_optionlist()
                else:
                    self.process_prompt()

            else:
                self.line_echo()

            self.advance_line()
        
        return self.data

    def process_optionlist(self):
        prompt = self.re_prompt.match(self.lines[self.current_line])
        self.advance_line()

        options = []
        
        while (True):
            if (self.line_is_option()):
                options.append(self.re_option.match(self.lines[self.current_line]).group(1))

                if (self.line_is_option(1)):
                    self.advance_line()
                else: 
                    break
            else:
                break
        
        self.data[prompt.group(1)] = cli.choose(prompt.group(2), options)

    def advance_line(self):
        self.current_line += 1

    def line_echo(self):
        print(self.lines[self.current_line])

    def line_is_prompt(self, lookahead = 0):
        if (self.current_line + lookahead) >= len(self.lines):
            return False

        return self.re_prompt.match(self.lines[self.current_line + lookahead])

    def line_is_option(self, lookahead = 0):
        if (self.current_line + lookahead) >= len(self.lines):
            return False
        
        return self.re_option.match(self.lines[self.current_line + lookahead])

    def process_prompt(self):
        match = self.re_prompt.match(self.lines[self.current_line])
        answer = cli.user_input(match.group(2) + ' ')

        self.data[match.group(1)] = answer

# used for interactive testing in dev
if __name__ == "__main__":
    """
    text = '\n'.join([
        'Lets test some',
        'age: How old are you?',
        'name: What is your name?',
        'the_job: What is your job?'
        '   - Painter',
        '   - Carpenter',
        '   - Else',
        'something else: Thats not a question'
    ])
    """
    text = '\n'.join([
        'the_job: What is your job?',
        '   - Painter',
        '   - Carpenter',
        '   - Else',
        'something else: Thats not a question'
    ])

    ip = InstructionParser()
    ip.parse(text)