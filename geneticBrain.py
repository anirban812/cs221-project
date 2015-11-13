import random
import board

NUMSEQUENCES = 200
NUMGENERATIONS = 5
NUMMOVES = 8
SCALE = 2.0

class GeneticBrain:
    def getSequenceScore(self, inputBoard, moves):
        score = 0
        for move in moves:
            inputBoard.makeMove(move)
            score += inputBoard.evaluate()
            inputBoard.processBoard()
        inputBoard.rollback()
        return score
    
    def initializeSequences(self, inputBoard):
        moveSequences = []
        for i in xrange(NUMSEQUENCES):
            moves = []
            for j in xrange(NUMMOVES):
                movePosition = (random.randint(0,board.HEIGHT-1),random.randint(0,board.WIDTH-2))
                moves.append(movePosition)
            score = self.getSequenceScore(inputBoard, moves)
            moveSequences.append((pow(score,SCALE),moves))
        return moveSequences

    def pickSequence(self, moveSequences):
        total = sum(move[0] for move in moveSequences)
        choice = random.random()*total
        index = 0
        while choice > 0:
            choice -= moveSequences[index][0]
            index += 1
        return moveSequences[index-1][1]

    def spliceSequences(self, seq1, seq2):
        swapPoint = random.randint(0,NUMMOVES-1)
        child1 = []
        child2 = []
        for i in xrange(swapPoint):
            child1.append(seq1[i])
            child2.append(seq2[i])
        for i in xrange(swapPoint,NUMMOVES):
            child1.append(seq2[i])
            child2.append(seq1[i])
        return child1, child2

    def newGeneration(self, inputBoard, moveSequences):
        newMoveSequences = []
        for i in xrange(NUMSEQUENCES/2):
            seq1 = self.pickSequence(moveSequences)
            seq2 = self.pickSequence(moveSequences)
            child1, child2 = self.spliceSequences(seq1, seq2)
            newMoveSequences.append((pow(self.getSequenceScore(inputBoard, child1),SCALE),child1))
            newMoveSequences.append((pow(self.getSequenceScore(inputBoard, child2),SCALE),child2))
        return newMoveSequences

    def findBestActions(self, inputBoard):
        moveSequences = self.initializeSequences(inputBoard)
        for i in xrange(NUMGENERATIONS):
            moveSequences = self.newGeneration(inputBoard, moveSequences)
        bestSequence = []
        bestScore = 0.0
        for sequence in moveSequences:
            if sequence[0] > bestScore:
                bestScore = sequence[0]
                bestSequence = sequence[1]
        return self.getSequenceScore(inputBoard, bestSequence), bestSequence


testBoard = board.Board()
testBoard.loadFromFile('TestBoards/random_board2.txt')
testBoard.processBoard()
testBoard.printBoard()
print ""
genBrain = GeneticBrain()
score, actions = genBrain.findBestActions(testBoard)
for action in actions:
    testBoard.makeMove(action)
    testBoard.printBoard()
    print ""
    testBoard.processBoard()
testBoard.printBoard()
print ""
print score
print actions

        