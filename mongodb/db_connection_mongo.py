#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here



import string
from pymongo import MongoClient


def connectDataBase():

    # Create a database connection object using psycopg2
    # --> add your Python code here
    client = MongoClient(host=['localhost:27017'])
    db_cur = client["corpus"]
    
    
    return db_cur


def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    

    # count number of chars, excluding spaces
    docText_noSpaces = docText.replace(" ","")
    docText_punc = docText_noSpaces.translate(str.maketrans('', '', string.punctuation))
    num_chars = len(docText_punc)
    
    # get list of terms
    docText_clearPunc = docText.translate(str.maketrans('', '', string.punctuation))
    docText_lower = docText_clearPunc.lower()
    docText_terms = docText_lower.split()
   
    term_map = {}
    for term in docText_terms:
        if term in term_map:
            term_map[term] += 1
        else:
            term_map[term] = 1
            
            
    # add terms to the term collection
    # add a reference the document being created to each appropriate term
    term_collec = cur['term']

    for term, count in term_map.items():
        
        # check if term already exists
        query_term_exists = {"term": term}
        if term_collec.find_one(query_term_exists):
            
            new_document = {
                "_id" : docId,
                "count": count,
                "title" : docTitle,
                "text" : docText,
                "num_chars" : num_chars,
                "date" : docDate,
                "category" : docCat,
            }
        
            term_collec.update_one({"term" : term}, {"$push": {"docs" : new_document}}, upsert = True)
            
        else:
            new_term = {
                "term" : term,
                "num_chars" : len(term),
                "docs": [
                    {
                        "_id" : docId,
                        "count": count,
                        "title" : docTitle,
                        "text" : docText,
                        "num_chars" : num_chars,
                        "date" : docDate,
                        "category" : docCat,
                    }
                ]
            }
        
            term_collec.insert_one(new_term)



def deleteDocument(cur, docId):
    
    term_collec = cur['term']
    
    num_deleted = term_collec.update_many(
        {},
        {"$pull": {"docs": {"_id": docId}}}
    
    )
    print(num_deleted)
        
    term_collec.delete_many({"docs" : { "$size" : 0}})


def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    # --> add your Python code here
    deleteDocument(cur, docId)

    # 2 Create the document with the same id
    # --> add your Python code here
    createDocument(cur, docId, docText, docTitle, docDate, docCat)
    

'''
def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    # 
    # 
    index_map = {}
    
    term_collec = cur['term']
    term_documents = term_collec.find({})
    
    for term_doc in term_documents:
        cur_term = term_doc["term"]
        
        for doc in term_doc['docs']:
            doc_id = doc["doc_id"]
            count = doc["count"]
            doc_collect = cur["document"]
            doc_document = doc_collect.find_one({"_id" : doc_id})
            doc_title = doc_document["title"]
            
            if cur_term in index_map:
                index_map[cur_term][doc_title] = count
            else:
                index_map[cur_term] = {}
                index_map[cur_term][doc_title] = count
                 
    inverse_index = "{"
    for key, inner_dict in index_map.items():
        inner_string = ",".join([f"{category}:{count}" for category, count in inner_dict.items()])
        inverse_index += f"'{key}':'{inner_string}',"
        
    inverse_index = "\n" + inverse_index.rstrip(',') + "}"
    
    return inverse_index

'''
    
