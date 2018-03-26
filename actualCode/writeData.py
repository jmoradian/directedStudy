import csv
import Tweet



def initializeCSV(filename):
	fieldnames = Tweet.KEYS
	with open(filename, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

def writeTweetsToCSV(filename, tweets):
	fieldnames = Tweet.KEYS
	with open(filename, 'a') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		for tweet in tweets:
			tweetDict = tweet.getTweetValDict()
			writer.writerow(tweetDict)