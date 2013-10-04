# -*- coding: utf-8 -*
#
from sys import argv
import datetime

if len(argv) < 3:
    print "For example, to generate list of 1000 days starting 1999-09-09, type: python generate-days.py 1999-09-09 20 > sample.txt"
else:
    y,m,d = [int(i) for i in argv[1].split('-')]
    # Get the number of days:
    n = int(argv[2])
    # Get to know the weekday of that day:
    d = datetime.date(y, m, d)
    # Go through the next n days:
    for i in range(n):
        day = d+datetime.timedelta(days=i)
        weekday = lambda x: x!=7 and x or '●'
        print "%5s ■ " % (str(i+1),), str(day), "["+str(weekday(day.weekday()+1))+"] "
