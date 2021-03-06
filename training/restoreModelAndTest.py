# -*- coding: utf-8 -*-

import tensorflow as tf
import pickle
import os

print("loading testing files...")
with open('test_inputs.txt', 'rb') as f:
    test_inputs = pickle.load(f)
with open('test_labels.txt', 'rb') as f:
    test_labels = pickle.load(f)
print("loading testing files...finished")

total_batch_inputs = [test_inputs[i:i+1000] for i in range(0, len(test_inputs), 1000)]
total_batch_labels = [test_labels[i:i+1000] for i in range(0, len(test_labels), 1000)]

print("len(total_batch_inputs) = ", len(total_batch_inputs))

# ConvNet
X = tf.placeholder(tf.float32, [None, 15, 15, 3])
# X = tf.placeholder(tf.float32, [15, 15, 3])
# X_reshape = tf.reshape(X, [-1, 15, 15, 3])
Y = tf.placeholder(tf.float32, [None, 225])
# Y = tf.placeholder(tf.float32, [1, 225])

W1 = tf.Variable(tf.random_normal([7, 7, 3, 256], stddev=0.1), name="W1")
L1 = tf.nn.conv2d(X, W1, strides=[1, 1, 1, 1], padding='SAME')
L1 = tf.nn.relu(L1) # output shape = (1, 15, 15, 128)

W2 = tf.Variable(tf.random_normal([5, 5, 256, 256], stddev=0.1), name="W2")
L2 = tf.nn.conv2d(L1, W2, strides=[1, 1, 1, 1], padding='SAME')
L2 = tf.nn.relu(L2) # output shape = (1, 15, 15, 128)

W3 = tf.Variable(tf.random_normal([3, 3, 256, 256], stddev=0.1), name="W3")
L3 = tf.nn.conv2d(L2, W3, strides=[1, 1, 1, 1], padding='SAME')
L3 = tf.nn.relu(L3) # output shape = (1, 15, 15, 128)

W4 = tf.Variable(tf.random_normal([3, 3, 256, 256], stddev=0.1), name="W4")
L4 = tf.nn.conv2d(L3, W4, strides=[1, 1, 1, 1], padding='SAME')
L4 = tf.nn.relu(L4) # output shape = (1, 15, 15, 128)
L4_flat = tf.reshape(L4, [-1, 15*15*256])
#W5 = tf.Variable(tf.random_normal([3, 3, 128, 128], stddev=0.1), name="W5")
#L5 = tf.nn.conv2d(L4, W5, strides=[1, 1, 1, 1], padding='SAME')
#L5 = tf.nn.relu(L5) # output shape = (1, 15, 15, 128)
#L5_flat = tf.reshape(L5, [-1, 15*15*128])

# FCNN
W5 = tf.get_variable("W5", shape=[15*15*256, 225],
                    initializer=tf.contrib.layers.xavier_initializer())
b = tf.Variable(tf.random_normal([225]))
logits = tf.matmul(L4_flat, W5) + b


print("logits.shape = ", logits.shape)
print("Y.shape = ", Y.shape)
#config = tf.ConfigProto()
#config.gpu_options.allow_growth = True


with tf.Session() as sess:
    saver = tf.train.Saver()
    saver.restore(sess, "../training_8_20170801/trained_model_at_epoch59.ckpt")
    print("Model Restored")

    with open("testing_log.txt", "w") as f:
        try:
            # Test model and check accuracy
            print('Testing model...')
            correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

            accuracy_list = []
            for k in range(len(total_batch_inputs)):
                result = sess.run(accuracy, \
                            feed_dict={X:total_batch_inputs[k], Y:total_batch_labels[k]})
                print(k, 'th Accuracy:', result, file=f)
                accuracy_list.append(result)

            print("MEAN = ", sess.run(tf.reduce_mean(accuracy_list)), file=f)
            print('Testing model...finished')
        except Exception as e:
            print(e, file=f)
            print(type(e), file=f)
