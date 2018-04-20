TWEET_MINUTE_BUCKET_FILE = "tweetBucketByMinute.csv"
BUCKET_SIZES = [1., .5]





""" given the filepath to a csv, returns a matrix. """
def CSVToMatrix(filename):
	with open(filename, 'r') as file_:
		return [row for row in csv.reader(file_.read().splitlines())][1:]





def main():
	minuteData = CSVToMatrix(TWEET_MINUTE_BUCKET_FILE)
	





if __name__ == "__main__":
	main()