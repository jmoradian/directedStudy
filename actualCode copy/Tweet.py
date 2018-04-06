import twitter

KEYS = [
		'favorite_count',
		'created_at',
		'retweet_count',
		'text',
		'followers_count',
		'listed_count',
		'verified',
		'friend_count',
		]

class Tweet(object):
	def __init__(self, tweet):
		self.tweetValDict = {
						'favorite_count': unicode(tweet.favorite_count).encode("utf-8"),
						'created_at': unicode(tweet.created_at).encode("utf-8"),
						'retweet_count': unicode(tweet.retweet_count).encode("utf-8"),
						'text': unicode(tweet.text).encode("utf-8"),
						'followers_count': unicode(tweet.user.followers_count).encode("utf-8"),
						'listed_count': unicode(tweet.user.listed_count).encode("utf-8"),
						'verified': unicode(tweet.user.verified).encode("utf-8"),
						'friend_count': unicode(tweet.user.friends_count).encode("utf-8"),
						}

	def getTweetValDict(self):
		return self.tweetValDict