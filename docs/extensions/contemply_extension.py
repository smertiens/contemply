from pygments_contemply import contemply_lexer

def setup(app):
    app.add_lexer("contemply", contemply_lexer.ContemplyLexer())
    return {'version': '0.1'}   # identifies the version of our extension