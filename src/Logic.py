import random
import constant as c

# TODO: 每次合并一个方块即停止循环
# 已完成内容：
# fst - 初始化矩阵储存各点数值
# sec - 在矩阵内随机两点生成2与4中的随机数值
# thd - 实现上下左右移动方块
# fourth - 每次移动后在空余位置生成一个方块


def initGame():
    matrix = []
    # Create a 4x4 matrix to store the grid variable.
    for i in range(4):
        matrix.append([0] * 4)
    initTwoRandomGrid(matrix)
    return matrix


def initTwoRandomGrid(matrix):
    col = random.randint(0, 3)
    row = random.randint(0, 3)
    matrix[col][row] = random.choice([2, 4])
    col__ = random.randint(0, 3)
    row__ = random.randint(0, 3)
    isRowColSame(matrix, row, row__, col, col__)


def isRowColSame(matrix, row, row__, col, col__):
    if row != row__ or col != col__:
        matrix[col__][row__] = random.choice([2, 4])
    else:
        col__ = random.randint(0, 3)
        row__ = random.randint(0, 3)
        isRowColSame(matrix, row, row__, col, col__)


def left(matrix):
    # 矩阵左移操作
    for j in range(c.COLUMN - 1, 0, -1):
        for i in range(c.ROW):
            if matrix[i][j] != 0 and j > 0:
                if matrix[i][j - 1] == 0:
                    matrix[i][j - 1] = matrix[i][j]
                    matrix[i][j] = 0
                elif matrix[i][j - 1] == matrix[i][j]:
                    matrix[i][j - 1] *= 2
                    matrix[i][j] = 0
    createGrid(matrix)


def right(matrix):
    for j in range(0, c.COLUMN - 1):
        for i in range(c.ROW):
            if matrix[i][j] != 0 and j < c.COLUMN:
                if matrix[i][j + 1] == 0:
                    matrix[i][j + 1] = matrix[i][j]
                    matrix[i][j] = 0
                elif matrix[i][j + 1] == matrix[i][j]:
                    matrix[i][j + 1] *= 2
                    matrix[i][j] = 0
    createGrid(matrix)


def up(matrix):
    # 进行 行变换
    for i in range(c.ROW - 1, 0, -1):
        for j in range(c.COLUMN):
            if matrix[i][j] != 0 and i < c.ROW:
                if matrix[i - 1][j] == 0:
                    matrix[i - 1][j] = matrix[i][j]
                    matrix[i][j] = 0
                elif matrix[i - 1][j] == matrix[i][j]:
                    matrix[i - 1][j] *= 2
                    matrix[i][j] = 0
    createGrid(matrix)


def down(matrix):
    for i in range(0, c.ROW - 1):
        for j in range(c.COLUMN):
            if matrix[i][j] != 0 and i < c.ROW:
                if matrix[i + 1][j] == 0:
                    matrix[i + 1][j] = matrix[i][j]
                    matrix[i][j] = 0
                elif matrix[i + 1][j] == matrix[i][j]:
                    matrix[i + 1][j] *= 2
                    matrix[i][j] = 0
    createGrid(matrix)


def createGrid(matrix):
    spaceList = []
    for i in range(c.COLUMN):
        for j in range(c.ROW):
            if matrix[i][j] == 0:
                spaceList.append([i, j])
    tmp = random.choice(spaceList)
    matrix[tmp[0]][tmp[1]] = random.choice([2, 4])


def isWinner(matrix):
    # 注：该函数应放置在死循环中
    for i in range(c.COLUMN):
        for j in range(c.ROW):
            if matrix[i][j] == 2048:
                return True
