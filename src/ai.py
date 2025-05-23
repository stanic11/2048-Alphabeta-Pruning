import math
import Logic
import constant as c
import pygame

class Ai:
    def __init__(self, game):
        self.GAME = game
        self.headNode = None  # Don't create the tree yet
        #########################
        self.smoothWeight = 0.1
        self.emptyWeight = 2.7
        self.maxWeight = 1.0
        self.monoWeight = 1.0  # 单调性权重
        ##########################

    def decide(self):
        # Reset alpha-beta values for each decision
        self.alpha = -math.inf
        self.beta = +math.inf
        
        # Create head node with initial state
        self.headNode = Node(self.GAME.matrix, 1, None)
        
        # Use a reduced depth for faster processing
        reduced_depth = 3  # Using 3 instead of 6 for better performance
        
        node, value = self.alphaBetaSearch(self.headNode, reduced_depth, True)
        print("AI chose move:", node.move)
        return node.move

    def alphaBetaSearch(self, node, depth, minimaxPlayer):
        # Process events occasionally to keep UI responsive
        if depth % 2 == 0:  # Check events every other depth level
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()

        if depth == 0 or self.GAME.gameState() == 'win':
            return node, self.eval(node.matrix.getMatrix())  # 返回节点和对应的值

        if minimaxPlayer:
            maxEval = -math.inf
            bestChild = node  # Default to self if no better move is found
            for child in node.getChildren():  # Use lazy child generation
                childNode, eValue = self.alphaBetaSearch(child, depth - 1, False)
                if eValue > maxEval:
                    maxEval = eValue
                    bestChild = child  # Store the immediate child, not the deep one
                self.alpha = max(self.alpha, eValue)
                if self.alpha >= self.beta:
                    break
            return bestChild, maxEval
        else:
            minEval = +math.inf
            bestChild = node  # Default to self if no better move is found
            for child in node.getChildren():  # Use lazy child generation
                childNode, eValue = self.alphaBetaSearch(child, depth - 1, True)
                if eValue < minEval:
                    minEval = eValue
                    bestChild = child  # Store the immediate child, not the deep one
                self.beta = min(self.beta, eValue)
                if self.beta <= self.alpha:
                    break
            return bestChild, minEval

    def eval(self, matrix):
        emptyCounts = self.getEmptyCounts(matrix)
        if emptyCounts != 0:
            return (self.getSmoothness(matrix) * self.smoothWeight +
                    self.getMonotonicity(matrix) * self.monoWeight +
                    math.log(emptyCounts) * self.emptyWeight +
                    self.getMaxValue(matrix) * self.maxWeight)
        else:
            return 0

    def machineOperator(self, node):
        for child in node:
            valueList = []
            matrixIndex = []
            for i in range(c.ROW):
                for j in range(c.COLUMN):
                    tmpMatrix = self.GAME.matrix
                    if tmpMatrix[i][j] == 0:
                        tmpMatrix.gridChange(i, j, 2)
                        valueList.append(self.eval(tmpMatrix.getMatrix()))
                        matrixIndex.append([i, j, 2])

                        tmpMatrix.gridChange(i, j, 4)
                        valueList.append(self.eval(tmpMatrix.getMatrix()))
                        matrixIndex.append([i, j, 4])
            index = valueList.index(min(valueList))
            child.matrix = child.matrix.gridChange(matrixIndex[index][0], matrixIndex[index][1], matrixIndex[index][2])

    def getSmoothness(self, matrix):
        # 计算每格平滑度
        smoothness = 0
        for i in range(c.ROW):
            for j in range(c.COLUMN):
                if matrix[i][j] != 0:
                    value = math.log(matrix[i][j]) / math.log(2)
                    # 行处理
                    tmpMatrix = matrix[i]
                    for k in range(len(tmpMatrix)):
                        if tmpMatrix[k] != 0 and k != j:
                            targetValue = math.log(tmpMatrix[k]) / math.log(2)
                            smoothness -= math.fabs(value - targetValue)
                        else:
                            smoothness -= value
                    # 列处理
                    colMatrix = Logic.getColMatrix(matrix, j)
                    for k in range(len(colMatrix)):
                        if colMatrix[k] != 0 and k != i:
                            targetValue = math.log(colMatrix[k]) / math.log(2)
                            smoothness -= math.fabs(value - targetValue)
                        else:
                            smoothness -= value
        return smoothness

    def getMonotonicity(self, matrix):
        scoreList = [0, 0, 0, 0]

        for x in range(c.ROW):
            current = 0
            next = current + 1
            while (next < 4):
                while next < 4 and matrix[x][next] == 0:
                    next += 1

                if next >= 4:
                    next -= 1
                if matrix[x][current] != 0:
                    currentValue = math.log(matrix[x][current]) / math.log(2)
                else:
                    currentValue = 0

                if matrix[x][next] != 0:
                    nextValue = math.log(matrix[x][next]) / math.log(2)
                else:
                    nextValue = 0

                if currentValue > nextValue:
                    scoreList[0] += nextValue - currentValue
                elif nextValue > currentValue:
                    scoreList[1] += currentValue - nextValue
                current = next
                next += 1

        for y in range(c.ROW):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and matrix[next][y] == 0:
                    next += 1
                if next >= 4:
                    next -= 1

                if matrix[current][y] != 0:
                    currentValue = math.log(matrix[current][y]) / math.log(2)
                else:
                    currentValue = 0

                if matrix[next][y] != 0:
                    nextValue = math.log(matrix[next][y]) / math.log(2)
                else:
                    nextValue = 0

                if currentValue > nextValue:
                    scoreList[2] += nextValue - currentValue
                elif nextValue > currentValue:
                    scoreList[3] += currentValue - nextValue
                current = next
                next += 1
        return max(scoreList[0], scoreList[1]) + max(scoreList[2], scoreList[3])

    def getEmptyCounts(self, matrix):
        counts = 0
        for i in range(c.ROW):
            for j in range(c.COLUMN):
                if matrix[i][j] == 0:
                    counts += 1
        return counts

    def getMaxValue(self, matrix):
        MAX = matrix[0][0]
        for i in range(c.ROW):
            for j in range(c.COLUMN):
                if matrix[i][j] >= MAX:
                    MAX = matrix[i][j]
        return MAX


class Node:
    def __init__(self, matrix, depth, movement):
        self.sonNode = []  # Start with empty list, generate children on demand
        self.depth = depth
        self.matrix = matrix
        self.move = movement
        self._children_generated = False

    def getChildren(self):
        # Lazy generation of children only when needed
        if not self._children_generated and self.depth <= 3:  # Reduced depth
            self.sonNode.append(Node(self.matrix.right(True), self.depth + 1, "right"))
            self.sonNode.append(Node(self.matrix.left(True), self.depth + 1, "left"))
            self.sonNode.append(Node(self.matrix.up(True), self.depth + 1, "up"))
            self.sonNode.append(Node(self.matrix.down(True), self.depth + 1, "down"))
            self._children_generated = True
        return self.sonNode