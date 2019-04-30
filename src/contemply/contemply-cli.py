from contemply.parser import *

if __name__ == '__main__':
    print('Contemply')

    parser = TemplateParser()
    parser.parseFile('../../samples/example1.pytpl')
