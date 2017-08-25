# -*- coding: utf-8 -*-


import random
import math
import copy
import time
import os
import tensorflow as tf
#import cnn
from omokboard import Board
from omokboard import renewNextActions
from omokboard import getPromisingActions
from omokboard import getFavorablePosition
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
        nextaction = rolloutPolicy(nextboard, node.nextActions, node.opponent)

        if nextboard.putStoneOnBoard(nextaction[0], nextaction[1], node.opponent) == False:
            continue

        newnode = Node(nextboard.board, nextaction, node.opponent, node.using_model)
        newnode.parent = node

        # score = self.ubtValue + self.parent.prob_distrib[currentAction]
        # [row, column] -> [coord_x, coord_y]
        # row = 14 - coord_y
        # column = coord_x
        coord_x = newnode.currentAction[1]
        coord_y = 14 - newnode.currentAction[0]
        idx = coord_x + 15*coord_y
        prob_distrib = newnode.parent.prob_distrib[idx]
        newnode.score = prob_distrib

        break

    # update parent node
    node.children.append(newnode)
    #del(node.nextActions[node.nextActions.index(nextaction)])
    #node.actionsLength -= 1

    return newnode


def backprop(current, value):

    global backprop_counter
    backprop_counter += 1
    print("backpropagation started...", backprop_counter)

    while True:
        current.visits += 1
        current.wins += value
        current.ubtValue = (current.wins / current.visits) + 2*1.44*math.sqrt((2*math.log10(current.parent.visits)) / current.visits)
        current.score += current.ubtValue
        current = current.parent
        if current.parent == None:
            break


def getBestChild(node, getChildList=False):

    score_list = [child.score for child in node.children]
    best_score = max(score_list)
    return node.children[score_list.index(best_score)]


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

    bestChild = getBestChild(root)
    print("bestchild -> [%d, %d], wins = %d, visits = %d, score = %f" \
                % (bestChild.currentAction[0], bestChild.currentAction[1], bestChild.wins, bestChild.visits, bestChild.score))

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
    currentPlayer = node.currentPlayer
    winner = None
    while True:

        # player change
        currentPlayer = node.board.getOpponentPlayer(currentPlayer)

        # renew possible actions
        temp_nextActions = renewNextActions(temp_board, currentPlayer)
        if len(temp_nextActions) == 0:
            break

        # next action chosen by rollout policy
        nextmove = rolloutPolicy(temp_board, temp_nextActions, currentPlayer)
        print("nextmove = ", nextmove)

        if temp_board.putStoneOnBoard(nextmove[0], nextmove[1], currentPlayer) == False:
            continue

        temp_board.drawCurrentBoard()
        winner = temp_board.winCheck(nextmove[0], nextmove[1], currentPlayer)
        print("winner = ", winner)
        #a = input()

        print("len(temp_nextActions) = ", len(temp_nextActions))
        if winner == False and len(temp_nextActions) > 0:
            continue
        else:
            break

    if winner == node.currentPlayer:
        return 1
    else:
        return 0


def rolloutPolicy(board, nextActions, currentPlayer, promisingActions=None):
    '''s
    rollout policy for executing rollout
    first, check if there is a place to defend
    and then choose a place where the number of stones placed in line increased
    '''

    cnt_4 = []
    cnt_3 = []
    cnt_2 = []
    nextmove = None
    random_actions = copy.deepcopy(nextActions)
    radnom_actions = random.shuffle(random_actions)
    opponent = board.getOpponentPlayer(currentPlayer)

    losing_pos = []
    for action in random_actions:
        # check if there is current player's winning position
        if board.winCheck(action[0], action[1], currentPlayer) == currentPlayer:
            print("winning position selected : ", action)
            return action

        # check if there is opponent player's winning position
        if board.winCheck(action[0], action[1], opponent) == opponent:
            losing_pos.append(action)

    if len(losing_pos) > 0:
        defense_pos_1 = getFavorablePosition(board, losing_pos, currentPlayer)
        defense_pos_2 = getFavorablePosition(board, losing_pos, opponent)
        defense_pos_1_cnt = board.cntStonesForFavPos(defense_pos_1[0], defense_pos_2[1], currentPlayer)
        defense_pos_2_cnt = board.cntStonesForFavPos(defense_pos_2[0], defense_pos_2[1], opponent)
        if defense_pos_1_cnt >= defense_pos_2_cnt:
            print("opponent's winning position selected : ", defense_pos_1)
            return defense_pos_1
        elif defense_pos_2_cnt > defense_pos_1_cnt:
            print("opponent's winninge position selected : ", defense_pos_2)
            return defense_pos_2


    nextmove_candidates = []
    for action in random_actions:
        # defence check
        if board.defenseCheck(action[0], action[1], opponent) == True:
            nextmove_candidates.append(action)

    if len(nextmove_candidates) > 0:
        nextmove_1 = getFavorablePosition(board, nextmove_candidates, currentPlayer)
        nextmove_2 = getFavorablePosition(board, nextmove_candidates, opponent)
        nextmove_1_cnt = board.cntStonesForFavPos(nextmove_1[0], nextmove_1[1], currentPlayer)
        nextmove_2_cnt = board.cntStonesForFavPos(nextmove_2[0], nextmove_2[1], opponent)
        if nextmove_1_cnt >= nextmove_2_cnt:
            print("defence position selected : ", nextmove_1)
            return nextmove_1
        elif nextmove_2_cnt > nextmove_1_cnt:
            print("defence position selected : ", nextmove_2)
            return nextmove_2


    for action in random_actions:
        # find attack position
        my_cnt = board.cntStonesInTheSameLine(action[0], action[1], currentPlayer)
        if my_cnt == 4:
            cnt_4.append(action)
        elif my_cnt == 3:
            cnt_3.append(action)
        elif my_cnt == 2:
            cnt_2.append(action)


    if nextmove == None:
        if len(cnt_4) > 0:
            nextmove = getFavorablePosition(board, cnt_4, currentPlayer)
            print("cnt_4 position selected : ", nextmove)
        elif len(cnt_3) > 0:
            nextmove = getFavorablePosition(board, cnt_3, currentPlayer)
            print("cnt_3 position selected : ", nextmove)
        elif len(cnt_2) > 0:
            nextmove = getFavorablePosition(board, cnt_2, currentPlayer)
            print("cnt_2 position selected : ", nextmove)
        else:
            nextmove = getDensePlace(board, nextActions)
            print("dense position selected : ", nextmove)

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

    print("in getDensPlace\n", len(nextActions))
    board.drawCurrentBoard()
    print(nextActions)
    directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
    min_empty_cnt = 8
    densePlaces = []
    for action in nextActions:
        if 0 in action:
            if len(nextActions) > 10:
                continue

        empty_cnt = 0
        for direction in directions:

            if board.isEmpty(action[0] + direction[0], action[1] + direction[0]) == True:
                empty_cnt += 1

            if board.isEmpty(action[0] - direction[0], action[1] - direction[0]) == True:
                empty_cnt += 1

        print(action, " : ", empty_cnt)
        if empty_cnt < min_empty_cnt:
            densePlaces.append(action)

    return random.choice(densePlaces)





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
