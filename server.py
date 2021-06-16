from flask import Flask
from flask import request
from flask import render_template
from flask import Response, json
from gevent import pywsgi
import re

from boolean_parser.parsers import Parser
from query_parser import group_1, group_2, group_3

app = Flask(__name__, template_folder="templates", static_folder="statics", static_url_path="/static")


class Indexer:

    def __init__(self):
        with open('statics/doc/documents.txt', 'r') as reader:
            self.docs_raw = reader.read().split("\n\n")
        self.index = {}

    def buildIndex(self):
        with open('statics/doc/documents.txt', 'r') as reader:
            docs = reader.read()
        for doc_id, doc in enumerate(docs.split('\n\n')):
            word_id = 0
            for para_id, para in enumerate(doc.split('\n')):
                para = re.sub(r'[,\'\":]', "", para)
                for sen_id, sen in enumerate(re.split(r'[\.\?!]', para)):
                    for word in sen.split():
                        self.index.setdefault(word, {}).setdefault(doc_id, []).append((para_id, sen_id, word_id))
                        word_id += 1
        return self.index

    def foo(self, p1, p2, doc, pre, k):
        answer = {}
        within_k = (lambda x, y: x - y <= k) if pre else (lambda x, y: abs(x - y) <= k)
        within_k_0 = (lambda x, y: 0 < x - y <= k) if pre else within_k
        pp1 = pp2 = 0
        while pp1 < len(p1) and pp2 < len(p2):
            if pre and p2[pp2][-1] - p1[pp1][-1] < 0:
                pp2 += 1
            elif within_k(p2[pp2][-1], p1[pp1][-1]):
                answer.setdefault(doc, []).append((p1[pp1][-1], p2[pp2][-1]))
                if p2[pp2][-1] > p1[pp1][-1]:
                    pp2 += 1
                else:
                    pp1 += 1
            else:
                if p2[pp2][-1] > p1[pp1][-1]:
                    pp1 += 1
                else:
                    pp2 += 1
        for i in range(pp1 + 1, len(p1)):
            if within_k_0(p2[-1][-1], p1[i][-1]):
                answer.setdefault(doc, []).append((p1[i][-1], p2[-1][-1]))
        for i in range(pp2 + 1, len(p2)):
            if within_k_0(p2[i][-1], p1[-1][-1]):
                answer.setdefault(doc, []).append((p1[-1][-1], p2[i][-1]))
        return answer

    def proximity(self, q1, q2, k, where='D', pre=False):
        answer = {}
        if not (q1 in self.index and q2 in self.index): return answer
        doc_candidates = set(self.index[q1].keys()) & set(self.index[q2].keys())
        if where == 'D':
            for doc_id in doc_candidates:
                p1 = self.index[q1][doc_id]
                p2 = self.index[q2][doc_id]
                answer.update(self.foo(p1, p2, doc_id, pre, k))
        elif where == 'P':
            for doc_id in doc_candidates:
                p1 = self.index[q1][doc_id]
                p2 = self.index[q2][doc_id]
                for pid in set([p[0] for p in p1]):
                    cp2 = [p for p in p2 if p[0] == pid]
                    if cp2:
                        cp1 = [p for p in p1 if p[0] == pid]
                        for key, value in self.foo(cp1, cp2, doc_id, pre, k).items():
                            answer.setdefault(key, []).extend(value)
        elif where == 'S':
            for doc_id in doc_candidates:
                p1 = self.index[q1][doc_id]
                p2 = self.index[q2][doc_id]
                for pid, sid in set([p[:2] for p in p1]):
                    cp2 = [p for p in p2 if p[0] == pid and p[1] == sid]
                    if cp2:
                        cp1 = [p for p in p1 if p[0] == pid and p[1] == sid]
                        for key, value in self.foo(cp1, cp2, doc_id, pre, k).items():
                            answer.setdefault(key, []).extend(value)
        # print(answer)
        return answer

    def search_content(self, q1, q2, k, where, pre):
        res = {}
        for doc, value in sorted(self.proximity(q1, q2, k, where=where, pre=pre).items(), key=lambda x: x[0]):
            for w1, w2 in value:
                words = re.split(r"[\s]", indexer.docs_raw[doc])
                w1, w2 = min(w1, w2), max(w1, w2)
                context = " ".join(words[max(0, w1 - 5): min(len(words), w2 + 5)])
                context = context.replace(" " + words[w1] + " ", f" <span class='highlight'>{words[w1]}</span> ") \
                    .replace(" " + words[w2] + " ", f" <span class='highlight'>{words[w2]}</span> ")
                res.setdefault(doc, []).append(context)
        return res


def prox_action(data):
    q1 = data['q1']
    q2 = data['q2']
    op = data['op']
    pre = 'order' in op
    where = op.get('type', 'D').upper()
    k = int(op.get('within', 1e9))
    command.setdefault('content', []) \
        .append((q1, q2, k, where, pre))
    return data


class Action1:
    def __init__(self, data):
        dd = data[0].asDict()
        self.field = dd['field']
        if 'value' in dd:
            self.value = dd['value']
        elif 'prox' in dd:
            self.value = prox_action(dd['prox'])

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


@app.route('/', methods=['GET'])
def paste():
    return render_template("index.html")


@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    command.clear()
    query_parser.parse(query)
    response = {}
    if "content" in command:
        for q1, q2, k, where, pre in command['content']:
            response = indexer.search_content(q1, q2, k, where, pre)
    return Response(json.dumps({'data': response}), content_type='application/json')


Parser.build_parser(clauses=[group_1, group_2, group_3], actions=[Action1, Action2, Action3])
query_parser = Parser()
indexer = Indexer()
indexer.buildIndex()
command = {}
server = pywsgi.WSGIServer(("localhost", 8000), app)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print('Searching Engine stopped serving.')
