import csv, numpy as np, calendar, os
from dateutil import parser
import ReadData, WriteData
import Featurize

DATE_INDEX = 1
SECONDS_IN_MIN = 60
MIN_TIME = 1523049660

CSV_FILEPATH = "../TweetData/"



def convertDateToIndex(time):
	return (time - MIN_TIME) // SECONDS_IN_MIN

def processTweet(tweet):
	Featurize.preProcessTweet(tweet)
	timestamp = tweet[DATE_INDEX - 1] #favorite count has been removed
	if timestamp >= MIN_TIME:
		WriteData.writeTweet(tweet, convertDateToIndex(timestamp))


def main():
	filenames = ReadData.listStdDir(CSV_FILEPATH)
	for filename in filenames:
		print filename
		tweets = ReadData.CSVFileToMatrix(filename)
		for tweet in tweets:
			processTweet(tweet)


if __name__ == "__main__":
	main()








