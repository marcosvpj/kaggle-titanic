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

fare_ceiling = 40

data[data[0::, 9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling - 1

fare_bracket_size = 10
number_of_price_brackets = int(fare_ceiling / fare_bracket_size)

number_of_classes = len(np.unique(data[0::, 2]))

survivor_table = np.zeros((2, number_of_classes, number_of_price_brackets))

for i in range(number_of_classes):
    for j in range(number_of_price_brackets):
        women_only = data[
            (data[0::, 4] == "female") & (data[0::, 2].astype(np.float) == i + 1) & (
                data[0:, 9].astype(np.float) >= j * fare_bracket_size) & (
                data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size), 1
        ]

        men_only = data[
            (data[0::, 4] != "female") & (data[0::, 2].astype(np.float) == i + 1) & (
                data[0:, 9].astype(np.float) >= j * fare_bracket_size) & (
                data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size), 1
        ]
        survivor_table[0, i, j] = np.mean(women_only.astype(np.float))
        survivor_table[1, i, j] = np.mean(men_only.astype(np.float))

        survivor_table[survivor_table != survivor_table] = 0

        survivor_table[survivor_table < 0.5] = 0
        survivor_table[survivor_table >= 0.5] = 1

print(survivor_table)

test_file = open('test.csv', 'r')
test_file_object = csv.reader(test_file)
test_file_object.__next__()

predictions_file = open("gender_class_model.csv", "w", newline='')
p = csv.DictWriter(predictions_file, fieldnames=["PassengerId", "Survived"])
p.writeheader()

for row in test_file_object:
    for j in range(number_of_price_brackets):
        try:
            row[8] = float(row[8])
        except:
            bin_fare = 3 - float(row[1])
            break
        if row[8] > fare_ceiling:
            bin_fare = number_of_price_brackets - 1
            break
        if j * fare_bracket_size <= row[8] < (j + 1) * fare_bracket_size:
            bin_fare = j
            break
    if row[3] == 'female':  # If the passenger is female
        p.writerow({'PassengerId': row[0], 'Survived': int(survivor_table[0, int(row[1]) - 1, bin_fare])})
    else:  # else if male
        p.writerow({'PassengerId': row[0], 'Survived': int(survivor_table[1, int(row[1]) - 1, bin_fare])})

test_file.close()
predictions_file.close()
