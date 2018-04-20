import csv, time, os

KEYS =  [
		'favorite_count',
		'created_at',
		'retweet_count',
		'sentiment',
		'followers_count',
		'verified',
		'friend_count',
		]


def initializeCSV(filename):
	with open(filename, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=KEYS)
		writer.writeheader()
	


def writeFinalProduct(minuteBuckets):
	for index, minute in enumerate(minuteBuckets):
		filename = '../buckets/' + str(index) + '.csv'
		initializeCSV(filename)
		with open(filename, 'a') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(minute)













