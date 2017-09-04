__author__ = "Pratyay Roy"
__copyright__ = "© 2016, Project Nightjar"
__credits__ = "Subrata Datta, Pratyay Roy"
__maintainer__ = "Pratyay Roy"
__email__ = "pratyayroy@outlook.com"
__status__ = "Trust with Top K"

import csv
import itertools
import time

start_time = time.time()

f = open('extend_1k.csv')
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
trust_min = input("Enter a minimum trust :: ")
cnt = 0
dissociation = 0
total_trust = 0
rules = [[]]
for x in itertools.combinations(item_set, 2):
    if set(x[0]) - set(x[1]) != set(x[0]):
        continue
    numerator = 0
    denominator = 0
    s_a = 0
    s_b = 0
    s_ab = 0
    s_ab1 = 0
    s_a1b = 0
    s_a1b1 = 0

    # Formula goes like.. Supp(x[0] + x[1])/supp(x[0])

    # Checking the number of times (x[0]&x[1]) exists
    f.seek(0)
    for row in csv_f:
        row = list(filter(None, row))
        if set(x[0]).issubset(row):
            s_a += 1
        if set(x[1]).issubset(row):
            s_b += 1
        if set(x[0]).issubset(row) and set(x[1]).issubset(row):
            s_ab += 1
        if set(x[0]).issubset(row) and not set(x[1]).issubset(row):
            s_ab1 += 1
        if not set(x[0]).issubset(row) and set(x[1]).issubset(row):
            s_a1b += 1
        if not set(x[0]).issubset(row) and not set(x[1]).issubset(row):
            s_a1b1 += 1
    p_ab = s_ab / transaction
    p_ab1 = s_ab1 / transaction
    p_a1b = s_a1b / transaction
    p_a1b1 = s_a1b1 / transaction
    p_a = s_a / transaction
    p_b = s_b / transaction

    trust = max(p_ab, (1 - (p_a1b + p_ab1))) / (max(p_a, p_b) + p_a1b1)

    if trust >= float(trust_min):
        cnt += 1
        print(str(cnt) + ". " + str(x[0]) + " -> " + str(x[1]) + "(" + str(trust) + ")" + " | " + str(
            p_a1b + p_ab1))
        dissociation += p_a1b + p_ab1
        total_trust += trust

        # Weighted Relative Accuracy (WRAcc)
        WRAcc = p_a * ((p_ab / p_a) - p_b)
        # Certainity Factor (cf)
        cf = max((((p_ab / p_a) - p_b) / (1 - p_b)), (((p_ab / p_b) - p_a) / (1 - p_a)))
        # Probability of Trust (pot)
        pot = trust / (trust + dissociation)
        # Gravity (gr) = u + WRAcc + cf
        gr = pot + WRAcc + cf

        conf = p_ab / p_a
        rule_support = s_ab / transaction

        rule_length = len(x[0] + x[1])

        #                             0             1           2           3             4           5          6        7
        # Rules are dispalyed as [antecedent], [consequent], [trust], [dissociation], [gravity], [confidence] [length] [support]
        rules[cnt - 1] = [x[0], x[1], trust, p_a1b + p_ab1, gr, conf, rule_length, rule_support]
        rules += [[]]

print("\n################### After Applying Gravity ###################\n")
del (rules[cnt])
print(rules)
rules = sorted(rules, key=lambda q: q[4], reverse=True)
for i, e in enumerate(rules):
    print(str(i + 1) + '.' + str(e[0]) + " -> " + str(e[1]) + "(" + str(e[2]) + ")" + " | " + str(e[3]) + " | " + str(
        e[4]))
print("The average dissociation is " + str(dissociation / cnt))
print("The average trust is " + str(total_trust / cnt))

with open("output6i.csv", "w") as ff:
    writer = csv.writer(ff)
    writer.writerows(rules)

rank_a = int(input("Enter the value of A ranking :: "))

min_rule_conf = 0
total_rule_length = 0
min_rule_supp = 0
for i in range(0,rank_a):
    if rules[i][5] > min_rule_conf:
        min_rule_conf = rules[i][5]
    if rules[i][6] > min_rule_conf:
        total_rule_length = rules[i][6]
    if rules[i][7] > min_rule_conf:
        min_rule_supp = rules[i][7]

print("Minimum Rule Confidence :: " + str(min_rule_conf))
print("Minimum Rule SUpport :: " + str(min_rule_supp))
print("Average Rule Length :: " + str(total_rule_length))
print("--- Execution Time :: %s seconds ---" % (time.time() - start_time))



# ***** Back Up (Delete) *****

# print("The average trust is " + str(total_trust / cnt))
# *******************