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

women_only_stats = data[0::, 4] == 'female'
men_only_stats = data[0::, 4] != 'female'

women_aboard = np.size(data[women_only_stats, 1].astype(np.float))
women_survivors = np.sum(data[women_only_stats, 1].astype(np.float))
survivors_female = women_survivors / women_aboard
print('Number of women aboard {}'.format(women_aboard))
print('Proportion of women survivors {}'.format(survivors_female))

men_aboard = np.size(data[men_only_stats, 1].astype(np.float))
men_survivors = np.sum(data[men_only_stats, 1].astype(np.float))
survivors_male = men_survivors / men_aboard
print('Number of men aboard {}'.format(men_aboard))
print('Proportion of men survivors {}'.format(survivors_male))

test_file = open('test.csv', 'r')
test_file_object = csv.reader(test_file, delimiter=',')
test_file_object.__next__()

prediction_file = open('gender_based_model.csv', 'w')
prediction_file_object = csv.writer(prediction_file)
prediction_file_object.writerow(["PassengerId", "Survived"])

for row in test_file_object:
    if row[3] == 'female':
        prediction_file_object.writerow([row[0], '1'])
    else:
        prediction_file_object.writerow([row[0], '0'])

test_file.close()
prediction_file.close()
