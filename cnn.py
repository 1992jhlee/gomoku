# -*- coding: utf-8 -*-


import tensorflow as tf
import numpy as np
import omokboard as ob
import os
import copy
import mcts

class Model:

    def __init__(self, sess, name):
        self.sess = sess
        self.name = name
        self._build_net()

    def _build_net(self):
        #with tf.variable_scope(self.name):
        # ConvNet
        self.X = tf.placeholder(tf.float32, [15, 15, 3])
        X_reshape = tf.reshape(self.X, [-1, 15, 15, 3])

        W1 = tf.Variable(tf.random_normal([7, 7, 3, 256], stddev=0.1), name="W1")
        L1 = tf.nn.conv2d(X_reshape, W1, strides=[1, 1, 1, 1], padding='SAME')
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

        # FCNN
        W5 = tf.get_variable("W5", shape=[15*15*256, 225],
                            initializer=tf.contrib.layers.xavier_initializer())
        b = tf.Variable(tf.random_normal([225]))
        logits = tf.matmul(L4_flat, W5) + b
        self.predict = tf.nn.softmax(logits)




    def prediction(self, input_feature):
        result = self.sess.run(self.predict, feed_dict={self.X:input_feature})
        prob_distrib = self.getProbDistrib(result)
        return prob_distrib


    def getProbDistrib(self, input_softmax):
        #candidates = []
        prob_distrib = list(input_softmax[0])
        #temp = copy.deepcopy(input_as_list)
        #temp.sort(reverse=True)
        #for i in range(howMany):
            #coord_x = int(input_as_list.index(temp[i]) % 15)
            #coord_y = int(input_as_list.index(temp[i]) / 15)
            # coord_x -> column, 14 - coord_y -> row
            #row = 14 - coord_y
            #column = coord_x

            #bigGuys.append([row, column])

        return prob_distrib









'''
with tf.Session() as sess:
    m1 = Model(sess, "m1")

    saver = tf.train.Saver()
    saver.restore(sess, str(os.getcwd()) + "\\training_8_20170801\\trained_model_at_epoch60.ckpt")
    print("Model Restored")

    print("start game")

    board = ob.getEmptyBoard(15)
    while True:
        #os.sys('CLS')
        ob.drawCurrentBoard(board)

        while True:
            my_action_row = int(input("row = "))
            my_action_col = int(input("column = "))
            if ob.putStoneOnBoard(board, my_action_row, my_action_col, 'B') == False:
                continue
            #os.sys('CLS')
            ob.drawCurrentBoard(board)
            if mcts.winCheck(board, my_action_row, my_action_col, 'B') == 'B':
                print(" YOU WIN ! ")
                break
            else:
                break

        input_feature = ob.boardToInputFeature(board)
        candidates = m1.prediction(input_feature)

        for i in range(len(candidates)):
            if ob.putStoneOnBoard(board, candidates[i][0], candidates[i][1], 'W') == False:
                continue
            else:
                break

        if mcts.winCheck(board, candidates[0][0], candidates[0][1], 'W') == 'W':
            print(" YOU LOSE ")
            break
'''
