import os

from shutil import move

##
# changes old file names to proper date format
##

#get a list of files in directory
folder = "" #"../Kursy walut"
list_of_files = os.listdir(folder) 
# list_of_files.sort(reverse=True)
#print(list_of_files)


name_list = []


for counter, element in enumerate(list_of_files):
    
    name = element.split(" ")[2].split(".")[0].split("-")
    
    
    if len(name[1]) == 1:
        name[1] = f'0{name[1]}'
    if len(name[2]) == 1:
        name[2] = f'0{name[2]}'
    
    name_str = '-'.join(name)
    print(f'Modyfikacja: {element} | {counter+1}')
    
    if name_str in name_list:
        print("BYŁO " + name_str)
    
    name_list.append(name_str)
    
    #os.rename(f'{folder}/{element}', f'../Nowe/{name_str}.txt')
    
    move(f'{folder}/{element}', f'../Nowe/{name_str}.txt')
    
    
    #name_list.append(name_str)
    
#name_list.sort(reverse=True)
#rint(name_list)
    

new_list = os.listdir("../Nowe") 
# list_of_files.sort(reverse=True)
print(f'{len(list_of_files)} | {len(new_list)}')




