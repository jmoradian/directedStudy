import csv, numpy as np, tweepy, textblob, calendar, string
from dateutil import parser
import ReadData, WriteData

GAPS = [60, 120, 360, 720, 1440]
SENTIMENT_BINS = [-1., -0.5, 0., 0.5]
TWEET_PARAMS = []
FEATURE_LENGTH = 8
DATE_INDEX = 1
TWEET_TEXT_INDEX = 3

# uses textblob library to analyze the tweet sentiment
# 	- textblob is trained on movie review data
def getTweetSentiment(tweet):
	text = tweet[TWEET_TEXT_INDEX]
	analysis = textblob.TextBlob(text) # may need to rid text of special characters
	print analysis.sentiment.polarity
	return analysis.sentiment.polarity
	# return 0

def getTimeStamp(timeStr):
	parsedDate = parser.parse(timeStr)
	timestamp = calendar.timegm(parsedDate.timetuple())
	return timestamp

def convertDateToIndex(time, minTime):
	return (time - minTime) // 60

def getTimeRange(tweets):
	min_, max_ = float('inf'), -float('inf')
	for tweet in tweets:
		timestamp = getTimeStamp(tweet[DATE_INDEX])
		min_ = min(min_, timestamp)
		max_ = max(max_, timestamp)
	return min_, max_

def getRoundedRange(minTime, maxTime):
	if minTime % 60 != 0: minTime += 60 - (minTime % 60)
	if maxTime % 60 != 0: maxTime -= minTime % 60
	return minTime, maxTime


def getMinuteArray(allTweets):
	actualMinTime, actualMaxTime = getTimeRange(allTweets)
	minTime, maxTime = getRoundedRange(actualMinTime, actualMaxTime)
	arrayLen = convertDateToIndex(maxTime, minTime) #normalized from second based to minute based
	print "arrayLen:", arrayLen, "minTime:", minTime, "maxTime:", maxTime
	minuteBuckets = [[] for _ in range(arrayLen)]
	return minuteBuckets, minTime, maxTime

def placeTweetInBucket(tweet, minuteBuckets, minTime, maxTime):
	sentiment = getTweetSentiment(tweet)
	tweet[TWEET_TEXT_INDEX] = sentiment
	timestamp = getTimeStamp(tweet[DATE_INDEX])
	if (timestamp >= minTime) and (timestamp < maxTime):
		index = convertDateToIndex(timestamp, minTime)
		minuteBuckets[index].append(tweet)

def bucketByMinute():
	allTweets = ReadData.CSVFileToMatrix()
	minuteBuckets, minTime, maxTime = getMinuteArray(allTweets)
	for tweet in allTweets:
		preProcessTweet(tweet)
		placeTweetInBucket(tweet, minuteBuckets, minTime, maxTime)
	return minuteBuckets

def preProcessTweet(tweet):
	printable = set(string.printable)
	tweet[TWEET_TEXT_INDEX] = filter(lambda char_: char_ in printable, tweet[TWEET_TEXT_INDEX])


def main():
	print "what's good"
	# WriteData.compileCSVFiles()
	print "buttplug"
	minuteBuckets = bucketByMinute()
	print len(minuteBuckets)
	for i, t in enumerate(minuteBuckets):
		if t != []: print i, t


if __name__ == "__main__":
	main()








