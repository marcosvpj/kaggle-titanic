import csv as csv
import numpy as np

PASSENGER_ID = 1
SEX_COLUMN = 4


def process_csv_file(file_name, do):
    file = open(file_name, 'r')
    file_object = csv.reader(file, delimiter=',')
    header = file_object.__next__()
    print(header)

    result = do(file_object)

    file.close()

    return result


def extract_data_to_array(file_object):
    processed_data = []
    for r in file_object:
        processed_data.append(r)

    return processed_data


def get_data_from_file(filename):
    d = process_csv_file(filename, extract_data_to_array)
    return np.array(d)


data = get_data_from_file('raw_data.csv')


def is_female(row_data):
    return row_data[3] == 'female'


# number_passengers = np.size(data[0::, PASSENGER_ID].astype(np.float))
# number_survivors = np.sum(data[0::, PASSENGER_ID].astype(np.float))
#
# print('Number of passengers {}'.format(number_passengers))
# print('Number of survivors {}'.format(number_survivors))
# print('Proportion survivors {}'.format(number_survivors / number_passengers))
#
# women_only_stats = data[0::, SEX_COLUMN] == 'female'
# men_only_stats = data[0::, SEX_COLUMN] != 'female'
#
# women_aboard = np.size(data[women_only_stats, 1].astype(np.float))
# women_survivors = np.sum(data[women_only_stats, 1].astype(np.float))
# survivors_female = women_survivors / women_aboard
# print('Number of women aboard {}'.format(women_aboard))
# print('Proportion of women survivors {}'.format(survivors_female))
#
# men_aboard = np.size(data[men_only_stats, 1].astype(np.float))
# men_survivors = np.sum(data[men_only_stats, 1].astype(np.float))
# survivors_male = men_survivors / men_aboard
# print('Number of men aboard {}'.format(men_aboard))
# print('Proportion of men survivors {}'.format(survivors_male))

def write_in_file(filename, data_to_write):
    file = open(filename, 'w')
    file_object = csv.writer(file)

    # do(file_object, data_to_write)
    for d in data_to_write:
        file_object.writerow(d)

    file.close()


def create_gender_based_model(file_object):
    # def gender_based_model(file_to_write, data_to_write):
    data_model = []
    for row in file_object:
        if row[3] == 'female':
            data_model.append([row[0], '1'])
        else:
            data_model.append([row[0], '0'])

    write_in_file('gender_based_model.csv', data_model)


process_csv_file('test.csv', create_gender_based_model)

fare_ceiling = 40

data[data[0::, 9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling - 1

fare_bracket_size = 10
number_of_price_brackets = int(fare_ceiling / fare_bracket_size)

number_of_classes = len(np.unique(data[0::, 2]))

survivor_table = np.zeros((2, number_of_classes, number_of_price_brackets))

for i in range(number_of_classes):
    for j in range(number_of_price_brackets):
        women_only = data[
            (data[0::, SEX_COLUMN] == "female") & (data[0::, 2].astype(np.float) == i + 1) & (
                data[0:, 9].astype(np.float) >= j * fare_bracket_size) & (
                data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size), 1
        ]

        men_only = data[
            (data[0::, SEX_COLUMN] != "female") & (data[0::, 2].astype(np.float) == i + 1) & (
                data[0:, 9].astype(np.float) >= j * fare_bracket_size) & (
                data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size), 1
        ]
        survivor_table[0, i, j] = np.mean(women_only.astype(np.float))
        survivor_table[1, i, j] = np.mean(men_only.astype(np.float))

        survivor_table[survivor_table != survivor_table] = 0

        survivor_table[survivor_table < 0.5] = 0
        survivor_table[survivor_table >= 0.5] = 1


def process_test_file(file_object):
    gender_class_model = []
    for row in file_object:
        print(row)
        for price_bracket in range(number_of_price_brackets):
            try:
                row[8] = float(row[8])
            except ValueError:
                bin_fare = 3 - float(row[1])
                break

            if row[8] > fare_ceiling:
                bin_fare = number_of_price_brackets - 1
                break
            if price_bracket * fare_bracket_size <= row[8] < (price_bracket + 1) * fare_bracket_size:
                bin_fare = price_bracket
                break

        if is_female(row):  # If the passenger is female
            gender_class_model.append([row[0], int(survivor_table[0, int(row[1]) - 1, bin_fare])])
        else:  # else if male
            gender_class_model.append([row[0], int(survivor_table[1, int(row[1]) - 1, bin_fare])])

    write_in_file("gender_class_model.csv", gender_class_model)


process_csv_file('test.csv', process_test_file)
