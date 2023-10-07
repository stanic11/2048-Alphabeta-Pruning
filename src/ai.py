import math
import Logic
import constant as c


def getSmoothness(matrix):
    # 计算每格平滑度
    smoothness = 0
    # 先对每一行进行单独求解
    for i in range(c.ROW):
        tmpMatrix = matrix[i]
        for j in range(len(tmpMatrix) - 1):
            if tmpMatrix[j] != 0:
                for k in range(j + 1, len(tmpMatrix)):
                    if tmpMatrix[k] != 0:
                        smoothness -= math.fabs(tmpMatrix[k] - tmpMatrix[j])
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
                        smoothness -= math.fabs(tmpMatrix[k] - tmpMatrix[t])
                        break

    return smoothness


def getMonotonicity(matrix):
    scoreList = [0, 0, 0, 0]
    # Right
    for i in range(c.ROW):
        tmpMatrix = matrix[i]
        for j in range(len(tmpMatrix) - 1):
            if tmpMatrix[j] != 0:
                for k in range(j + 1, len(tmpMatrix)):
                    if tmpMatrix[k] != 0:
                        if tmpMatrix[j] >= tmpMatrix[k]:
                            scoreList[0] += math.log(tmpMatrix[k]) / math.log(2) - math.log(tmpMatrix[j]) / math.log(2)
                        else:
                            scoreList[1] += math.log(tmpMatrix[k]) / math.log(2) - math.log(tmpMatrix[j]) / math.log(2)
    # Left
    for i in range(c.ROW):
        tmpMatrix = matrix[i]
        for j in range(len(tmpMatrix) - 1, 0, -1):
            if tmpMatrix[j] != 0:
                for k in range(j - 1, len(tmpMatrix), -1):
                    if tmpMatrix[k] != 0:
                        if tmpMatrix[j] >= tmpMatrix[k]:
                            scoreList[0] += math.log(tmpMatrix[k]) / math.log(2) - math.log(tmpMatrix[j]) / math.log(2)
                        else:
                            scoreList[1] += math.log(tmpMatrix[k]) / math.log(2) - math.log(tmpMatrix[j]) / math.log(2)

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
                            scoreList[2] += math.log(tmpMatrix[k]) / math.log(2) - math.log(tmpMatrix[t]) / math.log(2)
                        else:
                            scoreList[3] += math.log(tmpMatrix[k]) / math.log(2) - math.log(tmpMatrix[t]) / math.log(2)
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
                            scoreList[2] += math.log(tmpMatrix[k]) / math.log(2) - math.log(tmpMatrix[t]) / math.log(2)
                        else:
                            scoreList[3] += math.log(tmpMatrix[k]) / math.log(2) - math.log(tmpMatrix[t]) / math.log(2)
    return max(scoreList[0], scoreList[1]) + max(scoreList[2], scoreList[3])


def getEmptyCounts(matrix):
    counts = 0
    for i in range(c.ROW):
        for j in range(c.COLUMN):
            if matrix[i][j] == 0:
                counts += 1
    return counts


def getMaxValue(matrix):
    MAX = matrix[0][0]
    for i in range(c.ROW):
        for j in range(c.COLUMN):
            if matrix[i][j] >= MAX:
                MAX = matrix[i][j]
    return MAX


class Ai:
    __smoothWeight = 0.1
    __emptyWeight = 2.7
    __maxWeight = 1.0
    __monoWeight = 1.0  # 单调性权重

    def eval(self, matrix):
        return getSmoothness(matrix) * self.__smoothWeight + getMonotonicity(matrix) * self.__monoWeight + math.log(
            getEmptyCounts(matrix)) * self.__emptyWeight + getMaxValue(matrix) * self.__maxWeight

    def alphaBeta(self, matrix):
       