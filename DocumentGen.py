from bs4 import BeautifulSoup
import numpy as np
import requests


# Generate fake words
def WordGen(count=5):
    vowel = ['a', 'e', 'i', 'o', 'u']
    alphabet = [chr(ord('a') + i) for i in range(26)]
    consonant = list(set(alphabet) - set(vowel))
    while count:
        l, r = np.random.choice(consonant, 2)
        stem = np.hstack([
            np.random.choice(vowel, np.random.randint(1, 4)),
            np.random.choice(consonant, np.random.randint(1, 4))
        ])
        np.random.shuffle(stem)
        yield l + "".join(stem) + r
        count -= 1


# crawl CET-4 vocabulary
def wordset():
    url = "https://liuxue.ef.com.cn/english-references/english-vocabulary/top-3000-words/"
    res = requests.get(url)
    obj = BeautifulSoup(res.text, "lxml")
    raw = obj.find_all(class_="content")[0].find_all("p")[1].text
    return [word.strip() for word in raw.split("\n")]


if __name__ == '__main__':

    # words = [word for word in WordGen(50)]
    words = wordset()
    print(words)
    documents = [". ".join([
        " ".join(np.random.choice(words, np.random.randint(5, 15)))
        for j in range(np.random.randint(3, 5))]
    ) + "." for i in range(20)]
    with open("documents.txt", "w") as writer:
        writer.write('\n'.join(documents))
