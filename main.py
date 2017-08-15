# -*- coding: utf-8 -*-

#from webcam import getBoardState
from node import Node
from omokboard import Board
import mcts
import copy
import random
'''
board = ob.getEmptyBoard(15)

ob.putStoneOnBoard(board, 7, 7, 'B')
ob.putStoneOnBoard(board, 8, 8, 'B')
ob.putStoneOnBoard(board, 6, 6, 'B')
ob.putStoneOnBoard(board, 5, 5, 'B')
#ob.putStoneOnBoard(board, 4, 4, 'W')
#ob.putStoneOnBoard(board, 7, 6, 'W')
#ob.putStoneOnBoard(board, 9, 9, 'W')
#ob.putStoneOnBoard(board, 6, 5, 'W')
#ob.putStoneOnBoard(board, 6, 8, 'B')
#ob.putStoneOnBoard(board, 5, 4, 'W')

print(winCheck(board, 4, 4, 'B'))


newnode = Node(board, [5, 4], 'W')
newnode.printNodeInfo()


temp = copy.deepcopy(newnode.prob_distrib)
temp.sort(reverse=True)
for i in range(10):
    coord_x = int(newnode.prob_distrib.index(temp[i]) % 15)
    coord_y = int(newnode.prob_distrib.index(temp[i]) / 15)
    row = 14 - coord_y
    column = coord_x

    ob.putStoneOnBoard(board, row, column, 'B')

ob.drawCurrentBoard(board)
'''




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


    root = Node(gameBoard.board, [my_action_row, my_action_col], 'B')
    root.visits = 1
    #root.printNodeInfo()
    #rest = input()
    nextmove = None
    if root.actionsLength >= 222:
        # 1~2 번째 수를 둬야할 경우
        nextmove = mcts.getEarlyStageAction(root.board, root.currentAction)
    else:
        # defence check
        random_actions = copy.deepcopy(root.nextActions)
        radnom_actions = random.shuffle(random_actions)
        for action in random_actions:
            if gameBoard.winCheck(action[0], action[1], root.opponent) == root.opponent:
                nextmove = action
                break

            if gameBoard.winCheck(action[0], action[1], root.currentPlayer) == root.currentPlayer:
                nextmove = action
                break

            if gameBoard.defenseCheck(action[0], action[1], root.currentPlayer) == True:
                nextmove = action
                break

    # if there is no place to defence, choose the best actions
    while True:
        if nextmove == None:
            nextmove = mcts.getBestAction(root, 10)

        # 여기서 블루투스로 다음 수 전송
        # 전송한 후 수 착수 후 기계 원상태로 돌아 온 뒤 아두이노에서 신호 보냄
        # 신호 받고나서 다음으로 진행
        # 신호 받는게 안되니 그냥 키입력 대기했다가 끝나는거 보고 키 눌러서 진행

        if gameBoard.putStoneOnBoard(nextmove[0], nextmove[1], 'W') == False:
            continue
        else:
            break

    if gameBoard.winCheck(nextmove[0], nextmove[1], 'W') == 'W':
        print(" YOU LOSE ")
        break
