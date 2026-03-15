import os
import sys
import pymongo
import csv
from datetime import datetime


def get_client(db):
    myclient = pymongo.MongoClient(db)
    return myclient

def get_db(client, dbname):
    db = client[dbname]
    return db

def delete_all_documents(collection):
    x = collection.delete_many({})


def insert_contacts(collection):
    with open('./contact-data/WO_contacts.csv', mode='r') as c_file:
        csv_contacts = csv.DictReader(c_file)
        for line in csv_contacts:
            name_f, name_l = line['name'].split(' ',1)
            email = line['email']
            tel = line['telephone']
            addr_num, addr_name = line['address'].split(' ',1)
            print(name_f, name_l.strip(), addr_num.strip(), addr_name.strip())
            mydict = { "name_f"    : name_f,
                       "name_l"    : name_l,
                       "tel"       : tel,
                       "addr_num"  : addr_num,
                       "addr_name" : addr_name
            } 
            x = collection.insert_one(mydict)

def example_1_contacts():
    local_db = "mongodb://localhost:27017/"
    database_name = "mydatabase"
    collection_name = "contacts"

    myclient = get_client(local_db)
    c_db = get_db(myclient,database_name)
    c_collection = c_db[collection_name]

    debug   = True
    create  = False
    destroy = False
    query   = True
    query_limit = 5

    print("================ ", datetime.now())
    if debug:
        print("Database ", collection_name)
        print("Database names: ", myclient.list_database_names())

    if query:
        contact_query = { "addr_num": { "$regex": "^1[0-9]" } }
        c_doc = c_collection.find(contact_query)
        for c in c_doc: 
            if query_limit > 0:
                print(c)
                query_limit -= 1

    if create:
        insert_contacts(c_collection)
    if destroy:
        delete_all_documents(c_collection)

def main():
    example_1_contacts()
    return None

if __name__ == '__main__':
    sys.exit(main())