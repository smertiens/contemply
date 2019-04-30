class Token:

    def __init__(self, ttype, val=None):
        self._type = ttype
        self._val = val

    def value(self):
        return self._val

    def type(self):
        return self._type

    def __str__(self):
        return 'Token: {0} ({1})'.format(self._type, self._val)

    def __repr__(self):
        return self.__str__()


class ParserException(Exception):
    pass


class Function:

    def __init__(self, name, args):
        self._name = name
        self._args = args

    def name(self):
        return self._name

    def args(self):
        return self._args

    def __str__(self):
        return 'Function: {0} ({1})'.format(self._name, self._args)

    def __repr__(self):
        return self.__str__()


class List:

    def __init__(self, items):
        self._items = items

    def items(self):
        return self._items

    def __str__(self):
        return 'List: {0}'.format(self._items)

    def __repr__(self):
        return self.__str__()


class VariableAssignment:

    def __init__(self, varname, value):
        self._varname = varname
        self._value = value

    def varname(self):
        return self._varname

    def value(self):
        return self._value

    def __str__(self):
        return 'Assignment: {0} = {1}'.format(self._varname, self._value)

    def __repr__(self):
        return self.__str__()


class Condition:
    def __init__(self, lval, rval, comp):
        self._lval = lval
        self._rval = rval
        self._comp = comp

    def lval(self):
        return self._lval

    def rval(self):
        return self._rval

    def comp(self):
        return self._comp

    def solve(self):
        if self.comp() == '==':
            return self.lval() == self.rval()
        elif self.comp() == '<':
            return self.lval() < self.rval()
        elif self.comp() == '>':
            return self.lval() > self.rval()
        elif self.comp() == '<=':
            return self.lval() <= self.rval()
        elif self.comp() == '>=':
            return self.lval() >= self.rval()
        elif self.comp() == '!=':
            return self.lval() != self.rval()
        else:
            raise ParserException("Unrecognized operator: {0}".format(self.comp()))

    def __str__(self):
        return 'Condition: {0} {1} {2} = {3}'.format(self.lval(), self._comp, self._rval, self.solve())

    def __repr__(self):
        return self.__str__()


class Block:
    IF_BLOCK, ELSE_BLOCK = 'IF_BLOCK', 'ELSE_BLOCK'

    def __init__(self, cond, btype):
        self._cond = cond
        self._type = btype

    def cond(self):
        return self._cond

    def type(self):
        return self._type

    def set_type(self, btype):
        self._type = btype

    def __str__(self):
        return 'Block: {0}'.format(self.cond())

    def __repr__(self):
        return self.__str__()
