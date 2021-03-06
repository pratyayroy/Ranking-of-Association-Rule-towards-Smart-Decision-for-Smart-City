# Author: Apy
# Apriori Algorithm [Confidence for 1 Item set]
# Tested on 4i DataSet. Hopefully it is working. No bugs detected (26.10.2016 | 2:50pm)


import csv
import numpy as np
import itertools
from collections import Counter

f = open('7i.csv')                                                  # Opening and reading the .csv file
csv_f = csv.reader(f)                                               # Declaring the item list and number of transaction

Items = []
transaction = 0

for row in csv_f:                                                   # Iterating through each row of the dataset
    row = list(filter(None, row))                                   # Filtering the empty strings while fetching row
    transaction += 1
    l = len(row)                                                    # Iterating through each item in the transaction
    for i in range(0, l):
        if row[i] in Items:                                         # If the currently read item is already in the list
            pos = Items.index(row[i])
            pos += 1
            Items[pos] += 1                                         # If the currently read item is not in the list
        else:
            Items.append(row[i])
            Items.append(1)

npItems = np.array(Items)                                           # Creating a NumPy array
npItems = np.reshape(npItems, (-1, 2))                              # Converting it to a nx2 matrix
#np.savetxt("2o_freq.csv", npItems, delimiter=",", fmt="%s")         # Saving the frequency_output file

print("###############################")
print(transaction)
print(npItems)
print("###############################")
dim = npItems.shape

# axis = 1, for column insertions, for row = 0, posintional = no axis
supp = np.insert(npItems, 2, '0', axis=1)                           # Initializing "support matrix"

supp = supp.astype(object)                                          # Calculating Support
for row in supp:
    row[2] = int(row[1]) / transaction

#np.savetxt("2o_supp.csv", supp, delimiter=",", fmt="%s")            # Saving support_output file

val = input("Enter the minimum support :: ")                        # Getting minimum frequency from user
print(val)

supp = supp[(supp[:, 2] >= float(val))]                             # Selecting the rows that qualifies minimum support
print(supp)
#np.savetxt("2o_min_supp.csv", supp, delimiter=",", fmt="%s")

permute = (supp[:, 0])
permute.tolist();
print(permute)


conf = input("Enter a minimum confidence")
cnt = 0


for x in itertools.permutations(permute, 2):
    #print(x)
    numerator = 0
    denominator = 0
    s_a1b = 0
    s_ab1 = 0
    #print(" @@@@@ " + str(x[0]) + " -> " + str(x[1]))
    # Formula goes like.. Sup(x[0] + x[1])/supp(x[0])

    # Checking the number of times (x[0]&x[1]) exists..


    f.seek(0)
    t_no = 0
    for row in csv_f:
        t_no += 1
        row = list(filter(None, row))
        if x[0] in row:
            denominator += 1
        d = Counter(x)
        c = Counter(row)
        c.subtract(d)
        if all(v >= 0 for k, v in c.items()):
            numerator += 1
        if x[0] in row and x[1] not in row:
            s_ab1 += 1
            # print("** ab' **")
            # print(row)
        if x[0] not in row and x[1] in row:
            s_a1b += 1
            # print("** a'b **")
            # print(row)

    #print("Confidence = " + str(numerator/denominator))
    if numerator/denominator >= float(conf):
        cnt += 1
        p_a1b = s_a1b/transaction
        p_ab1 = s_ab1/transaction
        print(str(cnt) + ". " + str(x[0]) + " -> " + str(x[1] + "(" + str(numerator/denominator) + ")" + " | " + str(p_a1b + p_ab1)))

