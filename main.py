import csv as csv
import numpy as np

file = open('raw_data.csv', 'r')
csv_file_object = csv.reader(file, delimiter=',')
header = csv_file_object.__next__()

data = []
for row in csv_file_object:
    data.append(row)

data = np.array(data)
# print(a)

number_passengers = np.size(data[0::, 1].astype(np.float))
number_survivors = np.sum(data[0::, 1].astype(np.float))

print('Number of passengers {}'.format(number_passengers))
print('Number of survivors {}'.format(number_survivors))
print('Proportion survivors {}'.format(number_survivors / number_passengers))
