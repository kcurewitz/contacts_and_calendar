import os
import sys
import re
import collections
import vobject
import csv

contacts_file = "./contact-data/WO_contacts.vcf"
#contacts_file = "./contact-data/all.vcf"
output_csv = "./contact-data/WO_contacts.csv"

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

contacts = {}
count = 0

with open(contacts_file, "r") as in_f:
    for vcard in vobject.readComponents(in_f):
        count += 1
        person = []
        #if count == 1: print(vcard)
        if ("fn" in vcard.contents):
            name = vcard.contents["fn"][0].value
            phone = ""; email = ""; street = ""; error= ""
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
                error += " -> no phone found"
            try:
                for em in vcard.contents["email"]:
                    email = em.value
            except KeyError:
                error += " -> no email found"

            if ("adr" in vcard.contents):
                 street = vcard.contents["adr"][0].value.street

            contacts[name] = [phone, email, street]
            if (error != ""):
                print(name, " ",error)

ordered_contacts = collections.OrderedDict(sorted(contacts.items()))

with open(output_csv, 'w', encoding='UTF8', newline='') as out_f:
    header = ['name', 'telephone', 'email', 'address']
    writer = csv.writer(out_f)
    writer.writerow(header)
    for name in ordered_contacts:
        contact = [name, ordered_contacts[name][0],
                         ordered_contacts[name][1],
                         ordered_contacts[name][2]]
        writer.writerow(contact)
        print(contact)

print("%d records" % len(contacts))