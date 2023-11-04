from pymongo import MongoClient

client = MongoClient(port=27017)
if not 'CS121Project3' in client.list_database_names():
    print("No database found.")
    quit()

db = client["CS121Project3"]

urls = set()
for document in db["TfIdf"].find():
    urls.update(set(document['URLs'].keys()))

call = db.command("dbstats")
datasize = call['dataSize'] 

f = open("database_report.txt", "w")
f.write("Number of Documents: " + str(len(urls)))
f.write("\nNumber of [unique] words: " + str(db["TfIdf"].estimated_document_count()))

f.write("\nDatabase: " + str(call['db']))
f.write('\nObjects:'+ str(call['objects']))
f.write("\nCollections: " +str(call['collections']))
f.write("\nSize of database: " + str(datasize) + " bytes")
f.close()