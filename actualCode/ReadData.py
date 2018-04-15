import csv, time, os


def sortMatrixByDate(matrix):
	matrix.sort(key=lambda x: x[1])
	return matrix


""" given the filepath to a csv, returns a matrix. """
def CSVFileToMatrix():
	with open("compiledTweetData.csv", 'r') as file_:
		return [row for row in csv.reader(file_.read().splitlines())][1:]