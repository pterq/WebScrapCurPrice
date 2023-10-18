import requests
import bs4
import time
import datetime
import backoff
import os


def site_data_refresh_sync_start_countdown(seconds_when_to_start):
    # countdown to the start of scraping, to sync with data refresh on website
    current_time = datetime.datetime.now()
    is_first_print_on_timer = 0

    while current_time.second != seconds_when_to_start:
        current_time = datetime.datetime.now()
        if current_time.second > seconds_when_to_start:
            if is_first_print_on_timer == 1:
                print("\rWaiting to start: T-" + str(60 + (seconds_when_to_start - current_time.second)), end=" ")
            else:
                print("Waiting to start: T-" + str(60 + (seconds_when_to_start - current_time.second)), end=" ")
                is_first_print_on_timer = 1
        else:
            if is_first_print_on_timer == 1:
                print("\rWaiting to start: T-" + str(seconds_when_to_start - current_time.second), end=" ")
            else:
                print("Waiting to start: T-" + str(seconds_when_to_start - current_time.second), end=" ")
                is_first_print_on_timer = 1

        if current_time.second != 60:
            time.sleep(0.5)


def get_number_of_reads_in_file(file_name):
    f = open(f'{file_name}', "r")
    data = f.read()
    number_of_connection_errors = data.count("Connection error x5")
    number_of_reads = int((data.count("\n") - 4 - number_of_connection_errors) / 5)
    f.close()
    return number_of_reads
    # include cases when there is X number of "Connection error x5"


def generate_file_name_from_time(current_time, directory):
    new_file_name = f'{directory}/Kursy walut {current_time.year}-{current_time.month}-{current_time.day}.txt'
    return new_file_name


startSeconds = 20
fileStartTime = datetime.datetime.now()

# Create download dictionary if it doesnt exist
main_download_directory = "../Kursy walut"
# main_download_directory = "./test"
os.makedirs(main_download_directory, exist_ok=True)


# fileName = f'./{main_download_directory}/Kursy walut {startTime.year}-{startTime.month}-{startTime.day}_test.txt'
fileName = generate_file_name_from_time(fileStartTime, main_download_directory)
file = open(f'{fileName}', "a")
print(f'Opened file "{fileName}"')

# Check if file exists and has something in it
if os.path.getsize(fileName) == 0:
    file.write(f'#======================\n{fileStartTime.year}-{fileStartTime.month}-{fileStartTime.day}\n')
    file.write("# 1.EUR, 2.USD, 3.CHF, 4.GBP\n")
    file.write("Sell Price, Buy Price\n")

file.close()

numberOfReads = get_number_of_reads_in_file(fileName)
print(f'Number of reads already in the file: {numberOfReads}')
numberOfReads += 1

# print("Start at: XX:XX:" + str(startSeconds))
print(f'Starts at: XX:XX:{startSeconds}')

#for a in range(numberOfReads, 24 * 60):
while numberOfReads <= 24 * 60:
    site_data_refresh_sync_start_countdown(startSeconds)
    file = open(f'{fileName}', "a")

    nowTime = datetime.datetime.now()
    # print("Time: ", nowTime.year, nowTime.month, nowTime.day, nowTime.hour, nowTime.minute, nowTime.second)

    def backoff_hdlr(details):
        print("Connection error x5")
        # close the file when there is no connection to url
        file.write("Connection error x5\n")
        file.close()
        raise SystemExit(0)

    # decorator for any exception that shows up when there is no internet connection, it will try to reconnect 5 times
    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.RequestException,
        on_giveup=backoff_hdlr,
        max_tries=5,
    )
    def make_request():
        return requests.get("https://www.santander.pl/klient-indywidualny/karty-platnosci-i-kantor/kantor-santander")

    print("\nNum: " + str(numberOfReads) + "\nTime: " + time.asctime())

    # Processing request
    print("Sell     Buy      Spread")
    req = bs4.BeautifulSoup(make_request().text, "html.parser")
    sellPrice = req.find_all("div", {"class": "exchange_office__table-value js-exchange_office__rate-sell-value"})
    buyPrice = req.find_all("div", {"class": "exchange_office__table-value js-exchange_office__rate-buy-value"})

    # Saving exchange rates to file
    file.write(f'{str(numberOfReads)} {time.strftime("%H:%M:%S")}\n')
    for i in range(4):
        file.write(f'{sellPrice[i].text.strip()} {buyPrice[i].text.strip()}\n')
        sellPrice[i] = float(sellPrice[i].text.strip().replace(",", "."))
        buyPrice[i] = float(buyPrice[i].text.strip().replace(",", "."))
        print(f'{"{:.4f}".format(sellPrice[i])} | {"{:.4f}".format(buyPrice[i])} | {"{:.4f}".format((buyPrice[i] - sellPrice[i]))} | ')

    file.close()

    # Detecting if a new day started, if yes then change fileName to a new one and reset loop counter
    isSameDay = fileStartTime.year == nowTime.year and fileStartTime.month == nowTime.month and fileStartTime.day == nowTime.day
    if isSameDay:
        print(f'>Not a new day: {fileStartTime.day}-{fileStartTime.month}-{fileStartTime.year} == {nowTime.day}-{nowTime.month}-{nowTime.year}')
    else:
        print(f'>NEW DAY!: {fileStartTime.day}-{fileStartTime.month}-{fileStartTime.year} -> {nowTime.day}-{nowTime.month}-{nowTime.year}')
        fileStartTime = nowTime
        fileName = generate_file_name_from_time(fileStartTime, main_download_directory)
        numberOfReads = 0
        # print(f'New file name: {fileName}')
        # print(f'{fileStartTime.day}-{fileStartTime.month}-{fileStartTime.year} == {nowTime.day}-{nowTime.month}-{nowTime.year}')

        #!================================
        file = open(f'{fileName}', "a")
        print(f'Opened file "{fileName}"')
        file.write(f'#======================\n{fileStartTime.year}-{fileStartTime.month}-{fileStartTime.day}\n')
        file.write("# 1.EUR, 2.USD, 3.CHF, 4.GBP\n")
        file.write("Sell Price, Buy Price\n")
        file.close()

    # wait 1 minute for changes on the website
    time.sleep(0.5)
    nowTime = datetime.datetime.now()
    while nowTime.second != 20:
        nowTime = datetime.datetime.now()
        # print(nowTime.second)
        time.sleep(0.5)

    numberOfReads += 1

file.close()
print(f'File {fileName} is closed')



# Napisać wyświetlanie zmiany kursów w porównaniu do ostatniego zczytania [kurs(+/-?) kurs(+/-?)]

# Przypisać do numberOfRead kolejność występowania na podstawie czasu ?

# numberOfReads przy tworzeniu nowego pliku podczas zmiany dnia powinno wpisywać na początku 1 do pliku a wpisało 3(teraz wpisze 1?) # zrobione
