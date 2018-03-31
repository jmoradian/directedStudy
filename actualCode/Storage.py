import os

DATA_FILEPATH = 'TweetData/'
REPORTING_FILEPATH = 'Reporting/'

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

def calculateStorageInFilepath(fp):
	files = listStdDir(fp)
	size = 0

	for file_ in files:
		size += os.path.getsize(file_)

	return size

def calculateStorageUse():
	dataFilesSize = calculateStorageInFilepath(DATA_FILEPATH)
	reportingFilesSize = calculateStorageInFilepath(REPORTING_FILEPATH)

	return dataFilesSize + reportingFilesSize