from boolean_parser.parsers import Parser
import pyparsing as pp


word = pp.Word(pp.alphanums) | pp.quotedString

prox_a = pp.oneOf(['D', 'P', 'S']).setResultsName("type") \
         + pp.Optional('^' + pp.Word(pp.nums).setResultsName('within'))
prox_b = pp.Word(pp.nums).setResultsName('within') | prox_a

prox = pp.Combine(
    pp.Optional("PRE").setResultsName('order')
    + '/'
    + prox_b
).setResultsName('op')

prox_query = pp.Group('[' + word.setResultsName('q1') + prox + word.setResultsName('q2') + ']').setResultsName('prox')

field_1 = pp.Word('CONTENT').setResultsName('field')
value_1 = word.setResultsName('value') | prox_query
group_1 = pp.Group(field_1 + ':' + value_1)


field_2 = pp.oneOf(['AUTHOR', 'YEAR']).setResultsName('field')
value_2 = word.setResultsName('value')
group_2 = pp.Group(field_2 + ':' + value_2)

field_3 = pp.oneOf(['TITLE', 'DESCR']).setResultsName('field')
value_3 = word.setResultsName('value')
group_3 = pp.Group(field_3 + ':' + value_3)


class ProxAction:
    def __init__(self, data):
        self.q1 = data['q1']
        self.q2 = data['q2']
        self.op = data['op']

    def __repr__(self):
        return f'<Prox ({self.q1} {self.op["order"]}/{self.op["within"]} {self.q2})>'


class Action1:
    def __init__(self, data):
        dd = data[0].asDict()
        self.field = dd['field']
        if 'value' in dd:
            self.value = dd['value']
        elif 'prox' in dd:
            self.value = ProxAction(dd['prox'])

    def __repr__(self):
        return f'<Query ({self.field} : {self.value})>'


class Action2:
    def __init__(self, data):
        dd = data[0].asDict()
        self.field = dd['field']
        self.value = dd['value']

    def __repr__(self):
        return f'<Query ({self.field} : {self.value})>'


class Action3:
    def __init__(self, data):
        dd = data[0].asDict()
        self.field = dd['field']
        self.value = dd['value']

    def __repr__(self):
        return f'<Query ({self.field} : {self.value})>'


Parser.build_parser(clauses=[group_1, group_2, group_3], actions=[Action1, Action2, Action3])
parser = Parser()
# res = parser.parse('CONTENT : ["hello world" PRE/D^1 b] and TITLE : abc or AUTHOR : "Mark Twain"')
res = parser.parse('CONTENT : ["hello world" PRE/D^1 b]')
print(res)
