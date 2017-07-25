# -*- coding: utf-8 -*-

import numpy as np



def getOpponentPlayer(BorW):
    if BorW == 'B':
        return 'W'
    else:
        return 'B'




def getEmptyBoard(size):
    '''
    create empty board
    '''

    board = []
    for i in range(size):
        board.append([0]*size)
    return board




def drawCurrentBoard(board):
    '''
    draw current board
    '''

    lines = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
    line = " "
    size = len(board[0])

    for i in range(size+1):
        if i == 0:
            for j in range(size):
                if j == 0:
                    if i < size and j < size and board[i][j] == 1:
                        line = "●"
                    elif i < size and j < size and board[i][j] == -1:
                        line = "○"
                    else:
                        line = "┌"

                elif j == size-1:
                    if i < size and j < size and board[i][j] == 1:
                        line += "●" + lines[len(board[0])-i-1]
                    elif i < size and j < size and board[i][j] == -1:
                        line += "○" + lines[len(board[0])-i-1]
                    else:
                        line += "┐" + lines[len(board[0])-1]
                else:
                    if i < size and j < size and board[i][j] == 1:
                        line += "●"
                    elif i < size and j < size and board[i][j] == -1:
                        line += "○"
                    else:
                        line += "┬"

        elif i == size-1:
            for j in range(size):
                if j == 0:
                    if i < size and j < size and board[i][j] == 1:
                        line = "●"
                    elif i < size and j < size and board[i][j] == -1:
                        line = "○"
                    else:
                        line = "└"

                elif j == size-1:
                    if i < size and j < size and board[i][j] == 1:
                        line += "●" + lines[len(board[0])-i-1]
                    elif i < size and j < size and board[i][j] == -1:
                        line += "○" + lines[len(board[0])-i-1]
                    else:
                        line += "┘" + lines[len(board[0])-i-1]

                else:
                    if i < size and j < size and board[i][j] == 1:
                        line += "●"
                    elif i < size and j < size and board[i][j] == -1:
                        line += "○"
                    else:
                        line += "┴"

        elif i == size:
            line = ""
            for j in range(size):
                line += lines[j] + " "

        else:
            for j in range(size):
                if j == 0:
                    if i < size and j < size and board[i][j] == 1:
                        line = "●"
                    elif i < size and j < size and board[i][j] == -1:
                        line = "○"
                    else:
                        line = "├"

                elif j == size-1:
                    if i < size and j < size and board[i][j] == 1:
                        line += "●" + lines[len(board[0])-i-1]
                    elif i < size and j < size and board[i][j] == -1:
                        line += "○" + lines[len(board[0])-i-1]
                    else:
                        line += "┤" + lines[len(board[0])-i-1]
                else:
                    if i < size and j < size and board[i][j] == 1:
                        line += "●"
                    elif i < size and j < size and board[i][j] == -1:
                        line += "○"
                    else:
                        line += "┼"



        print(line)





def isEmpty(board, row, column):
    '''
    check board[row][column] is empty
    empty :     return True
    not empty : return False
    '''

    size = len(board[0])-1
    if row < 0 or row > size or column < 0 or column > size:
        print("wrong position")
        return False

    if board[row][column] == 0:
        return True
    else:
        return False





def colorCheck(board, row, column, BorW):
    '''
    check stone color is the same as that of BorW (if stone exists there).
    same : return True
    not same : return False
    empty : return None
    '''

    size = len(board[0])
    if row < 0 or row > size-1 or column < 0 or column > size-1:
        #print(row, column)
        #print("wrong position")
        return 'error'

    if BorW == 'B':
        if board[row][column] == 1:
            return True
        elif board[row][column] == -1:
            return False
        else:
            return None

    elif BorW == 'W':
        #print(row, column)
        if board[row][column] == -1:
            return True
        elif board[row][column] == 1:
            return False
        else:
            return None


def putStoneOnBoard(board, row, column, BorW):
    '''
    put stone of the same color as BorW on the position board[row][column]
    '''

    # check availability
    if not isEmpty(board, row, column):
        print("not empty")
        return False

    # 33 rule check
    if check33_violation(board, row, column, BorW) == True:
        print("3*3 rule violated. choose another position")
        return False

    # border check
    if IsInBorder(row, column, len(board)) == False:
        print("Out of border!")
        return False
    if BorW == 'W':
        board[row][column] = -1 # 흑은 board 행렬상에서 1로
    elif BorW == 'B':
        board[row][column] = 1  # 백은 board 행렬상에서 -1로




