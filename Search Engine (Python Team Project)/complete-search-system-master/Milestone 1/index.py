import json
import os
from HTMLparser import MyHTMLParser
import math
import re
from db import create_db
from urllib.parse import urlparse, parse_qs

class Index:
    WEBPAGES_RAW_NAME = "WEBPAGES_RAW"
    JSON_FILE_NAME = os.path.join(".", WEBPAGES_RAW_NAME, "bookkeeping.json")

    def __init__(self):
        self.file_url_map = json.load(open(self.JSON_FILE_NAME), encoding="utf-8")
        self.url_file_map = dict()
        for key in self.file_url_map:
            self.url_file_map[self.file_url_map[key]] = key


    def get_file_address(self,url):
        addr = self.url_file_map[url].split("/")
        dir = addr[0]
        file = addr[1]
        return os.path.join(".", self.WEBPAGES_RAW_NAME, dir, file)
    
            
    def loop_urls(self,client):

        tf={}
        df=dict()
        tf_idf = {}
        important_tags = dict()

        valid_doc_count = 0
        for url in self.url_file_map:
            if url not in tf and self.is_not_trap(url,tf):
                valid_doc_count += 1
                file_address = self.get_file_address(url)
                f=open(file_address,"r",encoding="utf8")

                parser = MyHTMLParser()
                parser.feed(f.read())
                text = parser.get_data()

                tf[url]={}
                word_set = set() #for df

                words=re.split("[^a-z0-9]+",text.lower())
                words=list(filter(None,words))
                for word in words:
                    if not word in tf[url]:
                        tf[url][word] = 1
                    else:
                        tf[url][word]+=1
                    if not word in word_set:
                        if not word in df:
                            df[word]=1
                        else:
                            df[word]+=1
                        word_set.add(word)

                important_tags[url]=parser.get_important_words()
                f.close()
        
        for doc in tf:
            for term in tf[doc]:
                if not term in tf_idf.keys():
                    tf_idf[term]={}
                tf_idf[term][doc]=(1+math.log(tf[doc][term],10)) * math.log(valid_doc_count/df[term])

        create_db(client,tf_idf,important_tags)


    def is_not_trap(self, url , urls_seen):
        parsed = urlparse(url)

        if re.search(r"^.*?(/.+?/).*?\1.*\1.*\1.*\1.*\1.*\1.*\1.*\1.*\1.*$|^.*?/(.+?/)\2.*\2.*\2.*\2.*\2.*\2.*\2.*\2.*\2.*$", parsed.path):  #10 times /item/ in a path
            return False

        if len(parsed.query)>0:
            past_urls = list(urls_seen.keys())
            queries = parse_qs(parsed.query)
            count = 0
            for i in range(0,10):
                if len(past_urls)==0:
                    break
                parsed_link = urlparse(past_urls.pop())
                link_queries = parse_qs(parsed_link.query)
                if (parsed.scheme + "://" + parsed.netloc + parsed.path) == (parsed_link.scheme + "://" + parsed_link.netloc + parsed_link.path):
                    if queries.keys() == link_queries.keys():
                        count+=1
            if count==10:
                return False

        return True