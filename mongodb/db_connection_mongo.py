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
    db_cur = client["documents"]
    
    
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

    # add document
    doc_collec = cur['document']
    
    new_document = {
        "_id" : docId,
        "title" : docTitle,
        "text" : docText,
        "num_chars" : num_chars,
        "date" : docDate,
        "category" : docCat,
    }
    
    doc_collec.insert_one(new_document)
    
    
    
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
            
            newIndex = {
                "doc_id" : docId,
                "count" : count
            }
            
            term_collec.update_one({"term" : term}, {"$push": {"docs" : newIndex}}, upsert = True)
            
        else:
            new_term = {
                "term" : term,
                "num_chars" : len(term),
                "docs": [
                    {
                        "doc_id" : docId,
                        "count" : count
                    }
                ]
            }
        
            term_collec.insert_one(new_term)



def deleteDocument(cur, docId):
    
    doc_collec = cur['document']
    document = doc_collec.find_one({"_id" : docId})
    if not document:
        print("Document not found!")
        return
    
    doc_text = document["text"]
    
    # get list of terms
    doc_text_clearPunc = doc_text.translate(str.maketrans('', '', string.punctuation))
    doc_text_lower = doc_text_clearPunc.lower()
    doc_text_terms = doc_text_lower.split()
    
    term_collec = cur['term']
    
    for term in doc_text_terms:
        cur_term = term_collec[term]
        cur_docs_index = cur_term["docs"]
        num_deleted = term_collec.update_many(
            {"term" : term},
            {"$pull": {"docs": {"doc_id": docId}}}
        )
        
        print(num_deleted)
        
    term_collec.delete_many({"docs" : { "$size" : 0}})
    
    # delete document
    delete_query = { "_id" : docId}
    doc_collec.delete_one(delete_query)


'''
def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    # --> add your Python code here
    deleteDocument(cur, docId)

    # 2 Create the document with the same id
    # --> add your Python code here
    createDocument(cur, docId, docText, docTitle, docDate, docCat)
    


def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    # 
    # 
    index_map = {}
    
    
    for doc in cur.find():
        doc_title = doc['title']
        doc_terms = doc['terms']
        for term, freq in doc_terms.items():
            if term not in index_map:
                index_map[term] = {}
                index_map[term][doc_title] = freq
            else:
                index_map[term][doc_title] = freq
            
                
    inverse_index = "{"
    for key, inner_dict in index_map.items():
        inner_string = ",".join([f"{category}:{count}" for category, count in inner_dict.items()])
        inverse_index += f"'{key}':'{inner_string}',"
        
    inverse_index = "\n" + inverse_index.rstrip(',') + "}"
    
    return inverse_index
        
'''
    
