import csv, numpy as np, tweepy, textblob

GAPS = [60, 120, 360, 720, 1440]
SENTIMENT_BINS = [-1., -0.5, 0., 0.5]
TWEET_PARAMS = []
TWEET_TEXT_INDEX = 

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



