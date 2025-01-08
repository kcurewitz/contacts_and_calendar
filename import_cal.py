import os
import sys
import re
import collections
import vobject
import csv
import datetime

cal_file = "calendar-data/cal.ics"
output_csv = "calendar-data/cal.csv"

appts = {}
dt_format_string = '%Y-%m-%d %H:%M'
d_format_string = '%Y-%m-%d'
t_format_string = '%H:%M'

with open(cal_file, "r") as in_f:
    for vcard in vobject.readComponents(in_f):
        for event in vcard.contents["vevent"]:
            try:
                #print(event.dtstart.value.strftime(dt_format_string))
                appts[event.dtstart.value.strftime(dt_format_string)] = [event.dtstart.value,
                                                                         event.dtend.value, 
                                                                         event.summary.value]
            except AttributeError:
                print("no dtstart: ", event.summary.value)
                pass

print("%d events" % len(appts))
ordered_events = collections.OrderedDict(sorted(appts.items()))

with open(output_csv, 'w', encoding='UTF8', newline='') as out_f:
    header = ['date', 'start', 'end', 'summary']
    writer = csv.writer(out_f)
    writer.writerow(header)
    for appt in ordered_events:
        todo = [ordered_events[appt][0].strftime(d_format_string), 
                ordered_events[appt][0].strftime(t_format_string),
                ordered_events[appt][1].strftime(t_format_string),
                ordered_events[appt][2]]
        writer.writerow(todo)
        print(todo)

print("%d records" % len(ordered_events))