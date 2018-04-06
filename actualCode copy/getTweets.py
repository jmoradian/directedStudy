import time, twitter, sys
import Tweet, WriteData, Storage
from accountInfo import APIS

NUM_APIS = len(APIS)
NUM_TWEETS_PER_15_MINS = 180
NUM_SECONDS_IN_15_MINS = 900
TIME_PER_API = NUM_SECONDS_IN_15_MINS / NUM_APIS

DATA_FILEPATH = 'TweetData/'
REPORTING_FILEPATH = 'Reporting/'


def makeTwitterRequest(api):
	try:
		return api.GetSearch(
							 term='bitcoin',
							 lang='en',
							 count=100)
	except twitter.error.TwitterError:
		WriteData.writeErrorReport()
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
	WriteData.initializeCSV(fname)
	sys.stdout.flush()

	iter_ = 0
	for _ in range(4):
		tweets = set()
		for api in APIS:
			startTime = time.time()
			tweets |= set(getTweets(api))
			iter_ += 1
			WriteData.writeProgressReport(iter_, len(tweets))
			sleepTime = max(TIME_PER_API - (time.time() - startTime), 0)
			time.sleep(sleepTime)
			sys.stdout.flush()


		WriteData.writeTweetsToCSV(fname, tweets)
		sys.stdout.flush()


def main():
	while Storage.calculateStorageUse() < 4500000000:
		try:
			runProcessFourTimes()
		except:
			pass



if __name__ == "__main__":
	main()