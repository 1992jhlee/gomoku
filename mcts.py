# -*- coding: utf-8 -*-


import random
import math
import copy
import time
import os
import tensorflow as tf
#import cnn
from omokboard import Board
from node import Node

selection_counter = 0
expansion_counter = 0
backprop_counter = 0
rollout_counter = 0

def selection(current):

    global selection_counter
    selection_counter += 1
    print("selection started...", selection_counter)

    if current.gameFinished == True: # 게임이 끝났으면 None 반환
        return None

    while True: # 게임이 끝나거나 둘 곳이 없으면 작동 x

        if current.actionsLength > 0: # if not fully expanded
            newnode = expansion(current)
            print("newnode created")
            return newnode
        else:
            select = getBestChild(current)
            print("best node selected")
            break


    return select


def expansion(node):


    global expansion_counter
    expansion_counter += 1
    print("expansion started...", expansion_counter)


    while True:

        nextboard = copy.deepcopy(node.board)
        nextaction = rolloutPolicy(nextboard, node.nextActions, node.currentPlayer)
        #idx = random.randint(0, node.actionsLength-1)
        #nextaction = node.nextActions[idx]

        if nextboard.putStoneOnBoard(nextaction[0], nextaction[1], node.opponent) == False:
            continue

        newnode = Node(nextboard.board, nextaction, node.opponent)
        newnode.parent = node
        break

    # update parent node
    node.children.append(newnode)
    del(node.nextActions[node.nextActions.index(nextaction)])
    node.actionsLength -= 1

    return newnode


def backprop(current, value):

    global backprop_counter
    backprop_counter += 1
    print("backpropagation started...", backprop_counter)

    while True:
        current.visits += 1
        current.wins += value
        current.ubtValue = (current.wins / current.visits) + 2*1.44*math.sqrt((2*math.log10(current.parent.visits)) / current.visits)
        current = current.parent
        if current.parent == None:
            break


def getBestChild(node, getChildList=False):
    bestChildren = []
    BestUBT = -1000

    for child in node.children:

        if child.ubtValue > BestUBT:
            BestUBT = child.ubtValue
            bestChildren.append(child)
        elif child.ubtValue == BestUBT:
            bestChildren.append(child)

    bestChild = random.choice(bestChildren)

    if getChildList == True:
        return bestChild, bestChildren
    else:
        return bestChild


def getBestAction(root, limit_time=10):

    total_time = 0
    while True:
        start_time = time.time()

        current = selection(root)
        value = rollout(current)
        backprop(current, value)

        spent_time = time.time() - start_time
        total_time += spent_time
        if total_time > limit_time:
            selection_counter = 0
            expansion_counter = 0
            rollout_counter = 0
            backprop_counter = 0
            break

    bestChild, bestChildren = getBestChild(root, getChildList = True)

    for i, child in enumerate(bestChildren):
        print("child[%d] -> [%d, %d], wins = %d, visits = %d, ubtValue = %d" \
    % (i, child.currentAction[0], child.currentAction[1], child.wins, child.visits, child.ubtValue))

    return bestChild.currentAction


def rollout(node):

    global rollout_counter
    rollout_counter += 1
    print("rollout started...", rollout_counter)

    # check if there is a winner
    if node.board.findWinner() == node.currentPlayer:
        return 1
    elif node.board.findWinner() == node.opponent:
        return 0

    # draw case
    if node.actionsLength == 0:
        return 0

    # simulation
    temp_board = copy.deepcopy(node.board)
    temp_nextActions = copy.deepcopy(node.nextActions)
    currentPlayer = node.currentPlayer
    winner = None
    while True:
        # player change
        currentPlayer = node.board.getOpponentPlayer(currentPlayer)

         # next action chosen by rollout policy
        nextmove = rolloutPolicy(temp_board, temp_nextActions, currentPlayer)
        del(temp_nextActions[temp_nextActions.index(nextmove)])
        #print("nextmove = ", nextmove)

        if temp_board.putStoneOnBoard(nextmove[0], nextmove[1], currentPlayer) == False:
            continue

        # ob.drawCurrentBoard(temp_board)
        winner = temp_board.winCheck(nextmove[0], nextmove[1], currentPlayer)
        #print("winner = ", winner)
        #a = input()

        if winner == False and len(temp_nextActions) > 0:
            continue
        else:
            break

    if winner == node.currentPlayer:
        return 1
    else:
        return 0


