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

f = open('t25i10d10k.csv')
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
rules = [[]]
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
    s_a = 0
    s_b = 0
    s_ab = 0
    s_ab1 = 0
    s_a1b = 0
    s_a1b1 = 0

    # Formula goes like.. Sup(x[0] + x[1])/supp(x[0])

    # Checking the number of times (x[0]&x[1]) exists
    f.seek(0)
    for row in csv_f:
        row = list(filter(None, row))
        if set(x[0]).issubset(row):
            denominator += 1
        if set(x[0]).issubset(row) and set(x[1]).issubset(row):
            numerator += 1
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

    if numerator / denominator >= float(conf):
        cnt += 1
        p_ab = s_ab / transaction
        p_ab1 = s_ab1 / transaction
        p_a1b = s_a1b / transaction
        p_a1b1 = s_a1b1 / transaction
        p_a = s_a / transaction
        p_b = s_b / transaction

        trust = max(p_ab, (1 - (p_a1b + p_ab1))) / (max(p_a, p_b) + p_a1b1)
        dissociation += p_a1b + p_ab1

        # Weighted Relative Accuracy (WRAcc)
        WRAcc = p_a * ((p_ab / p_a) - p_b)
        # Certainity Factor (cf)
        cf = max((((p_ab / p_a) - p_b) / (1 - p_b)), (((p_ab / p_b) - p_a) / (1 - p_a)))
        # Probability of Trust (pot)
        pot = trust / (trust + dissociation)
        # Gravity (gr) = u + WRAcc + cf
        gr = pot + WRAcc + cf
        # Antecedent Length
        ant_length = len(x[0])

        print(str(cnt) + ". " + str(x[0]) + " -> " + str(x[1]) + "(" + str(numerator / denominator) + ")" + " | " + str(
            p_a1b + p_ab1))

        #                          0          1              2           3           4             6           7
        # Rules are dispalyed as [rank], [antecedent], [consequent], [gravity], [ant length], [confidence] [support]
        rules[cnt - 1] = [cnt + 1, x[0], x[1], gr, ant_length, numerator/denominator, numerator/transaction]
        rules += [[]]

print("\n################### After Applying Gravity ###################\n")
del (rules[cnt])
print(rules)
rules = sorted(rules, key=lambda q: q[3], reverse=True)

# Tie Breaking
change = True
while change:
    change = False
    for i, e in enumerate(rules):
        if e[3] == rules[i-1][3]:
            if e[6] > rules[i-1][6]:
                temp = rules[i-1]
                rules[i - 1] = rules[i]
                rules[i - 1] = temp
                change = True
            if e[6] == rules[i - 1][6]:
                if e[7] > rules[i - 1][7]:
                    temp = rules[i - 1]
                    rules[i - 1] = rules[i]
                    rules[i - 1] = temp
                    change = True
                if e[7] == rules[i - 1][7]:
                    if e[4] < rules[i - 1][4]:
                        temp = rules[i - 1]
                        rules[i - 1] = rules[i]
                        rules[i - 1] = temp
                        change = True

n_rules = [[]]
for i, e in enumerate(rules):
    n_rules[i] = [i+1, e[0], e[1], e[3]]
    n_rules += [[]]
    print(str(i + 1) + '.' + str(e[0]) + " -> " + str(e[1]) + "(" + str(e[2]) + ")" + " | " + str(e[3]))
print("The average dissociation is " + str(dissociation / cnt))

with open("output_final_t25i10d10k.csv", "w") as ff:
    writer = csv.writer(ff)
    writer.writerows(n_rules)

print("The average dissociation is " + str(dissociation / cnt))
print("The average confidence is " + str(total_confidence / cnt))
print("--- Execution Time :: %s seconds ---" % (time.time() - start_time))
