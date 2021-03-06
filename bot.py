##TODO
##- automatically get users transaction information from exchange
##- error handling
##- Add support for other currencies than euros
##- functions...

#requires user to install requests, http://docs.python-requests.org/en/master/user/install/ 
import requests

import json
import time
import cfg

if cfg.telegramBot == True:
    #requires telegrambot https://github.com/python-telegram-bot/python-telegram-bot
    import telegram
    bot = telegram.Bot(token = cfg.telegramToken)
    from telegram.ext import Updater
    updater = Updater(token = cfg.telegramToken)
    dispatcher = updater.dispatcher
    bot.send_message(chat_id=cfg.chatID, text="Profit bot started!")


if cfg.textToSpeech == True:
    #requires user to install: https://github.com/mhammond/pywin32/releases
    import win32com.client
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    #Test that the text to speech is working correctly
    speaker.Speak("Hello, moon and lambos await us!")

while True:
    print(time.ctime())

    #Get the current ETH price from Coinbase
    print("Coinbase:")
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
        if cfg.telegramBot == True:
            bot.send_message(chat_id=cfg.chatID, text="ETH price goal reached!")

    if cfg.binance == True:
        print("Binance:")
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
                if cfg.telegramBot == True:
                    bot.send_message(chat_id=cfg.chatID, text=toSay)

    if cfg.kucoin == True:
        print("Kucoin:")
        for coin in cfg.coinsToTrackKucoin:
            response = requests.get("https://api.kucoin.com/v1/open/tick", params=coin)

            data = response.json()

            print(data["data"]["coinType"])
            symbol = data["data"]["coinType"]
            currentPrice = float(data["data"]["lastDealPrice"])
            currentPriceInEuro = ethPrice*currentPrice
            print("Current price: ", data["data"]["lastDealPrice"], "ETH. ", "%.2f" % currentPriceInEuro, "€")

            #Profit
            pair = data["data"]["symbol"]
            originalPrice = cfg.boughtAtKucoin[pair]     
            profit = ((currentPrice/originalPrice)-1)*100
            print("Profit: ", "%.2f" % profit, "%\n")

            #Profit check
            if profit > cfg.profitGoal:
                print("Profit goal reached on ", symbol, "\n")
                if cfg.textToSpeech == True:
                    toSay = "Profit goal reached on ", symbol
                    speaker.Speak(toSay)
                if cfg.telegramBot == True:
                    bot.send_message(chat_id=cfg.chatID, text=toSay)

    if cfg.cmc == True:
        print("Coinmarketcap")
        for coin in cfg.coinsToTrackCmc:
            url = "https://api.coinmarketcap.com/v1/ticker/%s" % (coin)
            response = requests.get(url)
            data = response.json()
            data = data[0]
            
            print(data["symbol"])
            symbol = data["symbol"]
            currentPrice = float(data["price_usd"])
            
            print("Current price: ", data["price_usd"], "$.\n")

            #Target price check
            currencyName = data["id"]
            if currentPrice > cfg.targetPrice[currencyName]:
                print("Goal price reached on ", symbol, "\n")
                if cfg.textToSpeech == True:
                    toSay = "Goal price reached on ", symbol
                    speaker.Speak(toSay)
                if cfg.telegramBot == True:
                    bot.send_message(chat_id=cfg.chatID, text=toSay)
        


    time.sleep(cfg.howOften)

