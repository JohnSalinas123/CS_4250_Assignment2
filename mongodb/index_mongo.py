from pymongo import MongoClient  # import mongo client to clientect
import pprint
import datetime

from db_connection_mongo import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Creating an instance of mongoclient and informing the clientection string
    cur = connectDataBase()
    
    
    #print a menu
    print("")
    print("######### Menu ##############")
    #print("#a - Create a category.")
    print("#b - Create a document")
    print("#c - Update a document")
    print("#d - Delete a document.")
    print("#e - Output the inverted index.")
    print("#q - Quit")

    option = ""
    while option != "q":

        print("")
        option = input("Enter a menu choice: ")

        '''
        if (option == "a"):

            catId = input("Enter the ID of the category: ")
            catName = input("Enter the name of the category: ")

            createCategory(catId, catName)
            client.commit()
        '''
        
        if (option == "b"):

            docId = input("Enter the ID of the document: ")
            docText = input("Enter the text of the document: ")
            docTitle = input("Enter the title of the document: ")
            docDate = input("Enter the date of the document: ")
            docCat = input("Enter the category of the document: ")

            createDocument(cur, docId, docText, docTitle, docDate, docCat)

        elif (option == "c"):

            docId = input("Enter the ID of the document: ")
            docText = input("Enter the text of the document: ")
            docTitle = input("Enter the title of the document: ")
            docDate = input("Enter the date of the document: ")
            docCat = input("Enter the category of the document: ")

            updateDocument(cur, docId, docText, docTitle, docDate, docCat)


        elif (option == "d"):

            docId = input("Enter the document id to be deleted: ")

            deleteDocument(cur, docId)


        elif (option == "e"):

            index = getIndex()
            print(index)

        elif (option == "q"):

            print("Leaving the application ... ")

        else:

            print("Invalid Choice.")

'''

    

    #Creating a dictionary and include our data
    document = {"_id": 1,
                "title": "Discovery",
                "date": datetime.datetime.strptime("2023-10-03T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.000Z"),
                }

    # Creating a document
    documents = db.documents
    # Inserting data
    documents.insert_one(document)
    # Fetching data
    pprint.pprint(documents.find_one())

    #updating data
    documents.update_one({"_id": 1}, {"$set": {"title": "Arizona"}})
    # Fetching data
    pprint.pprint(documents.find_one())

    #deleting data
    documents.delete_one({"_id": 1})
    # Fetching data
    pprint.pprint(documents.find_one())
    
    
'''