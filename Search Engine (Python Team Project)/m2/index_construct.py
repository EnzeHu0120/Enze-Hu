import os
from bs4 import BeautifulSoup
from math import log10
import re
from pymongo import MongoClient
from collections import defaultdict
from nltk.corpus import stopwords
import nltk


class Index:
    def __init__(self, js, client):
        self.client = client
        nltk.download('stopwords') # Just comment out if downloaded.
        self.stopwords = set(stopwords.words('english'))
        self.db = self.client['cs121p3']
        self.ind = self.db['ind']
        self.js = js
        self.index = defaultdict(dict)
        self.total_doc = 0
        self.begin()




    def begin(self):
        for id, url in self.js.items():
            doc_inf = id.split('/')
            path = os.path.join("C:\\", "WEBPAGES_RAW", doc_inf[0], doc_inf[1])
            file = open(path, 'r', encoding='utf-8')
            bs = BeautifulSoup(file, 'lxml')
            bs_txt = bs.get_text()
            title = bs.find('title')
            bold = bs.find('b')
            h1 = bs.find('h1')
            h2 = bs.find('h2')
            h3 = bs.find('h3')
            tdict = defaultdict(int)
            for i in re.findall(re.compile(r"[A-Za-z0-9]+"), bs_txt):
                if i not in self.stopwords:
                    tdict[str(i.lower())] += 1
            self.total_doc += 1
            list_tag = [title, bold, h1, h2, h3]
            for k, v in tdict.items():
                tag_score = 0
                standard = 1
                for i in list_tag:
                    if i is not None and i.string is not None and k in i.string.lower():
                        tag_score += standard
                    standard -= 0.2
                if k not in self.index:
                    self.index[k] = {'_id': k, 'index': defaultdict(dict)}
                self.index[k]['index'][id]['tf'] = v
                self.index[k]['index'][id]['tag_score'] = tag_score
                self.index[k]['index'][id]['URL'] = url
            file.close()
        for t in self.index.values():
            for ind in t['index'].values():
                idf = self.total_doc / len(t['index'])
                ind['tf-idf'] = (1 + log10(ind['tf'])) * log10(idf)
        self.ind.insert_many(self.index.values())





