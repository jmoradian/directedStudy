import csv, numpy as np, math, h5py
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Activation
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint

PRED_TIME = 60



def getModel(network_input, binary):
	model = Sequential()
	model.add(LSTM(
		2,
		input_shape=(network_input.shape[1], network_input.shape[2]),
		# return_sequences=True
	))

	# model.add(Dropout(0.3))
	# model.add(LSTM(64, return_sequences=True))
	# model.add(Dropout(0.3))
	# model.add(LSTM(32))
	# model.add(Dense(256))
	# model.add(Dropout(0.3))
	# model.add(Dense(2))
	model.add(Activation('softmax'))
	if binary: model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy']) #look into adam optimizer
	else: model.compile(loss='mse', optimizer='rmsprop')

	return model

def getContInputOutput(trainData):
	sequence_length = 1440 #entire day of data
	# create a dictionary to map pitches to integers
	network_input = []
	network_output = []

	# create input sequences and the corresponding outputs
	for i in range(0, len(trainData) - sequence_length - PRED_TIME):
		curr, fut_ = trainData[i + sequence_length], trainData[i + sequence_length + PRED_TIME]
		sequence_in = trainData[i:i + sequence_length]
		sequence_out = (fut_ - curr)/curr
		# print type(sequence_out)
		network_input.append([price for price in sequence_in])
		network_output.append(sequence_out)
	print "cont", network_output[0]
	n_patterns = len(network_input)
	# reshape the input into a format compatible with LSTM layers
	network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
	network_output = np.asarray(network_output)
	# normalize input
	network_input = np_utils.normalize(network_input)
	network_output = np_utils.normalize(network_output)
	# network_output = np_utils.to_categorical(network_output)
	return network_input, network_output

def getBinInputOutput(trainData):
	sequence_length = 900 #15 hours
	# create a dictionary to map pitches to integers
	network_input = []
	network_output = []

	# create input sequences and the corresponding outputs
	for i in range(0, len(trainData) - sequence_length - PRED_TIME):
		curr, fut_ = trainData[i + sequence_length], trainData[i + sequence_length + PRED_TIME]
		sequence_in = trainData[i:i + sequence_length]
		sequence_out = (fut_ - curr)/curr
		if (fut_ - curr) > 0: sequence_out = 1
		else: sequence_out = 0
		network_input.append([price for price in sequence_in])
		network_output.append(sequence_out)
	n_patterns = len(network_input)
	print "###### done with sequencing 1"
	# reshape the input into a format compatible with LSTM layers
	network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
	network_output = np.asarray(network_output)
	# normalize input
	network_input = np_utils.normalize(network_input)
	# network_output = np_utils.normalize(network_output)
	network_outputCat = np_utils.to_categorical(network_output, 2)
	# for ind in range(len(network_output)):
	# 	print network_outputCat[ind], network_output[ind]
	print "###### done with sequencing 2"
	return network_input, network_outputCat 

def runRegression(model, network_input, network_output):
	filepath = "saved-params/weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"    
	checkpoint = ModelCheckpoint(
		filepath, monitor='loss', 
		verbose=0,        
		save_best_only=True,        
		mode='min'
	)    
	callbacks_list = [checkpoint]   
	print network_input.shape
	print network_output.shape
	model.fit(network_input, network_output, epochs=100, batch_size=64, callbacks=callbacks_list)

def train(trainData):
	network_input, network_output = getBinInputOutput(trainData)
	# network_input, network_output = getContInputOutput(trainData)


	model = getModel(network_input, binary = True)
	runRegression(model, network_input, network_output)




""" given the filepath to a csv, returns a matrix. """
def csvToMatrix(filename):
	with open(filename, 'r') as file:
		return [row for row in csv.reader(file.read().splitlines())]

def processDataforMatrix(rawData):
	data = [row[1:] for row in rawData]		#remove timestamp
	data = data[:-1] 						#remove last datum
	labels = [row[-1:] for row in data]		#labels (next weighted price)

	return np.array(data), np.array(labels)

def processDataJustPrices(rawData):
	data = [row[-1:] for row in rawData]		#data (weighted price)
	data = data[1:]
	# print data[118]
	data = [[float(row[0])] for row in data]

	return np.array(data)


def main():
	rawData = csvToMatrix('coinbase_minute.csv')
	data = processDataJustPrices(rawData)
	# print data[:5]
	train(data)



if __name__ == "__main__":
	main()





