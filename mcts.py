# -*- coding: utf-8 -*-

import omokboard as ob
import random
import math
import copy
import time
import os

class Node:

    def __init__(self, board, current_action, BorW):
        self.children = []
        self.parent = None

        self.wins = 0
        self.visits = 1
        self.ubtValue = 0

        self.currentAction = current_action # [row, column]
        self.currentPlayer = BorW
        self.opponent = ob.getOpponentPlayer(BorW)

        self.board = copy.deepcopy(board)
        self.nextActions, self.actionsLength = self.getNextActions(board)
        self.gameFinished = isTerminal(self.board, self.currentAction, self.currentPlayer)

    def getNextActions(self, board):
        '''get positions that can be placed'''
        nextActions = []
        actionsLength = 0
        size = len(board[0])

        for row in range(size):
            for column in range(size):
                if ob.isEmpty(board, row, column) and ob.check33_violation(board, row, column, self.opponent) == False:
                    nextActions.append([row, column])
                    actionsLength += 1

        return nextActions, actionsLength




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
        ob.drawCurrentBoard(self.board)
        print("nextActions : \n", self.nextActions)
        print("actionsLength : ", self.actionsLength)

        return





selection_counter = 0
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



expansion_counter = 0
def expansion(node):


    global expansion_counter
    expansion_counter += 1
    print("expansion started...", expansion_counter)


    while True:

        nextboard = copy.deepcopy(node.board)
        nextaction = rolloutPolicy(nextboard, node.nextActions, node.currentPlayer)
        #idx = random.randint(0, node.actionsLength-1)
        #nextaction = node.nextActions[idx]

        if ob.putStoneOnBoard(nextboard, nextaction[0], nextaction[1], node.opponent) == False:
            continue

        newnode = Node(nextboard, nextaction, node.opponent)
        newnode.parent = node
        break

    # update parent node
    node.children.append(newnode)
    del(node.nextActions[node.nextActions.index(nextaction)])
    node.actionsLength -= 1

    return newnode



# rollout by random selection(without policy)
def rollout_random(node):

    #print("rollout start")

    # check if there is a winner
    if findWinner(node.board, node.currentPlayer) == node.currentPlayer:
        return 1
    elif findWinner(node.board, node.currentPlayer) == node.opponent:
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
        currentPlayer = ob.getOpponentPlayer(currentPlayer) # player change
        nextmove = random.choice(temp_nextActions) # choose a possible action randomly
        del(temp_nextActions[temp_nextActions.index(nextmove)]) # delete current action
        if ob.putStoneOnBoard(temp_board, nextmove[0], nextmove[1], currentPlayer) == False:
            continue
        winner = winCheck(temp_board, nextmove[0], nextmove[1], currentPlayer)

        if winner == None and len(temp_nextActions) > 0:
            continue
        else:
            break

    if winner == node.currentPlayer:
        print(temp_board)
        return 1
    else:
        return 0




backprop_counter = 0
def backprop(current, value):

    global backprop_counter
    backprop_counter += 1
    print("backpropagation started...", backprop_counter)

    while True:
        current.visits += 1
        current.wins += value
        current.ubtValue = (current.wins / current.visits) + 2*1.44*math.sqrt((2*math.log10(current.parent.visits)) / current.parent.visits)
        current = current.parent
        if current.parent == None:
            break




# 해당 좌표에 돌을 놓을 시, 승자 반환
def getWinner(board, row, column):
    if ob.winCount(board, row, column, 'B') == True:
        if ob.colorCheck(board, row, column, 'B') == 'B':
            return 'B'
    elif ob.winCount(board, row, column, 'W') == True:
        if ob.colorCheck(board, row, column, 'W') == 'W':
            return 'W'
    else:
        return None # game continues




def winCheck(board, row, column, BorW):
    if ob.winCount(board, row, column, BorW) == True:
        return BorW
    else:
        return False





# 현재 게임판에 이긴 사람이 있는지 확인
def findWinner(board, BorW):
    size = len(board[0])

    for row in range(size):
        for column in range(size):
            if ob.colorCheck(board, row, column, BorW) == BorW and winCheck(board, row, column, BorW) == BorW:

                return BorW

    return None



def isTerminal(board, position, BorW):
        # position = [row, column]
        if winCheck(board, position[0], position[1], BorW) == BorW:
            return True
        else:
            return False




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

    for child in bestChildren:
        print(child.wins, child.visits, child.ubtValue)

    return bestChild.currentAction




