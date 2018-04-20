import ccxt, time, WritePriceData
from exchanges import *

#exchanges that work every minute: kraken
# exchanges that consistently allow queries back to beginning of data intake: cex, coingi
# exchanges that inconsistently allow queries back to beginning of data intake: bitfinex, bitfinex2, ethfinex

def loopThroughAllExchanges(from_datetime):
	for ind, exchange in enumerate(exchanges):
		from_timestamp = exchange.parse8601(from_datetime)
		try:
			ohlcv = exchange.fetch_ohlcv("BTC/USD", '1m', since= from_timestamp, limit = 1000)
			for entry in ohlcv:
				print(ind, "	:	", exchange, "	:	", exchange.iso8601(entry[0]), "	:	", entry[1:5])
				break
		except: pass

def parseTimestamp(date_, exchange):
	return exchange.parse8601(date_)

def getEndTimestamp(ohlcv, exchange):
	return parseTimestamp(ohlcv[-1][0], exchange)

def queryPriceData(filename, exchange, from_timestamp):
	ohlcv = exchange.fetch_ohlcv("BTC/USD", '1m', since= from_timestamp, limit = 1000)
	WritePriceData.writePricesToCSV(filename, ohlcv, exchange)
	return getEndTimestamp(ohlcv, exchange)

def catchUp(exchange, from_datetime, filename):
	from_timestamp = parseTimestamp(from_datetime, exchange)
	WritePriceData.initializeCSV(filename)

	current_timestamp = int(time.time() * 1000)
	while (from_timestamp < current_timestamp - 60000 * 10): #while not within 10 minutes of current time
		from_timestamp = queryPriceData(filename, exchange, from_timestamp)
		current_timestamp = int(time.time() * 1000)
	return from_timestamp

def runContinuousQuery(exchange, from_timestamp, filename):
	WritePriceData.initializeCSV(filename)

	while True:
		from_timestamp = queryPriceData(filename, exchange, from_timestamp)
		time.sleep(120)


def main():
	exchange = ccxt.bitfinex()
	filename = 'priceData.csv'
	from_datetime = '2018-04-18T15:35:00.000Z'
	updatedEndTime = catchUp(exchange, from_datetime, filename)
	runContinuousQuery(exchange, updatedEndTime, filename)

	




if __name__ == "__main__": 
	main()