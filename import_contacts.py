import os
import sys
import re
import collections
import vobject
import csv
from collections import namedtuple

contacts_file = "../contact-data/WO_contacts.vcf"
output_csv = "../contact-data/WO_contacts.csv"
output_email_csv = "../contact-data/WO_contacts_email.csv"

def parse_phone(phone):
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
# Check if it's a valid 10z-digit number
    if len(digits) == 10:
        return digits
    # Check if it's a valid 11-digit number starting with 1 (US country code)
    elif len(digits) == 11 and digits.startswith('1'):
        return digits[1:]    
    else:
        return None

def phone_format(phone):
    digits = parse_phone(phone)
    if not digits or len(digits) != 10:
        return "Invalid number"
    return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"

pcontacts = {}
person = namedtuple('name',['tel', 'email', 'number', 'address'])

with open(contacts_file, "r") as in_f:    
    for vcard in vobject.readComponents(in_f):
        if ("fn" in vcard.contents):
            name = vcard.contents["fn"][0].value.strip(' ')
            phone, email, number, street, error = "","","","",""
            try:
                p_count = 0
                p_multi = len(vcard.contents["tel"]) > 1
                for tel in vcard.contents["tel"]:
                    p_count += 1
                    if (p_count > 1):
                        phone += " "
                    phone += phone_format(tel.value) 
                    if p_multi:
                        phone += " (" + tel.type_param[0].lower() + ")"
            except KeyError:
                error += " -> no phone"
            try:
                for em in vcard.contents["email"]:
                    email = em.value
            except KeyError:
                error += " -> no email"

            try:
                if ("adr" in vcard.contents):
                    number,street = vcard.contents["adr"][0].value.street.split(" ",1)
                    #street = street.replace(" ","%")
            except KeyError:
                error += " -> no street address"

            pcontacts[name] = person(phone, email, number, street)
            if (error != ""):
                print(name, " ",error)

ordered_pcontacts = collections.OrderedDict(sorted(pcontacts.items()))

with open(output_csv, 'w', encoding='UTF8', newline='') as out_f:
    header = ['name', 'telephone', 'email', 'number', 'address']
    writer = csv.writer(out_f)
    writer.writerow(header)
    for name in ordered_pcontacts:
        contact = [name, ordered_pcontacts[name].tel,
                         ordered_pcontacts[name].email,
                         ordered_pcontacts[name].number,
                         ordered_pcontacts[name].address]
        writer.writerow(contact)
        print(contact)

with open(output_email_csv, 'w', encoding='UTF8', newline='') as out_f:
    header = ['email']
    writer = csv.writer(out_f)
    writer.writerow(header)
    for name in ordered_pcontacts:
        contact = [ordered_pcontacts[name].email]
        writer.writerow(contact)
        for name in contact:
            if len(name) > 0:
                print(name,",")

print("%d records" % len(pcontacts))