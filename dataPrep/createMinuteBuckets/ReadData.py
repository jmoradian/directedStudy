import csv, time, os, codecs







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

# """ given the filepath to a csv, returns a matrix. """
def CSVFileToMatrix(filename):
	with open(filename, 'r') as file_:
		return [row for row in csv.reader(file_.read().splitlines())][1:]






