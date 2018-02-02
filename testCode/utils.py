import pickle as pkl, twitter


LOCATIONS = [('37.7749', '-122.4194', '50'), 	# San Francisco
			 ('40.7128', '-74.0060', '50')		# New York
			]
TOTAL_SLEEP_TIME = 225

ACCESS_TOKEN_KEY_JORDAN = '374277631-0lPePuaIbIdJAZrItYNsHNTO7ey4iD9aOIuZRMHS'
ACCESS_TOKEN_SECRET_JORDAN='qElAyPX6nPlh9YA4gulhMKNaKw1LMDU69W89WjQ6C9SU6'
CONSUMER_KEY_JORDAN='4EsFry3foprndToeCEaOSYUIE'
CONSUMER_SECRET_JORDAN='BsDxbfgY32suGzCH3IdFhBN7aKKam5WCmSAOmwX8SMuavdpzNr'

CONSUMER_KEY_NARIMON='vdp2mFsEfUOzoF7c3UbptAIHA'
CONSUMER_SECRET_NARIMON='iiumhVNsOTHqCRVbokFZ8C7qNjCD2Jav2ksg4snq4EWNEVd34V'
ACCESS_TOKEN_KEY_NARIMON='1961862606-6U3xLyyaXh9DTw39hONBnNwObs8nzAGbaCRYZ1H'
ACCESS_TOKEN_SECRET_NARIMON='pnykzbUsHjNH3gqIGNJ9uKTbqTXc5MvBXgOK6Vf3XTFnk'

apiJordan = twitter.Api(consumer_key=CONSUMER_KEY_JORDAN,
				  consumer_secret=CONSUMER_SECRET_JORDAN,
				  access_token_key=ACCESS_TOKEN_KEY_JORDAN,
				  access_token_secret=ACCESS_TOKEN_SECRET_JORDAN,
				  # sleep_on_rate_limit=True
				  )
apiNarimon = twitter.Api(consumer_key=CONSUMER_KEY_NARIMON,
				  consumer_secret=CONSUMER_SECRET_NARIMON,
				  access_token_key=ACCESS_TOKEN_KEY_NARIMON,
				  access_token_secret=ACCESS_TOKEN_SECRET_NARIMON,
				  # sleep_on_rate_limit=True
				  )

def loadPickle(filepath):
	with open(filepath, 'r') as file_:
		return pkl.load(file_)

def writePickle(obj, filepath):
	with open(filepath, 'w') as file_:
		pkl.dump(obj, file_)