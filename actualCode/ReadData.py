import csv, time, os


def sortMatrixByDate(matrix):
	matrix.sort(key=lambda x: x[1])
	return matrix

def CSVFileToMatrix():
	tweetMatrix = []
	with open('compiledTweetData.csv', 'r') as file_:
		file_.next()
		for tweet in file_: tweetMatrix.append(tweet)
	return tweetMatrix	
	