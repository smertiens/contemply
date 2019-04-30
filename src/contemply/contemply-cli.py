from contemply.parser import *

if __name__ == '__main__':
    print('Contemply')

    parser = TemplateParser()
    parser._parse('funcname ("arg1","arg2",["lst_agr_1", 123])')
    parser._parse('varname = 124')
