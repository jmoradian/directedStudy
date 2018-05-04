import string, calendar
#textblob
from dateutil import parser

FAVORITE_INDEX = 0
DATE_INDEX = 1
TEXT_INDEX = 3
LISTED_INDEX = 5
VERIFIED_INDEX = 6
FRIEND_INDEX = 7

def getTimeStamp(timeStr):
	parsedDate = parser.parse(timeStr)
	timestamp = calendar.timegm(parsedDate.timetuple())
	return timestamp

# uses textblob library to analyze the tweet sentiment
# 	- textblob is trained on movie review data
def getTweetSentiment(tweet):
	# printable = set(string.printable)
	# tweetText = filter(lambda char_: char_ in printable, tweet[TEXT_INDEX])
	# sentiment = float(textblob.TextBlob(tweetText).sentiment.polarity) # may need to rid text of special characters
	# return sentiment
	return 0.


def preProcessTweet(tweet):
	tweet[TEXT_INDEX] = getTweetSentiment(tweet)
	tweet[VERIFIED_INDEX] = 0 if tweet[VERIFIED_INDEX] == "False" else 1
	tweet[DATE_INDEX] = getTimeStamp(tweet[DATE_INDEX])
	del tweet[FRIEND_INDEX]
	del tweet[LISTED_INDEX]
	del tweet[FAVORITE_INDEX]