import os
import random
import xml.etree.ElementTree as ET

import constant as c


# 已完成内容：
# fst - 初始化矩阵储存各点数值
# sec - 在矩阵内随机两点生成2与4中的随机数值
# thd - 实现上下左右移动方块
# 4th - 每次移动后在空余位置生成一个方块
# TODO: 提示功能

class game:
    def __init__(self):
        # 初始化游戏
        self.matrix = Matrix()
        self.initTwoRandomGrid()
        # 初始化积分列表
        self.root = ET.Element("data")
        self.tree = ET.ElementTree(self.root)

    def __XML__init__(self):
        if os.path.exists(c.xmlFile):
            return
        else:
            return

    def initTwoRandomGrid(self):
        # 随机在矩阵中找寻两个格子生成随机数
        # 若两次生成的为同一格子，则进入while死循环，直到生成的格子不同为止
        col = random.randint(0, 3)
        row = random.randint(0, 3)
        newCol = random.randint(0, 3)
        newRow = random.randint(0, 3)
        # 防止生成在同一格子内
        while newCol == col and newRow == row:
            newCol = random.randint(0, 3)
            newRow = random.randint(0, 3)
        self.matrix.gridChange(col, row, random.choice([2, 4]))
        self.matrix.gridChange(newCol, newRow, random.choice([2, 4]))

    def restart(self):
        # 按下按键之后
        self.__init__()

    def gameState(self):
        # 检测是否胜利
        # 每次移动之后再进行检测，以此节约CPU资源
        zeroCount = 0
        for i in range(c.COLUMN):
            for j in range(c.ROW):
                if self.matrix.getMatrix()[i][j] == 2048:
                    return 'win'
                if self.matrix.getMatrix()[i][j] == 0:
                    zeroCount += 1
        if zeroCount == 0:
            return 'game over'
        # 数零个数，若零个数为0 说明格子全部占满，游戏失败

    def pointsList(self):
        file = open('rank.xml', 'r')

    def gameTips(self):
        # 按下按钮 输出提示

        return


class Matrix:
    def __init__(self):
        self.matrix = []
        # 初始化一个4x4的矩阵用于储存数据
        for i in range(c.COLUMN):
            self.matrix.append([0] * c.ROW)

    def getMatrix(self):
        return self.matrix

    def rewriteMatrix(self,matrix):
        self.matrix = matrix

    def gridChange(self, i, j, value):
        self.matrix[i][j] = value

    ########################################################################
    def left(self):
        # 矩阵左移操作
        for i in range(c.ROW):
            # 抽出矩阵的每一行
            self.matrix[i] = self.matrixChange(self.matrix[i], 'left')
        self.createGrid(self.matrix)
        return self

    def right(self):
        for i in range(c.ROW):
            # 抽出矩阵的每一行
            self.matrix[i] = self.matrixChange(self.matrix[i], 'right')
        self.createGrid(self.matrix)
        return self

    def up(self):
        # 进行 行变换
        for j in range(c.COLUMN):
            tmpMatrix = []
            for i in range(c.ROW):
                # 抽出矩阵的每一列
                tmpMatrix.append(self.matrix[i][j])
            tmpMatrix = self.matrixChange(tmpMatrix, 'up')
            # 将临时矩阵的值返回到原矩阵
            for i in range(c.ROW):
                self.matrix[i][j] = tmpMatrix[i]
        self.createGrid(self.matrix)
        return self

    def down(self):
        # 进行 行变换
        for j in range(c.COLUMN):
            tmpMatrix = []
            for i in range(c.ROW):
                # 抽出矩阵的每一列
                tmpMatrix.append(self.matrix[i][j])
            tmpMatrix = self.matrixChange(tmpMatrix, 'down')
            # 将临时矩阵的值返回到原矩阵
            for i in range(c.ROW):
                self.matrix[i][j] = tmpMatrix[i]
        self.createGrid(self.matrix)
        return self

    ########################################################################

    def createGrid(self, matrix):
        spaceList = []
        for i in range(c.COLUMN):
            for j in range(c.ROW):
                if matrix[i][j] == 0:
                    spaceList.append([i, j])
        if len(spaceList) != 0:
            tmp = random.choice(spaceList)
            matrix[tmp[0]][tmp[1]] = random.choice([2, 4])

    def matrixChange(self, matrix, front):
        newMatrixRow = []
        count = 0
        for i in range(c.COLUMN):
            if matrix[i] != 0:
                newMatrixRow.append(matrix[i])
            else:
                count += 1
        newMatrixRow = self.merge(newMatrixRow, front)
        if front == 'left' or front == 'up':
            for j in range(count):
                newMatrixRow.append(0)
        else:
            for j in range(count):
                newMatrixRow.insert(0, 0)
        return newMatrixRow

    def merge(self, matrix, front):
        if front == 'left' or front == 'up':
            for i in range(len(matrix) - 1):
                if matrix[i] == matrix[i + 1] and matrix[i] != 0:
                    matrix[i] *= 2
                    matrix[i + 1] = 0
                    i += 1  # 跳到下一个非零元素
                elif matrix[i] == 0 and matrix[i + 1] != 0:
                    matrix[i] = matrix[i + 1]
                    matrix[i + 1] = 0
        if front == 'right' or front == 'down':
            for i in range(len(matrix) - 1, 0, -1):
                if matrix[i] == matrix[i - 1] and matrix[i] != 0:
                    matrix[i] *= 2
                    matrix[i - 1] = 0
                    i -= 1  # 跳到下一个非零元素
                elif matrix[i] == 0 and matrix[i - 1] != 0:
                    matrix[i] = matrix[i - 1]
                    matrix[i - 1] = 0
        return matrix
