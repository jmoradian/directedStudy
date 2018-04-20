import csv, time, os, codecs


CSV_FILEPATH = "../TweetData/"




"""filepath stuff"""

def read(filePath):
    with open(filePath, "r") as file:
        return file.read()

def hidden(path):
    return path.find(".") == 0

def listStdDir(dirPath):
	std = []
	for name in os.listdir(dirPath):
		 if not hidden(name):
			std.append(os.path.join(dirPath, name))
	return std



def sortMatrixByDate(matrix):
	matrix.sort(key=lambda x: x[1])
	return matrix


# """ given the filepath to a csv, returns a matrix. """
def CSVFileToMatrix(filename):
	with open(filename, 'r') as file_:
		return [row for row in csv.reader(file_.read().splitlines())][1:]


def compileCSVFiles():
	allTweets = []
	for filename in listStdDir(CSV_FILEPATH):
		allTweets += CSVFileToMatrix(filename)

	return allTweets





