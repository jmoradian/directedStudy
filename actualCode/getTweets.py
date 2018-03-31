import time, twitter
import Tweet, writeData
from accountInfo import APIS

NUM_APIS = len(APIS)
NUM_TWEETS_PER_15_MINS = 180
NUM_SECONDS_IN_15_MINS = 900
TIME_PER_API = NUM_SECONDS_IN_15_MINS / NUM_APIS

DATA_FILEPATH = 'TweetData/'


def makeTwitterRequest(api):
	try:
		return api.GetSearch(
							 term='bitcoin',
							 lang='en',
							 count=100)
	except twitter.error.TwitterError:
		writeData.writeErrorReport()
		return []

def getTweets(api):
	tweets = set()
	for _ in range(180):
		thisIterTweets = makeTwitterRequest(api)
		thisIterTweets = [Tweet.Tweet(tweet) for tweet in thisIterTweets]	# convert to Tweet Object
		tweets |= set(thisIterTweets)
	return tweets
	

def runProcessFourTimes():
	fname = DATA_FILEPATH + str(time.time()) + '_data.csv'
	writeData.initializeCSV(fname)

	iter_ = 0
	for _ in range(1):
		tweets = set()
		for api in APIS:
			startTime = time.time()
			tweets |= set(getTweets(api))
			iter_ += 1
			writeData.writeProgressReport(iter_, len(tweets))
			sleepTime = max(TIME_PER_API - (time.time() - startTime), 0)
			time.sleep(sleepTime)

		writeData.writeTweetsToCSV(fname, tweets)

def main():
	while True:
		try:
			runProcessFourTimes()
		except:
			pass



if __name__ == "__main__":
	main()