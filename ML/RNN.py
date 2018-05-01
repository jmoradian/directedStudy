import tensorflow as tf, numpy as np, collections, sys, csv
from tensorflow.contrib import rnn
from math import sqrt
# need to restructure everything
# 		- change labels to onehot vector (1 == pos change) 
# 		- input needs to be series of size [featurelength X desired length of sequence]

class RNN(object):
	def __init__(self, learning_rate, state_dimension, input_size, output_size, hidden_state_size):
		tf.reset_default_graph()
		self.learning_rate = learning_rate
		self.state_dimension = state_dimension
		self.input_size = input_size
		self.output_size = output_size
		self.hidden_state_size = hidden_state_size
		self.batch_size = 1

		# tf Graph input
		self.inSeq = tf.placeholder("float", [None, self.input_size, self.state_dimension], name = "inp_seq")
		# should rename input_size to sequence size
		# self.labels = tf.placeholder("float", [None, self.output_size], name = "labels")
		self.labels = tf.placeholder("float", [None, self.input_size, self.output_size], name = "labels")

		# RNN output node weights and biases
		self.weights = {'out': tf.Variable(tf.random_normal([self.hidden_state_size, self.output_size]), name = "W")}
		self.biases = {'out': tf.Variable(tf.random_normal([self.output_size]), name = "b")}
		tf.summary.histogram('weights', self.weights['out'])
  		tf.summary.histogram('biases', self.biases['out'])
		print "##########################"

		self.pred = self.rnn(self.inSeq, self.weights, self.biases, name = "rnn")
		# self.pred = self.rnnScratch(self.inSeq, self.labels, self.weights, self.biases, name = "rnn")

		# Loss and optimizer (change to categorical cross_entropy) - UPDATE: this is a discrete loss function
		# self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.pred, labels=self.labels))
		with tf.name_scope("loss"):
			# self.loss = tf.reduce_mean(self.pred[1])
			self.loss = tf.reduce_mean(tf.losses.mean_squared_error(predictions=self.pred, labels=self.labels))
		with tf.name_scope("train"):
			self.optimizer = tf.train.RMSPropOptimizer(learning_rate=self.learning_rate).minimize(self.loss)
		print "optimizer initialized"

		# Model Evaluation
		# self.correct_pred = tf.equal(tf.argmax(self.pred,1), tf.argmax(self.labels,1))
		self.accuracy =  self.loss
		# self.accuracy = tf.metrics.mean_squared_error(labels = self.labels, predictions = self.pred)
		print "#########################"

		# Initializing the variables
		self.init = tf.global_variables_initializer()
		print "variables initialized"
		self.step_size = self.input_size
		# Save trained model
		self.saver = tf.train.Saver()
		
  		#summaries
  		tf.summary.scalar('loss', self.loss)
  		


  		#log path
		self.logs_path = '/tmp/tensorflow/rnn_graph'
		# Merge all summary inforation.
		self.merged_summary = tf.summary.merge_all()
		self.writer = tf.summary.FileWriter(self.logs_path)

		print "writer initialzed"

	def rnn(self, inSeq, weights, biases, name = "rnn"):
		with tf.name_scope(name):
			# reshapes to have the input feature matrix that we've already created in theory
			# reshape to [1, INPUT_STATE_SIZE]
			inSeq = tf.reshape(inSeq, [-1, self.state_dimension * self.input_size])
			# Generate a INPUT_STATE_SIZE-element sequence of inputs
			inSeq = tf.split(inSeq,self.input_size,1)

			# 2-layer LSTM, each layer has INPUT_STATE_SIZE units.
			# rnn_cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(self.hidden_state_size),rnn.BasicLSTMCell(self.hidden_state_size)])

			# 1-layer LSTM with INPUT_STATE_SIZE units  fasterbut with lower accuracy.
			# Uncomment line below to test but comment out the 2-layer rnn.MultiRNNCell above
			rnn_cell = rnn.BasicLSTMCell(self.hidden_state_size)

			# generate prediction
			outputs, states = rnn.static_rnn(rnn_cell, inSeq, dtype=tf.float32)
			# print outputs[-1].get_shape()
			# output rn is of size of feature vector because its not unraveling the input sequence
			# return tf.matmul(outputs[-1], weights['out']) + biases['out']
			predictions = [tf.matmul(output, weights['out']) + biases['out']  for output in outputs]
			return predictions


	def rnnScratch(self, inSeq, weights, biases, name = "lstm"):
		# tf.reset_default_graph()
		with tf.name_scope(name):
			# reshapes to have the input feature matrix that we've already created in theory
			# reshape to [1, INPUT_STATE_SIZE]
			inSeq = tf.reshape(inSeq, [-1, self.input_size])
			labels = tf.reshape(labels, [-1, self.input_size])
			# Generate a INPUT_STATE_SIZE-element sequence of inputs
			inSeq = tf.split(inSeq,self.input_size,1)
			labels = tf.split(labels,self.input_size,1)
			lstmCell = rnn.LSTMCell(self.hidden_state_size)
			hidden_state = tf.zeros([self.batch_size, self.hidden_state_size])
			curr_state = tf.zeros([self.batch_size, self.hidden_state_size])
			# hidden_state = tf.zeros([self.batch_size, lstm.state_size])
			# curr_state = tf.zeros([self.batch_size, lstm.state_size])
			state = hidden_state, curr_state
			loss = 0.
			predictions = []
			for featVec, label in zip(inSeq, labels):
				output, state = lstmCell(featVec, state)

				prediction = tf.matmul(output, self.weights['out']) + self.biases['out']
				predictions.append(prediction)
			loss /= self.input_size

			return predictions


	def dynamicRnn(self, inSeq, weights, biases, name = "drnn"):
		with tf.name_scope(name):

			lstm_cell = tf.contrib.rnn.LSTMCell(num_units=self.state_dimension)
			outputs, state = tf.nn.dynamic_rnn(cell=lstm_cell, dtype=tf.float32, inputs=inSeq)

			# generate prediction
			print tf.shape(tf.matmul(outputs, weights['out']))
			return tf.matmul(outputs[-1], weights['out']) + biases['out']

	def restoreSession(self, sess):
		print "Enter step to restore: "
		step = sys.stdin.readline()
		restore_path = "model/saved_model_"+step+".ckpt"
		meta_path = "model/saved_model_"+step+".ckpt.meta"
		saver = tf.train.import_meta_graph(meta_path)
		ckpt = tf.train.get_checkpoint_state(restore_path)
		if ckpt and ckpt.model_checkpoint_path:
			self.saver.restore(sess, ckpt.model_checkpoint_path)
			print "Succesfully restored model"

	def trainStep(self, step, sess, trainingData, labels):
		batchData = trainingData[step:step + self.step_size]
		batchLabels = labels[step:step + self.step_size] #will probably have to reshape
		# batchLabels = [labels[step + self.step_size]]
		# specific for just bitcoin data
		batchData = np.reshape(batchData, (1, self.input_size, self.state_dimension))
		batchLabels = np.reshape(batchLabels, (1, self.input_size, self.output_size))
		return sess.run([self.optimizer, self.accuracy, self.loss, self.pred], \
								feed_dict={self.inSeq: batchData, self.labels: batchLabels})

	def validationStep(self, step, sess, trainingData, labels):
		batchData = trainingData[step:step + self.step_size]
		batchLabels = labels[step:step + self.step_size] #will probably have to reshape
		# batchLabels = [labels[step + self.step_size]]
		# specific for just bitcoin data
		batchData = np.reshape(batchData, (1, self.input_size, self.state_dimension))
		batchLabels = np.reshape(batchLabels, (1, self.input_size, self.output_size))
		return sess.run([self.merged_summary, self.loss], feed_dict={self.inSeq: batchData, self.labels: batchLabels})

	def runnSess(self, trainingData, labels):
		with tf.Session() as sess:
			sess.run(self.init)

			# Conditionally restore model weights ---- this does not work
			# if raw_input("Restore training session (y/n)   ") == 'y':
			# 	self.restoreSession(sess)

			self.writer.add_graph(sess.graph)
			acc_total, loss_total, step, iter_ = 0, 0, 0, 1
			
			while step < min(len(trainingData), len(labels)) - self.step_size:
				if iter_ % 20 == 0:
					summ, val_loss = self.validationStep(step, sess, trainingData, labels)
					self.writer.add_summary(summ, iter_)
					print "Validation loss at timestep " + str(step) + " is " + str(val_loss), "last batchPred:", batchPred[-1], "labels:", labels[step + self.step_size]
					acc_total, loss_total, iter_ = 0, 0, 0
				_, acc, loss, batchPred = self.trainStep(step, sess, trainingData, labels)
				# print self.biases['out'].eval()
				loss_total += loss
				acc_total += acc

				step += self.step_size//8
				iter_ += 1		

			return loss_total/float(iter_)	





