import Logic
import Print
import os
import pygame
import sys
import ai
import copy
import constant as c
import xml.etree.ElementTree as ET


class game:
    def __init__(self):
        # 初始化游戏
        self.matrix = Logic.Matrix()
        self.copyMatrix = self.matrix
        self.printer = Print.Printer(self)
        self.maxScore = self.findMaxScore()
        # 初始化积分列表
        self.tree = ""
        self.root = ""
        self.readPointList()
        #初始化音乐
        pygame.mixer.init()
        pygame.mixer.music.load(c.musicPath)
        pygame.mixer.music.play()

    def findMaxScore(self):
        if os.path.exists(c.xmlFile):
            tree = ET.parse(c.xmlFile)
            root = tree.getroot()
            # 查找所有包含数据的data元素
            data_elements = root.findall(".//data[point]")
            if data_elements:
                # 遍历所有包含数据的data元素，获取其中的point元素的文本内容
                points = [int(data.find("point").text) for data in data_elements]
                if points:
                    max_point = max(points)
                    return max_point
        return 0

    def start(self):
        self.printer.start()

    def beginPlayerGame(self):
        pygame.init()
        # 创建窗口
        screen = pygame.display.set_mode((self.printer.WIDTH, self.printer.HEIGHT))
        # 创建计时器（防止while循环过快，占用太多CPU的问题）
        clock = pygame.time.Clock()

        while True:
            # 事件检测（鼠标点击、键盘按下等）
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if (15 <= mouse_x <= 115) and (200 <= mouse_y <= 250):
                        self.__init__()  # 重新开始游戏
                    if (135 <= mouse_x <= 235) and (200 <= mouse_y <= 250):
                        c.tipString = self.getGameTips()  # 提示功能
                    if (255 <= mouse_x <= 355) and (200 <= mouse_y <= 250):
                        self.matrix = self.copyMatrix  # 返回上一步
                        pygame.display.update()

                elif event.type == pygame.KEYDOWN:
                    self.copyMatrix = copy.deepcopy(self.matrix)
                    # 检测具体按键
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.matrix.left()
                        self.printer.numsPrint(screen, self.matrix)
                        self.gameState()
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.matrix.right()
                        self.printer.numsPrint(screen, self.matrix)
                        self.gameState()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.matrix.up()
                        self.printer.numsPrint(screen, self.matrix)
                        self.gameState()
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.matrix.down()
                        self.printer.numsPrint(screen, self.matrix)
                        self.gameState()

            screen.fill(pygame.Color(self.printer.BG_COLOR))
            # 显示棋盘
            self.printer.chessBoardPrint(screen, self.matrix)
            # 显示棋盘上的标签(分数、最高分)和按钮
            self.printer.buttonsPrint(screen, self.matrix.point, self.maxScore)
            # 显示棋盘上的数字
            self.printer.numsPrint(screen, self.matrix)
            # 刷新显示
            pygame.display.update()
            clock.tick(60)

    def beginAiGame(self):
        BetaGo = ai.Ai(self)
        pygame.init()
        # 创建窗口
        screen = pygame.display.set_mode((self.printer.WIDTH, self.printer.HEIGHT))
        # 创建计时器（防止while循环过快，占用太多CPU的问题）
        clock = pygame.time.Clock()
        while True:
            # 事件检测
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            action = BetaGo.decide()
            if action == 'left':
                self.matrix.left()
            elif action == 'right':
                self.matrix.right()
            elif action == 'up':
                self.matrix.up()
            elif action == 'down':
                self.matrix.down()
            if self.gameState() == 'win' or self.gameState() == 'game over':
                break
            screen.fill(pygame.Color(self.printer.BG_COLOR))
            # 显示棋盘
            self.printer.chessBoardPrint(screen, self.matrix)
            # 显示棋盘上的标签(分数、最高分)和按钮
            self.printer.buttonsPrint(screen, self.matrix.point, self.maxScore)
            # 显示棋盘上的数字
            self.printer.numsPrint(screen, self.matrix)
            # 刷新显示
            pygame.display.update()
            clock.tick(60)

    def readPointList(self):
        if os.path.exists(c.xmlFile):
            self.tree = ET.parse(c.xmlFile)
            self.root = self.tree.getroot()
            # 查找所有包含数据的data元素
            data_elements = self.root.findall(".//data[point]")
            if data_elements:
                # 遍历所有包含数据的data元素，获取其中的point元素的文本内容
                points = [int(data.find("point").text) for data in data_elements]
                if points:
                    max_point = max(points)
                    self.maxScore = max_point
                else:
                    print("No data")
            else:
                print("No data")
        else:
            print("File does not exist")

    def gameState(self):
        # 检测是否胜利
        # 每次移动之后再进行检测，以节约资源
        text = ""
        zeroCount = 0
        for i in range(c.COLUMN):
            for j in range(c.ROW):
                if self.matrix.getMatrix()[i][j] == 2048:
                    text = 'win'
                    break  # 找到2048就退出循环
                if self.matrix.getMatrix()[i][j] == 0:
                    zeroCount += 1

        if zeroCount == 0 and text != 'win':
            # 数零个数，若零个数为0说明格子全部占满，再判断是否有相邻的相同的数字
            for i in range(c.COLUMN):
                for j in range(c.ROW):
                    if i - 1 >= 0 and self.matrix.getMatrix()[i][j] == self.matrix.getMatrix()[i - 1][j]:
                        text = 'game over'
                        break  # 找到相邻相同数字就退出循环
                    if i + 1 < c.COLUMN and self.matrix.getMatrix()[i][j] == self.matrix.getMatrix()[i + 1][j]:
                        text = 'game over'
                        break
                    if j - 1 >= 0 and self.matrix.getMatrix()[i][j] == self.matrix.getMatrix()[i][j - 1]:
                        text = 'game over'
                        break
                    if j + 1 < c.ROW and self.matrix.getMatrix()[i][j] == self.matrix.getMatrix()[i][j + 1]:
                        text = 'game over'
                        break

        if text == 'win' or text == 'game over':
            print("game over")
            self.updatePointList(self.matrix.point)
            self.printer.miniWindow(self.matrix.point, self.maxScore)
        return text

    def updatePointList(self, current_score):
        # 更新XML文件，将当前分数写入
        if self.tree is not None and self.root is not None:
            # 创建一个新的data元素
            new_data = ET.Element("data")
            point_element = ET.SubElement(new_data, "point")
            point_element.text = str(current_score)

            # 将新的data元素添加到root中
            self.root.append(new_data)
            # 保存更改到XML文件
            self.tree.write(c.xmlFile)
            print("分数写入rank.xml")
        else:
            print("XML树或根元素未初始化")

    def getGameTips(self):
        # 循环遍历所有位置，查找可以移动的方向
        text = ""
        for i in range(c.COLUMN):
            for j in range(c.ROW):
                if self.matrix.getMatrix()[i][j] != 0:
                    # 只在当前位置有方块的情况下才考虑可能的移动方向
                    if i - 1 >= 0 and (self.matrix.getMatrix()[i - 1][j] == 0 or self.matrix.getMatrix()[i - 1][j] ==
                                       self.matrix.getMatrix()[i][j]):
                        text = '向左'
                        break
                    if i + 1 < c.COLUMN and (
                            self.matrix.getMatrix()[i + 1][j] == 0 or self.matrix.getMatrix()[i + 1][j] ==
                            self.matrix.getMatrix()[i][j]):
                        text = '向右'
                        break
                    if j - 1 >= 0 and (self.matrix.getMatrix()[i][j - 1] == 0 or self.matrix.getMatrix()[i][j - 1] ==
                                       self.matrix.getMatrix()[i][j]):
                        text = '向上'
                        break
                    if j + 1 < c.ROW and (self.matrix.getMatrix()[i][j + 1] == 0 or self.matrix.getMatrix()[i][j + 1] ==
                                          self.matrix.getMatrix()[i][j]):
                        text = '向下'
                        break
        return text
