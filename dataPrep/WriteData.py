import csv, time, os


KEYS =  [
		'favorite_count',
		'created_at',
		'retweet_count',
		'sentiment',
		'followers_count',
		'listed_count',
		'verified',
		'friend_count',
		]


def initializeCSV(filename):
	with open(filename, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=KEYS)
		writer.writeheader()


def writeFinalProduct():
	initializeCSV("tweetBucketByMinute.csv")













