import csv

# Reading in the previous CSV
f1 = open('input.csv')
csv_f = csv.reader(f1)

# reading the base gravity
b_gr = 1000000.0
for row in csv_f:
    if len(row) == 0:
        continue
    if float(row[3]) < float(b_gr):
        b_gr = row[3]
print(b_gr)

