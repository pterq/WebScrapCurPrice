from itertools import islice
import os

##
# converts Old files with proper date names to CSV file
##
csv_file_name = "../../kursy.csv"
list_of_files = os.listdir("../../Kursy walut - nowe nazwy")

print("=================================================================================================")
#get a list of files in directory
list_of_files.sort()

#print(list_of_files)
num_of_files = len(list_of_files)
print(f'| Files in directory: {num_of_files} |')


#create CSV file for records if its not there already


if os.path.isfile(csv_file_name) == False:
    csv_file = open(f'{csv_file_name}', "a+")
    csv_file.close()

csv_file = open(f'{csv_file_name}', "r")
csv_num_of_lines_begin = len(csv_file.readlines())
csv_file.close()


csv_file = open(f'{csv_file_name}', "a")
print(f'| CSV file "{csv_file_name}" | Number of lines:  {csv_num_of_lines_begin} |')

# Check if file exists and has something in it
if os.path.getsize(csv_file_name) == 0:
    csv_file.write("Date;Time;EUR sell;EUR buy;USD sell;USD buy;CHF buy;CHF sell;GBP buy;GBP sell\n")

#read "one" record from first file from file list and convert it to csv then save data to csv

print("---------------------------------------------------------")
num_of_all_records = 0
for num, element in enumerate(list_of_files):
    
    #read data from one file
    file_path = f'../Kursy walut - nowe nazwy/{element}'
    file = open(f'{file_path}', "r")
    #print(f'| Opened file "{file_path}" |')

    data = file.readlines()

    num_of_lines = len(data)
    

    file_date = str(data[1]).split("\n")[0]
    
    #print(f' | {file_date} | Number of lines in file: {num_of_lines} |')

    num_of_records = 0
    counter = 4
    
    while counter < num_of_lines:
        
        # Detecting recoreded connection error
        while "error" in data[counter]:
            print(f'{file_date} | {data[counter]}')
            x = input()
            
            counter+=1
            #print(f'| {counter} |')
            if counter == num_of_lines:
                break
            
        if counter+2 >= num_of_lines:
            break

        # Reading a block with time and currency rates for that time
        block = []
        for i in range (0, 4):
            try:
                read_line = data[counter+i].split("\n")[0]
                split_table = read_line.split(" ")
                block.append(split_table[0])
                block.append(split_table[1])
            except:
                print("except read")
                print(f' | {file_date} | {read_line} | {split_table} | {counter} | +5 {counter+5} | {num_of_lines}')
                exit(1)
        
        rec_time = block[1]
        
        
        #print("Block: " + str(block))
        
        entry = f'{file_date};{rec_time};{block[2]};{block[3]};{block[4]};{block[5]};{block[6]};{block[7]};\n'
        
        
       
        
        # try:
            
        # except:
        #     print("except block")
        #     print(block)
        #     exit(1)
        #print(entry.split("\n")[0])
        num_of_records+=1
        num_of_all_records+=1
        
        csv_file.write(entry)
        
        counter+=5

    print(f' | {num+1} | File date: {file_date} | Number of recrods added: {num_of_records} | ')
    file.close()
    

csv_file = open(f'{csv_file_name}', "r")
csv_num_of_lines_end = len(csv_file.readlines())
csv_file.close()

diff = csv_num_of_lines_end-csv_num_of_lines_begin
print(f'| CSV number of lines: begin/diff/end/num_of_all_records/con: {csv_num_of_lines_begin}/{csv_num_of_lines_end}/{diff}/{num_of_all_records}/{bool(diff == num_of_all_records)} |')



