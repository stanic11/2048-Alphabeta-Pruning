import math
import Logic
import constant as c


class Ai:
    def __init__(self, game):
        self.GAME = game
        self.alpha = -math.inf
        self.beta = +math.inf
        self.headNode = Node(self.GAME.matrix, 1, None)
        # self.depth = 6
        #########################
        self.smoothWeight = 0.1
        self.emptyWeight = 2.7
        self.maxWeight = 1.0
        self.monoWeight = 1.0  # 单调性权重
        ##########################

    def decide(self):
        node, value = self.alphaBetaSearch(self.headNode, c.nodeDepth, True)
        print("test")
        return node.move

    def alphaBetaSearch(self, node, depth, minimaxPlayer):
        if depth == 0 or self.GAME.gameState() == 'win':
            return node, self.eval(node.matrix.getMatrix())  # 返回节点和对应的值

        if minimaxPlayer:
            maxEval = -math.inf
            bestChild = None  # 用于记录最大值的子节点
            for child in node.sonNode:
                childNode, eValue = self.alphaBetaSearch(child, depth - 1, False)
                if eValue > maxEval:
                    maxEval = eValue
                    bestChild = childNode  # 更新最大值的子节点
                self.alpha = max(self.alpha, eValue)
                if self.alpha >= self.beta:
                    break
            return bestChild, maxEval  # 返回最大值所对应的子节点和值
        else:
            minEval = +math.inf
            bestChild = None  # 用于记录最小值的子节点
            for child in node.sonNode:
                childNode, eValue = self.alphaBetaSearch(child, depth - 1, True)
                if eValue < minEval:
                    minEval = eValue
                    bestChild = childNode  # 更新最小值的子节点
                self.beta = min(self.beta, eValue)
                if self.beta <= self.alpha:
                    break
            return bestChild, minEval  # 返回最小值所对应的子节点和值

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
        self.sonNode = []
        self.depth = depth
        self.matrix = matrix
        self.move = movement
        # 构造子节点
        if self.depth <= c.nodeDepth:
            self.sonNode.append(Node(self.matrix.right(True), self.depth + 1, "right"))
            self.sonNode.append(Node(self.matrix.left(True), self.depth + 1, "left"))
            self.sonNode.append(Node(self.matrix.up(True), self.depth + 1, "up"))
            self.sonNode.append(Node(self.matrix.down(True), self.depth + 1, "down"))
