__author__ = "Pratyay Roy"
__copyright__ = "© 2016, Project Nightjar"
__credits__ = "Subrata Datta, Pratyay Roy"
__maintainer__ = "Pratyay Roy"
__email__ = "pratyayroy@outlook.com"
__status__ = "N-item minimum confidence"

import csv
import itertools
import time

start_time = time.time()

f = open('test.csv')
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

print(item_set, sep="\n")

##############################################################################################
conf = input("Enter a minimum confidence :: ")
cnt = 0
dissociation = 0
total_confidence = 0
for x in itertools.permutations(item_set, 2):
    if set(x[0]) - set(x[1]) != set(x[0]):
        continue
    numerator = 0
    denominator = 0
    s_a1b = 0
    s_ab1 = 0

    # Formula goes like.. Sup(x[0] + x[1])/supp(x[0])

    # Checking the number of times (x[0]&x[1]) exists
    f.seek(0)
    for row in csv_f:
        row = list(filter(None, row))
        if set(x[0]).issubset(row):
            denominator += 1
        if set(x[0]).issubset(row) and set(x[1]).issubset(row):
            numerator += 1
        if set(x[0]).issubset(row) and not set(x[1]).issubset(row):
            s_ab1 += 1
        if not set(x[0]).issubset(row) and set(x[1]).issubset(row):
            s_a1b += 1

    if numerator / denominator >= float(conf):
        cnt += 1
        p_a1b = s_a1b / transaction
        p_ab1 = s_ab1 / transaction
        print(str(cnt) + ". " + str(x[0]) + " -> " + str(x[1]) + "(" + str(numerator / denominator) + ")" + " | " + str(
            p_a1b + p_ab1))
        dissociation += p_a1b + p_ab1
        total_confidence += numerator/denominator


print("The average dissociation is " + str(dissociation/cnt))
print("The average confidence is " + str(total_confidence/cnt))
print("--- Execution Time :: %s seconds ---" % (time.time() - start_time))
