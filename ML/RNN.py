import tensorflow as tf, numpy as np, collections, sys, csv
from tensorflow.contrib import rnn

# need to restructure everything
# 		- change labels to onehot vector (1 == pos change) 
# 		- input needs to be series of size [featurelength X desired length of sequence]

class RNN(object):
	def __init__(self, learning_rate, state_dimension, input_size, output_size, hidden_state_size):
		#documentation
		self.logs_path = '/tmp/tensorflow/rnn_words'
		self.writer = tf.summary.FileWriter(self.logs_path)
		print "writer initialzed"
		self.learning_rate = learning_rate
		self.state_dimension = state_dimension
		self.input_size = input_size
		self.output_size = output_size
		self.hidden_state_size = hidden_state_size

		# tf Graph input
		self.inSeq = tf.placeholder("float", [None, self.input_size, self.state_dimension])
		self.labels = tf.placeholder("float", [None, self.output_size])

		# RNN output node weights and biases
		self.weights = {'out': tf.Variable(tf.random_normal([self.hidden_state_size, self.output_size]))}
		self.biases = {'out': tf.Variable(tf.random_normal([self.output_size]))}
		print "##########################"
		self.pred = self.rnn(self.inSeq, self.weights, self.biases)

		# Loss and optimizer (change to categorical cross_entropy) - UPDATE: this is a discrete loss function
		# self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.pred, labels=self.labels))
		self.loss = tf.reduce_mean(tf.losses.mean_squared_error(predictions=self.pred, labels=self.labels, weights = 1.0))
		self.optimizer = tf.train.RMSPropOptimizer(learning_rate=self.learning_rate).minimize(self.loss)
		print "optimizer initialized"

		# Model Evaluation
		# self.correct_pred = tf.equal(tf.argmax(self.pred,1), tf.argmax(self.labels,1))
		# self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))
		self.mse = tf.metrics.mean_squared_error(labels = self.labels, predictions = self.pred)
		print "#########################"

		# Initializing the variables
		self.init = tf.global_variables_initializer()
		print "variables initialized"
		self.step_size = 800
		# Save trained model
		self.saver = tf.train.Saver()

	def rnn(self, inSeq, weights, biases):
		print "length inseq: ", inSeq.get_shape()
		# reshapes to have the input feature matrix that we've already created in theory
		# reshape to [1, INPUT_STATE_SIZE]
		inSeq = tf.reshape(inSeq, [-1, self.input_size])
		print "length inseq after reshape: ", inSeq.get_shape()
		# Generate a INPUT_STATE_SIZE-element sequence of inputs
		inSeq = tf.split(inSeq,self.input_size,1)
		print "length inseq after split: ", len(inSeq), "length inseq elem: ", inSeq[0].get_shape()

		# 2-layer LSTM, each layer has INPUT_STATE_SIZE units.
		rnn_cell = rnn.MultiRNNCell([rnn.BasicLSTMCell(self.hidden_state_size),rnn.BasicLSTMCell(self.hidden_state_size)])

		# 1-layer LSTM with INPUT_STATE_SIZE units but with lower accuracy.
		# Uncomment line below to test but comment out the 2-layer rnn.MultiRNNCell above
		# rnn_cell = rnn.BasicLSTMCell(INPUT_STATE_SIZE)

		# generate prediction
		outputs, states = rnn.static_rnn(rnn_cell, inSeq, dtype=tf.float32)

		# there are INPUT_STATE_SIZE outputs but
		# we only want the last output??????????????????????????? this is from tutorial .. idk why
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

	def printCheckPoints(self, step, mse_total, loss_total, iter_):
		print "Start Index: ", step, "Average mse: ", mse_total/iter_, "Average loss: ", loss_total/iter_
		if iter_ % 20 == 0:
			mse_total, loss_total, iter_ = 0,0, 0
			print "Averages reset."

		# save_path = "model/saved_model_"+str(step)+".ckpt"
				# self.saver.save(sess, save_path)
				# print "Saved model to "+save_path

		return mse_total, loss_total, iter_

	def trainStep(self, step, sess, trainingData, labels):
		batchData = trainingData[step:step + self.step_size]
		batchLabels = [labels[step + self.step_size]] #will probably have to reshape
		# specific for just bitcoin data
		batchData = np.reshape(batchData, (1, self.input_size, 1))
		# batchLabels = [label for ind_, label in enumerate(batchLabels) if ind_ % 200 == 0 ]
		return sess.run([self.optimizer, self.mse, self.loss, self.pred], \
								feed_dict={self.inSeq: batchData, self.labels: batchLabels})

	def runnSess(self, trainingData, labels):
		with tf.Session() as sess:
			sess.run(self.init)

			# Conditionally restore model weights ---- this does not work
			# if raw_input("Restore training session (y/n)   ") == 'y':
			# 	self.restoreSession(sess)

			self.writer.add_graph(sess.graph)
			mse_total, loss_total, step, iter_ = 0, 0, 0, 1

			# for testing purposes
			batchPred = []
			while step < len(trainingData) - self.step_size:
				_, mse, loss, batchPred = self.trainStep(step, sess, trainingData, labels)

				loss_total += loss
				mse_total += mse
				
				mse_total, loss_total, iter_ = self.printCheckPoints(step, mse_total, loss_total, iter_)
				
				step += self.step_size//16
				iter_ += 1

				print "batchPred:", batchPred, "label: ", [labels[step + self.step_size]]
			





