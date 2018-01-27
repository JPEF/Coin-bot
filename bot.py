##TODO
##- implement IM alert when target price is reached. along side of the text to speech
##- support for checking the profit of mining, prob throug coinmarketcap api
##- automatically get users transaction information from binance
##- error handling
##- Add support for other currencies than euros

#requires user to install requests, http://docs.python-requests.org/en/master/user/install/ 
import requests

import json
import time
import cfg


if cfg.textToSpeech == True:
    #requires user to install: https://github.com/mhammond/pywin32/releases
    import win32com.client
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    #Test that the text to speech is working correctly
    speaker.Speak("Hello, moon and lambos await us!")

while True:
    print(time.ctime())

    #Get the current ETH price from Coinbase
    response = requests.get("https://api.coinbase.com/v2/exchange-rates?currency=ETH")
    if response.status_code == 429:
            print("Coinbase API rate limit warning. Waiting 1 minute.")
            time.sleep(cfg.apiRateWait)
    data = response.json()
    print(data["data"]["currency"])
    print(data["data"]["rates"]["EUR"], "€\n")

    ethPrice = data["data"]["rates"]["EUR"]
    ethPrice = float(ethPrice)

    #ETH price goal check
    if ethPrice < cfg.ethPriceGoal:
        print("ETH price goal reached!\n")
        if cfg.textToSpeech == True:
            speaker.Speak("ETH price goal reached!")

    for coin in cfg.coinsToTrack:
        #Get the price information from Binance
        response = requests.get("https://api.binance.com/api/v3/ticker/price", params=coin)
        if response.status_code == 429:
            print("Binance API rate limit warning. Waiting 1 minute.")
            time.sleep(cfg.apiRateWait)

        #Current price    
        data = response.json()
        print(data["symbol"])
        symbol = data["symbol"]
        currentPrice = float(data["price"])
        currentPriceInEuro = ethPrice*currentPrice
        print("Current price: ", data["price"], "ETH. ", "%.2f" % currentPriceInEuro, "€")

        #Profit
        originalPrice = cfg.boughtAt[symbol]     
        profit = ((currentPrice/originalPrice)-1)*100
        print("Profit: ", "%.2f" % profit, "%\n")

        #Profit check
        if profit > cfg.profitGoal:
            print("Profit goal reached on ", symbol, "\n")
            if cfg.textToSpeech == True:
                toSay = "Profit goal reached on ", symbol
                speaker.Speak(toSay)

    time.sleep(cfg.howOften)

