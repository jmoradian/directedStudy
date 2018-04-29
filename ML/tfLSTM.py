import tensorflow as tf, numpy as np, collections
from tf.contrib import rnn

NUM_ENGAGEMENT_METS = 6
SENT_BUCKET_SIZE = .5
INPUT_STATE_SIZE = (2/SENT_BUCKET_SIZE) * NUM_ENGAGEMENT_METS + 1
HIDDEN_STATE_SIZE = 512 #subject to change - size of longterm memory but allegedly must match the output size - should be 2
OUTPUT_SIZE = 2 # either positive or negative
LEARNING_RATE = .005


def initPlaceholders():
	# tf Graph input
	inSeq = tf.placeholder("float", [None, INPUT_STATE_SIZE, 1])
	labels = tf.placeholder("float", [None, OUTPUT_SIZE])
	# RNN output node weights and biases
	weights = {'out': tf.Variable(tf.random_normal([INPUT_STATE_SIZE, OUTPUT_SIZE]))}
	biases = {'out': tf.Variable(tf.random_normal([OUTPUT_SIZE]))}

	return inSeq, labels, weights, biases


def initLossOptimizer(pred, labels):
	# Loss and optimizer
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=labels))
	optimizer = tf.train.RMSPropOptimizer(learning_rate=LEARNING_RATE).minimize(cost)


def RNN(inSeq, weights, biases):

	# reshapes to have the input feature matrix that we've already created in theory
	# # reshape to [1, INPUT_STATE_SIZE]
    # inSeq = tf.reshape(inSeq, [-1, INPUT_STATE_SIZE])

 #    # Generate a INPUT_STATE_SIZE-element sequence of inputs
    # inSeq = tf.split(inSeq,INPUT_STATE_SIZE,1)


    # 2-layer LSTM, each layer has INPUT_STATE_SIZE units.
    rnn_cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(INPUT_STATE_SIZE),rnn.BasicLSTMCell(INPUT_STATE_SIZE)])

    # 1-layer LSTM with INPUT_STATE_SIZE units but with lower accuracy.
    # Uncomment line below to test but comment out the 2-layer rnn.MultiRNNCell above
    # rnn_cell = rnn.BasicLSTMCell(INPUT_STATE_SIZE)

    # generate prediction
    outputs, states = rnn.static_rnn(rnn_cell, inSeq, dtype=tf.float32)

    # there are INPUT_STATE_SIZE outputs but
    # we only want the last output??????????????????????????? this is from tutorial .. idk why
    return tf.matmul(outputs[-1], weights['out']) + biases['out']


def modelEvaluators(pred):
	# Model evaluation
	correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(labels,1))
	accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
	return correct_pred, accuracy


def runSession():



# Arguments: 
# 			1. featureMatrix - each timestemp is featurized data aggregated within timeblocks
# 			2. Categorical labels from bitcoin price data
def rnnMain(featureMatrix, labels):
	inSeq, labels, weights, biases = initPlaceholders()
	pred = RNN(inSeq, weights, biases)

	cost, optimizer = initLossOptimizer(pred, labels)
	correct_pred, accuracy = modelEvaluators(pred);
	
	# Initializing the variables
	init = tf.global_variables_initializer()


	

	












