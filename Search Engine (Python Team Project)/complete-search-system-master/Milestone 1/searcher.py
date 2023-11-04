from pymongo import MongoClient
import math

class Searcher:
    def __init__(self,db):
        self.tfidf = db["TfIdf"]
        self.tags = db["Tags"]

    def find(self,query):
        scores = dict()

        query_words = query.lower().split()
        for term in set(query_words):
            myquery = {"term": term}            
            url_score = self.tfidf.find(myquery)
            
            if url_score.count()>0:
                for k,v in url_score[0]['URLs'].items():
                    if not k in scores:
                        scores[k]=v
                    else:
                        scores[k]+=v

        sorted_scores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        for url in sorted_scores[:20]:
            myquery = {"URL": url}
            tag_score = self.tags.find(myquery)

            if tag_score.count()>0:
                for k,v in tag_score[0]['tags'].items():
                    for word in v:
                        if word in query_words:
                            if k=="title":
                                scores[url]+=2
                            elif k=="h1":
                                scores[url]+=1
                            elif k=="h2":
                                scores[url]+=.5
                            elif k=="h3":
                                scores[url]+=.25
                            elif k=="b":
                                scores[url]+=1

        return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:20]