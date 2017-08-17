# -*- coding: utf-8 -*-


import os
import tensorflow as tf
import cnn
from omokboard import Board


class Node(Board):

    def __init__(self, board, current_action, BorW, model=None):
        self.children = []
        self.parent = None

        self.wins = 0
        self.visits = 0
        self.ubtValue = 0

        self.currentAction = current_action # [row, column]
        self.currentPlayer = BorW
        self.opponent = self.getOpponentPlayer(BorW)

        self.board = Board(15, board)
        self.nstone = self.board.getNumberOfStones()
        self.nextActions, self.actionsLength = self.getNextActions()
        self.input_feature = self.board.boardToInputFeature()

        if model != None:
            self.prob_distrib = model.prediction(self.input_feature)
            self.promisingActions = self.getPromisingActions()

        self.gameFinished = self.isTerminal()
        #self.winner =


    def getNextActions(self):
        '''get positions that can be placed'''
        nextActions = []
        actionsLength = 0

        row_lower_limit, row_upper_limit, col_lower_limit, col_upper_limit = self.board.getLimit()
        row_lower_limit = max(row_lower_limit-2, 0)
        row_upper_limit = min(row_upper_limit+2, 14)
        col_lower_limit = max(col_lower_limit-2, 0)
        col_upper_limit = min(col_lower_limit+2, 14)

        for row in range(row_lower_limit, row_upper_limit+1):
            for column in range(col_lower_limit, col_upper_limit+1):
                if self.board.isEmpty(row, column) == True and \
                    self.board.check33_violation(row, column, self.currentPlayer) == False:
                    actionsLength += 1
                    nextActions.append([row, column])

        return nextActions, actionsLength


    def getPromisingActions(self, howMany=7):
        promisingActions = []

        probs_sorted = sorted(self.prob_distrib, reverse=True)
        for i in range(howMany):
            bestIdx = self.prob_distrib.index(probs_sorted[i])
            coord_x = int(bestIdx % 15)
            coord_y = int(bestIdx / 15)
            row = 14 - coord_y
            column = coord_x
            promisingActions.append([row, column])

        return promisingActions


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
        print("nstone : ", self.nstone)
        print("probability distribution : \n", self.prob_distrib)
        print("promisingActions : \n", self.promisingActions)




if __name__ == "__main__":

    with tf.Session() as sess:
        m = cnn.Model(sess, "my_model")
        saver = tf.train.Saver()
        saver.restore(sess, str(os.getcwd()) +                                  "\\training_9_20170811\\trained_model_at_epoch100.ckpt")

        b = Board(15, "EMPTY")

        b.putStoneOnBoard(7, 7, 'B')
        # b.putStoneOnBoard(7, 8, 'W')
        # b.putStoneOnBoard(6, 7, 'B')
        # b.putStoneOnBoard(8, 7, 'W')
        # b.putStoneOnBoard(8, 6, 'B')
        # b.putStoneOnBoard(9, 6, 'W')
        # b.putStoneOnBoard(6, 9, 'B')
        # b.drawCurrentBoard()

        print("rollout start")
        node = Node(b.board, [7, 7], 'B', m)
        node.board.drawCurrentBoard()
        while True:

            for action in node.promisingActions:
                if node.board.putStoneOnBoard(action[0], action[1], node.opponent) != False:
                    break

            node = Node(node.board.board, node.promisingActions[0], node.opponent, m)
            node.board.drawCurrentBoard()

            key = input()




# b = Board(15, "EMPTY")
#
# b.putStoneOnBoard(7, 7, 'B')
# b.putStoneOnBoard(6, 8, 'W')
# b.putStoneOnBoard(6, 6, 'B')
# b.putStoneOnBoard(7, 9, 'W')
# b.putStoneOnBoard(8, 8, 'B')
# # b.putStoneOnBoard(6, 9, 'B')
# # b.putStoneOnBoard(7, 8, 'W')
#
# node = Node(b.board, [8, 8], 'B')
# node.printNodeInfo()
