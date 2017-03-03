import pandas as pd
import numpy as np
import tensorflow as tf

xy = np.loadtxt('test3.data', dtype='float32', skiprows=0, unpack=True)

test = np.loadtxt('test.data', dtype='float32', unpack=True)
test = np.transpose(test)

x_data = xy.T[0:,0:2]
y_data = xy.T[0:,2:3]

x_data = x_data/x_data.max()
y_data = y_data/y_data.max()
test = test/test.max()

#Xavier Initialization
def xavier_init(n_inputs, n_outputs, uniform=True):
        if uniform:
                init_range = tf.sqrt(6.0 / (n_inputs + n_outputs))
                return tf.random_uniform_initializer(-init_range, init_range)
        else:
                stddev = tf.sqrt(3.0 / (n_inputs + n_outputs))
                return tf.truncated_normal_initializer(stddev=stddev)

print('normalized x_data:\n',x_data)

X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)
"""
#Weight Xavier
W1 = tf.get_variable("W1", shape=[2,3000], initializer=xavier_init(2,3000))
W2 = tf.get_variable("W2", shape=[3000,1], initializer=xavier_init(3000,1))
"""
W1 = tf.Variable(tf.random_uniform( [2,3000], -1.0, 1.0))
#W2 = tf.Variable(tf.random_uniform( [3000,500], -1.0, 1.0))
W2 = tf.Variable(tf.random_uniform( [3000,1], -1.0, 1.0))
W3 = tf.Variable(tf.random_uniform( [500,1], -1.0, 1.0))

b1 = tf.Variable(tf.zeros([3000]), name="bias1")


z1 = ( tf.sigmoid(tf.matmul(X,W1) + b1))
#z2 = ( tf.sigmoid( tf.matmul(z1,W2) ))
#hypothesis = ( ( tf.matmul(z2,W3) ))
hypothesis = tf.matmul(z1,W2)

cost = tf.reduce_mean(tf.square(hypothesis-Y))

a = tf.Variable(0.001)
optimizer = tf.train.GradientDescentOptimizer(a)
train = optimizer.minimize(cost)

init = tf.initialize_all_variables()

with tf.Session() as sess:
        sess.run(init)
        batch_size = 50
        datapoint_size = len(y_data)

        for step in range(1000001):
                if datapoint_size == batch_size:
                  # Batch mode so select all points starting from index 0
                  batch_start_idx = 0
                elif datapoint_size < batch_size:
                  # Not possible
                  raise ValueError("datapoint_size: %d, must be greater than batch_size: %d" % (datapoint_size, batch_size))
                else:
                  # stochastic/mini-batch mode: Select datapoints in batches
                  #                             from all possible datapoints
                  batch_start_idx = (step * batch_size) % (datapoint_size - batch_size)
                  batch_end_idx = batch_start_idx + batch_size
                  batch_xs = x_data[batch_start_idx:batch_end_idx]
                  batch_ys = y_data[batch_start_idx:batch_end_idx]

                sess.run(train, feed_dict = {X:batch_xs, Y:batch_ys})


                if step%100 == 0:
                        print(
                                step,
                                sess.run(cost, feed_dict={X:x_data, Y:y_data}),
                                sess.run(W1),
                                sess.run(W2)
                        )
#       print(  sess.run(hypothesis*256, feed_dict = {X:x_data[0:100,0:]}))
        print(  sess.run(hypothesis*256, feed_dict = {X:test[0:,0:]}))
