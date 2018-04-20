import string
# import textblob

TEXT_INDEX = 3
VERIFIED_INDEX = 6
FRIEND_INDEX = 7
LISTED_INDEX = 5


# uses textblob library to analyze the tweet sentiment
# 	- textblob is trained on movie review data
def getTweetSentiment(tweet):
	printable = set(string.printable)
	tweetText = filter(lambda char_: char_ in printable, tweet[TEXT_INDEX])
	# analysis = textblob.TextBlob(text) # may need to rid text of special characters
	return .5


def preProcessTweet(tweet):
	tweet[TEXT_INDEX] = getTweetSentiment(tweet)
	tweet[VERIFIED_INDEX] = 0 if tweet[VERIFIED_INDEX] == "False" else 1
	del tweet[FRIEND_INDEX]
	del tweet[LISTED_INDEX]