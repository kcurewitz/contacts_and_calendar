import os
import sys
import pymongo
import csv

local_db = "mongodb://localhost:27017/"

def get_client(db):
    myclient = pymongo.MongoClient(db)
    return myclient

def get_db(client, dbname):
    mydb = client[dbname]
    return mydb

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
    collection_name = "contacts"
    myclient = get_client(local_db)
    mydb = get_db(myclient,"mydatabase")
    mycol = mydb[collection_name]

    debug   = True
    create  = False
    destroy = False
    report  = False
    query   = True

    if debug:
        print("Database ", collection_name)
        print(myclient.list_database_names())

    if report:
        for x in mycol.find():
            print(x)

    if query:
        contact_query = { "addr_num": { "$regex": "^5" } }
        c_doc = mycol.find(contact_query)
        for c in c_doc: print(c)

    if create:
        insert_contacts(mycol)
    if destroy:
        delete_all_documents(mycol)

def main():
    example_1_contacts()

if __name__ == '__main__':
    sys.exit(main())