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


def Action1(data):
    dd = data[0].asDict()
    field = dd['field']
    answer = []
    if 'value' in dd:
        value = dd['value']
        response.setdefault('content', []).append(set(dd['value']))
    elif 'prox' in dd:
        value = dd['prox']
        response.setdefault('content', []).append(set(dd['prox']['q1']))
    return f'response["content"][%d]' % (len(response['content']) - 1)


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


def and_(*para):
    res = eval(para[0])
    for s in para:
        res = res & eval(s)
    return res


def or_(*para):
    res = set()
    for s in para:
        res = res | eval(s)
    return res


response = {}
Parser.build_parser(clauses=[group_1, group_2, group_3], actions=[Action1, Action2, Action3])
query_parser = Parser()
res = query_parser.parse('CONTENT : [world PRE/D^1 world] and CONTENT : hello')
# res = query_parser.parse('CONTENT : ["hello world" PRE/D^1 b]')
print(res)
print(eval(res.__repr__()))
