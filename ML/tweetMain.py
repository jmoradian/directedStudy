import tensorflow as tf, numpy as np, collections, sys, csv
from tensorflow.contrib import rnn
import RNN


FILEPATHS = [
				'../../../../dataPrep/determineBestBucketSize/featureMatrices/BucketSizeFeatureMatrix10.csv',
				'../../../../dataPrep/determineBestBucketSize/featureMatrices/BucketSizeFeatureMatrix05.csv',
				'../../../../dataPrep/determineBestBucketSize/featureMatrices/BucketSizeFeatureMatrix025.csv']

def getContLabels():
	labels = []
	with open('../../../../dataPrep/determineBestBucketSize/labels/percentLabels.csv') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			label = 10000.*float(row[0])
			labels.append([label])
	return labels

def getCatLabels():
	labels = []
	with open('../../../../dataPrep/determineBestBucketSize/labels/oneHotLabels.csv') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			label = map(float, row)
			labels.append(label)
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


# def main():
# 	tot_losses = []
# 	avg_losses = [0] * 3
# 	labels = getContLabels()
# 	trainLabels, testLabels = splitLabelSet(labels, splitProportion = 1.)
# 	for i_ in range(10):
# 		print "iteration " + str(i_ + 1)
# 		losses = []
# 		for filepath in FILEPATHS:
# 			data = getData(filepath)
# 			trainData, testData = splitDataSet(labels, splitProportion = 1.)
# 			rnn = RNN.RNN(learning_rate = .01, state_dimension = len(trainData[0]), input_size = 120, output_size = 1, hidden_state_size = 512, categorical = False)
# 			losses.append(rnn.runnSess(trainData, trainLabels))
# 		for ind, loss in enumerate(losses):
# 			avg_losses[ind] += loss
# 		tot_losses.append(losses)
# 	avg_losses = [loss/10. for loss in avg_losses]

# 	print tot_losses
# 	print avg_losses

# .01 always comes out on top
LEARNING_RATES = [.05, .01, .005, .001]
HIDDEN = [5, 25, 50, 112, 512]
def main():
	losses = []
	labels = getCatLabels()
	trainLabels, testLabels = splitLabelSet(labels, splitProportion = 1.)
	for filepath in ['../../../../dataPrep/determineBestBucketSize/featureMatrices/BucketSizeFeatureMatrix05.csv']:
		data = getData(filepath)
		trainData, testData = splitDataSet(labels, splitProportion = 1.)
		for hs in [50]:
			print "HIDDEN SIZE " + str(hs) + "	####################"
			rnn = RNN.RNN(learning_rate = .01, state_dimension = len(trainData[0]), input_size = 340, output_size = len(labels[0]), hidden_state_size = hs, categorical = True)
			losses.append(rnn.runnSess(trainData, trainLabels, iterations = 10))

	print losses
# top loss = 123
# hidden size of 5 result in outputs being decimal size with labels still being multiplied by 10000
# 25, 50, and 112 all within range to be top unit picks

# tensorboard --logdir /tmp/tensorflow/rnn_graph/

if __name__ == "__main__":
	main()




