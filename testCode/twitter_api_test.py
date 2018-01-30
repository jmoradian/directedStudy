import twitter, requests, time, pickle as pkl

CONSUMER_KEY='vdp2mFsEfUOzoF7c3UbptAIHA'
CONSUMER_SECRET='iiumhVNsOTHqCRVbokFZ8C7qNjCD2Jav2ksg4snq4EWNEVd34V'
ACCESS_TOKEN_KEY='1961862606-6U3xLyyaXh9DTw39hONBnNwObs8nzAGbaCRYZ1H'
ACCESS_TOKEN_SECRET='pnykzbUsHjNH3gqIGNJ9uKTbqTXc5MvBXgOK6Vf3XTFnk'

api = twitter.Api(consumer_key=CONSUMER_KEY,
				  consumer_secret=CONSUMER_SECRET,
				  access_token_key=ACCESS_TOKEN_KEY,
				  access_token_secret=ACCESS_TOKEN_SECRET,
				  # sleep_on_rate_limit=True
				  )


LOCATIONS = [('37.7749', '-122.4194', '50'), 	# San Francisco
			 ('40.7128', '-74.0060', '50')		# New York
			]

# print len(statuses)
# print
# for index, status in enumerate(statuses):
# 	print index
# 	print status.created_at, "  ", status.text

def addTweetsToAllTweets(allTweets, thisIterTweets):
	for tweet in thisIterTweets:
		allTweets.add(tweet)

	return allTweets


def getTweets():
	# for lat, lng, rad in LOCATIONS:
	# 	geocode_ = lat + ',' + lng + ',' + rad + 'mi'
	try:
		statuses = api.GetSearch(
								 term='bitcoin',
								 lang='en',
								 # geocode=geocode_,
								 count=100)
	except twitter.error.TwitterError:
		print "rate limit exceeded"
		time.sleep(1)


	return statuses


def main():
	allTweets = set()
	iter_ = 0

	startTime = time.time()
	while time.time() - startTime < 1:
		thisIterTweets = getTweets()
		preTheseTweets = len(allTweets)
		allTweets = addTweetsToAllTweets(allTweets, thisIterTweets)
		postTheseTweets = len(allTweets)
		print 'num tweets from api: ', len(thisIterTweets), 'num tweets added: ', postTheseTweets-preTheseTweets
		print 'iter:', iter_, ' numTweets: ', len(allTweets)
		iter_ += 1
		time.sleep(5)
	for tweet in allTweets:
		print tweet
		break

	# statuses = api.GetSearch(term='bitcoin', count=100)
	# print statuses[0] == statuses[0]
	# print statuses[0] == statuses[1]

	# dictTest = {}
	# dictTest[statuses[0]] = True
	# if statuses[0] in dictTest: print 'ayy'
	# if statuses[1] not in dictTest: print 'ayy'
	

if __name__ == "__main__":
	main()