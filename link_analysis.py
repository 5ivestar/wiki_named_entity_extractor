import json
import glob
import sys
from urllib.parse import unquote
from collections import defaultdict, Counter

from bs4 import BeautifulSoup

if len(sys.argv)<2:
    print("usage: $python {} <extracted_directory>".format(sys.argv[0]))
    exit(1)

d = defaultdict(Counter)
files = glob.glob('{}/**/wiki*'.format(sys.argv[1]))
for file in files:
    print(file)
    with open(file,encoding="utf-8") as f:
        doc = f.read()
    soup = BeautifulSoup(doc)
    for link in soup.find_all('a', href=True):
        if link.has_attr('href'):
            href = unquote(link['href'])
            text = link.text
            d[href][text] += 1

with open('linkfreq.json', 'w',encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False)
