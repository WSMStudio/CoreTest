import re


class Indexer:

    def __init__(self):
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
                        print(pid)
        elif where == 'S':
            pass
        print(answer)
        return answer


indexer = Indexer()
indexer.buildIndex()
pre_n = indexer.proximity("to", "the", 3, pre=False, where='P')