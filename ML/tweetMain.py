import tensorflow as tf, numpy as np, collections, sys, csv
from tensorflow.contrib import rnn
import RNN


FILEPATHS = [
				'../dataPrep/determineBestBucketSize/featureMatrices/BucketSizeFeatureMatrix10.csv',
				'../dataPrep/determineBestBucketSize/featureMatrices/BucketSizeFeatureMatrix05.csv',
				'../dataPrep/determineBestBucketSize/featureMatrices/BucketSizeFeatureMatrix025.csv']

def getContLabels():
	labels = []
	with open('../dataPrep/determineBestBucketSize/labels/percentLabels.csv') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			label = float(row[0])
			labels.append([label])
	return labels

def getData(filepath):
	data = []
	with open(filepath) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			featVec = map(float, row)
			data.append(featVec)
	return data

# takes splitProportion as a fraction
def splitDataSet(data, splitProportion):
	length = len(data)
	splitInd = int(length * splitProportion)

	trainData = data[:splitInd]
	testData= data[splitInd:]
	return trainData, testData

# takes splitProportion as a fraction
def splitLabelSet(labels, splitProportion):
	length = len(labels)
	splitInd = int(length * splitProportion)

	trainLabels = labels[:splitInd]
	testLabels = labels[splitInd:]
	return trainLabels, testLabels


def main():
	tot_losses = []
	avg_losses = [0] * 3
	labels = getContLabels()
	trainLabels, testLabels = splitLabelSet(labels, splitProportion = 1.)
	for i_ in range(10):
		print "iteration " + (i_ + 1)
		losses = []
		for filepath in FILEPATHS:
			data = getData(filepath)
			trainData, testData = splitDataSet(labels, splitProportion = 1.)
			rnn = RNN.RNN(learning_rate = .01, state_dimension = len(trainData[0]), input_size = 120, output_size = 1, hidden_state_size = 512)
			losses.append(rnn.runnSess(trainData, trainLabels))
		for ind, loss in enumerate(losses):
			avg_losses[ind] += loss
		tot_losses.append(losses)
	avg_losses = [loss/10. for loss in avg_losses]

	print tot_losses
	print avg_losses


# def main():
# 	losses = []
# 	labels = getContLabels()
# 	trainLabels, testLabels = splitLabelSet(labels, splitProportion = 1.)
# 	for filepath in ['../dataPrep/determineBestBucketSize/featureMatrices/BucketSizeFeatureMatrix10.csv']:
# 		data = getData(filepath)
# 		trainData, testData = splitDataSet(labels, splitProportion = 1.)
# 		rnn = RNN.RNN(learning_rate = .01, state_dimension = len(trainData[0]), input_size = 120, output_size = 1, hidden_state_size = 512)
# 		losses.append(rnn.runnSess(trainData, trainLabels))

# 	print losses

# tensorboard --logdir /tmp/tensorflow/rnn_graph/

if __name__ == "__main__":
	main()




