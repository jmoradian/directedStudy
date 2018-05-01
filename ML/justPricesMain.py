import tensorflow as tf, numpy as np, collections, sys, csv
from tensorflow.contrib import rnn
import RNN

def getPriceData():
	trainingData = []
	labels = []
	with open('../ExchangeQuery/priceData.csv') as csvfile:
		reader = csv.reader(csvfile)
		iter_ = 1
		for row in reader:
			closePrice = row[4]
			trainingData.append(closePrice)

		length = len(trainingData)
		for ind_, price in enumerate(trainingData[61:]):
			if price > trainingData[ind_+1]: labels.append([1,0])
			else: labels.append([0,1])
		return trainingData[1:length-61], labels

def getPriceDataContinuous():
	trainingData = []
	labels = []
	with open('../ExchangeQuery/priceData.csv') as csvfile:
		reader = csv.reader(csvfile)
		iter_ = 1
		for row in reader:
			closePrice = row[4]
			trainingData.append(closePrice)

		length = len(trainingData)
		for ind_, price in enumerate(trainingData[61:]):
			# print ind_, price, trainingData[ind_+1]
			label = (float(price) - float(trainingData[ind_ + 1]))/float(trainingData[ind_ + 1])
			labels.append([label])
		return trainingData[1:length-61], labels

# to test with just price data
def main():
	trainingData, labels = getPriceDataContinuous()
	rnn = RNN.RNN(learning_rate = .01, state_dimension = 1, input_size = 100, output_size = 1, hidden_state_size = 512)
	rnn.runnSess(trainingData, labels)




if __name__ == "__main__":
	main()
