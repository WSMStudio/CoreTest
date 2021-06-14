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
    k = int(op.split("/")[-1])
    response = []
    for doc, w1, w2 in proximity(q1, q2, k, index):
        words = re.split(r"[\s]", docs_raw[doc])
        context = " ".join(words[max(0, w1 - 5): min(len(words), w2 + 5)])
        context = context.replace(words[w1], f"<span class='highlight'>{words[w1]}</span>") \
                         .replace(words[w2], f"<span class='highlight'>{words[w2]}</span>")
        response.append([context, str(doc + 1)])
    return Response(json.dumps({'data': response}), content_type='application/json')


def buildIndex(docs: list):
    index = {}
    for doc_id, doc in enumerate(docs):
        word_id, sen_id = 0, 0
        for para_id, para in enumerate(doc):
            for sen in para:
                for word in sen.split():
                    if word not in index:
                        index[word] = {doc_id: [word_id]}
                    elif doc_id not in index[word]:
                        index[word][doc_id] = [word_id]
                    else:
                        heapq.heappush(index[word][doc_id], word_id)
                    word_id += 1
                sen_id += 1
    return index


def proximity(q1, q2, k, index):
    answer = []
    if not (q1 in index and q2 in index): return answer
    doc_candidates = set(index[q1].keys()) & set(index[q2].keys())
    for doc in doc_candidates:
        p1 = index[q1][doc]
        p2 = index[q2][doc]
        pp1 = pp2 = 0
        print(f"{p1}, {p2}")
        while pp1 < len(p1) and pp2 < len(p2):
            if p2[pp2] - p1[pp1] < 0:
                pp2 += 1
            elif p2[pp2] - p1[pp1] <= k:
                answer.append((doc, p1[pp1], p2[pp2]))
                pp2 += 1
            else:
                pp1 += 1
        for i in range(pp1 + 1, len(p1)):
            if 0 < p2[-1] - p1[i] <= k:
                answer.append((doc, p1[i], p2[-1]))
        for i in range(pp2 + 1, len(p2)):
            if 0 < p2[i] - p1[-1] <= k:
                answer.append((doc, p1[-1], p2[i]))
    print(answer)
    return answer


with open('statics/doc/documents.txt', 'r') as reader:
    docs = []
    for document in reader.read().split('\n\n'):
        doc = []
        for para in document.split('\n'):
            para = re.sub(r'[,\'\":]', "", para)
            sens = re.split(r'[\.\?!]', para)
            sens = [sen for sen in sens if sen]
            doc.append(sens)
        docs.append(doc)

index = buildIndex(docs)
with open('statics/doc/documents.txt', 'r') as reader:
    docs_raw = reader.read().split("\n\n")

server = pywsgi.WSGIServer(("localhost", 8000), app)
try:
    server.serve_forever()
except KeyboardInterrupt:
    print('Searching Engine stopped serving.')
