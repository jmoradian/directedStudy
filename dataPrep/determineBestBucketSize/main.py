import readData
from math import floor

SENTIMENT_RANGE = 2.
BUCKET_SIZES = [1., .5, .25]
FILEPATH_TO_TWEETS = '../minutes/'
TIMESTEP = 5
CREATED_AT_INDEX = 0	# must be removed
SENTIMENT_INDEX = 2 
MAX_SENTIMENT = 1.99



def getMinuteData():
	tweetsByMinute = []
	minutes = readData.getSortedFiles(FILEPATH_TO_TWEETS)
	for minute in minutes:
		minuteMatrix = readData.CSVToMatrix(minute)
		tweetsByMinute.append(minuteMatrix)

	return tweetsByMinute


def convertTweetsToTimestep(tweetsByMinute):
	tweetsByTimestep = []
	numTimesteps = len(tweetsByMinute) / TIMESTEP

	index = 0
	while index < numTimesteps * TIMESTEP:
		tweetsInTimestep = []
		for _ in range(TIMESTEP):
			tweetsInTimestep += tweetsByMinute[index]
			index += 1
		tweetsByTimestep.append(tweetsInTimestep)

	return tweetsByTimestep

def preProcessTweet(tweet):
	del tweet[SENTIMENT_INDEX]
	del tweet[CREATED_AT_INDEX]
	return [int(val) for val in tweet]


def getSentiment(tweet):
	sentiment = float(tweet[SENTIMENT_INDEX])
	sentiment += 1	#change scale from -1 to 1 to a scale from 0 to 2
	sentiment = min(sentiment, MAX_SENTIMENT) # to avoid out of bounds errors
	return sentiment

	# emptyFeatureVector = [0] * len(tweetsByMinute[0][0])
	# numTimesteps = len(tweetsByMinute) / 5
	# tweetsByTimestep = [emptyFeatureVector for _ in range(numTimesteps)]
def convertTweetsToFeatureMatrix(tweetByTimestep, bucketSize):
	featureMatrix = []
	numBuckets = int(SENTIMENT_RANGE / bucketSize)

	print len(tweetByTimestep)
	i = 0
	for tweets in tweetByTimestep:
		print i, tweets[0][0]
		i += 1
		emptyFeatureVector = [0] * (len(tweetByTimestep[0][0]) - 2) 	#created_at, sentiment
		bucketedMatrix = [emptyFeatureVector for _ in range(numBuckets)]
		for tweet in tweets:
			# if len(tweet) < 5: print tweet
			sentiment = getSentiment(tweet)
			tweet = preProcessTweet(tweet)
			index = int(floor(sentiment / bucketSize))
			# print sentiment, index




def main():
	tweetsByMinute = getMinuteData()
	tweetByTimestep = convertTweetsToTimestep(tweetsByMinute)
	for bucketSize in BUCKET_SIZES:
		featureMatrix = convertTweetsToFeatureMatrix(tweetByTimestep, bucketSize)

	





if __name__ == "__main__":
	main()