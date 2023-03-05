import numpy as np
import copy

class Mancala:
    def __init__(self, playMode, boardSize, marbleCount):
        self.playMode = playMode # 1 = two humans, 2 = 1 bot, 1 human
        self.boardSize = boardSize
        self.board = self.initBoard(boardSize, marbleCount)
        self.player1 = 0
        self.player2 = 0
        self.turn = 1

    def __str__(self):
        string = ""
        string += "\t<-- Player 1's side\n"
        string += "-------------------------------------------------\n"

        temp1 = "|\t(P1)\t| "
        for x in range(self.boardSize):
                temp1 += (str(self.board[0][x]) + " |")
        temp1 += "\t(P2)\t|\n"
        string += temp1

        string += "|\t" + str(self.player1) + "\t|------------------|\t" + str(self.player2)+ "\t|\n"

        temp1 = "|\t\t| "
        for x in range(self.boardSize):
            temp1 += str(self.board[1][x]) + " |"
        temp1 += "\t\t|\n"

        string += temp1
        string += "-------------------------------------------------\n"
        string += "\t\t\tPlayer 2's side -->\n"
        string += "Space numbers:    0  1  2  3  4  5"

        return string

    def initBoard(self, boardSize, count):
        board = []
        temp1 = []
        temp2 = []
        for x in range(boardSize):
            temp1.append(count)
            temp2.append(count)
        board.append(temp1)
        board.append(temp2)

        return board

    def play(self, bot1):
        print(self)
        while self.player1HasMoves() or self.player2HasMoves():
            if self.turn == 1: #Player 1's turn
                print("Player 1's turn:")
                if self.player1HasMoves() == False:
                    print("Player 1 has no available moves.")
                    self.turn = 2
                elif self.playMode == 1:
                    move = self.getConsoleMove()
                    repeatFlag = self.move(move)
                    print(self)
                    if repeatFlag == True:
                        print("Player 1 gets to go again!")
                    else:
                        self.turn = 2
                elif self.playMode == 2:
                    print("HERE")
                    move = bot1.alphaBetaSearch(copy.deepcopy(self))
                    print("Player 1 selects " + str(move))
                    repeatFlag = self.move(move)
                    print(self)
                    if repeatFlag == True:
                        print("Player 1 gets to go again!")
                    else:
                        self.turn = 2
            elif self.turn == 2:
                print("Player 2's turn:")
                if self.player2HasMoves() == False:
                    print("Player 2 has no available moves.")
                    self.turn = 1
                elif self.playMode != 3:
                    move = self.getConsoleMove()
                    repeatFlag = self.move(move)
                    print(self)
                    if repeatFlag == True:
                        print("Player 2 gets to go again!")
                    else:
                        self.turn = 1
        print("Game over!")


    def getConsoleMove(self):
        print("Player " + str(self.turn) + " enter move:")
        inp = int(input())
        while inp >= self.boardSize or inp < 0:
            print("That's not a valid move, please try again.")
            inp = int(input())
        while self.board[self.turn - 1][inp] == 0:
            print("There are no marbles there! Please select another move.")
            inp = int(input())
        return inp

    def player1HasMoves(self):
        for x in range(self.boardSize):
            if self.board[0][x] != 0:
                return True
        return False

    def player2HasMoves(self):
        for x in range(self.boardSize):
            if self.board[1][x] != 0:
                return True

    def move(self, y):
        count = self.board[self.turn - 1][y]
        self.board[self.turn - 1][y] = 0
        loc = [self.turn-1, y]
        x = 0
        while x < count:
            if loc[0] == 0:
                if loc[1] == 0:
                    if self.turn == 1:
                        self.player1 += 1
                        x +=1
                        if x == count:
                            return True
                    loc[0] = 1
                else:
                    loc[1] -= 1
            elif loc[0] == 1:
                if loc[1] == (self.boardSize - 1):
                    if self.turn == 2:
                        self.player2 += 1
                        x +=1
                        if x == count:
                            return True
                    loc[0] = 0
                else:
                    loc[1] += 1
            self.board[loc[0]][loc[1]] += 1
            x += 1

        if self.turn == (loc[0]+1) and self.board[loc[0]][loc[1]] == 1:
            oppRow = 1
            if self.turn == 2:
                oppRow = 0

            temp = 0
            temp += self.board[loc[0]][loc[1]]
            self.board[loc[0]][loc[1]] = 0
            temp += self.board[oppRow][loc[1]]
            self.board[oppRow][loc[1]] = 0

            if self.turn == 1:
                self.player1 += temp
            else:
                self.player2 += temp

        return False

    def setState(self, board, p1, p2):
        self.board = board
        self.player1 = p1
        self.player2 = p2

    def gameEnd(self):
        return (self.player1HasMoves() and self.player2HasMoves())

    def utility(self):
        return (self.player1 - self.player2)

    def getMoves(self):
        moves = []
        row = self.turn - 1
        for col in range(self.boardSize):
            if self.board[row][col] != 0:
                moves.append(col)
        return moves

    def nextState(self, move):
        copyNext = copy.deepcopy(self)
        if move != None:
            copyNext.move(move)
        if copyNext.turn == 1:
            copyNext.turn = 2
        return copyNext

class AlphaBetaPlayer:
    def __init__(self):
        return

    def getMove(self, state):
        return self.alphaBetaSearch(state)

    def alphaBetaSearch(self, state):
        alpha = -np.inf
        beta = np.inf
        bestAction = None
        possibleMoves= state.getMoves()
        for action in possibleMoves:
            val = self.minFunc(state.nextState(action), alpha, beta)
            if val > alpha:
                alpha = val
                bestAction = action
        return bestAction

    def maxFunc(self, state, alpha, beta):
        if state.gameEnd():
            return state.utility()
        val = -np.inf
        possibleMoves = state.getMoves()
        if possibleMoves == []:
            val = max(val, self.minFunc(state.nextState(None), alpha, beta))
            if val >= beta:
                return val
            alpha = max(alpha, val)
        else:
            for action in possibleMoves:
                val = max(val, self.minFunc(state.nextState(action), alpha, beta))
                if val >= beta:
                    return val
                alpha = max(alpha, val)
        return val

    def minFunc(self, state, alpha, beta):
        if state.gameEnd():
            return state.utility()
        val = np.inf
        possibleMoves = state.getMoves()
        if possibleMoves == []:
            val = min(val, self.maxFunc(state.nextState(None), alpha, beta))
            if val >= alpha:
                return val
            beta = min(beta, value)
        else:
            for action in state.getMoves():
                val = min(val, self.maxFunc(state.nextState(action), alpha, beta))
                if val >= alpha:
                    return val
                beta = min(beta, value)
        return val

mancala = Mancala(2, 6, 4)
print(mancala)
ABPlayer = AlphaBetaPlayer()

#selection = ABPlayer.alphaBetaSearch(mancala)
#print(selection)
#print(mancala)
mancala.play(ABPlayer)
