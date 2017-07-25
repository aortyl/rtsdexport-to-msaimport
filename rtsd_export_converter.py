import csv
import argparse
import pprint

pp = pprint.PrettyPrinter()

parser = argparse.ArgumentParser(description='csv converter')
parser.add_argument('-i', help='file to convert', type=argparse.FileType('r'))
parser.add_argument('-o', help='name of output file created', type=argparse.FileType('w'))

args = vars(parser.parse_args())
input_csv = args.get('i', None)
output_csv = args.get('o', None)

if input_csv is None:
    print("Invalid input")
elif output_csv is None:
    print("Invalid output")
else:

    def build_parent_record(row):
        return {
            'First_Name': row[' First Name'].strip(),
            'Last_Name': row[' Last Name'].strip(),
            'Phone': row[' Home Phone'].strip(),
            'Phone_Description': '',
            'Email': row[' Email Address'].strip()
        }

    def build_student_record(row):
        return {
            'Last_Name': row[' Last Name'].strip(),
            'S1_First_Name': row[' First Name'].strip(),
            'S1_Grade': row[' Graduation Date'].strip(),
            'S1_Phone': row[' Cell Phone'].strip() if row[' Cell Phone'].strip() else row[' Home Phone'].strip(),
            'S1_Email': row[' Email Address']
        }

    def build_house_record(row):
        return {
            'Street': row[' Street Address'].strip(),
            'City': row[' City'].strip(),
            'State': row[' State'].strip(),
            'Zip': row[' Zip'].strip(),
            'Home_Phone': row[' Home Phone'].strip(),
            '_parents': [build_parent_record(row)]
        }

    def build_parent_dict(houses):
        new_dict = {}
        house_count = 0

        for house in houses:
            house_count += 1
            for key in houses[house]:
                if key != '_parents':
                    new_dict['H' + str(house_count) + '_' + key] = houses[house].get(key)

            parent_count = 0
            for parent in houses[house]['_parents']:
                parent_count += 1
                for key in parent:
                    new_dict['H' + str(house_count) + '_Parent_' + str(parent_count) + '_' + key] = parent.get(key)

        return new_dict

    reader = csv.DictReader(input_csv)
    writer = csv.DictWriter(output_csv, [
        'Last_Name',
        'S1_First_Name',
        'S1_Grade',
        'S1_Phone',
        'S1_Email',
        'H1_Street',
        'H1_City',
        'H1_State',
        'H1_Zip',
        'H1_Home_Phone',
        'H2_Street',
        'H2_City',
        'H2_State',
        'H2_Zip',
        'H2_Home_Phone',
        'H1_Parent_1_First_Name',
        'H1_Parent_1_Last_Name',
        'H1_Parent_1_Phone',
        'H1_Parent_1_Phone_Description',
        'H1_Parent_1_Email',
        'H1_Parent_2_First_Name',
        'H1_Parent_2_Last_Name',
        'H1_Parent_2_Phone',
        'H1_Parent_2_Phone_Description',
        'H1_Parent_2_Email',
        'H2_Parent_1_First_Name',
        'H2_Parent_1_Last_Name',
        'H2_Parent_1_Phone',
        'H2_Parent_1_Phone_Description',
        'H2_Parent_1_Email',
        'H2_Parent_2_First_Name',
        'H2_Parent_2_Last_Name',
        'H2_Parent_2_Phone',
        'H2_Parent_2_Phone_Description',
        'H2_Parent_2_Email'
    ])

    writer.writeheader()

    user_name = ''
    students = []
    houses = {}

    for row in reader:
        if user_name != row[' User ID']:
            for student in students:
                new_row = student.copy()
                new_row.update(build_parent_dict(houses))

                writer.writerow(new_row)

            # Track user name
            user_name = row[' User ID']
            # reset values
            students = []
            houses = {}

        if row[' Record Type'].strip() == 'S':
            students.append(build_student_record(row))
        elif row[' Record Type'].strip() == 'P':
            if houses.get(row[' Street Address'], None) is not None and \
                            len(houses[row[' Street Address']]['_parents']) == 1:
                # If a house already exists, add an additional parent. There can't be more than 2 parents per house
                houses[row[' Street Address']]['_parents'].append(build_parent_record(row))
            else:
                # If there is NOT a house with this address, create it and add parent
                houses[row[' Street Address']] = build_house_record(row)
