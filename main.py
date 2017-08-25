# -*- coding: utf-8 -*-

#from webcam import getBoardState
from node import Node
from omokboard import Board
from omokboard import getFavorablePosition
import mcts
import copy
import random
import tensorflow as tf
import os
from cnn import Model

with tf.Session() as sess:
    m = Model(sess, "my_model")
    saver = tf.train.Saver()
    saver.restore(sess, str(os.getcwd()) +                                  "\\training_9_20170811\\trained_model_at_epoch100.ckpt")

    gameBoard = Board(15, "EMPTY")
    while True:
        gameBoard.drawCurrentBoard()

        while True:
            my_action_row = int(input("row = "))
            my_action_col = int(input("column = "))
            if gameBoard.putStoneOnBoard(my_action_row, my_action_col, 'B') == False:
                continue

            gameBoard.drawCurrentBoard()
            if gameBoard.winCheck(my_action_row, my_action_col, 'B') == 'B':
                print(" YOU WIN ! ")
                break
            else:
                break


        root = Node(gameBoard.board, [my_action_row, my_action_col], 'B', m)
        root.visits = 1
        #root.printNodeInfo()
        #rest = input()
        nextmove = None
        if root.nstone <= 2: # 원래 222
            # 1~2 번째 수를 둬야할 경우
            nextmove = mcts.getEarlyStageAction(root.board, root.currentAction)
        else:
            # defence check
            random_actions = copy.deepcopy(root.nextActions)
            radnom_actions = random.shuffle(random_actions)
            oppos_winning_pos = []
            for action in random_actions:
                if gameBoard.winCheck(action[0], action[1], root.opponent) == root.opponent:
                    nextmove = action
                    break

                if gameBoard.winCheck(action[0], action[1], root.currentPlayer) == root.currentPlayer:
                    oppos_winning_pos.append(action)

            if nextmove == None:
                if len(oppos_winning_pos) > 0:
                    defense_pos_1 = getFavorablePosition(root.board, oppos_winning_pos, root.currentPlayer)
                    defense_pos_2 = getFavorablePosition(root.board, oppos_winning_pos, root.opponent)
                    defense_pos_1_cnt = root.board.cntStonesForFavPos(defense_pos_1[0], defense_pos_2[1], root.currentPlayer)
                    defense_pos_2_cnt = root.board.cntStonesForFavPos(defense_pos_2[0], defense_pos_2[1], root.opponent)
                    if defense_pos_1_cnt >= defense_pos_2_cnt:
                        print("opponent's winning position selected : ", defense_pos_1)
                        nextmove = defense_pos_1
                    elif defense_pos_2_cnt > defense_pos_1_cnt:
                        print("opponent's winninge position selected : ", defense_pos_2)
                        nextmove = defense_pos_2

            if nextmove = None:
                nextmove_candidates = []
                for action in random_actions:
                    # defence check
                    if root.board.defenseCheck(action[0], action[1], root.opponent) == True:
                        nextmove_candidates.append(action)

                if len(nextmove_candidates) > 0:
                    nextmove_1 = getFavorablePosition(root.board, nextmove_candidates, root.currentPlayer)
                    nextmove_2 = getFavorablePosition(root.board, nextmove_candidates, root.opponent)
                    nextmove_1_cnt = root.board.cntStonesForFavPos(nextmove_1[0], nextmove_1[1], root.currentPlayer)
                    nextmove_2_cnt = root.board.cntStonesForFavPos(nextmove_2[0], nextmove_2[1], root.opponent)
                    if nextmove_1_cnt >= nextmove_2_cnt:
                        print("defence position selected : ", nextmove_1)
                        nextmove = nextmove_1
                    elif nextmove_2_cnt > nextmove_1_cnt:
                        print("defence position selected : ", nextmove_2)
                        nextmove = nextmove_2

        # if there is no place to defence, choose the best actions
        while True:
            if nextmove == None:
                nextmove = mcts.getBestAction(root, 30)

            # 여기서 블루투스로 다음 수 전송
            # 전송한 후 수 착수 후 기계 원상태로 돌아 온 뒤 아두이노에서 신호 보냄
            # 신호 받고나서 다음으로 진행
            # 신호 받는게 안되니 그냥 키입력 대기했다가 끝나는거 보고 키 눌러서 진행

            elif gameBoard.putStoneOnBoard(nextmove[0], nextmove[1], 'W') == False:
                continue
            else:
                break

        if gameBoard.winCheck(nextmove[0], nextmove[1], 'W') == 'W':
            print(" YOU LOSE ")
            break