rollout_counter = 0
# rollout by rollout policy
def rollout(node):

    global rollout_counter
    rollout_counter += 1
    print("rollout started...", rollout_counter)

    # check if there is a winner
    if findWinner(node.board, node.currentPlayer) == node.currentPlayer:
        return 1
    elif findWinner(node.board, node.opponent) == node.opponent:
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
        currentPlayer = ob.getOpponentPlayer(currentPlayer) # player change
        nextmove = rolloutPolicy(temp_board, temp_nextActions, currentPlayer) # next action chosen by rollout policy
        print("nextmove = ", nextmove)
        del(temp_nextActions[temp_nextActions.index(nextmove)]) # delete current action
        if ob.putStoneOnBoard(temp_board, nextmove[0], nextmove[1], currentPlayer) == False:
            continue
        ob.drawCurrentBoard(temp_board)
        winner = winCheck(temp_board, nextmove[0], nextmove[1], currentPlayer)
        print("winner = ", winner)
        #a = input()
        if not winner == currentPlayer and len(temp_nextActions) > 0:
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

    for action in random_actions:

        # defence check
        direction, opponent_cnt = ob.cntStoneInDirection(board, action[0], action[1], ob.getOpponentPlayer(currentPlayer), with_direction=True)

        if winCheck(board, action[0], action[1], ob.getOpponentPlayer(currentPlayer)) == ob.getOpponentPlayer(currentPlayer):
            # 상대방이 놓으면 무조건 지는 포지션 먼저 검사
            nextmove = action
            break

        if opponent_cnt == 4:
            if checkSpaceInRow(board, action, direction, ob.getOpponentPlayer(currentPlayer)) == True:
                continue

            nextmove = action
            break


        # find attack position
        my_cnt = ob.cntStoneInDirection(board, action[0], action[1], currentPlayer)
        if winCheck(board, action[0], action[1], currentPlayer) == currentPlayer:
            nextmove = action
            break
        elif my_cnt == 4:
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
            nextmove = random.choice(cnt_4)
        elif len(cnt_3) > 0:
            nextmove = random.choice(cnt_3)
        elif len(cnt_2) > 0:
            nextmove = random.choice(cnt_2)
        else:
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
    size = len(board[0])
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
        if ob.IsInBorder(nextmove[0], nextmove[1], size) == False or ob.isEmpty(board, nextmove[0], nextmove[1]) == False:
            continue
        else:
            break

    return nextmove



def checkSpaceInRow(board, action, direction, BorW):
    '''
    check if a shape of stone row is like o_ooo
    '''

    row = action[0]
    column = action[1]
    near = [[row + direction[0], column + direction[1]],
            [row - direction[0], column - direction[1]]]
    if ob.colorCheck(board, near[0][0], near[0][1], BorW) == None and ob.colorCheck(board, near[1][0], near[1][1], BorW) == None:
        return True
    else:
        return False



def getDensePlace(board, nextActions):
    '''
    Find dense places by counting the number of stones around''
    '''

    directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
    empty_cnt_list = []
    empty_cnt = 0
    for action in nextActions:
        for direction in directions:
            if ob.isEmpty(board, action[0] + direction[0], action[1] + direction[0]) == True:
                print([action[0] + direction[0], action[1] + direction[0]])
                empty_cnt += 1
            else:
                pass

            if ob.isEmpty(board, action[0] - direction[0], action[1] - direction[0]) == True:
                empty_cnt += 1
            else:
                pass

        empty_cnt_list.append(empty_cnt)

    idx = empty_cnt_list.index(min(empty_cnt_list))
    densePlace = nextActions[idx]

    return densePlace

'''
board = ob.getEmptyBoard(15)
ob.putStoneOnBoard(board, 7, 7, 'B')
ob.putStoneOnBoard(board, 7, 8, 'W')
ob.putStoneOnBoard(board, 8, 7, 'B')
ob.putStoneOnBoard(board, 6, 7, 'W')
ob.putStoneOnBoard(board, 6, 8, 'B')
ob.putStoneOnBoard(board, 5, 6, 'W')
ob.putStoneOnBoard(board, 8, 9, 'B')
ob.putStoneOnBoard(board, 4, 5, 'W')
ob.putStoneOnBoard(board, 3, 4, 'B')
ob.putStoneOnBoard(board, 7, 6, 'W')
ob.putStoneOnBoard(board, 8, 5, 'B')
ob.putStoneOnBoard(board, 8, 6, 'W')
ob.putStoneOnBoard(board, 6, 6, 'B')
ob.putStoneOnBoard(board, 5, 8, 'W')
ob.putStoneOnBoard(board, 7, 9, 'B')
ob.putStoneOnBoard(board, 4, 9, 'W')
ob.putStoneOnBoard(board, 5, 7, 'B')

root = Node(board, [5, 7], 'B')
ob.drawCurrentBoard(root.board)
newpos = getBestAction(root)
print(newpos)
ob.putStoneOnBoard(board, newpos[0], newpos[1], root.opponent)
ob.drawCurrentBoard(board)
'''