def winCount(board, row, column, BorW):
    '''
    check stone number in a row for 8 directions
    if BorW wins : return True
    other cases  : return False
    '''

    direction = [(0, 1), (1, 1), (1, 0), (1, -1)] # (row_direction, colum_direction) → ↘ ↓ ↙
    cnt = 1
    color = BorW
    ref_point_x = row
    ref_point_y = column

    for i in range(4):
        # i = 0 -> check direction[0]
        drow = direction[i][0]
        dcolumn = direction[i][1]
        drow_ = -direction[i][0]
        dcolumn_ = -direction[i][1]


        for j in range(1, 5):
            if not IsInBorder(ref_point_x + j*drow, ref_point_y + j*dcolumn, len(board[0])):
                continue

            if colorCheck(board, ref_point_x + j*drow, ref_point_y + j*dcolumn, color):
                cnt += 1
            else:
                break

        # inverse direction
        for j in range(1, 5):
            if not IsInBorder(ref_point_x + j*drow_, ref_point_y + j*dcolumn_, len(board[0])):
                continue

            if colorCheck(board, ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color):
                cnt += 1
            else:
                break

        #print(cnt)
        if cnt >= 5 :
            break
        else:
            cnt = 1

    if cnt == 5:
        return True
    else:
        return None





def cntStoneInDirection(board, row, column, BorW, with_direction=False):

    direction = [(0, 1), (1, 1), (1, 0), (1, -1)] # (row_direction, colum_direction) → ↘ ↓ ↙
    cnt = 1
    color = BorW
    ref_point_x = row
    ref_point_y = column

    cnt_list = []
    direction_list = []
    for i in range(4):
        # i = 0 -> check direction[0]
        drow = direction[i][0]
        dcolumn = direction[i][1]
        drow_ = -direction[i][0]
        dcolumn_ = -direction[i][1]


        for j in range(1, 6): # 레퍼런스 기준으로 +- 5개 위치 확인
            if not IsInBorder(ref_point_x + j*drow, ref_point_y + j*dcolumn, len(board[0])):
                continue

            if colorCheck(board, ref_point_x + j*drow, ref_point_y + j*dcolumn, color) == True:
                #print("first")
                cnt += 1

            elif colorCheck(board, ref_point_x + j*drow, ref_point_y + j*dcolumn, color) == False: # 막혀있는지 확인
                #print("second")
                cnt -= 1
                break
            elif colorCheck(board, ref_point_x + j*drow, ref_point_y + j*dcolumn, color) == None:
                #print("third")
                if colorCheck(board, ref_point_x + (j+1)*drow, ref_point_y + (j+1)*dcolumn, color) == None:
                    break
            else: # out of border
                cnt -= 1
                break
            #print(cnt)
        #print(direction[i], "정방향 = ", cnt)

        # inverse direction
        for j in range(1, 6):
            if not IsInBorder(ref_point_x + j*drow_, ref_point_y + j*dcolumn_, len(board[0])):
                continue

            if colorCheck(board, ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color) == True:
                #print("first-")
                cnt += 1

            elif colorCheck(board, ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color) == False:
                #print("second-")
                cnt -= 1
                break
            elif colorCheck(board, ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color) == None:
                #print("third-")
                if colorCheck(board, ref_point_x + (j+1)*drow_, ref_point_y + (j+1)*dcolumn_, color) == None:
                    break
            else: # out of border
                cnt -= 1
                break
            #print(cnt)
        #print(direction[i], "역방향 = ", cnt)


        cnt_list.append(cnt)
        direction_list.append(direction[i])
        cnt = 1

    #print(cnt_list)
    if with_direction == True:
        return direction_list[cnt_list.index(max(cnt_list))], max(cnt_list)
    else:
        return max(cnt_list)






def check33_violation(board, row, column, BorW):
    '''
    Check if 3*3 rule is violated
    violated     : return True
    not violated : return False
    '''

    direction = [(1, 0), (1, -1), (0, -1), (-1, -1)] # → ↘ ↓ ↙
    color = BorW
    cnt = 1
    cnt_33 = 0
    ref_point_x = row
    ref_point_y = column

    for i in range(4):
        # i = 0 -> check direction[0]
        drow = direction[i][0]
        dcolumn = direction[i][1]
        drow_ = -direction[i][0]
        dcolumn_ = -direction[i][1]


        for j in range(1, 5):
            if not IsInBorder(ref_point_x + j*drow, ref_point_y + j*dcolumn, len(board[0])):
                continue

            if colorCheck(board, ref_point_x + j*drow, ref_point_y + j*dcolumn, color):
                cnt += 1
            else:
                break

        # inverse direction
        for j in range(1, 5):
            if not IsInBorder(ref_point_x + j*drow_, ref_point_y + j*dcolumn_, len(board[0])):
                continue

            if colorCheck(board, ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color):
                cnt += 1
            else:
                break

        #print(cnt)
        if cnt == 3:
            cnt_33 += 1
            cnt = 1
        else:
            cnt = 1

        #print(cnt_33)
        if cnt_33 == 2:
            #print("3*3 rule violated")
            return True

    return False




def IsInBorder(row, column, size):
    if row < 0 or row > size-1 or column < 0 or column > size-1:
        return False # out of border
    else:
        return True # in the border
