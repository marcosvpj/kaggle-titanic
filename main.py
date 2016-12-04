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


def is_female(row_data):
    return row_data[3] == 'female'


def write_in_file(filename, data_to_write):
    file = open(filename, 'w', newline='')
    file_object = csv.DictWriter(file, fieldnames=["PassengerId", "Survived"])
    file_object.writeheader()

    for d in data_to_write:
        file_object.writerow(d)

    file.close()


def create_gender_based_model(file_object):
    data_model = []
    for row in file_object:
        if is_female(row):
            data_model.append({'PassengerId': row[0], 'Survived': '1'})
        else:
            data_model.append({'PassengerId': row[0], 'Survived': '0'})

    write_in_file('gender_based_model.csv', data_model)


data = get_data_from_file('raw_data.csv')

process_csv_file('test.csv', create_gender_based_model)


fare_bracket_size = 10
fare_ceiling = 40


def generate_number_of_price_brackets():

    data[data[0::, 9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling - 1

    return int(fare_ceiling / fare_bracket_size)


def generate_survival_table():
    number_of_price_brackets = generate_number_of_price_brackets()

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

            # print(np.mean(women_only.astype(np.float)))
            survivor_table[0, i, j] = np.mean(women_only.astype(np.float))
            # print(np.mean(men_only.astype(np.float)))
            survivor_table[1, i, j] = np.mean(men_only.astype(np.float))
            # print(survivor_table)

            survivor_table[survivor_table != survivor_table] = 0.
            survivor_table[survivor_table < 0.5] = 0
            survivor_table[survivor_table >= 0.5] = 1

    return survivor_table


def create_gender_class_model(file_object):
    number_of_price_brackets = generate_number_of_price_brackets()
    survivor_table = generate_survival_table()

    gender_class_model = []
    for row in file_object:
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

        row_data = {'PassengerId': row[0], 'Survived': 0}
        if is_female(row):
            row_data['Survived'] = int(survivor_table[0, int(row[1]) - 1, bin_fare])
        else:
            row_data['Survived'] = int(survivor_table[1, int(row[1]) - 1, int(bin_fare)])
        gender_class_model.append(row_data)

    write_in_file("gender_class_model.csv", gender_class_model)


process_csv_file('test.csv', create_gender_class_model)
