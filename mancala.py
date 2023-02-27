class Mancala:
    def __init__(self, playMode, boardSize, marbleCount):
        self.playMode = playMode
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

    def play(self):
        print(self)
        while self.player1HasMoves() or self.player2HasMoves():
            if self.turn == 1: #Player 1's turn
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
            elif self.turn == 2:
                if self.player2HasMoves() == False:
                    print("Player 2 has no available moves.")
                    self.turn = 1
                elif self.playMode == 1:
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

        return False


mancala = Mancala(1, 6, 4)
print(mancala)
mancala.play()
