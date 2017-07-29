# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
import pickle
import os

print("loading data files...")
with open('training_inputs.txt', 'rb') as f:
    training_inputs = pickle.load(f)
with open('training_labels.txt', 'rb') as f:
    training_labels = pickle.load(f)
with open('validation_inputs.txt', 'rb') as f:
    validation_inputs = pickle.load(f)
with open('validation_labels.txt', 'rb') as f:
    validation_inputs = pickle.load(f)
with open('test_inputs.txt', 'rb') as f:
    test_inputs = pickle.load(f)
with open('test_labels.txt', 'rb') as f:
    test_labels = pickle.load(f)
print("loading data files...finished")

print("len(training_inputs) = ", len(training_inputs))
print("len(test_inputs) = ", len(test_inputs))
####
batch_size = 128

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

### 1*1 kernal instead of the FC layers
#W5 = tf.Variable(tf.random_normal([1, 1, 256, 1], stddev=0.1))
#L5 = tf.nn.conv2d(L4, W5, strides=[1, 1, 1, 1], padding='SAME')
#L5 = tf.nn.relu(L5) # output shape = (1, 15, 15 ,1)
#L5 = tf.reshape(L5, [-1, 15 * 15 * 1]) # output shape = (1, 225)

#H = tf.nn.softmax(L5) # output shape = (1, 225)



# define cost and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)


# Add ops to save and restore all the variables.
saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    tf.train.start_queue_runners(sess)

    training_epochs = 30
    print("start training..\n")
    f = open("training_log.txt", "w")
    for epoch in range(training_epochs):
        avg_cost = 0
        total_batch = int(len(training_inputs) / batch_size)
        for batch in range(total_batch):
            # get mini batch
            batch_mask = np.random.choice(len(training_inputs), batch_size)
            random_features = [training_inputs[k] for k in batch_mask]
            random_labels = [training_labels[k] for k in batch_mask]
            batch_inputs = np.zeros([batch_size, 15, 15, 3], dtype=np.float32)
            batch_labels = np.zeros([batch_size, 225], dtype=np.float32)
            for i in range(batch_size):
                batch_inputs[i] = random_features[i]
                batch_labels[i] = random_labels[i]

            input_dict = {X : batch_inputs, Y : batch_labels}
            # training
            c, _ = sess.run([cost, optimizer], feed_dict = input_dict)
            avg_cost += c / total_batch

        print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.9f}'.format(avg_cost), file=f)
        print('Epoch:', '%04d' % (epoch + 1), 'cost =', '{:.9f}'.format(avg_cost))
        if epoch % 10 == 0:
            save_path = saver.save(sess, str(os.getcwd()) + "//trained_model//trained_model_at_epoch" + str(epoch) + ".ckpt")
            print("Model saved in file: %s" % save_path)

    # save completely trained model
    save_path = saver.save(sess, str(os.getcwd()) + "//trained_model//trained_model.ckpt")
    print("Model saved in file: %s" % save_path)

    f.close()
    print('training finished!')


try:
    # Test model and check accuracy
    print('Testing model...')
    f = open("testing_log.txt", "w")
    correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    print('Accuracy:', sess.run(accuracy, feed_dict={X:test_inputs, Y:test_labels}), file=f)
    print('Accuracy:', sess.run(accuracy, feed_dict={X:test_inputs, Y:test_labels}))
    f.close()
    print('Testing model...finished')
except Exception as e:
    print(e)
    print(type(e))
