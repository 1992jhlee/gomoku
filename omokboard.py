# -*- coding: utf-8 -*-

import numpy as np


class Board:


    def __init__(self, size, board):
        self.size = size
        if board == "EMPTY":
            self.board = self.getEmptyBoard(size)
        else:
            self.board = self.setBoard(board)


    def setBoard(self, board):
        temp_board = self.getEmptyBoard(self.size)
        for row in range(self.size):
            for column in range(self.size):
                temp_board[row][column] = board[row][column]

        return temp_board


    def getEmptyBoard(self, size):
        # create empty board
        board = []
        for i in range(size):
            board.append([0]*size)
        return board


    def getOpponentPlayer(self, BorW):
        if BorW == 'B':
            return 'W'
        else:
            return 'B'


    def drawCurrentBoard(self):
        #draw current board

        lines = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
        line = " "

        for i in range(self.size+1):
            if i == 0:
                for j in range(self.size):
                    if j == 0:
                        if i < self.size and j < self.size and self.board[i][j] == 1:
                            line = "●"
                        elif i < self.size and j < self.size and self.board[i][j] == -1:
                            line = "○"
                        else:
                            line = "┌"

                    elif j == self.size-1:
                        if i < self.size and j < self.size and self.board[i][j] == 1:
                            line += "●" + lines[self.size-i-1]
                        elif i < self.size and j < self.size and self.board[i][j] == -1:
                            line += "○" + lines[self.size-i-1]
                        else:
                            line += "┐" + lines[self.size-1]
                    else:
                        if i < self.size and j < self.size and self.board[i][j] == 1:
                            line += "●"
                        elif i < self.size and j < self.size and self.board[i][j] == -1:
                            line += "○"
                        else:
                            line += "┬"

            elif i == self.size-1:
                for j in range(self.size):
                    if j == 0:
                        if i < self.size and j < self.size and self.board[i][j] == 1:
                            line = "●"
                        elif i < self.size and j < self.size and self.board[i][j] == -1:
                            line = "○"
                        else:
                            line = "└"

                    elif j == self.size-1:
                        if i < self.size and j < self.size and self.board[i][j] == 1:
                            line += "●" + lines[self.size-i-1]
                        elif i < self.size and j < self.size and self.board[i][j] == -1:
                            line += "○" + lines[self.size-i-1]
                        else:
                            line += "┘" + lines[self.size-i-1]

                    else:
                        if i < self.size and j < self.size and self.board[i][j] == 1:
                            line += "●"
                        elif i < self.size and j < self.size and self.board[i][j] == -1:
                            line += "○"
                        else:
                            line += "┴"

            elif i == self.size:
                line = ""
                for j in range(self.size):
                    line += lines[j] + " "

            else:
                for j in range(self.size):
                    if j == 0:
                        if i < self.size and j < self.size and self.board[i][j] == 1:
                            line = "●"
                        elif i < self.size and j < self.size and self.board[i][j] == -1:
                            line = "○"
                        else:
                            line = "├"

                    elif j == self.size-1:
                        if i < self.size and j < self.size and self.board[i][j] == 1:
                            line += "●" + lines[self.size-i-1]
                        elif i < self.size and j < self.size and self.board[i][j] == -1:
                            line += "○" + lines[self.size-i-1]
                        else:
                            line += "┤" + lines[self.size-i-1]
                    else:
                        if i < self.size and j < self.size and self.board[i][j] == 1:
                            line += "●"
                        elif i < self.size and j < self.size and self.board[i][j] == -1:
                            line += "○"
                        else:
                            line += "┼"

            print(line)


    def isInBorder(self, row, column):
        if row < 0 or row > self.size-1 or column < 0 or column > self.size-1:
            return False # out of border
        else:
            return True # in the border


    def isEmpty(self, row, column):
        '''
        check if board[row][column] is empty
        empty          : return True
        not empty      : return False
        wrong position : return -1
        '''

        if not self.isInBorder(row, column):
            print("wrong position(out of border)")
            return -1

        if self.board[row][column] == 0:
            return True
        else:
            return False


    def getColorOfStone(self, row, column):
        '''
        Get color of stone at board[row][column]
        Black : return 'B'
        White : return 'W'
        Empty : return 'empty'
        '''
        if self.board[row][column] == 1:
            return 'B'
        elif self.board[row][column] == -1:
            return 'W'
        else:
            return 'empty'


    def colorCheck(self, row, column, BorW):
        '''
        "is the color of this BorW?"
        check stone color is the same as that of BorW (if stone exists there).
        same           : return True
        not same       : return False
        empty          : return None
        wrong position : return -1
        '''

        if not self.isInBorder(row, column):
            print("wrong position(out of border)")
            return -1

        if BorW == 'B':
            if self.board[row][column] == 1:
                return True
            elif self.board[row][column] == -1:
                return False
            else:
                return None

        elif BorW == 'W':
            #print(row, column)
            if self.board[row][column] == -1:
                return True
            elif self.board[row][column] == 1:
                return False
            else:
                return None


    def putStoneOnBoard(self, row, column, BorW):
        '''
        put stone of the same color as BorW on the position board[row][column]
        '''

        # border check
        if self.isInBorder(row, column) == False:
            print("Out of border!")
            return False

        # check availability
        if not self.isEmpty(row, column):
            print("not empty")
            return False

        # 33 rule check
        if self.check33_violation(row, column, BorW) == True:
            print("3*3 rule violated. choose another position")
            return False

        if BorW == 'W':
            self.board[row][column] = -1 # 흑은 board 행렬상에서 1로
        elif BorW == 'B':
            self.board[row][column] = 1  # 백은 board 행렬상에서 -1로


    def check33_violation(self, row, column, BorW):
        '''
        Check if 3*3 rule is violated
        violated     : return True
        not violated : return False
        '''

        direction = [(1, 0), (1, -1), (0, -1), (-1, -1)] # → ↘ ↓ ↙
        color = BorW
        cnt_33 = 0
        ref_point_x = row
        ref_point_y = column

        for i in range(4):

            stone_cnt = 1
            blank_cnt = 0
            blank_idx = 0
            block_flag = None
            # i = 0 -> check direction[0]
            drow = direction[i][0]
            dcolumn = direction[i][1]
            drow_ = -direction[i][0]
            dcolumn_ = -direction[i][1]


            for j in range(1, 5):
                if not self.isInBorder(ref_point_x + j*drow, ref_point_y + j*dcolumn):
                    continue

                if self.colorCheck(ref_point_x + j*drow, ref_point_y + j*dcolumn, color) == True:
                    # same color stone
                    stone_cnt += 1
                elif self.colorCheck(ref_point_x + j*drow, ref_point_y + j*dcolumn, color) == None:
                    # empty
                    blank_cnt += 1
                    blank_idx = j
                    if blank_cnt == 2:
                        blank_cnt = 0
                        break
                else:
                    # different color stone
                    if abs(j - blank_idx) == 1:
                        block_flag = False
                    elif blank_cnt < 2:
                        block_flag = True
                    break

            # stop counting if blocked with different color stone
            if block_flag == True:
                break

            # inverse direction
            blank_cnt = 0
            for j in range(1, 5):
                if not self.isInBorder(ref_point_x + j*drow_, ref_point_y + j*dcolumn_):
                    continue

                if self.colorCheck(ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color) == True:
                    # same color stone
                    stone_cnt += 1
                elif self.colorCheck(ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color) == None:
                    # empty
                    blank_cnt += 1
                    blank_idx = j
                    if blank_cnt == 2:
                        blank_cnt = 0
                        break
                else:
                    # different color stone
                    if abs(j - blank_idx) == 1:
                        block_cnt = False
                    elif blank_cnt < 2:
                        block_cnt = True
                    break

            # stop counting if blocked with different color stone
            if block_flag == True:
                break

            #print(cnt)
            if stone_cnt == 3:
                cnt_33 += 1

            #print(cnt_33)
            if cnt_33 == 2:
                return True

        return False


    def winCount(self, row, column, BorW):
        '''
        check stone number in a row for 8 directions
        if BorW wins : return True
        other cases  : return False
        '''

        direction = [(0, 1), (1, 1), (1, 0), (1, -1)] # (row_direction, colum_direction) → ↘ ↓ ↙
        stone_cnt = 1
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
                if not self.isInBorder(ref_point_x + j*drow, ref_point_y + j*dcolumn):
                    continue

                if self.colorCheck(ref_point_x + j*drow, ref_point_y + j*dcolumn, color) == True:
                    stone_cnt += 1
                else:
                    break

            # inverse direction
            for j in range(1, 5):
                if not self.isInBorder(ref_point_x + j*drow_, ref_point_y + j*dcolumn_):
                    continue

                if self.colorCheck(ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color) == True:
                    stone_cnt += 1
                else:
                    break

            #print(cnt)
            if stone_cnt >= 5 :
                break
            else:
                stone_cnt = 1

        if stone_cnt == 5:
            return True
        else:
            return None


    def defenseCheck(self, row, column, BorW):

        if self.check33_violation(row, column, BorW) == True:
            return False

        direction = [(0, 1), (1, 1), (1, 0), (1, -1)] # (row_direction, colum_direction) → ↘ ↓ ↙
        color = BorW
        ref_point_x = row
        ref_point_y = column

        defenseCheck_by_direction = []
        for i in range(4):
            stone_cnt = 1
            stone_cnt_ = 1
            blank_cnt = 0
            blank_cnt_ = 0
            blank_idx = []
            blank_idx_ = []
            block_flag = None
            block_flag_ = None
            block_idx = None
            block_idx_ = None

            # i = 0 -> check direction[0]
            drow = direction[i][0]
            dcolumn = direction[i][1]
            drow_ = -direction[i][0]
            dcolumn_ = -direction[i][1]

            for j in range(1, 6): # 레퍼런스 기준으로 +- 5개 위치 확인
                if not self.isInBorder(ref_point_x + j*drow, ref_point_y + j*dcolumn):
                    continue

                if self.colorCheck(ref_point_x + j*drow, ref_point_y + j*dcolumn, color) == True:
                    # same color stone
                    stone_cnt += 1
                elif self.colorCheck(ref_point_x + j*drow, ref_point_y + j*dcolumn, color) == False:
                    # different color stone(blocked)
                    # if stone_cnt == 4 and blank_cnt == 1:
                    #     block_flag = None
                    #else:
                    block_flag = True
                    block_idx = j
                    break
                elif self.colorCheck(ref_point_x + j*drow, ref_point_y + j*dcolumn, color) == None:
                    # empty
                    blank_cnt += 1
                    blank_idx.append(j)
                    if blank_cnt == 2:
                        if blank_idx[1] - blank_idx[0] == 1: # if continuous blank
                            blank_cnt = 0
                            break

                else: # out of border
                    block_flag = True
                    block_idx = j
                    break


            # inverse direction
            for j in range(1, 6):
                if not self.isInBorder(ref_point_x + j*drow_, ref_point_y + j*dcolumn_):
                    continue

                if self.colorCheck(ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color) == True:
                    # same color stone
                    stone_cnt_ += 1
                elif self.colorCheck(ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color) == False:
                    # different color stone(blocked)
                    # if stone_cnt_ == 4 and blank_cnt_ == 1:
                    #     # o_xxxv
                    #     block_flag_ = None
                    #else:
                    block_flag_ = True
                    block_idx_ = j
                    break
                elif self.colorCheck(ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color) == None:
                    # empty
                    blank_cnt_ += 1
                    blank_idx_.append(j)
                    if blank_cnt_ == 2:
                        if blank_idx_[1] - blank_idx_[0] == 1: # if continuous blank
                            blank_cnt_ = 0
                            break
                else: # out of border
                    block_flag_ = True
                    block_idx_ = j
                    break

            total_stone = stone_cnt + stone_cnt_ - 1

            if block_flag == True and block_flag_ == True:
                if total_stone == 5:
                    defenseCheck_by_direction.append(True)
                elif total_stone == 4 and blank_cnt == 1 and blank_cnt_ == 1:
                    if block_idx - blank_idx[0] == 1 and \
                                    block_idx_ - blank_idx_[0] == 1:
                        # o_xvxx_o
                        defenseCheck_by_direction.append(True)
                else:
                    defenseCheck_by_direction.append(False)

            if block_flag == True and block_flag_ == None:
                if total_stone == 5:
                    defenseCheck_by_direction.append(True)
                elif total_stone == 4 and blank_cnt == 1:
                    if blank_idx[0] == 4:
                    # o_xxxv
                        defenseCheck_by_direction.append(True)
                    elif blank_idx[0] == 1:
                    # oxxx_v
                        defenseCheck_by_direction.append(False)

            if block_flag == None and block_flag_ == True:
                if total_stone == 5:
                    defenseCheck_by_direction.append(True)
                elif total_stone == 4 and blank_cnt_ == 1:
                    if blank_idx_[0] == 4:
                    # o_xxxv
                        defenseCheck_by_direction.append(True)
                    elif blank_idx_[0] == 1:
                    # oxxx_v
                        defenseCheck_by_direction.append(False)

            if block_flag == None and block_flag_ == None:
                if total_stone == 5:
                    if blank_cnt != 0 or blank_cnt_ != 0:
                        defenseCheck_by_direction.append(False)
                    else:
                        defenseCheck_by_direction.append(True)
                elif total_stone == 4:
                    if blank_cnt >= 1 or blank_cnt_ >= 1:
                        defenseCheck_by_direction.append(False)
                    else:
                        defenseCheck_by_direction.append(True)

            #print(defenseCheck_by_direction)
            if True in defenseCheck_by_direction:
                return True

        return False


    def cntStonesInTheSameLine(self, row, column, BorW):

        # (row_direction, colum_direction) → ↘ ↓ ↙
        direction = [(0, 1), (1, 1), (1, 0), (1, -1)]
        color = BorW
        ref_point_x = row
        ref_point_y = column

        cnt_list = []
        for i in range(4):
            stone_cnt = 1
            stone_cnt_ = 1
            blank_cnt = 0
            blank_cnt_ = 0
            blank_idx = []
            blank_idx_ = []
            block_flag = None
            block_flag_ = None
            block_idx = None
            block_idx_ = None

            # i = 0 -> check direction[0]
            drow = direction[i][0]
            dcolumn = direction[i][1]
            drow_ = -direction[i][0]
            dcolumn_ = -direction[i][1]

            for j in range(1, 6): # 레퍼런스 기준으로 +- 5개 위치 확인
                if not self.isInBorder(ref_point_x + j*drow, ref_point_y + j*dcolumn):
                    continue

                if self.colorCheck(ref_point_x + j*drow, ref_point_y + j*dcolumn, color) == True:
                    # same color stone
                    stone_cnt += 1
                elif self.colorCheck(ref_point_x + j*drow, ref_point_y + j*dcolumn, color) == False:
                    # different color stone(blocked)
                    if stone_cnt == 4:
                        if blank_cnt == 1:
                            block_flag = None
                        else:
                            blog_flag =True
                    else:
                        block_flag = True
                        block_idx = j
                        stone_cnt -= 1
                        break
                elif self.colorCheck(ref_point_x + j*drow, ref_point_y + j*dcolumn, color) == None:
                    # empty
                    blank_cnt += 1
                    blank_idx.append(j)
                    if blank_cnt == 2:
                        if blank_idx[1] - blank_idx[0] == 1: # if continuous blank
                            blank_cnt = 0
                            break
                else:
                    # out of border
                    block_flag = True
                    block_idx = j
                    stone_cnt -= 1
                    break


            # inverse direction
            for j in range(1, 6):
                if not self.isInBorder(ref_point_x + j*drow_, ref_point_y + j*dcolumn_):
                    continue

                if self.colorCheck(ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color) == True:
                    # same color stone
                    stone_cnt_ += 1
                elif self.colorCheck(ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color) == False:
                    # different color stone(blocked)
                    if stone_cnt_ == 4:
                        if blank_cnt_ == 1:
                            block_flag_ = None
                        else:
                            block_flag_ = True
                    else:
                        block_flag_ = True
                        block_idx_ = j
                        stone_cnt_ -= 1
                        break
                elif self.colorCheck(ref_point_x + j*drow_, ref_point_y + j*dcolumn_, color) == None:
                    # empty
                    blank_cnt_ += 1
                    blank_idx_.append(j)
                    if blank_cnt_ == 2:
                        if blank_idx_[1] - blank_idx_[0] == 1: # if continuous blank
                            blank_cnt_ = 0
                            break
                else: # out of border
                    block_flag_ = True
                    block_idx_ = j
                    stone_cnt_ -= 1
                    break

            total_stone = stone_cnt + stone_cnt_ - 1
            total_blank = blank_cnt + blank_cnt_
            if total_stone == 2:
                if total_blank != 0:
                    total_stone = 1
            elif total_stone == 3:
                if total_blank >= 2:
                    total_stone = 1

            cnt_list.append(total_stone)

        return max(cnt_list)


    def boardToInputFeature(self):
        gameBoard_B = np.zeros([15, 15], dtype=np.float32)
        gameBoard_W = np.zeros([15, 15], dtype=np.float32)
        gameBoard_E = np.ones([15, 15], dtype=np.float32)
        input_tensor = np.zeros([3, 15, 15], dtype=np.float32)


        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    gameBoard_B[i][j] = 1
                elif self.board[i][j] == -1:
                    gameBoard_W[i][j] = 1
                else:
                    gameBoard_E[i][j] = 1

        input_tensor[0] = gameBoard_B.copy()
        input_tensor[1] = gameBoard_W.copy()
        input_tensor[2] = gameBoard_E.copy()
        input_tensor = np.transpose(input_tensor, (1,2,0))

        return input_tensor


    def winCheck(self, row, column, BorW):
        if self.winCount(row, column, BorW) == True:
            return BorW
        else:
            return False


    def findWinner(self):
        # Check if there is a winner
        for row in range(self.size):
            for column in range(self.size):
                color = self.getColorOfStone(row, column)
                if self.winCheck(row, column, color) == color:
                    return color

        return None


    def getLimit(self):
        row_lower_limit = 14
        row_upper_limit = 0
        col_lower_limit = 14
        col_upper_limit = 0

        for row in range(self.size):
            for column in range(self.size):
                if self.board[row][column] != 0:
                    if row < row_lower_limit:
                        row_lower_limit = row
                    if row > row_upper_limit:
                        row_upper_limit = row
                    if column < col_lower_limit:
                        col_lower_limit = column
                    if column < col_lower_limit:
                        col_lower_limit = column

        return row_lower_limit, row_upper_limit, col_lower_limit, col_upper_limit


    def getNumberOfStones(self):
        cnt = 0
        for row in range(self.size):
            cnt += self.board[row].count(1)
            cnt += self.board[row].count(-1)

        return cnt


