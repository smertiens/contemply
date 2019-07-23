from pygments.lexer import RegexLexer, include, words, bygroups
from pygments.token import *

keywords = ('for', 'in', 'while', 'endwhile', 'endif', 'if', 'else', 'endfor', 'elseif', 'endif', 'break')
builtins = ('True', 'False', 'None')

class ContemplyLexer(RegexLexer):
    name = 'Contemply'
    aliases = ['contemply']
    filenames = ['*.pytpl']

    tokens = {
        'sqs': [
            (r'.*?\'', String.Literal, '#pop'),
        ],

        'dqs': [
            (r'.*?"', String.Literal, '#pop'),
        ],

        'comment': [
            (r'\s*#%.*\n', Comment)
        ],

        'root': [
            (r'^#::.*\n', Name.Decorator, 'commandblock'),
            (r'^#:', Name.Decorator, 'commandline'),
            include('comment'),
            (r'.*\n', Text)
        ],

        'commandline': [
            (r'\n', Text, '#pop'),
            include('commandblock')
        ],

        'commandblock': [
            (r'^#::.*\n', Name.Decorator, '#pop'),
            (r'\'', String.Literal, 'sqs'),
            (r'"', String.Literal, 'dqs'),
            (r'\-\>', Keyword),
            (r'\>\>', Keyword),
            (r'\<\<', Keyword),
            (r'\d+', Number),
            (r'[,\[\]]', Punctuation),
            (r'\s+', Text),
            (r'(\w+)(\s*)(\()', bygroups(Name.Function, Text, Punctuation), 'function'),
            (words(keywords, suffix=r'\b'), Keyword),
            (words(builtins, suffix=r'\b'), Name.Builtin),
            (r'\w+', Name.Variable),
            (r'(\+=|\+|\-|\/|\*|==|=|!=|\<|\>)', Operator),
            include('comment')
        ],

        'function': [
            (r'\)', Punctuation, '#pop'),
            include('commandblock')
        ]
    }

def setup(app):
    app.add_lexer("contemply", ContemplyLexer())
    return {'version': '0.1'}   # identifies the version of our extension
