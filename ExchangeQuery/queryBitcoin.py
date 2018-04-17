import ccxt, time
from exchanges import *


# if exchange.has['fetchOHLCV']:
#     for symbol in exchange.markets:
#         time.sleep (exchange.rateLimit / 1000) # time.sleep wants seconds
#         print (symbol, exchange.fetch_ohlcv (symbol, '1d'))

# exchange = ccxt.
# print (exchange.has['fetchOHLCV'])
# poloniex.fetch_ohlcv("ETH/BTC", '5m', since, until)

# exchange = ccxt.kraken()
from_datetime = '2018-04-06 15:22:00'

for exchange in exchanges:
	from_timestamp = exchange.parse8601(from_datetime)
	try:
		ohlcv = exchange.fetch_ohlcv("BTC/USD", '1m', since= from_timestamp, limit = 1000)
		for ind, entry in enumerate(ohlcv):
			print(ind, exchange.iso8601(entry[0]), entry[1:5])
			break
	except: pass
