import tkinter
from index import Index
from pymongo import MongoClient
from searcher import Searcher
import webbrowser

def internet(e):
    weblink = mylist.get(tkinter.ACTIVE)
    webbrowser.open(weblink)

def search_and_show():
    query = query_box.get()
    
    ranked_results = searcher.find(query)
    
    output = []
    for result in ranked_results:
        output.append(result[0])

    mylist.delete(0,tkinter.END)
    
    for line in output:
        mylist.insert( tkinter.END, str(line))
    mylist.bind( "<Double-Button-1>" , internet )
    mylist.pack( side = tkinter.TOP, fill = tkinter.BOTH, expand=tkinter.YES )
    
    tkinter.mainloop()
    

if __name__ == "__main__":
    client = MongoClient(port=27017)
    if not 'CS121Project3' in client.list_database_names():
        Index().loop_urls(client)

    database = client["CS121Project3"]
    searcher = Searcher(database)
    
    m = tkinter.Tk()
    m.title('Search the ICS Domain')
    m.geometry("600x600")
    tkinter.Label(m, text='Enter a query:').pack(side=tkinter.TOP, fill=tkinter.BOTH)
    query_box = tkinter.Entry(m)
    submit_button = tkinter.Button(m, text="Search", command=search_and_show)
    query_box.pack(side = tkinter.TOP, fill = tkinter.BOTH)
    submit_button.pack(side = tkinter.TOP, fill = tkinter.BOTH)

    mylist = tkinter.Listbox(m)

    m.mainloop()



