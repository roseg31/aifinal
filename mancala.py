import numpy as np
import copy
import random
import time

#Virtual mancala game: can choose
#play mode (which players to use),
#board size (add/remove pots)
#marble count (how many marbles start in each pot)
class Mancala:
    def __init__(self, playMode, boardSize, marbleCount):
        self.playMode = playMode # 1 = two humans, 2 = A-B bot vs human, 3 = MCTS bot vs human, 4= A-B bot vs MCTS bot
        self.boardSize = boardSize
        self.board = self.initBoard(boardSize, marbleCount)
        self.player1 = 0
        self.player2 = 0
        self.turn = 1
        self.turns1 = 0
        self.turns2 = 0

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

    def play(self, bot1, bot2):
        print(self)
        while self.player1HasMoves() or self.player2HasMoves():
            if self.turn == 1: #Player 1's turn
                print("Player 1's turn:")
                self.turns1 += 1
                if self.player1HasMoves() == False:
                    self.turns1 -= 1
                    print("Player 1 has no available moves.")
                    self.turn = 2
                elif self.playMode == 1: #Player 1 is human
                    move = self.getConsoleMove()
                    repeatFlag = self.move(move)
                    print(self)
                    if repeatFlag == True:
                        print("Player 1 gets to go again!")
                    else:
                        self.turn = 2
                elif self.playMode == 2 or self.playMode == 4: #Player 1 is Alpha-beta
                    print("Bot is thinking...")
                    move = bot1.alphaBetaSearch(copy.deepcopy(self))
                    #move = bot2.MCTS(copy.deepcopy(self))
                    print("Player 1 selects " + str(move))
                    repeatFlag = self.move(move)
                    print(self)
                    if repeatFlag == True:
                        print("Player 1 gets to go again!")
                    else:
                        self.turn = 2
                elif self.playMode == 3:
                    move = bot2.MCTS(copy.deepcopy(self))
                    print("Player 1 selects " + str(move))
                    repeatFlag = self.move(move)
                    print(self)
                    if repeatFlag == True:
                        print("Player 1 gets to go again!")
                    else:
                        self.turn = 2
            elif self.turn == 2:
                print("Player 2's turn:")
                self.turns2 += 1
                if self.player2HasMoves() == False:
                    self.turns2 -= 1
                    print("Player 2 has no available moves.")
                    self.turn = 1
                elif self.playMode != 4: #Player 2 is human
                    move = self.getConsoleMove()
                    repeatFlag = self.move(move)
                    print(self)
                    if repeatFlag == True:
                        print("Player 2 gets to go again!")
                    else:
                        self.turn = 1
                elif self.playMode == 4: #Player 2 is MCTS
                    move = bot2.MCTS(copy.deepcopy(self))
                    #move = bot1.alphaBetaSearch(copy.deepcopy(self))
                    print("Player 2 selects " + str(move))
                    repeatFlag = self.move(move)
                    print(self)
                    if repeatFlag == True:
                        print("Player 2 gets to go again!")
                    else:
                        self.turn = 1
        print("Game over!")

    #Function to get user input for the move -- takes ONLY integers!
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
        return False

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
        return not (self.player1HasMoves() and self.player2HasMoves())

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
        if copyNext.turn == 2:
            copyNext.turn = 1
        return copyNext

class AlphaBetaPlayer:
    def __init__(self, limit):
        self.limit = limit

    def getMove(self, state):
        return self.alphaBetaSearch(state)

    def alphaBetaSearch(self, state):
        alpha = -np.inf
        beta = np.inf
        bestAction = None
        possibleMoves= state.getMoves()
        for action in possibleMoves:
            val = self.minFunc(state.nextState(action), alpha, beta, 0)
            if val > alpha:
                alpha = val
                bestAction = action
        return bestAction

    def maxFunc(self, state, alpha, beta, count):
        if state.gameEnd() or count > self.limit:
            return state.utility()
        val = -np.inf
        possibleMoves = state.getMoves()
        if possibleMoves == []:
            val = max(val, self.minFunc(state.nextState(None), alpha, beta, count+1))
            if val >= beta:
                return val
            alpha = max(alpha, val)
        else:
            for action in possibleMoves:
                val = max(val, self.minFunc(state.nextState(action), alpha, beta, count+1))
                if val >= beta:
                    return val
                alpha = max(alpha, val)
        return val

    def minFunc(self, state, alpha, beta, count):
        if state.gameEnd() or count > self.limit:
            return state.utility()
        val = np.inf
        possibleMoves = state.getMoves()
        if possibleMoves == []:
            val = min(val, self.maxFunc(state.nextState(None), alpha, beta, count+1))
            if val >= alpha:
                return val
            beta = min(beta, value)
        else:
            for action in state.getMoves():
                val = min(val, self.maxFunc(state.nextState(action), alpha, beta, count+1))
                if val >= alpha:
                    return val
                beta = min(beta, val)
        return val

class MCTSPlayer:
    def __init__(self, limit):
        self.limit = limit

    def MCTS(self, state):
        root = MCTSNode(state=state)
        for i in range(self.limit):
            leaf = self.getLeaf(root)
            child = self.expand(leaf)
            result = self.simulate(child)
            self.backpropagate(child, result)

        maxStateNode = max(root.children, key=lambda p: p.N)
        return maxStateNode.action

    def getLeaf(self, node):
        if node.children:
            return self.getLeaf(max(node.children.keys(), key=ucb))
        else:
            return node

    def expand(self, node):
        if len(node.children)==0 and not node.state.gameEnd():
            node.children = {MCTSNode(parent=node, state=node.state.nextState(move), action=move): move
                                              for move in node.state.getMoves()}
        return self.getLeaf(node)

    def simulate(self, node):
        state = node.state
        while not state.gameEnd():
            action = random.choice(list(state.getMoves()))
            state = state.nextState(action)
        v = -state.utility()
        return -v

    def backpropagate(self, node, util):
        if util > 0:
            node.U += util
        node.N += 1
        if node.parent:
            self.backpropagate(node.parent, -util)


#node helper class for MCTS
class MCTSNode:
    def __init__(self, parent=None, state=None, action=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, action=action, U=U, N=N)
        self.state = state
        self.parent = parent
        self.children = {}
        self.actions = None

###################
######HELPERS######
###################

#ucb helper for MCTS
def ucb(n):
    return np.inf if n.N == 0 else n.U / n.N + np.sqrt(np.log(n.parent.N) / n.N)


############################
###Board/Game/Agent Setup###
############################

mancala = Mancala(1, 6, 4) #default 1,6,4
mancala2 = copy.deepcopy(mancala)
print(mancala)
ABPlayer = AlphaBetaPlayer(10)
mctsPlayer = MCTSPlayer(1000)

#Code for measuring time:

#t0 = time.time()
#selection = mctsPlayer.MCTS(mancala)
#t1 = time.time()
#print("TIME MCTS: " + str(t1-t0))
#print(selection)

#t0 = time.time()
#selection = ABPlayer.alphaBetaSearch(mancala2)
#t1 = time.time()
#print("TIME A-B: " + str(t1-t0))
#print(selection)

#mancala.play(ABPlayer)

#Play game
mancala.play(ABPlayer, mctsPlayer)
print("player 1: " + str(mancala.turns1))
print("player 2: " + str(mancala.turns2))
