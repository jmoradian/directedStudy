import csv, time, os

KEYS =  [
	'created_at',
	'retweet_count',
	'sentiment',
	'followers_count',
	'verified'
	]


def initializeCSV(filename):
	with open(filename, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=KEYS)
		writer.writeheader()
	


def writeFinalProduct(minuteBuckets):
	for index, minute in enumerate(minuteBuckets):
		filename = '../minutes/' + str(index) + '.csv'
		initializeCSV(filename)
		with open(filename, 'a') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(minute)













