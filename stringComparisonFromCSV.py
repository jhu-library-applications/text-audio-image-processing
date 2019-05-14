import csv
import argparse
from fuzzywuzzy import fuzz
import time

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fileName', help='the CSV file of headings. optional - if not provided, the script will ask for input')
parser.add_argument('-c', '--columnName', help='the name of the column in the CSV file containing the strings to be compared. optional - if not provided, the script will ask for input')
parser.add_argument('-t', '--threshold', help='the threshold (e.g. \'90\' means the strings are 90% similar and 10% different). optional - if not provided, the script will ask for input')
args = parser.parse_args()

if args.fileName:
    fileName = args.fileName
else:
    fileName = input('Enter the file name of the CSV of headings (including \'.csv\'): ')
if args.columnName:
    columnName = args.columnName
else:
    columnName = input('Enter the name of the column in the CSV file containing the strings to be compared: ')
if args.threshold:
    threshold = int(args.threshold)
else:
    threshold = int(input('Enter threshold (e.g. \'90\' means the strings are 90% similar and 10% different): '))

startTime = time.time()
nameList = []
with open(fileName) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nameList.append(str(row[columnName]))
counter = len(nameList)
f=csv.writer(open(fileName[:fileName.index('.')]+'NearMatches.csv','w'))
f.writerow(['percentage']+['name1']+['name2'])
completeNearMatches = []
for name in nameList:
    counter -= 1
    print('Rows remaining: ', counter)
    for name2 in nameList:
        if name != name2:
            ratio = fuzz.ratio(name, name2)
            partialRatio = fuzz.partial_ratio(name, name2)
            tokenSort = fuzz.token_sort_ratio(name, name2)
            tokenSet = fuzz.token_set_ratio(name, name2)
            avg = (ratio+partialRatio+tokenSort+tokenSet)/4
            if avg > threshold:
                nearMatch = [avg, name, name2]
                nearMatch = sorted(nearMatch)
                if nearMatch not in completeNearMatches:
                    completeNearMatches.append(nearMatch)
        else:
            pass

for nearMatch in completeNearMatches:
    f.writerow([nearMatch[0]]+[nearMatch[1]]+[nearMatch[2]])

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print('Total script run time: ', '%d:%02d:%02d' % (h, m, s))
