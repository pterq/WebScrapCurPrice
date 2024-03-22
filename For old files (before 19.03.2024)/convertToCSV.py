from itertools import islice
import os

##
# convertToCSV.py converts old files with proper date names to CSV file
##

csv_file_name = "../kursy_2.csv"
list_of_files = os.listdir("../Kursy walut - nowe nazwy")

print("=================================================================================================")
# Get a list of files in directory
list_of_files.sort()

# print(list_of_files)
num_of_files = len(list_of_files)
print(f'| Files in directory: {num_of_files} |')

# Create CSV file for records if its not there already
if os.path.isfile(csv_file_name) == False:
    csv_file = open(f'{csv_file_name}', "a+")
    csv_file.close()

csv_file = open(f'{csv_file_name}', "r")
csv_num_of_lines_begin = len(csv_file.readlines())
csv_file.close()

csv_file = open(f'{csv_file_name}', "a")
print(f'| CSV file "{csv_file_name}" |')

# Check if file exists and has something in it
if os.path.getsize(csv_file_name) == 0:
    csv_file.write("Date;Time;EUR sell;EUR buy;USD sell;USD buy;CHF buy;CHF sell;GBP buy;GBP sell\n")

print("---------------------------------------------------------")
num_of_all_records = 0

# Going through all file one at a time
for num, element in enumerate(list_of_files):

    # read data from one file
    dir_and_file_path = f'../Kursy walut - nowe nazwy/{element}'
    file = open(f'{dir_and_file_path}', "r")

    data = file.readlines()

    num_of_lines = len(data)

    file_date = str(data[1]).split("\n")[0]

    num_of_records = 0
    counter = 4
    count_to_5 = 0

    # Reading data from one file
    while counter < num_of_lines:
        block = []  # stores time of read and buy and sell prices for 4 currencies

        # Check if at the end of file there is enough text lines to hold an entry
        if num_of_lines - counter < 5:
            counter = num_of_lines - 1
            break

        # Get entry time
        if count_to_5 == 0:
            while ":" not in data[counter]:
                counter += 1

        block.append(data[counter].split("\n")[0].split(" ")[1])
        counter += 1

        # Get currency 1
        count_to_5 += 1
        if "," in data[counter]:
            split_table = data[counter].split("\n")[0].split(" ")
            block.append(split_table[0])
            block.append(split_table[1])
            counter += 1
        elif ":" in data[counter]:
            # Check for solo time values
            break

        # Get currency 2
        count_to_5 += 1
        if "," in data[counter]:
            split_table = data[counter].split("\n")[0].split(" ")
            block.append(split_table[0])
            block.append(split_table[1])
            counter += 1

        # Get currency 3
        count_to_5 += 1
        if "," in data[counter]:
            split_table = data[counter].split("\n")[0].split(" ")
            block.append(split_table[0])
            block.append(split_table[1])
            counter += 1

        # Get currency 4
        count_to_5 += 1
        if "," in data[counter]:
            split_table = data[counter].split("\n")[0].split(" ")
            block.append(split_table[0])
            block.append(split_table[1])
            counter += 1

        # print(f'Block: {file_date}: {block} | C5: {count_to_5} | Counter: {counter} | num_of_lines: {num_of_lines}')
        rec_time = block[0]

        entry = f'{file_date};{block[0]};{block[1]};{block[2]};{block[3]};{block[4]};{block[5]};{block[6]};{block[7]};{block[8]};\n'

        # print(f' | {entry.split("\n")[0]} | ')

        num_of_records += 1
        num_of_all_records += 1

        csv_file.write(entry)

        count_to_5 = 0

    print(f' | {num + 1} | File done: {file_date} | Number of recrods added: {num_of_records} | ')
    file.close()

csv_file = open(f'{csv_file_name}', "r")
csv_num_of_lines_end = len(csv_file.readlines())
csv_file.close()

diff = csv_num_of_lines_end - csv_num_of_lines_begin

if csv_num_of_lines_begin == 0:
    conditon = diff - 1 == num_of_all_records
else:
    conditon = diff == num_of_all_records

print(f'| CSV number of lines end check:\n begin: {csv_num_of_lines_begin} | end: {csv_num_of_lines_end} | diff: {diff} | num_of_all_records: {num_of_all_records} | Is everything converted?: {conditon} |')
