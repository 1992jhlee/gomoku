# -*- coding: utf-8 -*-


import os
import tensorflow as tf
#import cnn
from omokboard import Board


class Node(Board):

    def __init__(self, board, current_action, BorW):
        self.children = []
        self.parent = None

        self.wins = 0
        self.visits = 0
        self.ubtValue = 0

        self.currentAction = current_action # [row, column]
        self.currentPlayer = BorW
        self.opponent = self.getOpponentPlayer(BorW)

        self.board = Board(15, board)
        self.nextActions, self.actionsLength = self.getNextActions()
        #self.prob_distrib = self.getProbabilityDistribution(board)
        self.gameFinished = self.isTerminal()
        #self.winner =


    def getNextActions(self):
        '''get positions that can be placed'''
        nextActions = []
        actionsLength = 0
        for row in range(self.board.size):
            for column in range(self.board.size):
                if self.board.isEmpty(row, column) == True and \
                    self.board.check33_violation(row, column, self.currentPlayer) == False:
                    nextActions.append([row, column])
                    actionsLength += 1

        return nextActions, actionsLength


    def getProbabilityDistribution(self, board):
        with tf.Session() as sess:
            m = cnn.Model(sess, "m")
            saver = tf.train.Saver()
            saver.restore(sess, str(os.getcwd()) +                                  "\\training_8_20170801\\trained_model_at_epoch60.ckpt")
            input_feature = ob.boardToInputFeature(board)
            prob_distrib = m.prediction(input_feature)

        return prob_distrib


    def isTerminal(self):
        if self.board.findWinner() != None:
            return True
        else:
            return False


    def printNodeInfo(self):
        print("\n\n")
        print("children : ", self.children)
        print("parent : ", self.parent)
        print("wins : ", self.wins)
        print("visits : ", self.visits)
        print("ubtValue : ", self.ubtValue)
        print("currentplayer : ", self.currentPlayer)
        print("current action : ", self.currentAction)
        print("board state : \n")
        self.board.drawCurrentBoard()
        print("nextActions : \n", self.nextActions)
        print("actionsLength : ", self.actionsLength)
        #print("probability distribution : \n", self.prob_distrib)

        return
