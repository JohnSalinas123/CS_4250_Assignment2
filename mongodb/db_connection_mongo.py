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
    db = client["documents"]
    collection_cursor = db["document"]
    
    return collection_cursor


def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    

    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    # --> add your Python code here
    
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
        
    
    new_document = {
        "_id" : docId,
        docTitle : {
            "text" : docText,
            "num_chars" : num_chars,
            "date" : docDate,
            "category" : docCat,
            "terms" : term_map
        }
    }
    
    cur.insert_one(new_document)


def deleteDocument(cur, docId):

    
    # delete document
    delete_query = { "_id" : docId}
    cur.delete_one(delete_query)
    

def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    # --> add your Python code here
    deleteDocument(cur, docId)

    # 2 Create the document with the same id
    # --> add your Python code here
    createDocument(cur, docId, docText, docTitle, docDate, docCat)
    

'''
def getIndex():

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    # 
    # 
'''