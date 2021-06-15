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

    def proximity(self, q1, q2, k, pre=False):
        answer = []
        if not (q1 in self.index and q2 in self.index): return answer
        doc_candidates = set(self.index[q1].keys()) & set(self.index[q2].keys())
        within_k = (lambda x, y: x - y <= k) if pre else (lambda x, y: abs(x - y) <= k)
        within_k_0 = (lambda x, y: 0 < x - y <= k) if pre else within_k
        for doc in doc_candidates:
            p1 = self.index[q1][doc]
            p2 = self.index[q2][doc]
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
        print(answer)
        return answer


indexer = Indexer()
indexer.buildIndex()
pre_n = indexer.proximity("to", "the", 3, pre=False)
pre_y = indexer.proximity("to", "the", 3, pre=True)
print(set(pre_n) - set(pre_y))