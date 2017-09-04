# Author: Apy
# Apriori Algorithm


import csv
import numpy as np
import itertools

f = open('4i.csv')                                                  # Opening and reading the .csv file
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

for x in itertools.permutations(permute, 1):
    print(x)
