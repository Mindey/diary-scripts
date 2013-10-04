# -*- coding: utf-8 -*-
from os import system, path

# Copy file to home directory, decrypt it, and securely delete the ncrypted ones:
system('cp ~/Dropbox/F.gpg ~/F.gpg && gpg -d -q ~/F.gpg > ~/F.txt && shred -f -u -z -n 25 ~/F.gpg')

# Read the decrypted files F.txt into RAM, and securely delete it:
f = open(path.join(path.expanduser("~"),'F.txt'), 'rb'); F = f.readlines(); f.close(); system('shred -f -u -z -n 25 ~/F.txt'); del f

# Given lines of diary file, return a vector (Python list) of diary entries without the dates:
def daysof(diary):
    """
    Given diary lines, return a vector of contents of the days.
    daycontent(A)[0] -- content of the 1st day of life.
    Each day in diary, begins with "ID ■  ", and has "] " before the text.
    """
    content = []
    dates = []
    for line in diary:
        line = line[:-1]
        if ('%s ■  ' % (len(content)+1) in line) and (']' in line):
            dates.append(line.split(']')[0]+']')
            content.append(line.split(']')[1])
        else:
            content[-1] += '\n'+line
    return dates, content

fdates, fdays = daysof(F)

def tagsof(day):
    result = []
    import re
    findall = lambda x, symbol: [day.start() for day in list(re.finditer(symbol, x))]
    count = 0
    start = False
    for i in sorted(findall(day,'{:') + findall(day,':}')):
        if day[i:i+2] == '{:':
            count += 1
        if day[i:i+2] == ':}':
            count += -1
        if not start and count == 1:
            start = i
        if count == 0:
            result.append(day[start:i]+':}')
            start = False
    return result

t = tagsof(s)

def contof(tag):
    '''
        tag here is defined as a string starting with {: and ending with :}
        tag may have functional expressions, e.g., {:function(x,y)|content:}
        this function gets the content and the function
    '''
    if '|' in tag and '{:' in tag and ':}' in tag:
        return (tag[2:tag.index('|')], tag[tag.index('|')+1:-2])
    else:
        return (False, False)

def scdia(alldays):
    '''
        given a list of days, goes over every day, and creates dictionary of lists of results of application of functions,
        each key of the dictionary corresponds to the fuction applied
        each value of the dictionary is a list of tuples, (n, result), where n corresponds to the day number
        if the same function was applied twice in the same day, they occur in the same order as they were written in diary
    '''
    outputs = {}
    for i, day in enumerate(alldays):
        for j, tag in enumerate(tagsof(day)):
            func, cont = contof(tag)
            if func not in outputs.keys():
                outputs[func] = []
            outputs[func].append((i,cont))
    return outputs

fdic = scdia(fdays)

# Now, let's say we want to create a new diary, such that 
# it has only the results of application of function 'to(box)', 

dayids, contents = zip(*fdic['to(box)'])
for i, day in enumerate(fdays):
    print fdates[i]
    for ix in [y for y, x in enumerate(dayids) if x == i]:
        print contents[ix]

# Let's say we want to copy it to /home/mi/Dropbox/Mindey/mi.txt
