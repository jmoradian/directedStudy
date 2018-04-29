import readData, writeData, util
import time
from math import floor

MIN_TIME = 1523049660

FILEPATH_TO_TWEETS = '../minutes/'
TIMESTEP = 5
BUCKET_SIZES = [1., .5, .25]
SENTIMENT_RANGE = 2.
SENTIMENT_INDEX = 2
CREATED_AT_INDEX = 0	# must be removed
MAX_SENTIMENT = 1.99
NUM_FEATURES_PER_BUCKET = 3

AVERAGES = {}
FEATURE_MATRIX = {}
COUNT_NON_EMPTY_TIMESTEPS = 0	
COUNT_EMPTY_TIMESTEPS = 0


PRICE_FILENAME = 'priceData.csv'
OPEN_INDEX = 1
CLOSE_INDEX = 4


def initAverages():
	for bucketSize in BUCKET_SIZES:
		numBuckets = int(SENTIMENT_RANGE / bucketSize)
		numFeatures = NUM_FEATURES_PER_BUCKET * numBuckets
		AVERAGES[bucketSize] = [0] * numFeatures

def initFeatureMatrix():
	for bucketSize in BUCKET_SIZES:
		FEATURE_MATRIX[bucketSize] = []

def normalizeFeatureVector(featureVector):
	numBuckets = len(featureVector) / NUM_FEATURES_PER_BUCKET

	sums = [0] * NUM_FEATURES_PER_BUCKET

	for sumIndex in range(NUM_FEATURES_PER_BUCKET):
		featureIndex = sumIndex
		for _ in range(numBuckets):
			sums[sumIndex] += featureVector[featureIndex]
			featureIndex += NUM_FEATURES_PER_BUCKET

	for featureIndex,val in enumerate(featureVector):
		sumIndex = featureIndex % NUM_FEATURES_PER_BUCKET
		featureVector[featureIndex] = val / max(sums[sumIndex], 1)

	return featureVector

def calcAverageFeatureVectors():
	for bucketSize in BUCKET_SIZES:
		AVERAGES[bucketSize] = normalizeFeatureVector(AVERAGES[bucketSize])

def aggregateAverages(featureVector, bucketSize):
	if not util.vectorIsEmpty(featureVector):
		global COUNT_NON_EMPTY_TIMESTEPS
		COUNT_NON_EMPTY_TIMESTEPS += 1. / NUM_FEATURES_PER_BUCKET
		for featureIndex, val in enumerate(featureVector):
			AVERAGES[bucketSize][featureIndex] += val
	else:
		global COUNT_EMPTY_TIMESTEPS
		COUNT_EMPTY_TIMESTEPS += 1. / NUM_FEATURES_PER_BUCKET


def addToFeatureMatrix(featureVector, bucketSize):
	if util.vectorIsEmpty(featureVector):
		featureVector = AVERAGES[bucketSize]

	normalizeFeatureVector(featureVector)
	FEATURE_MATRIX[bucketSize].append(featureVector)


def getSentiment(tweet):
	sentiment = float(tweet[SENTIMENT_INDEX])
	sentiment += 1	#change scale from -1 to 1 to a scale from 0 to 2
	sentiment = min(sentiment, MAX_SENTIMENT) # to avoid out of bounds errors
	return sentiment


def preProcessTweet(tweet):
	tweet = tweet[:SENTIMENT_INDEX] + tweet[SENTIMENT_INDEX+1 :]
	tweet = tweet[:CREATED_AT_INDEX] + tweet[CREATED_AT_INDEX+1 :]
	return [int(val) for val in tweet]


def convertTimestepToFeatureVector(timestep, bucketSize):
	numBuckets = int(SENTIMENT_RANGE / bucketSize)
	bucketedMatrix = [[0] * NUM_FEATURES_PER_BUCKET for _ in range(numBuckets)]

	for tweet in timestep:
		sentiment = getSentiment(tweet)
		tweet = preProcessTweet(tweet)
		bucketIndex = int(floor(sentiment / bucketSize))
		for featureIndex, val in enumerate(tweet):
			bucketedMatrix[bucketIndex][featureIndex] += val

	return util.concatenateMatrix(bucketedMatrix)


def doToAllTweets(filenames, func):
	minuteIndex = 0
	numTimesteps = len(filenames) / TIMESTEP
	numMinutes = numTimesteps * TIMESTEP 	# guarantees complete timesteps

	while (minuteIndex < numMinutes):
		timestep = []
		for _ in range(TIMESTEP):
			timestep += readData.CSVToMatrix(filenames[minuteIndex])
			minuteIndex += 1
		for bucketSize in BUCKET_SIZES:
			featureVector = convertTimestepToFeatureVector(timestep, bucketSize)
			func(featureVector, bucketSize)

def convertToTimestamp(priceTime):
	date_str = priceTime.replace('T',' ')[:-5]
	time_tuple = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
	timestamp = time.mktime(time_tuple)
	return int(timestamp)

def findIndexOfFirstMinute(labelMatrix):
	for index, minute in enumerate(labelMatrix):
		timestamp = convertToTimestamp(minute[0])
		if timestamp == MIN_TIME:
			return index + TIMESTEP  	# start at next timesteps change

def percentToOneHot(percentChange):
	if percentChange > 0.:
		return [1,0]
	else:
		return [0,1]


def convertLabelMatrixToLabels(labelMatrix):
	numTimesteps = int(COUNT_NON_EMPTY_TIMESTEPS + COUNT_EMPTY_TIMESTEPS)
	firstIndex = findIndexOfFirstMinute(labelMatrix)
	labelMatrix = labelMatrix[firstIndex:]

	percentLabels = []
	oneHotBinaryLabels = []

	minuteIndex = 0
	for _ in range(numTimesteps):
		open_ = float(labelMatrix[minuteIndex][OPEN_INDEX])
		minuteIndex += TIMESTEP - 1
		close_ = float(labelMatrix[minuteIndex][CLOSE_INDEX])

		percentChange = (close_ - open_) / open_
		percentLabels.append(percentChange)

		oneHot = percentToOneHot(percentChange)
		oneHotBinaryLabels.append(oneHot)

		minuteIndex += 1

	return percentLabels, oneHotBinaryLabels


def writeLabels(percentLabels, oneHotBinaryLabels):
	writeData.writePercentLabels(percentLabels)
	writeData.writeOneHotBinaryLabels(oneHotBinaryLabels)



def main():
	#features
	filenames = readData.getSortedFiles(FILEPATH_TO_TWEETS)
	
	initAverages()
	doToAllTweets(filenames, aggregateAverages)
	calcAverageFeatureVectors()

	initFeatureMatrix()
	doToAllTweets(filenames, addToFeatureMatrix)
	writeData.writeFeatureMatrix(FEATURE_MATRIX)

	#labels
	labelMatrix = readData.CSVToMatrix(PRICE_FILENAME)
	percentLabels, oneHotBinaryLabels = convertLabelMatrixToLabels(labelMatrix)
	writeLabels(percentLabels, oneHotBinaryLabels)

if __name__ == "__main__":
	main()
