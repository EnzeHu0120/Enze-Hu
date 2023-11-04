from html.parser import HTMLParser
import json
import re

class MyHTMLParser(HTMLParser): # From https://docs.python.org/3/library/html.parser.html
    def __init__(self):
        super().__init__()
        self.reset()
        self.tag = None
        self.is_in_body = False
        self.data = []
        self.important_data = dict()

    def handle_starttag(self, tag, attrs):
        self.tag=tag
        if tag == "body":
            self.is_in_body=True

    def handle_endtag(self, tag):
        self.tag = None
        if tag == "body":
            self.is_in_body=False

    def handle_data(self, d):
        if (self.is_in_body and self.tag!="script") or self.tag== "title":
            self.data.append(d)

        words=re.split("[^a-z0-9]+",d.lower())
        words=filter(None,words)
        if self.tag=="h1":
            if not "h1" in self.important_data:
                self.important_data["h1"]=set(words)
            else:
                self.important_data["h1"].union(set(words))
        elif self.tag=="h2":
            if not "h2" in self.important_data:
                self.important_data["h2"]=set(words)
            else:
                self.important_data["h2"].union(set(words))
        elif self.tag=="h3":
            if not "h3" in self.important_data:
                self.important_data["h3"]=set(words)
            else:
                self.important_data["h3"].union(set(words))
        elif self.tag=="b":
            if not "b" in self.important_data:
                self.important_data["b"]=set(words)
            else:
                self.important_data["b"].union(set(words))
        elif self.tag=="title":
            if not "title" in self.important_data:
                self.important_data["title"]=set(words)
            else:
                self.important_data["title"].union(set(words))

    def get_data(self):
        return ' '.join(self.data)

    def get_important_words(self):
        for k,v in self.important_data.items():
            self.important_data[k] = list(v)
        return self.important_data