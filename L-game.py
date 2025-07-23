import sys
import os
import math
from itertools import permutations

class LGame:
    def __init__(self):
        # this sets up a 4x4 grid filled with 0
        self.grid = [['0' for _ in range(4)] for _ in range(4)]
        # this is where player 1 starts
        self.p1Pos = [(0, 0), (0, 1), (0, 2), (1, 0)]
        # place player 1's piece on the board
        self.placePiece(self.p1Pos, 'L1')
        # this is where player 2 starts
        self.p2Pos = [(3, 3), (3, 2), (3, 1), (2, 3)]
        # place player 2's piece on the board
        self.placePiece(self.p2Pos, 'L2')
        # neutral pieces start here
        self.neutralPieces = [(1, 1), (2, 2)]
        # place neutral pieces on the board
        self.placeNeutralPieces()
        # these are different shapes of the l piece
        self.lPositions = {
            'N': [(0, 0), (1, 0), (2, 0), (2, 1)],
            'NM': [(0, 1), (1, 1), (2, 1), (2, 0)],
            'E': [(0, 0), (0, 1), (0, 2), (1, 0)],
            'EM': [(0, 0), (0, 1), (0, 2), (1, 2)],
            'S': [(0, 1), (0, 0), (1, 1), (2, 1)],
            'SM': [(0, 0), (1, 0), (2, 0), (2, -1)],
            'W': [(0, 2), (1, 0), (1, 1), (1, 2)],
            'WM': [(0, 0), (1, 0), (1, 1), (1, 2)],
        }
        # start with player 1
        self.currentPlayer = 'L1'
        self.p1Type = None
        self.p2Type = None
        self.aiDepth = None
        # cache for storing states
        self.cache = {}

    def clearScreen(self):
        # clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')

    def isValidMove(self, positions):
        # check if all positions are on board and empty
        for x, y in positions:
            if not (0 <= x < 4 and 0 <= y < 4):
                return False
            if self.grid[x][y] != '0':
                return False
        return True

    def genLegalMoves(self, player):
        # generate all moves that player can do
        currPos = self.p1Pos if player == 'L1' else self.p2Pos
        # remove player piece first
        for x, y in currPos:
            self.grid[x][y] = '0'
        legalMoves = []
        # try placing l piece in different spots
        for i in range(4):
            for j in range(4):
                for pos in self.lPositions.values():
                    newPos = [(i + dx, j + dy) for dx, dy in pos]
                    if self.isValidMove(newPos):
                        legalMoves.append(newPos)
        # remove any moves that are same as current position
        currPosPermutations = list(permutations(currPos))
        legalMoves = [
            move for move in legalMoves
            if tuple(sorted(move)) not in map(tuple, map(sorted, currPosPermutations))
        ]
        # put player piece back
        for x, y in currPos:
            self.grid[x][y] = player
        return legalMoves

    def placePiece(self, positions, player):
        # place a piece on the board
        for x, y in positions:
            self.grid[x][y] = player

    def removePiece(self, positions):
        # remove a piece from the board
        for x, y in positions:
            self.grid[x][y] = '0'

    def placeNeutralPieces(self):
        # place the two neutral pieces
        for x, y in self.neutralPieces:
            self.grid[x][y] = 'N'

    def printGrid(self):
        # show the board
        self.clearScreen()
        for row in self.grid:
            print(" | ".join(f"{cell:2}" for cell in row))
            print("-" * 17)

    def parseInput(self, input_str):
        # parse the move that user types
        parts = input_str.split()
        if len(parts) != 3 and len(parts) != 7:
            print("Invalid Format")
            return None, None
        x, y = int(parts[1])-1, int(parts[0])-1
        orientation = parts[2].lower()
        initial_nx, initial_ny = 0, 0
        final_nx, final_ny = 0, 0
        if len(parts) == 7:
            initial_nx, initial_ny = int(parts[4])-1, int(parts[3])-1
            final_nx, final_ny =int(parts[6])-1, int(parts[5])-1
        if orientation == 'n':
            valid_moves = [(x-1, y-1), (x, y-1), (x, y), (x-1, y)]
            valid_moves_mirrored = [(x-1, y), (x, y), (x, y+1), (x, y+2)]
        elif orientation == 's':
            valid_moves = [(x, y-2), (x, y-1), (x, y), (x+1, y)]
            valid_moves_mirrored = [(x+1, y), (x, y), (x, y+1), (x, y+2)]
        elif orientation == 'e':
            valid_moves = [(x-2, y), (x-1, y), (x, y), (x, y+1)]
            valid_moves_mirrored = [(x+1, y), (x+2, y), (x, y), (x, y+1)]
        elif orientation == 'w':
            valid_moves = [(x, y-1), (x, y), (x+1, y-1), (x+1, y)]
            valid_moves_mirrored = [(x, y-1), (x, y), (x+1, y), (x+2, y)]
        else:
            print(f"Unknown orientation: {orientation}")
            return None, None
        
        if len(parts) == 7:
            # check if neutral piece move is valid
            if initial_nx < 0 or initial_nx >= 4 or initial_ny < 0 or initial_ny >= 4 or self.grid[initial_nx][initial_ny] != 'N':
                print("Invalid Initial Neutral Coordinates")
                return None, None
            
            if final_nx < 0 or final_nx >= 4 or final_ny < 0 or final_ny >= 4:
                print("Invalid Final Neutral Coordinates")
                return None, None

        legal_moves = self.genLegalMoves(self.currentPlayer)
        valid_moves_set = set(valid_moves)
        valid_moves_mirrored_set = set(valid_moves_mirrored)
        legal_moves_sets = [set(move) for move in legal_moves]        

        final_coords = (final_nx, final_ny)
        if valid_moves_set in legal_moves_sets:
            if final_coords in valid_moves_set:
                print("Invalid Final Neutral Coordinates")
                return None, None
        elif valid_moves_mirrored_set in legal_moves_sets:
            if final_coords in valid_moves_mirrored_set:
                print("Invalid Final Neutral Coordinates")
                return None, None

        new_l_position = None
        if valid_moves_set in legal_moves_sets:
            new_l_position = valid_moves
        elif valid_moves_mirrored_set in legal_moves_sets:
            new_l_position = valid_moves_mirrored
        if new_l_position:
            return new_l_position, [initial_nx, initial_ny, final_nx, final_ny]
        print("Invalid Move")
        return None, None
    

    def editInitialState(self, input_str):
        # change the starting layout based on user input
        initial_parts = input_str.split()
        self.p1Pos = []
        self.p2Pos = []
        self.grid = [['0' for _ in range(4)] for _ in range(4)]
        self.printGrid()

        
        if len(initial_parts) != 10:
            print("Invalid Format")
            return None
        
        neutral_x1, neutral_y1 = 0, 0
        neutral_x2, neutral_y2 = 0, 0

        l1x, l1y = int(initial_parts[1]) - 1, int(initial_parts[0]) - 1
        l1_orientation = initial_parts[2].lower()

        l2x, l2y = int(initial_parts[8]) - 1, int(initial_parts[7]) - 1
        l2_orientation = initial_parts[9].lower()

        neutral_x1, neutral_y1 = int(initial_parts[4]) - 1, int(initial_parts[3]) - 1
        neutral_x2, neutral_y2 = int(initial_parts[6]) - 1, int(initial_parts[5]) - 1

        if l1_orientation == 'n':
            valid_moves = [(l1x-1, l1y-1), (l1x, l1y-1), (l1x, l1y), (l1x-1, l1y)]
            valid_moves_mirrored = [(l1x-1, l1y), (l1x, l1y), (l1x, l1y+1), (l1x, l1y+2)]
        elif l1_orientation =='s':
            valid_moves = [(l1x, l1y-2), (l1x, l1y-1), (l1x, l1y), (l1x+1, l1y)]
            valid_moves_mirrored = [(l1x+1, l1y), (l1x, l1y), (l1x, l1y+1), (l1x, l1y+2)]
        elif l1_orientation == 'e':
            valid_moves = [(l1x-2, l1y), (l1x-1, l1y), (l1x, l1y), (l1x, l1y+1)]
            valid_moves_mirrored = [(l1x+1, l1y), (l1x+2, l1y), (l1x, l1y), (l1x, l1y+1)]
        elif l1_orientation == 'w':
            valid_moves = [(l1x, l1y-1), (l1x, l1y), (l1x+1, l1y-1), (l1x+1, l1y)]
            valid_moves_mirrored = [(l1x, l1y-1), (l1x, l1y), (l1x+1, l1y), (l1x+2, l1y)]
        else:
            print(f"Unknown orientation")
            return None, None
        
        legal_moves = self.genLegalMoves(self.currentPlayer)
        valid_moves_set = set(valid_moves)
        valid_moves_mirrored_set = set(valid_moves_mirrored)
        legal_moves_sets = [set(move) for move in legal_moves]

        if valid_moves_set in legal_moves_sets:
            self.p1Pos = valid_moves_mirrored
            self.placePiece(self.p1Pos, 'L1')
        elif valid_moves_mirrored_set in legal_moves_sets:
            self.p1Pos = valid_moves_mirrored
            self.placePiece(self.p1Pos, 'L1')
        

        if l2_orientation== 'n':
            valid_moves = [(l2x-1, l2y-1), (l2x, l2y-1), (l2x, l2y), (l2x-1, l2y)]
            valid_moves_mirrored = [(l2x-1, l2y), (l2x, l2y), (l2x, l2y+1), (l2x, l2y+2)]
        elif l2_orientation == 's':
            valid_moves = [(l2x, l2y-2), (l2x, l2y-1), (l2x, l2y), (l2x+1, l2y)]
            valid_moves_mirrored = [(l2x+1, l2y), (l2x, l2y), (l2x, l2y+1), (l2x, l2y+2)]
        elif l2_orientation== 'e':
            valid_moves = [(l2x-2, l2y), (l2x-1, l2y), (l2x, l2y), (l2x, l2y+1)]
            valid_moves_mirrored = [(l2x+1, l2y), (l2x+2, l2y), (l2x, l2y), (l2x, l2y+1)]
        elif l2_orientation == 'w':
            valid_moves = [(l2x, l2y-1), (l2x, l2y), (l2x+1, l2y-1), (l2x+1, l2y)]
            valid_moves_mirrored = [(l2x, l2y-1), (l2x, l2y), (l2x+1, l2y), (l2x+2, l2y)]
        else:
            print(f"Unknown orientation")
            return None, None
        
        legal_moves = self.genLegalMoves(self.currentPlayer)
        valid_moves_set = set(valid_moves)
        valid_moves_mirrored_set = set(valid_moves_mirrored)
        legal_moves_sets = [set(move) for move in legal_moves]

        if valid_moves_set in legal_moves_sets:
            self.p2Pos = valid_moves
            self.placePiece(self.p2Pos, 'L2')
        elif valid_moves_mirrored_set in legal_moves_sets:
            self.p2Pos = valid_moves_mirrored 
            self.placePiece(self.p2Pos, 'L2')
        
        if neutral_x1 < 0 or neutral_x1 >= 4 or neutral_y1 < 0 or neutral_y1 >= 4 or self.grid[neutral_x1][neutral_y1] != '0' or neutral_x2 < 0 or neutral_x2 >= 4 or neutral_y2 < 0 or neutral_y2 >= 4 or self.grid[neutral_x2][neutral_y2] != '0':
            print("Invalid Neutral Coordinates")
            return None, None
        else: 
            self.neutralPieces = [(neutral_x1, neutral_y1), (neutral_x2, neutral_y2)]
            self.placeNeutralPieces()



    def startGame(self):
        # start the game loop
        while True:
            choice = input("Select an option: (1) Start Game, (2) Edit Starting States: ")
            if choice == '1':
                break 
            elif choice == '2':
                inputstr = input("Enter New Initial State: ")
                self.editInitialState(inputstr)
                break  
            else:
                print("Invalid input. Please select '1' to start the game or '2' to edit the starting states.")

        while True:
            mode = input("Select mode: (1) Human vs Human, (2) Human vs Computer, (3) Computer vs Computer: ")
            if mode in ['1', '2', '3']:
                break
        if mode == '1':
            self.p1Type = 'human'
            self.p2Type = 'human'
        elif mode == '2':
            self.p1Type = 'human'
            self.p2Type = 'ai'
        else:
            self.p1Type = 'ai'
            self.p2Type = 'ai'
        first = input("Who goes first? Enter '1' for Player1, '2' for Player2: ")
        if first == '2':
            self.currentPlayer = 'L2'
        else:
            self.currentPlayer = 'L1'
        if self.p1Type == 'ai' or self.p2Type == 'ai':
            d = input("Enter search depth (e.g. 3): ")
            if d.isdigit():
                self.aiDepth = int(d) + 5
            else:
                self.aiDepth = 10
        while True:
            legalMoves = self.genLegalMoves(self.currentPlayer)
            if len(legalMoves) <= 1:
                winner = 'L2' if self.currentPlayer == 'L1' else 'L1'
                print(f"No legal moves left for {self.currentPlayer}. {winner} wins!")
                break
            self.printGrid()
            print(f"Current Player: {self.currentPlayer}")
            cType = self.p1Type if self.currentPlayer == 'L1' else self.p2Type
            if cType == 'human':
                chosenMove = None
                while chosenMove == None:
                    userInput = input("Enter your move: ")
                    if userInput.lower() == 'q':
                        print("Quitting the game.")
                        return 0
                    chosenMove, chosenNeutralMove = self.parseInput(userInput)
            else:
                chosenMove = self.chooseAiMoveMinimax(legalMoves, self.currentPlayer, self.aiDepth)
                chosenNeutralMove = None
            self.makeMove(chosenMove)
            self.printGrid()
            self.moveNeutralPiece(chosenNeutralMove)
            self.printGrid()
            self.currentPlayer = 'L2' if self.currentPlayer == 'L1' else 'L1'

    def makeMove(self, newPositions):
        # make the chosen move
        oldPositions = self.p1Pos if self.currentPlayer == 'L1' else self.p2Pos
        self.removePiece(oldPositions)
        self.placePiece(newPositions, self.currentPlayer)
        if self.currentPlayer == 'L1':
            self.p1Pos = newPositions
        else:
            self.p2Pos = newPositions

    def moveNeutralPiece(self, chosenNeutralMove):
        # move the neutral piece if human chosen
        cType = self.p1Type if self.currentPlayer == 'L1' else self.p2Type

        if cType == 'human':
            if chosenNeutralMove is not None:
                oldX, oldY, newX, newY = chosenNeutralMove

                if (oldX, oldY) not in self.neutralPieces:
                    print("Error: Invalid starting neutral piece position.")
                    return

                if self.grid[newX][newY] != '0':
                    print("Error: Target position is not empty.")
                    return

                self.grid[oldX][oldY] = '0'
                self.grid[newX][newY] = 'N'

                for idx, piece in enumerate(self.neutralPieces):
                    if piece == (oldX, oldY):
                        self.neutralPieces[idx] = (newX, newY)
                        break

        else:
            # if ai is playing, let it pick neutral move
            if not self.neutralPieces:
                return

            aiMove = self.chooseAiNeutralMove()
            if aiMove is not None:
                pieceIndex, newX, newY = aiMove
                oldX, oldY = self.neutralPieces[pieceIndex]

                self.grid[oldX][oldY] = '0'
                self.grid[newX][newY] = 'N'

                self.neutralPieces[pieceIndex] = (newX, newY)

        self.validateNeutralPieces()


    def validateNeutralPieces(self):
        # make sure we always have two neutral pieces
        neutral_count = sum(cell == 'N' for row in self.grid for cell in row)
        if neutral_count != 2:
            print(f"Error: Invalid number of neutral pieces ({neutral_count}). Resetting...")
            self.resetNeutralPieces()



    def chooseAiMoveMinimax(self, legalMoves, player, depth):
        # choose best move using minimax with alpha beta pruning
        opponent = 'L1' if player == 'L2' else 'L2'
        bestMove = None
        bestValue = -math.inf
        alpha = -math.inf
        beta = math.inf
        originalGrid = [row[:] for row in self.grid]
        originalP1Pos = self.p1Pos[:]
        originalP2Pos = self.p2Pos[:]
        originalNeutrals = self.neutralPieces[:]
        for move in legalMoves:
            self.simulateMove(player, move)
            value = self.minimax(opponent, depth - 1, alpha, beta, maximizing=(opponent == 'L2'))
            self.restoreState(originalGrid, originalP1Pos, originalP2Pos)
            self.neutralPieces = originalNeutrals[:]
            if value > bestValue:
                bestValue = value
                bestMove = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return bestMove

    def minimax(self, player, depth, alpha, beta, maximizing):
        # minimax algorithm with caching
        key = (tuple(tuple(row) for row in self.grid), tuple(self.p1Pos), tuple(self.p2Pos), tuple(sorted(self.neutralPieces)), player, depth, maximizing)
        if key in self.cache:
            return self.cache[key]
        if depth == 0:
            v = self.heuristicEvaluation()
            self.cache[key] = v
            return v
        legalMoves = self.genLegalMoves(player)
        if not legalMoves:
            v = self.heuristicEvaluation()
            self.cache[key] = v
            return v
        opponent = 'L1' if player == 'L2' else 'L2'
        originalGrid = [row[:] for row in self.grid]
        originalP1Pos = self.p1Pos[:]
        originalP2Pos = self.p2Pos[:]
        originalNeutrals = self.neutralPieces[:]
        if maximizing:
            value = -math.inf
            for move in legalMoves:
                self.simulateMove(player, move)
                score = self.minimax(opponent, depth - 1, alpha, beta, maximizing=(opponent=='L2'))
                self.restoreState(originalGrid, originalP1Pos, originalP2Pos)
                self.neutralPieces = originalNeutrals[:]
                value = max(value, score)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            self.cache[key] = value
            return value
        else:
            value = math.inf
            for move in legalMoves:
                self.simulateMove(player, move)
                score = self.minimax(opponent, depth - 1, alpha, beta, maximizing=(opponent=='L2'))
                self.restoreState(originalGrid, originalP1Pos, originalP2Pos)
                self.neutralPieces = originalNeutrals[:]
                value = min(value, score)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            self.cache[key] = value
            return value

    def simulateMove(self, player, move):
        # simulate placing the piece in new position
        oldPositions = self.p1Pos if player == 'L1' else self.p2Pos
        self.removePiece(oldPositions)
        self.placePiece(move, player)
        if player == 'L1':
            self.p1Pos = move
        else:
            self.p2Pos = move

    def heuristicEvaluation(self):
        # basic heuristic: difference in number of moves
        l1Moves = len(self.genLegalMoves('L1'))
        l2Moves = len(self.genLegalMoves('L2'))
        return l2Moves - l1Moves

    def chooseAiNeutralMove(self):
        # ai tries moving neutral pieces to reduce opponent moves
        player = self.currentPlayer
        opponent = 'L1' if player == 'L2' else 'L2'
        bestMove = None
        bestScore = self.evaluateOpponentMoves(opponent)
        originalNeutrals = self.neutralPieces[:]
        originalGrid = [row[:] for row in self.grid]
        originalP1Pos = self.p1Pos[:]
        originalP2Pos = self.p2Pos[:]
        for i, (nx, ny) in enumerate(self.neutralPieces):
            self.grid[nx][ny] = '0'
            for x in range(4):
                for y in range(4):
                    if self.grid[x][y] == '0':
                        self.grid[x][y] = 'N'
                        self.neutralPieces[i] = (x, y)
                        newScore = self.evaluateOpponentMoves(opponent)
                        if newScore < bestScore:
                            bestScore = newScore
                            bestMove = (i, x, y)
                        self.grid[x][y] = '0'
                        self.neutralPieces[i] = (nx, ny)
            self.grid[nx][ny] = 'N'
        self.restoreState(originalGrid, originalP1Pos, originalP2Pos)
        self.neutralPieces = originalNeutrals
        return bestMove

    def evaluateOpponentMoves(self, opponent):
        # check how many moves opponent can do
        return len(self.genLegalMoves(opponent))

    def restoreState(self, originalGrid, originalP1Pos, originalP2Pos):
        # restore board and positions to previous state
        for i in range(4):
            for j in range(4):
                self.grid[i][j] = originalGrid[i][j]
        self.p1Pos = originalP1Pos[:]
        self.p2Pos = originalP2Pos[:]

if __name__ == "__main__":
    game = LGame()
    game.startGame()
