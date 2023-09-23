import random
import constant as c


# 已完成内容：
# fst - 初始化矩阵储存各点数值
# sec - 在矩阵内随机两点生成2与4中的随机数值
# TODO: thd - 实现上下左右移动方块
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
    for i in range(c.COLUMN):
        for j in range(c.ROW):
            if matrix[i][j] != 0:
                if j == 0:
                    # At the fst grid in X
                    continue
                elif j == 1:
                    if (matrix[i][j - 1] == matrix[i][j] and matrix[i][j] != 0) or matrix[i][j] == 0:
                        matrix[i][j - 1] += matrix[i][j]
                        matrix[i][j] = 0
                elif j == 2:
                    if matrix[i][j - 1] == matrix[i][j] or matrix[i][j] == 0:
                        matrix[i][j - 1] += matrix[i][j]
                        matrix[i][j] = 0
                elif j == 3:
                    continue
                    #
                    # TODO:优化方法，撰写四个函数，分别先将 j位上的数字移动到j-1位上，运行j-1位对应的函数递归下去.......
                    #
            else:
                continue


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

