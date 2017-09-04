__author__ = "Pratyay Roy"
__copyright__ = "© 2016, Project Nightjar"
__credits__ = "Subrata Datta, Pratyay Roy"
__maintainer__ = "Pratyay Roy"
__email__ = "pratyayroy@outlook.com"
__status__ = "Build 1.0"

import csv
import itertools
import time
start_time = time.time()

f = open('6i.csv')
csv_f = csv.reader(f)

unique_items = []
transaction = 0

for row in csv_f:
    row = list(filter(None, row))
    transaction += 1
    l = len(row)
    for i in range(0, l):
        if row[i] in unique_items:
            pos = unique_items.index(row[i])
        else:
            unique_items.append(row[i])

print("Read " + str(transaction) + " transactions successfully..")

print("\n################### Generating unique items ###################\n")
for i, e in enumerate(unique_items, 1):
    print(str(i) + '.', e)

channel2 = unique_items
item_set = []
i = 0
cnt = 1
min_support = float(input("Enter the minimum support :: "))

while channel2:
    i += 1
    channel1 = []

    print("\n################### Generating Frequent " + str(i) + " item-set ###################\n")
    for x in itertools.combinations(channel2, i):
        total_occurence = 0
        f.seek(0)
        for row in csv_f:
            row = list(filter(None, row))
            x = list(x)
            # print(x)
            # print(set(row))
            if set(x).issubset(row):
                total_occurence += 1

        if total_occurence / transaction >= min_support:
            print(str(cnt) + ". " + str(x) + " | " + str(total_occurence / transaction))
            cnt += 1
            item_set.append(x)
            channel1.append(x)

    channel2 = []
    # channel1 = sum(channel1, [])

    for x in channel1:
        # print(x)
        # print(channel2)

        channel2 = channel2 + list(set(x) - set(channel2))
        # print(channel2)
        # dummy = input("test")
print("--- Execution Time :: %s seconds ---" % (time.time() - start_time))