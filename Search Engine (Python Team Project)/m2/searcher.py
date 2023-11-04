from pymongo import MongoClient
from collections import defaultdict
import json
import os
from bs4 import BeautifulSoup


class Searcher:
    def __init__(self, client, query):
        self.client = client
        self.query = query
        self.index = self.client['cs121p3']['ind']

    def search(self):
        query_list = self.query.split()
        score_dict = defaultdict(float)
        url_list = []
        for i in set(query_list):
            query = {'_id': i}
            if self.index.count_documents(query) > 0:
                find = self.index.find(query)
                tdic = find.next()
                idict = tdic['index']
                for k, v in sorted(idict.items(), key=lambda x: x[1]['tf-idf'], reverse=True):
                    if k not in score_dict:
                        score_dict[k] = idict[k]['tf-idf'] + idict[k]['tag_score']
                    else:
                        score_dict[k] += idict[k]['tf-idf'] + idict[k]['tag_score']
        for k, v in sorted(score_dict.items(), key=lambda x: x[1], reverse=True):
            url_list.append(k)

        return url_list

    def convert_url(self, url_list, start, end):
        title_dic = {}
        if len(url_list) > 0:
            if end > len(url_list):
                end = len(url_list)
            for i in range(start, end):
                url = json.load(open("C:\\WEBPAGES_RAW\\bookkeeping.json"))[url_list[i]]
                doc_inf = url_list[i].split('/')
                path = os.path.join("C:\\", "WEBPAGES_RAW", doc_inf[0], doc_inf[1])
                file = open(path, 'r', encoding='utf-8')
                bs = BeautifulSoup(file, 'lxml')
                title = url
                tag = bs.find('title')
                if tag is not None and tag.string is not None:
                    title = tag.string.strip()
                title_dic[title] = url
        return title_dic



