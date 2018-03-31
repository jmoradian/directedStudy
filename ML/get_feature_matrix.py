import csv, numpy as np

GAPS = [60, 120, 360, 720, 1440]
SENTIMENT_BINS = [0.5, 0., -0.5, -1.]
TWEET_PARAMS = []

def getLabel(data, currentTimestep):
	label = data[currentTimestep + 60][-1] - data[currentTimestep][-1]
	return label

def getLabelVector(data):
	labels = []
	for timestep in range(len(data)):
		label = getLabel(data, timestep)
		labels.append(label)
	return np.array(labels)

def getPriceChange(data, currentTimestep):
	deltas = []
	prices = [row[-1:] for row in data]
	for gap in GAPS:
		if (currentTimestep > gap): delta = data[currentTimestep][-1] - data[currentTimestep - gap][-1]
		else: delta = None
		deltas.append(delta)
	return np.array(deltas)

def getTweetSentiment(tweet):

def discretizeSentiment(sentiment):

def aggregateSentiments(tweets):
	sentimentDict = {bin: [0] * len(TWEET_PARAMS) for bin in SENTIMENT_BINS}
	for tweet in tweets:
		sentiment = getTweetSentiment(tweet)
		bin = discretizeSentiment(sentiment)
		for feat, featVal in enumerate(tweet):
			sentimentDict[bin][feat] += featVal
	return sentimentDict.values()

def getFeatureMatrix(data, timestep):
	

