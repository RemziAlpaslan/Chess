"""This class is responsible for staring all the information about the current state of a cheese game. It will also ve
responsible for determine the void moves at the current state. It will also a move log."""


class GameState:
    def __init__(self):
        # board is a 8x8 2d list, each element of the list has 2 characters.
        # The first character represents the color of the piece, "b" or "w".
        # The  second character represents the type of the piece, "K", "Q", "R", "B", "N" or "P"
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves, }
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False

    """
    Takes a Move as a parameter and executes it this will not work for castling, pawn promotion, and en-passant
    """

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "__"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # lof the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap players
        # update the king's location if moved
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.whiteKingLocation = (move.endRow, move.endCol)

    """
    Undo the last move made
    """

    def udoMove(self):
        if len(self.moveLog) != 0:  # make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back
            # update the king's location if moved
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.whiteKingLocation = (move.startRow, move.startCol)

    """
    All move considering checks
    """

    def getValidMoves(self):
        # 1.) generate all possible moves
        moves = self.getAllPossibleMoves()
        # 2.) for each move, make the move
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            # 3.) generate all opponent' s moves
            # 4.) for each of your opponent' s moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])  # 5.) if they do attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove
            self.udoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves  # for now, we will not worry about checks

    """
    Determine if the current player is in check
    """

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    """
    Determine if the enemy can attack the square r,c
    """

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # switch to opponent' s turn
        oopMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # switch turns back
        for move in oopMoves:
            if move.endRow == r and move.endCol == c:  # square is under attack
                return True
        return False

    """
    All Moves without considering checks
    """

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # calls the appropriate move function based on piece type
        return moves

    """
    Get all the pawn moves for the pawn located at row, col and add these moves to the list 
    """

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves
            if self.board[r - 1][c] == "__":  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "__":  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # captures to left
                if self.board[r - 1][c - 1][0] == "b":  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to right
                if self.board[r - 1][c + 1][0] == "b":  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        if not self.whiteToMove:  # black pawn moves
            if self.board[r + 1][c] == "__":  # 1 square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "__":  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # captures to left
                if self.board[r + 1][c - 1][0] == "w":  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:  # captures to right
                if self.board[r + 1][c + 1][0] == "w":  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    """
    Get all the rook moves for the pawn located at row, col and add these moves to the list 
    """

    def getRookMoves(self, r, c, moves):
        if self.whiteToMove:  # white rook moves
            C = "w"
        else:
            C = "b"

        for i in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            a = 1
            b = 1
            while 0 <= r + a * i[0] <= 7 and 0 <= c + b * i[1] <= 7:
                if self.board[r + a * i[0]][c + a * i[1]] == "__":
                    moves.append(Move((r, c), (r + a * i[0], c + b * i[1]), self.board))
                    a += 1
                    b += 1
                elif self.board[r + a * i[0]][c + b * i[1]][0] != C:
                    moves.append(Move((r, c), (r + a * i[0], c + b * i[1]), self.board))
                    break
                else:
                    break

    """
        Get all the knight moves for the pawn located at row, col and add these moves to the list 
        """

    def getKnightMoves(self, r, c, moves):
        if self.whiteToMove:  # white rook moves
            C = "w"
        else:
            C = "b"
        for a in [2, -2]:
            for b in [1, -1]:
                if 0 <= r + a <= 7 and 0 <= c + b <= 7:
                    if self.board[r + a][c + b][0] != C:
                        moves.append(Move((r, c), (r + a, c + b), self.board))
                if 0 <= r + b <= 7 and 0 <= c + a <= 7:
                    if self.board[r + b][c + a][0] != C:
                        moves.append(Move((r, c), (r + b, c + a), self.board))

    """
        Get all the bishop moves for the pawn located at row, col and add these moves to the list 
        """

    def getBishopMoves(self, r, c, moves):
        if self.whiteToMove:  # white rook moves
            C = "w"
        else:
            C = "b"

        for i in [[1, 1], [1, -1], [-1, 1], [-1, -1]]:
            a = 1
            b = 1
            while 0 <= r + a * i[0] <= 7 and 0 <= c + b * i[1] <= 7:
                if self.board[r + a * i[0]][c + a * i[1]] == "__":
                    moves.append(Move((r, c), (r + a * i[0], c + b * i[1]), self.board))
                    a += 1
                    b += 1
                elif self.board[r + a * i[0]][c + b * i[1]][0] != C:
                    moves.append(Move((r, c), (r + a * i[0], c + b * i[1]), self.board))
                    break
                else:
                    break

    """
        Get all the queen moves for the pawn located at row, col and add these moves to the list 
        """

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    """
        Get all the king moves for the pawn located at row, col and add these moves to the list 
        """

    def getKingMoves(self, r, c, moves):
        if self.whiteToMove:  # white rook moves
            C = "w"
        else:
            C = "b"
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if 0 <= r + a <= 7 and 0 <= c + a <= 7:
                    if self.board[r + a][c + b][0] != C:
                        moves.append(Move((r, c), (r + a, c + b), self.board))


class Move:
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0, }
    rowsToRank = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)

    """
    Overriding the equals method
    """

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        # you can add to make this like real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRank[r]
