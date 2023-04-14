import requests
import bs4
import time
import datetime
import backoff

beginTimeSeconds = 20
startTime = datetime.datetime.now()


today = datetime.datetime.now()
fileName = f'Kurs walut {today.year}-{today.month}-{today.day}.txt'
file = open(f'{fileName}', "a")
print(f'Opened file "{fileName}"')
file.write(f'#======================\n{today.year}-{today.month}-{today.day}\n')
file.write("# 1.EUR, 2.USD, 3.CHF, 4.GBP\nSell Price, Buy Price\n")
file.close()

print("Start at: XX:XX:" + str(beginTimeSeconds))
for a in range(1440):
    file = open(f'{fileName}', "a")
    # countdown to start, for sync up with data refresh on website
    isFirstPrintOnTimer = 0
    while startTime.second != beginTimeSeconds:
        startTime = datetime.datetime.now()
        if(startTime.second>beginTimeSeconds):
            if(isFirstPrintOnTimer == 1):
                print("\rWaiting to start. T-" + str(60+(beginTimeSeconds - startTime.second)), end=" ")
            else:
                print("Waiting to start. T-" + str(60 + (beginTimeSeconds - startTime.second)), end=" ")
                isFirstPrintOnTimer = 1
        else:
            if(isFirstPrintOnTimer == 1):
                print("\rWaiting to start. T-" + str(beginTimeSeconds - startTime.second), end=" ")
            else:
                print("Waiting to start. T-" + str(beginTimeSeconds - startTime.second), end=" ")
                isFirstPrintOnTimer = 1

        if startTime.second != 60:
            time.sleep(0.5)

    print("\nNr: " + str(a+1) + "\nCzas: " + time.asctime())

    now = datetime.datetime.now()
    print("Czas: ", now.year, now.month, now.day, now.hour, now.minute, now.second)

    file.write(f'{str(a+1)} {time.strftime("%H:%M")}\n')

    def backoff_hdlr(details):
        print("Definite connection error")
        # close the file when there is no connection to url
        file.write("Definite connection error")
        file.close()
        raise SystemExit(0)

    #decorator for any exception that shows up when there is no internet connection, will try 5 times
    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.RequestException,
        on_giveup=backoff_hdlr,
        max_tries=5,
    )
    def make_request():
        return requests.get("https://www.santander.pl/klient-indywidualny/karty-platnosci-i-kantor/kantor-santander")

    # starting the url request
    print("Sprzedaż  Zakup")

    req = bs4.BeautifulSoup(make_request().text, "html.parser")
    sellPrice = req.find_all("div", {"class": "exchange_office__table-value js-exchange_office__rate-sell-value"})
    buyPrice = req.find_all("div", {"class": "exchange_office__table-value js-exchange_office__rate-buy-value"})

    for i in range(4):
        print(sellPrice[i].text.strip() + " " + buyPrice[i].text.strip())
        file.write(f'{sellPrice[i].text.strip()} {buyPrice[i].text.strip()}\n')

    file.close()

    # wait for 1 minut for changes on the website
    time.sleep(0.5)
    now2 = datetime.datetime.now()
    while now2.second != 20:
        now2 = datetime.datetime.now()
        # print(now2.second)
        time.sleep(0.5)

file.close()
print(f'File {fileName} is closed')








