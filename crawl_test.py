import requests
url = "https://gutenberg.org/files/52/52.txt"

res = requests.get(url)
print(res.text)