import os
from index import Index
from pymongo import MongoClient
from searcher import Searcher


if __name__ == "__main__":
    client = MongoClient(port=27017)
    if not 'CS121Project3' in client.list_database_names():
        Index().loop_urls(client)

    db = client["CS121Project3"]
    searcher = Searcher(db)

    f = open("log.txt", "w")

    is_searching = True
    while is_searching:
        query = input("Enter a query: ")
        while len(query)==0:
            query = input("Enter a valid query: ")

        ranked_results = searcher.find(query)


        f.write("\nQuery: " + query)
        for result in ranked_results:
            print(result[0])
            f.write("\n\t" + result[0])

        continue_search = input("Do you want to continue searching? (Y/N): ")
        while continue_search.lower()!="y":
            if continue_search.lower()=="n":
                is_searching=False
                break
            else:
                continue_search = input("Do you want to continue searching? (Y/N): ")
         
    
    f.close()
    