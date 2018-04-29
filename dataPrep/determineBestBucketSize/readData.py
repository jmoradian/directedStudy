import os, csv

""" given the filepath to a csv, returns a matrix. """
def CSVToMatrix(filename):
	with open(filename, 'r') as file_:
		return [row for row in csv.reader(file_.read().splitlines())][1:]

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

def getSortedFiles(dirPath):
	std = listStdDir(dirPath)
	std.sort(key=lambda elem: int(elem.split('/')[2].split('.')[0]))
	return std