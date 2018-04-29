import csv, numpy as np, calendar
from dateutil import parser
import ReadData, WriteData
import Featurize

FEATURE_LENGTH = 8
DATE_INDEX = 1
SECONDS_IN_MIN = 60
MIN_TIME = 1523049660

def getTimeStamp(timeStr):
	parsedDate = parser.parse(timeStr)
	timestamp = calendar.timegm(parsedDate.timetuple())
	return timestamp

def convertDateToIndex(time):
	return (time - MIN_TIME) // SECONDS_IN_MIN

def getMaxTime(tweets):
	max_ = -float('inf')
	for tweet in tweets:
		timestamp = getTimeStamp(tweet[DATE_INDEX])
		max_ = max(max_, timestamp)
	return max_ - max_ % SECONDS_IN_MIN

def getMinuteArray(allTweets):
	maxTime = getMaxTime(allTweets)
	arrayLen = convertDateToIndex(maxTime) #normalized from second based to minute based
	minuteBuckets = [[] for _ in range(arrayLen)]
	return minuteBuckets, maxTime

def placeTweetInBucket(tweet, minuteBuckets, maxTime):
	timestamp = tweet[DATE_INDEX - 1] #favorite count has been removed
	if (timestamp >= MIN_TIME) and (timestamp < maxTime):
		index = convertDateToIndex(timestamp)
		minuteBuckets[index].append(tweet)

def bucketByMinute(allTweets):
	minuteBuckets, maxTime = getMinuteArray(allTweets)
	for tweet in allTweets:
		Featurize.preProcessTweet(tweet)
		placeTweetInBucket(tweet, minuteBuckets, maxTime)
	return minuteBuckets

def main():
	allTweets = ReadData.compileCSVFiles()
	minuteBuckets = bucketByMinute(allTweets)
	WriteData.writeFinalProduct(minuteBuckets)


if __name__ == "__main__":
	main()








