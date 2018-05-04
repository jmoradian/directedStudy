import csv, time, os

KEYS =  [
	'created_at',
	'retweet_count',
	'sentiment',
	'followers_count',
	'verified'
	]


CSV_EXTENSION = ".csv"
FILEPATH = "../minutes/"

def initializeCSV(filename):
	with open(filename, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=KEYS)
		writer.writeheader()
	

def writeTweet(tweet, index):
	filename = FILEPATH + str(index) + CSV_EXTENSION
	if not os.path.isfile(filename):
		initializeCSV(filename)
	with open(filename, 'a') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows([tweet])













