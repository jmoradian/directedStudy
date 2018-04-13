import csv, numpy as np, tweepy, textblob, calendar
from dateutil import parser
import ReadData

GAPS = [60, 120, 360, 720, 1440]
SENTIMENT_BINS = [-1., -0.5, 0., 0.5]
TWEET_PARAMS = []
FEATURE_LENGTH = 8, DATE_INDEX = 1, TWEET_TEXT_INDEX = 3

def getLabel(priceData, timestep):
	label = data[timestep + 60][-1] - data[timestep][-1]
	return label

def getLabelVector(priceData):
	labels = []
	for timestep in range(len(data)):
		label = getLabel(data, timestep)
		labels.append(label)
	return np.array(labels)

def getPriceChanges(priceData, timestep):
	deltas = []
	prices = [row[-1:] for row in data]
	for gap in GAPS:
		if (timestep > gap): delta = data[timestep][-1] - data[timestep - gap][-1]
		else: delta = None
		deltas.append(delta)
	return np.array(deltas)

# uses textblob library to analyze the tweet sentiment
# 	- textblob is trained on movie review data
def getTweetSentiment(tweet):
	text = tweet[TWEET_TEXT_INDEX]
	analysis = textblob.TextBlob(text) # may need to rid text of special characters
	return analysis.sentiment.polarity

# floors sentiment to closest bin
def discretizeSentiment(sentiment):
	for ind_, bin in enumerate(SENTIMENT_BINS):
		if sentiment < bin: return (ind_ - 1)
	return len(SENTIMENT_BINS) - 1

#returns a list of feature lists at each sentiment level
def aggregateSentiments(tweets):
	sentimentDict = {bin: [0] * len(TWEET_PARAMS) for bin in SENTIMENT_BINS}
	for tweet in tweets:
		sentiment = getTweetSentiment(tweet)
		bin = discretizeSentiment(sentiment)
		# feat is the feature index
		for feat, featVal in enumerate(tweet):
			sentimentDict[bin][feat] += featVal
	return sentimentDict.values()

def getFeatureMatrix(priceData, tweets, timestep):
	priceChanges = getPriceChanges(priceData, timestep)
	tweetFeatsBySent = aggregateSentiments(tweets) 
	vectorizedTweetFeats = []
	vectorizedTweetFeats.append(sentFeatures) for sentFeatures in tweetFeatsBySent.values()
	vectorizedTweetFeats.append(priceChanges)
	return vectorizedTweetFeats

def getTimeStamp(timeStr):
	parsedDate = parser.parse(timeStr)
	timestamp = calendar.timegm(parsedDate)
	return timestamp

def convertDateToIndex(date_):
	return date_ // 60

def getMinuteArray():
	minTime, maxTime = getTimeRange(allTweets)
	minTimestamp, maxTimestamp = getTimeStamp(minTime), getTimeStamp(maxTime)
	arrayLen = convertDateToIndex(maxTimestamp - minTimestamp) #normalized from second based to minute based
	minuteBuckets = [[] for i in range(arrayLen)]
	return minuteBuckets

def aggregateByMinute():
	allTweets = ReadData.CSVFileToMatrix()
	minuteBuckets = getMinuteArray(allTweets)
	for tweet in allTweets:
		sentiment = getTweetSentiment(tweet)
		tweet[TWEET_TEXT_INDEX] = sentiment
		index = getTimeStamp(tweet[DATE_INDEX])
		minuteBuckets[index].append(tweet)

	# easy to be really inefficient




