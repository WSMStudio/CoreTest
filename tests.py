import re


def buildIndex():
    index = {}
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

    for doc_id, doc in enumerate(docs):
        word_id = 0
        for para_id, para in enumerate(doc):
            for sen_id, sen in enumerate(para):
                for word in sen.split():
                    if word not in index:
                        index[word] = {}
                    if doc_id not in index[word]:
                        index[word][doc_id] = {}
                    if para_id not in index[word][doc_id]:
                        index[word][doc_id][para_id] = {}
                    if sen_id not in index[word][doc_id][para_id]:
                        index[word][doc_id][para_id][sen_id] = []
                    index[word][doc_id][para_id][sen_id].append({'wid': word_id, 'next': None, 'prev': None})
                    word_id += 1

        for word in index:
            queue = [index[word]]
            prev = None
            while queue:
                tmp = queue.pop()
                if type(tmp) == list:
                    for p in tmp:
                        p['prev'] = prev
                        prev = p
                else:
                    queue = list(tmp.values()) + queue
            while prev:
                prev['prev']['next'] = prev
                prev = prev['prev']
            print()
    return index


# def proximity(q1, q2, k, index):
#     answer = []
#     if not (q1 in index and q2 in index): return answer
#     doc_candidates = set(index[q1].keys()) & set(index[q2].keys())
#     for doc in doc_candidates:
#         p1 = index[q1][doc]
#         p2 = index[q2][doc]
#         pp1 = pp2 = 0
#         print(f"{p1}, {p2}")
#         while pp1 < len(p1) and pp2 < len(p2):
#             if p2[pp2] - p1[pp1] < 0:
#                 pp2 += 1
#             elif p2[pp2] - p1[pp1] <= k:
#                 answer.append((doc, p1[pp1], p2[pp2]))
#                 pp2 += 1
#             else:
#                 pp1 += 1
#         for i in range(pp1 + 1, len(p1)):
#             if 0 < p2[-1] - p1[i] <= k:
#                 answer.append((doc, p1[i], p2[-1]))
#         for i in range(pp2 + 1, len(p2)):
#             if 0 < p2[i] - p1[-1] <= k:
#                 answer.append((doc, p1[-1], p2[i]))
#     print(answer)
#     return answer


index = buildIndex()
# with open('statics/doc/documents.txt', 'r') as reader:
#     docs_raw = reader.read().split("\n\n")

# print(proximity("and", "the", 1, index))

# print(index)
