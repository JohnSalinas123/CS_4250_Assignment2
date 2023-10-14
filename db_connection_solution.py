#-------------------------------------------------------------------------
# AUTHOR: John Salinas
# FILENAME: db_connection_solution
# SPECIFICATION: Perform CRUD operations on corpus database
# FOR: CS 4250- Assignment #2
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
import string
import psycopg2
from psycopg2.extras import RealDictCursor

def connectDataBase():
    
    DB_NAME = "corpus"
    DB_USER = "postgres"
    DB_PASS = "123"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,
                                cursor_factory=RealDictCursor)
        
        return conn
        
    except:
        print("Database not connected successfully")
    
    
    # Create a database connection object using psycopg2
    # --> add your Python code here

def createCategory(cur, catId, catName):
    # Insert a category in the database
    # --> add your Python code here
    
    sql = "INSERT INTO category (id, name) Values (%s, %s)"
    
    recset = [catId,catName]
    cur.execute(sql, recset)

   

def createDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Get the category id based on the informed category name
    # --> add your Python code here
    
    sql_getCatName = "SELECT id FROM category where name= %s"
    
    recset_getCatName = [docCat]
    cur.execute(sql_getCatName, recset_getCatName)
    
    cat_row = cur.fetchone()
    cat_id = cat_row['id']

    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    # --> add your Python code here
    
    docText_noSpaces = docText.replace(" ","")
    num_chars = len(docText_noSpaces)
    
    sql_createDoc = "INSERT INTO documents (doc, cat_id, text, num_chars, date, title) VALUES (%s,%s,%s,%s,%s,%s)"
    
    recset_createDoc = [docId, cat_id, docText, num_chars,docDate,docTitle]
    cur.execute(sql_createDoc, recset_createDoc)
    

    # 3 Update the potential new terms.
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember to lowercase terms and remove punctuation marks.
    # 3.2 For each term identified, check if the term already exists in the database
    # 3.3 In case the term does not exist, insert it into the database
    # --> add your Python code here
    
    docText_clearPunc = docText.translate(str.maketrans('', '', string.punctuation))
    docText_lower = docText_clearPunc.lower()
    docText_terms = docText_lower.split()
    
    for term in docText_terms:
        sql_check_term = "SELECT 1 FROM term where term=%s"
        recset_check_term = [term]
        cur.execute(sql_check_term, recset_check_term)
        term_exists = cur.fetchone()
        
        if not term_exists:
            num_chars_term = len(term)
            sql_insert_term = "INSERT INTO term (term, num_chars) VALUES (%s,%s)"
            recset_insert_term = [term, num_chars_term]
            cur.execute(sql_insert_term,recset_insert_term)
            
        

    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    # 4.3 Insert the term and its corresponding count into the database
    # --> add your Python
    # code here
    
    term_map = {}
    for term in docText_terms:
        if term in term_map:
            term_map[term] += 1
        else:
            term_map[term] = 1
    for key in term_map.keys():
        sql_update_index = "INSERT INTO index (doc_id, term, count) VALUES (%s, %s, %s)"
        recset_update_index = [docId, key, term_map[key]]
        cur.execute(sql_update_index, recset_update_index)
    
    
    

def deleteDocument(cur, docId):
    
    # 1 Query the index based on the document to identify terms
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    # --> add your Python code here
    
    sql_index_terms = "SELECT * FROM index where doc_id=%s"
    recset_index_terms = [docId]
    cur.execute(sql_index_terms, recset_index_terms)
    index_rows = cur.fetchall()
    
    index_terms = []
    for row in index_rows:
        cur_term = row['term']
        index_terms.append(cur_term)
        sql_delete_index = "DELETE FROM index WHERE doc_id=%s AND term=%s"
        recset_delete_index = [docId,cur_term]
        cur.execute(sql_delete_index, recset_delete_index)
        print("Row: (", docId,cur_term,") deleted from index!")
        
        sql_check_term = "SELECT 1 FROM index where term=%s"
        recset_check_term = [cur_term]
        cur.execute(sql_check_term, recset_check_term)
        index_exists = cur.fetchone()
        
        if not index_exists:
            sql_delete_term = "DELETE FROM term WHERE term=%s"
            recset_delete_term = [cur_term]
            cur.execute(sql_delete_term, recset_delete_term)
            print("No other occurences of (", cur_term, ") ,removing from DB!")
        

    # 2 Delete the document from the database
    # --> add your Python code here
    
    sql_delete_doc = "DELETE FROM documents WHERE doc=%s"
    recset_delete_doc = [docId]
    cur.execute(sql_delete_doc, recset_delete_doc)
    print("Document with id ", docId," deleted!")


def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    # --> add your Python code here
    deleteDocument(docId)

    # 2 Create the document with the same id
    # --> add your Python code here
    createDocument(docId, docText, docTitle, docDate, docCat)

def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    
    sql_query_index = "SELECT I.doc_id, I.term, I.count, D.title FROM INDEX I JOIN documents D ON I.doc_id = D.doc"
    cur.execute(sql_query_index)
    index_list = cur.fetchall()
    
    index_map = {}
    for index in index_list:
        cur_term = index['term']
        cur_title = index['title']
        cur_count = index['count']
        
        if cur_term in index_map:
            index_map[cur_term][cur_title] = cur_count
        else:
            index_map[cur_term] = {}
            index_map[cur_term][cur_title] = cur_count
    
    inverse_index = "{"
    for key, inner_dict in index_map.items():
        inner_string = ",".join([f"{category}:{count}" for category, count in inner_dict.items()])
        inverse_index += f"'{key}':'{inner_string}',"
        
    inverse_index = "\n" + inverse_index.rstrip(',') + "}"
            
    return inverse_index
        
        

