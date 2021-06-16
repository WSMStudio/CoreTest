from boolean_parser.parsers import Parser
# from boolean_parser.clauses import words

# x = Parser('TITLE="a" and CONTENT="B" or AUTHOR="C"')
# print(x.parse())
# 'conditions', 'filter', 'logicop', 'params'

import pyparsing as pp

field = pp.oneOf(['TITLE', 'AUTHOR', 'YEAR']).setResultsName('field')
op = pp.oneOf(['=', ':']).setResultsName('op')
value = pp.dblQuotedString.setResultsName('value')
query = pp.Group(field + op + value).setResultsName('query')


class Street(object):
    def __init__(self, data):
        dd = data[0].asDict()
        self.field = dd['field']
        self.op = dd['op']
        self.value = dd['value']

    def __repr__(self):
        return f'<Query ({self.field} {self.op} {self.value})>'


Parser.build_parser(clauses=[query], actions=[Street])

parser = Parser()
res = parser.parse('TITLE = "hello world" and AUTHOR = "abc" or YEAR = "1234"')
print(res)
