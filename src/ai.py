import math

import Logic
import constant as c


class Ai:
    def __init__(self):
        self.GAME = Logic.game()
        self.alpha = -math.inf
        self.beta = +math.inf
        self.headNode = Node(self.GAME.matrix, 1)
        self.depth = 6
        #########################
        self.smoothWeight = 0.1
        self.emptyWeight = 2.7
        self.maxWeight = 1.0
        self.monoWeight = 1.0  # 单调性权重
        ##########################

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
        emptyCounts = math.fabs(self.getEmptyCounts(matrix))
        if emptyCounts == 0:
            return (self.getSmoothness(matrix) * self.smoothWeight +
                    self.getMonotonicity(matrix) * self.monoWeight +
                    self.getMaxValue(matrix) * self.maxWeight)
        return (self.getSmoothness(matrix) * self.smoothWeight +
                self.getMonotonicity(matrix) * self.monoWeight +
                math.log(emptyCounts) * self.emptyWeight +
                self.getMaxValue(matrix) * self.maxWeight)

    # 暂不考虑
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

    @classmethod
    def getSmoothness(cls, matrix):
        # 计算每格平滑度
        smoothness = 0
        for i in range(c.ROW):
            for j in range(c.COLUMN):
                if matrix[i][j] != 0:
                    value = math.log(matrix[i][j]) / math.log(2)
                    # 该行处理
                    tmpMatrix = matrix[i]

        # 先对每一行进行单独求解
        for i in range(c.ROW):
            tmpMatrix = matrix[i]
            for j in range(len(tmpMatrix) - 1):
                if tmpMatrix[j] != 0:
                    for k in range(j + 1, len(tmpMatrix)):
                        if tmpMatrix[k] != 0:
                            smoothness -= math.log(math.fabs(tmpMatrix[k] - tmpMatrix[j])) / math.log(2)
                            break

        # 对每一列求解
        for j in range(c.COLUMN):
            tmpMatrix = []
            for i in range(c.ROW):
                # 抽出矩阵的每一列
                tmpMatrix.append(matrix[i][j])
            for k in range(len(tmpMatrix) - 1):
                if tmpMatrix[k] != 0:
                    for t in range(k + 1, len(tmpMatrix)):
                        if tmpMatrix[t] != 0:
                            smoothness -= math.log(math.fabs(tmpMatrix[k] - tmpMatrix[t])) / math.log(2)
                            break
        return smoothness

    @classmethod
    def getMonotonicity(cls, matrix):
        scoreList = [0, 0, 0, 0]
        # Right
        for i in range(c.ROW):
            tmpMatrix = matrix[i]
            for j in range(len(tmpMatrix) - 1):
                if tmpMatrix[j] != 0:
                    for k in range(j + 1, len(tmpMatrix)):
                        if tmpMatrix[k] != 0:
                            if tmpMatrix[j] >= tmpMatrix[k]:
                                scoreList[0] += math.log(tmpMatrix[k]) / math.log(2) - math.log(
                                    tmpMatrix[j]) / math.log(2)
                            else:
                                scoreList[1] += math.log(tmpMatrix[k]) / math.log(2) - math.log(
                                    tmpMatrix[j]) / math.log(2)
        # Left
        for i in range(c.ROW):
            tmpMatrix = matrix[i]
            for j in range(len(tmpMatrix) - 1, 0, -1):
                if tmpMatrix[j] != 0:
                    for k in range(j - 1, len(tmpMatrix), -1):
                        if tmpMatrix[k] != 0:
                            if tmpMatrix[j] >= tmpMatrix[k]:
                                scoreList[0] += math.log(tmpMatrix[k]) / math.log(2) - math.log(
                                    tmpMatrix[j]) / math.log(2)
                            else:
                                scoreList[1] += math.log(tmpMatrix[k]) / math.log(2) - math.log(
                                    tmpMatrix[j]) / math.log(2)

        # Up
        for j in range(c.COLUMN):
            tmpMatrix = []
            for i in range(c.ROW):
                # 抽出矩阵的每一列
                tmpMatrix.append(matrix[i][j])
            for k in range(len(tmpMatrix) - 1):
                if tmpMatrix[k] != 0:
                    for t in range(k + 1, len(tmpMatrix)):
                        if tmpMatrix[t] != 0:
                            if tmpMatrix[k] >= tmpMatrix[t]:
                                scoreList[2] += math.log(tmpMatrix[k]) / math.log(2) - math.log(
                                    tmpMatrix[t]) / math.log(2)
                            else:
                                scoreList[3] += math.log(tmpMatrix[k]) / math.log(2) - math.log(
                                    tmpMatrix[t]) / math.log(2)
        # Down
        for j in range(c.COLUMN):
            tmpMatrix = []
            for i in range(c.ROW):
                # 抽出矩阵的每一列
                tmpMatrix.append(matrix[i][j])
            for k in range(len(tmpMatrix) - 1, 0, -1):
                if tmpMatrix[k] != 0:
                    for t in range(k - 1, len(tmpMatrix), -1):
                        if tmpMatrix[t] != 0:
                            if tmpMatrix[k] >= tmpMatrix[t]:
                                scoreList[2] += math.log(tmpMatrix[k]) / math.log(2) - math.log(
                                    tmpMatrix[t]) / math.log(2)
                            else:
                                scoreList[3] += math.log(tmpMatrix[k]) / math.log(2) - math.log(
                                    tmpMatrix[t]) / math.log(2)
        return max(scoreList[0], scoreList[1]) + max(scoreList[2], scoreList[3])

    @classmethod
    def getEmptyCounts(cls, matrix):
        counts = 0
        for i in range(c.ROW):
            for j in range(c.COLUMN):
                if matrix[i][j] == 0:
                    counts += 1
        return counts

    @classmethod
    def getMaxValue(cls, matrix):
        MAX = matrix[0][0]
        for i in range(c.ROW):
            for j in range(c.COLUMN):
                if matrix[i][j] >= MAX:
                    MAX = matrix[i][j]
        return MAX


class Node:
    def __init__(self, matrix, depth):
        self.sonNode = []
        self.depth = depth
        self.matrix = matrix

        # 构造子节点
        if self.depth <= 6:
            self.sonNode.append(Node(self.matrix.right(), self.depth + 1))
            self.sonNode.append(Node(self.matrix.left(), self.depth + 1))
            self.sonNode.append(Node(self.matrix.up(), self.depth + 1))
            self.sonNode.append(Node(self.matrix.down(), self.depth + 1))


# Run the Code
alphaGo = Ai()
node, value = alphaGo.alphaBetaSearch(alphaGo.headNode, 6, True)
if node is not None:
    for i in range(4):
        print(node.matrix.getMatrix()[i])
