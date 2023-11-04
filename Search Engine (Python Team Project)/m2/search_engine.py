from tkinter import *
from pymongo import MongoClient
import json
import index_construct
import searcher
import webbrowser
from bs4 import BeautifulSoup
import os
import tkinter.messagebox

class Search:
    def __init__(self):
        self.client = MongoClient(port=27017)
        self.index = self.db_initialization()
        self.tk = Tk()
        self.showurl = False
        self.tk.title('Welcome to ICS Searching Engine!')
        self.tk.geometry("600x600")
        label = Label(self.tk, text='Enter your words:')
        label.pack(side=TOP, fill=BOTH)
        self.query = Entry(self.tk)
        self.query.pack(side=TOP, fill=BOTH)
        search_button = Button(self.tk, text="Search", command=self.result)
        search_button.pack(side=TOP, fill=BOTH)
        self.leftbutton = Button(self.tk, text='Previous', command=self.goleft)
        self.leftbutton.pack(side=TOP, fill=BOTH)
        self.leftbutton['state'] = DISABLED
        self.rightbutton = Button(self.tk, text='Next', command=self.goright)
        self.rightbutton.pack(side=TOP, fill=BOTH)
        self.rightbutton['state'] = DISABLED
        self.urlbutton = Button(self.tk, text='show URL ', command=self.show_url)
        self.urlbutton.pack(side=TOP, fill=BOTH)
        self.titlebutton = Button(self.tk, text='Show Website Title', command=self.show_title)
        self.titlebutton.pack(side=TOP, fill=BOTH)
        self.urlbutton['state'] = DISABLED
        self.titlebutton['state'] = DISABLED
        self.url_list = Listbox(self.tk)
        self.start = 0
        self.end = 20
        self.search_result = {}
        mainloop()


    def show_url(self):
        self.showurl = True
        self.result()

    def show_title(self):
        self.showurl = False
        self.result()

    def result(self):
        query_word = self.query.get()
        search = searcher.Searcher(self.client, query_word)
        self.search_result = search.convert_url(search.search(), self.start, self.end)
        if len(self.search_result) == 0:
            self.leftbutton['state'] = DISABLED
            self.rightbutton['state'] = DISABLED
            self.url_list.delete(0, END)
            tkinter.messagebox.showinfo('Warning!', 'Sorry, No result found!')
        else:
            self.url_list.delete(0, END)
            if self.showurl:
                self.urlbutton['state'] = DISABLED
                self.titlebutton['state'] = NORMAL
                for i in self.search_result.values():
                    self.url_list.insert(END, i)
                self.url_list.bind("<<ListboxSelect>>", self.open_url)
                self.url_list.pack(side=TOP, fill=BOTH, expand=YES)
                self.rightbutton['state'] = NORMAL
            else:
                self.urlbutton['state'] = NORMAL
                self.titlebutton['state'] = DISABLED
                for i in self.search_result.keys():
                    self.url_list.insert(END, i)
                self.url_list.bind("<<ListboxSelect>>", self.open_title)
                self.url_list.pack(side=TOP, fill=BOTH, expand=YES)
                self.rightbutton['state'] = NORMAL
        mainloop()

    def goleft(self):
        self.start -= 20
        self.end -= 20
        if self.start == 0 and self.end == 20:
            self.leftbutton['state'] = DISABLED
        self.result()

    def goright(self):
        self.start += 20
        self.end += 20
        self.leftbutton['state'] = NORMAL
        self.result()

    def open_title(self, args):
        link = self.url_list.get(ACTIVE)
        webbrowser.open(self.search_result[str(link)])

    def open_url(self, args):
        link = self.url_list.get(ACTIVE)
        webbrowser.open(link)

    def db_initialization(self):
        if 'cs121p3' not in self.client.list_database_names():
            js = json.load(open("C:\\WEBPAGES_RAW\\bookkeeping.json", encoding='utf-8'))
            return index_construct.Index(js, self.client).ind
        else:
            return self.client['cs121p3']['ind']


if __name__ == "__main__":
    Search()