def rolloutPolicy(board, nextActions, currentPlayer):
    '''
    rollout policy for executing rollout
    first, check if there is a place to defend
    and then choose a place where the number of stones placed in line increased
    '''

    cnt_4 = []
    cnt_3 = []
    cnt_2 = []
    others = []
    nextmove = None
    random_actions = copy.deepcopy(nextActions)
    radnom_actions = random.shuffle(random_actions)
    opponent = board.getOpponentPlayer(currentPlayer)

    for action in random_actions:
        # check if there is current player's win position
        if board.winCheck(action[0], action[1], currentPlayer) == currentPlayer:
            print("winning position selected")
            nextmove = action
            break

        # defence check
        if board.defenseCheck(action[0], action[1], opponent) == True:
            print("defence position selected")
            nextmove = action
            break

        # find attack position
        my_cnt = board.cntStonesInTheSameLine(action[0], action[1], currentPlayer)
        if my_cnt == 4:
            cnt_4.append(action)
        elif my_cnt == 3:
            cnt_3.append(action)
        elif my_cnt == 2:
            cnt_2.append(action)
        else:
            others.append(action)
    # for문 종료

    if nextmove == None:
        if len(cnt_4) > 0:
            print("cnt_4 position selected")
            nextmove = random.choice(cnt_4)
        elif len(cnt_3) > 0:
            print("cnt_3 position selected")
            nextmove = random.choice(cnt_3)
        elif len(cnt_2) > 0:
            print("cnt_2 position selected")
            nextmove = random.choice(cnt_2)
        else:
            print("dense position selected")
            nextmove = getDensePlace(board, nextActions)

    return nextmove


def getEarlyStageAction(board, currentAction):
    '''
    At early stage, like just a stone put on the board
    next player select a one of the eight adjacent positions.
    Becaus rollout policy does not work well when there are few stones in the beginning.
    '''


    row = currentAction[0]
    column = currentAction[1]
    near = [[row+1, column+1],
            [row+1, column-1],
            [row+1, column],
            [row-1, column+1],
            [row-1, column-1],
            [row-1, column],
            [row, column+1],
            [row, column-1]]

    while True:
        nextmove = random.choice(near)
        if board.isInBorder(nextmove[0], nextmove[1]) == False or \
                                    board.isEmpty(nextmove[0], nextmove[1]) == False:
            continue
        else:
            break

    return nextmove


def getDensePlace(board, nextActions):
    '''
    Find dense places by counting the number of stones around
    '''

    directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
    empty_cnt_list = []
    empty_cnt = 0
    for action in nextActions:
        for direction in directions:
            if board.isEmpty(action[0] + direction[0], action[1] + direction[0]) == True:
                print([action[0] + direction[0], action[1] + direction[0]])
                empty_cnt += 1
            else:
                pass

            if board.isEmpty(action[0] - direction[0], action[1] - direction[0]) == True:
                empty_cnt += 1
            else:
                pass

        empty_cnt_list.append(empty_cnt)

    idx = empty_cnt_list.index(min(empty_cnt_list))
    densePlace = nextActions[idx]

    return densePlace





if __name__ == "__main__":

    b = Board(15, "EMPTY")

    b.putStoneOnBoard(7, 7, 'B')
    b.putStoneOnBoard(7, 6, 'W')
    b.putStoneOnBoard(8, 6, 'B')
    b.putStoneOnBoard(8, 7, 'W')
    b.putStoneOnBoard(6, 8, 'B')
    b.putStoneOnBoard(9, 5, 'W')
    b.putStoneOnBoard(5, 9, 'B')

    print(type(b.board))
    node = Node(b.board, [5, 9], 'B')
    node.printNodeInfo()