def renewNextActions(board, currentPlayer):

    row_lower_limit = 14
    row_upper_limit = 0
    col_lower_limit = 14
    col_upper_limit = 0

    for row in range(board.size):
        for column in range(board.size):
            if board.board[row][column] != 0:
                if row < row_lower_limit:
                    row_lower_limit = row
                if row > row_upper_limit:
                    row_upper_limit = row
                if column < col_lower_limit:
                    col_lower_limit = column
                if column > col_upper_limit:
                    col_upper_limit = column

    row_lower_limit = max(row_lower_limit-2, 0)
    row_upper_limit = min(row_upper_limit+2, 14)
    col_lower_limit = max(col_lower_limit-2, 0)
    col_upper_limit = min(col_upper_limit+2, 14)

    nextActions = []
    for row in range(row_lower_limit, row_upper_limit+1):
        for column in range(col_lower_limit, col_upper_limit+1):
            if board.isEmpty(row, column) == True and \
                board.check33_violation(row, column, currentPlayer) == False:
                nextActions.append([row, column])

    print("renewed : ", nextActions)
    return nextActions




if __name__ == "__main__":
    b = Board(15, "EMPTY")

    b.putStoneOnBoard(7, 7, 'B')
    b.putStoneOnBoard(6, 6, 'B')
    b.putStoneOnBoard(8, 8, 'B')
    b.putStoneOnBoard(9, 9, 'W')
    #b.putStoneOnBoard(6, 7, 'W')
    #b.putStoneOnBoard(5, 8, 'B')
    #b.putStoneOnBoard(6, 6, 'B')
    #b.putStoneOnBoard(8, 8, 'W')
    #b.putStoneOnBoard(9, 7, 'W')
    #b.putStoneOnBoard(5, 7, 'W')
    #b.putStoneOnBoard(7, 5, 'W')
    #b.putStoneOnBoard(5, 5, 'B')


    b.drawCurrentBoard()

    print(b.cntStonesInTheSameLine(5, 5, 'B'))
