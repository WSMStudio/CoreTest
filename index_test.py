import re, pickle, os

indexes, bads = {}, []

with open('docs.id', 'rb') as reader:
    docs = pickle.load(reader)

for i, doc_id in enumerate(docs):
    if i % 10 == 0:
        print(f"Busy with {i}/{4954} ...")
    if not os.path.exists(f"../crawler/guten_data/content/pg{doc_id}.txt"):
        bads.append(doc_id)
        print(doc_id)
        continue
    with open(f"../crawler/guten_data/content/pg{doc_id}.txt", "r") as reader:
        doc = reader.read()
    word_id = 0
    for para_id, para in enumerate(re.split(r'[\n]+', doc)):
        para = re.sub(r'[^a-z0-9\.\?!\s]', "", para)
        for sen_id, sen in enumerate(re.split(r'[\.\?!]', para)):
            for word in sen.split():
                indexes.setdefault(word, {}).setdefault(doc_id, []).append((para_id, sen_id, word_id))
                word_id += 1

with open('bads.id', 'wb') as writer:
    pickle.dump(bads, writer, 2)

with open('content.index', 'wb') as writer:
    pickle.dump(indexes, writer, 2)