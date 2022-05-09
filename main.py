import requests
import bs4
import time
import datetime


beginTimeSeconds = 20
startTime = datetime.datetime.now()

print("Start at: XX:XX:" + str(beginTimeSeconds))
for a in range(1000):

    while startTime.second != beginTimeSeconds:
        startTime = datetime.datetime.now()
        if(startTime.second>beginTimeSeconds):
            print("Waiting to start. T-" + str(60+(beginTimeSeconds - startTime.second)))
        else:
            print("Waiting to start. T-" + str(beginTimeSeconds - startTime.second))
        if startTime.second != 60:
            time.sleep(0.5)

    print()

    print("Nr: " + str(a+1) + "\nCzas: " + time.asctime())

    now = datetime.datetime.now()
    print("Czas: ", now.year, now.month, now.day, now.hour, now.minute, now.second)

    print("Zakup  Sprzedaż")
    res = requests.get("https://www.santander.pl/klient-indywidualny/karty-platnosci-i-kantor/kantor-santander")
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    sellPrice = soup.find_all("div", {"class": "exchange_office__table-value js-exchange_office__rate-sell-value"})
    buyPrice = soup.find_all("div", {"class": "exchange_office__table-value js-exchange_office__rate-buy-value"})

    for i in range(4):
        print(sellPrice[i].text.strip() + " " + buyPrice[i].text.strip())

    time.sleep(0.5)
    now2 = datetime.datetime.now()
    while now2.second != 20:
        now2 = datetime.datetime.now()
        # print(now2.second)
        time.sleep(0.5)

    print()









