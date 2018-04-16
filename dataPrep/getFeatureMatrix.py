import csv, numpy as np, calendar
from dateutil import parser
import ReadData, WriteData
import Featurize

FEATURE_LENGTH = 8
DATE_INDEX = 1
SECONDS_IN_MIN = 60


def getTimeStamp(timeStr):
	parsedDate = parser.parse(timeStr)
	timestamp = calendar.timegm(parsedDate.timetuple())
	return timestamp

def convertDateToIndex(time, minTime):
	return (time - minTime) // SECONDS_IN_MIN

def getTimeRange(tweets):
	min_, max_ = float('inf'), -float('inf')
	for tweet in tweets:
		timestamp = getTimeStamp(tweet[DATE_INDEX])
		min_ = min(min_, timestamp)
		max_ = max(max_, timestamp)
	return min_, max_

def getRoundedRange(minTime, maxTime):
	if minTime % SECONDS_IN_MIN != 0: minTime += SECONDS_IN_MIN - (minTime % SECONDS_IN_MIN)
	if maxTime % SECONDS_IN_MIN != 0: maxTime -= minTime % SECONDS_IN_MIN
	return minTime, maxTime


def getMinuteArray(allTweets):
	actualMinTime, actualMaxTime = getTimeRange(allTweets)
	minTime, maxTime = getRoundedRange(actualMinTime, actualMaxTime)
	arrayLen = convertDateToIndex(maxTime, minTime) #normalized from second based to minute based
	print "arrayLen:", arrayLen, "minTime:", minTime, "maxTime:", maxTime
	minuteBuckets = [[] for _ in range(arrayLen)]
	return minuteBuckets, minTime, maxTime

def placeTweetInBucket(tweet, minuteBuckets, minTime, maxTime):
	timestamp = getTimeStamp(tweet[DATE_INDEX])
	if (timestamp >= minTime) and (timestamp < maxTime):
		index = convertDateToIndex(timestamp, minTime)
		minuteBuckets[index].append(tweet)

def bucketByMinute(allTweets):
	minuteBuckets, minTime, maxTime = getMinuteArray(allTweets)
	for tweet in allTweets:
		Featurize.preProcessTweet(tweet)
		placeTweetInBucket(tweet, minuteBuckets, minTime, maxTime)
	return minuteBuckets

def main():
	allTweets = ReadData.compileCSVFiles()
	minuteBuckets = bucketByMinute(allTweets)
	


if __name__ == "__main__":
	main()








