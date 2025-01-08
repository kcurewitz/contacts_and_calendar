import os
import sys
import re
import collections
import vobject
import csv
import datetime

cal_file = "./calendar-data/cal.ics"
output_csv = "./calendar-data/cal.csv"

events = {}
dt_format_string = '%Y-%m-%d %H:%M'
d_format_string = '%Y-%m-%d'
t_format_string = '%H:%M'

with open(cal_file, "r") as in_f:
    for vcard in vobject.readComponents(in_f):      # this is a "VCALENDAR"
        for event in vcard.contents["vevent"]:      # this is a "VEVENT"
            try:
                events[event.dtstart.value.strftime(dt_format_string)] = [event.dtstart.value, event.dtend.value, event.summary.value]
            except AttributeError:
                print("exception: ", event.summary.value)

print("%d events" % len(events))
ordered_events = collections.OrderedDict(sorted(events.items()))

with open(output_csv, 'w', encoding='UTF8', newline='') as out_f:
    header = ['date', 'start', 'end', 'summary']
    writer = csv.writer(out_f)
    writer.writerow(header)
    for ev in ordered_events:
        event = [ordered_events[ev][0].strftime(d_format_string), 
                 ordered_events[ev][0].strftime(t_format_string),
                 ordered_events[ev][1].strftime(t_format_string),
                 ordered_events[ev][2]]
        writer.writerow(event)
        print(event)

print("%d records" % len(ordered_events))