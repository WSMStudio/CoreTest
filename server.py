from flask import Flask
from flask import request
from flask import render_template
from flask import Response, json
from gevent import pywsgi
import heapq
import re

app = Flask(__name__, template_folder="templates", static_folder="statics", static_url_path="/static")


@app.route('/', methods=['GET'])
def paste():
    return render_template("index.html")


@app.route('/search', methods=['POST'])
def search():
    # GET: request.args.get('text')
    query = request.form.get('query').split()
    if len(query) < 3:
        return Response(json.dumps({'code': -1}), content_type='application/json')
    q1, op, q2 = query
    pre, foo = op.split("/")
    where, k = foo.split('^')
    response = []
    for doc, w1, w2 in indexer.proximity(q1, q2, int(k), where=where.upper(), pre=bool(pre)):
        words = re.split(r"[\s]", indexer.docs_raw[doc])
        context = " ".join(words[max(0, w1 - 5): min(len(words), w2 + 5)])
        context = context.replace(" " + words[w1] + " ", f" <span class='highlight'>{words[w1]}</span> ") \
            .replace(" " + words[w2] + " ", f" <span class='highlight'>{words[w2]}</span> ")
        response.append([context, str(doc + 1)])
    return Response(json.dumps({'data': response}), content_type='application/json')


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
        answer = []
        within_k = (lambda x, y: x - y <= k) if pre else (lambda x, y: abs(x - y) <= k)
        within_k_0 = (lambda x, y: 0 < x - y <= k) if pre else within_k
        pp1 = pp2 = 0
        while pp1 < len(p1) and pp2 < len(p2):
            if pre and p2[pp2][-1] - p1[pp1][-1] < 0:
                pp2 += 1
            elif within_k(p2[pp2][-1], p1[pp1][-1]):
                answer.append((doc, p1[pp1][-1], p2[pp2][-1]))
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
                answer.append((doc, p1[i][-1], p2[-1][-1]))
        for i in range(pp2 + 1, len(p2)):
            if within_k_0(p2[i][-1], p1[-1][-1]):
                answer.append((doc, p1[-1][-1], p2[i][-1]))
        return answer

    def proximity(self, q1, q2, k, where='D', pre=False):
        answer = []
        if not (q1 in self.index and q2 in self.index): return answer
        doc_candidates = set(self.index[q1].keys()) & set(self.index[q2].keys())
        if where == 'D':
            for doc_id in doc_candidates:
                p1 = self.index[q1][doc_id]
                p2 = self.index[q2][doc_id]
                answer += self.foo(p1, p2, doc_id, pre, k)
        elif where == 'P':
            for doc_id in doc_candidates:
                p1 = self.index[q1][doc_id]
                p2 = self.index[q2][doc_id]
                for pid in set([p[0] for p in p1]):
                    cp2 = [p for p in p2 if p[0] == pid]
                    if cp2:
                        cp1 = [p for p in p1 if p[0] == pid]
                        answer += self.foo(cp1, cp2, doc_id, pre, k)
        elif where == 'S':
            for doc_id in doc_candidates:
                p1 = self.index[q1][doc_id]
                p2 = self.index[q2][doc_id]
                for pid, sid in set([p[:2] for p in p1]):
                    cp2 = [p for p in p2 if p[0] == pid and p[1] == sid]
                    if cp2:
                        cp1 = [p for p in p1 if p[0] == pid and p[1] == sid]
                        answer += self.foo(cp1, cp2, doc_id, pre, k)
        print(answer)
        return answer


indexer = Indexer()
indexer.buildIndex()
server = pywsgi.WSGIServer(("localhost", 8000), app)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print('Searching Engine stopped serving.')
