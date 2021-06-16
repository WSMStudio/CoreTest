import re, pickle, requests, time

indexes, docs = {}, []

with open('../crawler/guten_data/content/error.txt', 'r') as reader:
    bads = [int(bad_id) for bad_id in reader.readlines()]

with open('gutenberg_0-4999.txt', 'r') as reader:
    indexes['ptime'] = {}
    indexes['descr'] = {}
    indexes['title'] = {}
    indexes['authr'] = {}
    for line in reader.readlines():
        link_intro, authors, title, ptime, descr, link_down = line.split('\t')
        authors = [author.strip() for author in authors.split(',') if not "-" in author]
        doc_id = int(link_intro.split("/")[-1])

        # if doc_id > 2202 and doc_id in bads and link_down.strip().endswith(".txt"):
        #     res = requests.get(link_down.strip())
        #     with open(f"pg{doc_id}.txt", 'w') as writer:
        #         writer.write(res.text)
        #     print(doc_id, link_down, res.status_code)
        #     time.sleep(0.3)

        indexes['ptime'].setdefault(ptime, set()).add(doc_id)

        if descr == "No description": descr = ""
        descr = re.sub(r'[^a-z0-9\s]', "", descr)
        for word in re.split(r'\s', descr):
            indexes['descr'].setdefault(word, set()).add(doc_id)

        title = re.sub(r'[^a-z0-9\s]', "", title)
        for word in re.split(r'\s', title):
            indexes['title'].setdefault(word, set()).add(doc_id)

        for author in authors:
            author = re.sub(r"[^a-z\s]", "", author)
            for word in re.split(r'\s', author):
                indexes['authr'].setdefault(word, set()).add(doc_id)

        docs.append(doc_id)

file = open("docs.id", 'wb')
pickle.dump(docs, file, 2)

file = open('meta.index', 'wb')
pickle.dump(indexes, file, 2)
