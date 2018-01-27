#Add here the coins which profits are to be tracked
#Example: coinsToTrack = [{"symbol": "VENETH"}, {"symbol": "BNBETH"}]
coinsToTrack = [{"symbol": ""}]

#Add here the price you paid in ETH per coin
#Example boughtAt = {"VENETH": 0.0047505967741935, "BNBETH": 0.0146148181818182}
boughtAt = {"": 0}

#Define here your profit goal in percents
#Default value is 100
profitGoal = 100

#Define here the ETH price goal (in euros), after which the bot will alert you
ethPriceGoal = 803.9

#Define here how often the bot will check the prices (in seconds), default 15 mins
howOften = 900

#Text to speech ON = True, OFF = False, currently only supported on Windows and requires the user to install https://github.com/mhammond/pywin32/releases
textToSpeech = True

#Define here if you want to get notification messages to your telegram
#Requires installation of https://github.com/python-telegram-bot/python-telegram-bot
#And creating a bot via https://core.telegram.org/bots#6-botfather
#Following the guide will give you the token to be used
#ChatID can be found using this address https://api.telegram.org/bot<BOTTOKENHERE>/getUpdates
telegramBot = True
telegramToken = ""
chatID = 

#This is the value in seconds which the bot will wait if the API rate limit is reached
apiRateWait = 60
