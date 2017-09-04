__author__ = "Pratyay Roy"
__copyright__ = "© 2016, Project Nightjar"
__credits__ = "Subrata Datta, Pratyay Roy"
__maintainer__ = "Pratyay Roy"
__email__ = "pratyayroy@outlook.com"
__status__ = "confidence with top-k rules"

import csv
import itertools
import time

start_time = time.time()

f = open('chess.csv')
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
cnt = 0

minconf = float(input("Enter the minimum confidence :: "))
top_k = int(input("Enter the number of rules you want to generate ::"))
dissociation = 0
total_confidence = 0
rules = [[]] * top_k
minsup = 0

for L in range(1, len(unique_items) + 1):
    for lhs in itertools.combinations(unique_items, L):
        for R in range(1, len(unique_items) + 1):
            for rhs in itertools.combinations(unique_items, R):
                if set(lhs) - set(rhs) != set(lhs):
                    continue
                print(str(lhs) + '->' + str(rhs))
                numerator = 0
                denominator = 0
                s_a1b = 0
                s_ab1 = 0
                f.seek(0)
                for row in csv_f:
                    row = list(filter(None, row))
                    if set(lhs).issubset(row):
                        denominator += 1
                    if set(lhs).issubset(row) and set(rhs).issubset(row):
                        numerator += 1
                    if set(lhs).issubset(row) and not set(rhs).issubset(row):
                        s_ab1 += 1
                    if not set(lhs).issubset(row) and set(rhs).issubset(row):
                        s_a1b += 1

                p_a1b = s_a1b / transaction
                p_ab1 = s_ab1 / transaction

                # is Support of antecedant is 0, skipping it..
                if denominator == 0:
                    continue

                # print("conf = " + str(numerator / denominator) + "   support = " + str(numerator / transaction))
                # print(cnt)

                # Blindly adding rules till k
                if cnt != top_k:
                    # syntax of rule => lhs, rhs, confidence, support, dissociation
                    rules[cnt] = [lhs, rhs, numerator / denominator, numerator / transaction, p_a1b + p_ab1]
                    cnt += 1
                    # print(cnt)
                    # print(rules)
                    continue

                rules = sorted(rules, key=lambda x: x[3], reverse=True)
                minsup = rules[top_k - 1][3]
                if numerator / denominator >= minconf and numerator / transaction >= minsup:
                    # print("fun time")
                    del rules[top_k - 1]
                    rules = rules + [[]]
                    # syntax of rule => lhs, rhs, confidence, support, dissociation
                    rules[top_k - 1] = [lhs, rhs, numerator / denominator, numerator / transaction, p_a1b + p_ab1]
                    # print(rules)

rules = sorted(rules, key=lambda x: x[3], reverse=True)
print("\n################### Generating Rules ###################\n")
for i, e in enumerate(rules, 5):
    print(str(e[0]) + " -> " + str(e[1]) + " |  conf = " + str(e[2]) + " |  supp = " + str(e[3]) + " |  diss = " + str(
        e[4]))
