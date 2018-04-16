import csv, time, os
import Tweet

PROGRESS_FILEPATH = 'Reporting/progressReport.txt'
ERROR_FILEPATH = 'Reporting/errorReport.txt'
CSV_FILEPATH = 'TweetData/'


def writeProgressReport(iter_, lenTweets):
	report =  "iter : " + str(iter_) + " time : " + str(time.time()) + " len(tweets) : " + str(lenTweets) + '\n'
	file_ = open(PROGRESS_FILEPATH, 'a')
	file_.write(report)
	file_.close()

def writeErrorReport():
	report =  "Error at time : " + str(time.time()) + '\n'
	file_ = open(ERROR_FILEPATH, 'a')
	file_.write(report)
	file_.close()

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











