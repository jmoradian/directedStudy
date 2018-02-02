import twitter, requests, time, pickle as pkl
from dateutil.parser import parse
from utils import *


def getTweets(api):
	try:
		statuses = api.GetSearch(
								 term='bitcoin',
								 lang='en',
								 count=100)
	except twitter.error.TwitterError:
		print "rate limit exceeded"
		return []

	return statuses

def runIterations(api):
	tweets = set()
	for _ in range(180):
		thisIterTweets = getTweets(api)
		tweets |= set(thisIterTweets)
	return tweets

def collectTweets():
	nariTweets = set()
	jordanTweets = set()
	
	t0 = time.time()
	#iterate through first account
	nariTweets = runIterations(apiNarimon)
	
	print "Done with first account. Time cost: ", time.time() - t0
	toSleep = TOTAL_SLEEP_TIME - (time.time() - t0)
	time.sleep(toSleep)

	#iterate through second account
	jordanTweets = runIterations(apiJordan)

	#merge tweet sets
	return nariTweets | jordanTweets

def main():
	if raw_input("Collect tweets? (y/n)   ") == 'y':
		allTweets = collectTweets()
		write.pickle(allTweets, "allTweetsJordan.pkl")
	else: allTweets = loadPickle("allTweetsJordan.pkl")
	min_ = time.time()
	max_ = 0
	for tweet in allTweets:
		curr = time.mktime(parse(tweet.created_at).timetuple())
		if curr < min_: min_ = curr
		if curr > max_: max_ = curr
	maxDate, minDate = datetime.utcfromtimestamp(min_), datetime.utcfromtimestamp(max_)
	print maxDate, minDate











if __name__ == "__main__":
	main()