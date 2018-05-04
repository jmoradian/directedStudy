import ccxt, csv, os


def parseEntryDate(entry, exchange):
	entry[0] = exchange.iso8601(entry[0])

def getPriceEntryDict(fieldnames, entry):
	return dict(zip(fieldnames, entry))

def writePricesToCSV(filename, ohlcv, exchange):
	fieldnames = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
	with open(filename, 'a') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		for entry in ohlcv:
			parseEntryDate(entry, exchange)
			entryDict = getPriceEntryDict(fieldnames, entry)
			writer.writerow(entryDict)

def initializeCSV(filename):
	if not os.path.isfile(filename):
		fieldnames = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
		with open(filename, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()