'''
board = ob.getEmptyBoard(15)
while True:
    #os.sys('CLS')
    ob.drawCurrentBoard(board)

    while True:
        my_action= int(input("my action = "))
        if ob.putStoneOnBoard(board, int(my_action / 10), my_action % 10, 'B') == False:
            continue
        #os.sys('CLS')
        ob.drawCurrentBoard(board)
        if winCheck(board, int(my_action / 10), my_action % 10, 'B') == 'B':
            print(" YOU WIN ! ")
            break
        else:
            break

    root = Node(board, [int(my_action / 10), my_action % 10], 'B')
    print("root.currentAction = ", root.currentAction)
    if root.actionsLength >= 222: # 1~2 번째 수를 둬야할 경우
        newpos = getEarlyStageAction(root.board, root.currentAction)
    else:
        newpos = rolloutPolicy(board, root.nextActions, 'W')
        print("newpoas = ", newpos)

    ob.putStoneOnBoard(board, newpos[0], newpos[1], 'W')
    if winCheck(board, newpos[0], newpos[1], 'W') == 'W':
        print(" YOU LOSE ")
        break
'''



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
        if winCheck(board, my_action_row, my_action_col, 'B') == 'B':
            print(" YOU WIN ! ")
            break
        else:
            break


    root = Node(board, [my_action_row, my_action_col], 'B')
    #root.printNodeInfo()
    #rest = input()
    nextmove = None
    if root.actionsLength >= 222:
        # 1~2 번째 수를 둬야할 경우
        nextmove = getEarlyStageAction(root.board, root.currentAction)
    else:
        random_actions = copy.deepcopy(root.nextActions)
        radnom_actions = random.shuffle(random_actions)
        # defence check
        for action in random_actions:
            direction, opponent_cnt = ob.cntStoneInDirection(root.board, action[0], action[1], root.currentPlayer, with_direction=True)
            #print(action, opponent_cnt)
            if winCheck(root.board, action[0], action[1], root.currentPlayer) == root.currentPlayer:
                nextmove = action
                break

            if opponent_cnt == 4:
                if checkSpaceInRow(root.board, action, direction, root.currentPlayer) == True:
                    continue

                nextmove = action
                break

    if nextmove == None:
        nextmove = getBestAction(root, 3)

    ob.putStoneOnBoard(board, nextmove[0], nextmove[1], 'W')
    if winCheck(board, nextmove[0], nextmove[1], 'W') == 'W':
        print(" YOU LOSE ")
        break





'''
board = ob.getEmptyBoard(15)

ob.putStoneOnBoard(board, 7, 7, 'B')
ob.putStoneOnBoard(board, 8, 8, 'B')
ob.putStoneOnBoard(board, 6, 6, 'B')
ob.putStoneOnBoard(board, 5, 5, 'B')
ob.putStoneOnBoard(board, 4, 4, 'W')
ob.putStoneOnBoard(board, 7, 6, 'W')
ob.putStoneOnBoard(board, 9, 9, 'W')
ob.putStoneOnBoard(board, 6, 5, 'W')
ob.putStoneOnBoard(board, 6, 8, 'B')

ob.drawCurrentBoard(board)
print(findWinner(board, 'B'))
print(winCheck(board, 4, 4, 'B'))
print(ob.winCount(board, 4, 4, 'B'))
#print(checkSpaceInRow(board, [4, 4], [1, 1], 'B'))
#print(winCheck(board, 5, 5, 'B'))
#cnt = ob.cntStoneInDirection(board, 5, 9, 'B')
#print(cnt)
#cnt = ob.cntStoneInDirection(board, 9, 5, 'B')
#print(cnt)
#cnt = ob.cntStoneInDirection(board, 4, 10, 'B')
#print(cnt)
#cnt = ob.cntStoneInDirection(board, 10, 4, 'B')
#print(cnt)
'''
