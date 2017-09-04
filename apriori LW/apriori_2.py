# Author: Apy
# Apriori Algorithm


import csv
import numpy as np
import itertools

f = open('4i.csv')                                                  # Opening and reading the .csv file
csv_f = csv.reader(f)                                               # Declaring the item list and number of transaction
partition = []
ifm = []
unq_sot = []
unq_item = []
transaction = 0

Items = []
transaction = 0

for row in csv_f:
    sz = len(row)
    transaction += 1
    for i in range(0, sz):                              # Identifying the unique items
        if row[i] not in unq_item:
            unq_item.append(row[i])

unq_item.sort()
unq_item.remove('')
print("Total transactions is :: " + str(transaction))
print("The unique elements are :: " + str(unq_item))
f.seek(0)


permute = unq_item
item_set = 1
while len(permute) != 0:
    print("##########   COMBINATIONS    #############")
    for x in itertools.combinations(permute, item_set):
        print(x)

    for row in csv_f:
        row = list(filter(None, row))
        l = len(row)
        for i in range(0, l):
            if row[i] in Items:
                pos = Items.index(row[i])
                pos += 1
                Items[pos] += 1
            else:
                Items.append(row[i])
                Items.append(1)

    npItems = np.array(Items)  # Creating a NumPy array
    npItems = np.reshape(npItems, (-1, 2))  # Converting it to a nx2 matrix

    dummy = input("Rational Check :: ")

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


