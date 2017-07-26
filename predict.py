# -*- coding: utf-8 -*-

import tensorflow as tf

with open('training_inputs.txt', 'rb') as f:
    training_inputs = pickle.load(f)

def getCandidates(input_board):
    # ConvNet
    X = tf.placeholder(tf.float32, [15, 15, 3])
    # X = tf.placeholder(tf.float32, [15, 15, 3])
    # X_reshape = tf.reshape(X, [-1, 15, 15, 3])
    Y = tf.placeholder(tf.float32, [225])
    # Y = tf.placeholder(tf.float32, [1, 225])

    W1 = tf.Variable(name="W1")
    L1 = tf.nn.conv2d(X, W1, strides=[1, 1, 1, 1], padding='SAME')
    L1 = tf.nn.relu(L1) # output shape = (1, 15, 15, 128)

    W2 = tf.Variable(name="W2")
    L2 = tf.nn.conv2d(L1, W2, strides=[1, 1, 1, 1], padding='SAME')
    L2 = tf.nn.relu(L2) # output shape = (1, 15, 15, 128)

    W3 = tf.Variable(name="W3")
    L3 = tf.nn.conv2d(L2, W3, strides=[1, 1, 1, 1], padding='SAME')
    L3 = tf.nn.relu(L3) # output shape = (1, 15, 15, 128)

    W4 = tf.Variable(name="W4")
    L4 = tf.nn.conv2d(L3, W4, strides=[1, 1, 1, 1], padding='SAME')
    L4 = tf.nn.relu(L4) # output shape = (1, 15, 15, 128)
    L4_flat = tf.reshape(L4, [-1, 15*15*128])

    # FCNN
    W5 = tf.get_variable("W5", shape=[15*15*128, 225],
                        initializer=tf.contrib.layers.xavier_initializer())
    b = tf.Variable(tf.random_normal([225]))
    logits = tf.matmul(L4_flat, W5) + b

    ### 1*1 kernal instead of the FC layers
    #W5 = tf.Variable(tf.random_normal([1, 1, 256, 1], stddev=0.1))
    #L5 = tf.nn.conv2d(L4, W5, strides=[1, 1, 1, 1], padding='SAME')
    #L5 = tf.nn.relu(L5) # output shape = (1, 15, 15 ,1)
    #L5 = tf.reshape(L5, [-1, 15 * 15 * 1]) # output shape = (1, 225)

    #H = tf.nn.softmax(L5) # output shape = (1, 225)

    saver = tf.train.Saver()

    with tf.Session() as sess:
        saver.restore(sess, "/trained_model/trained_model.ckpt")
        print("Model Restored")
        result = sess.run(logits, feed_dict={X:input_board})

    return result

candidates = getCandidates(training_inputs[100])
print(candidates)
