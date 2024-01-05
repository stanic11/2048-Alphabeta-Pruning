import sys
import pygame
import constant as c


class Printer:
    def __init__(self, game):
        # 屏幕尺寸
        self.WIDTH = c.WIDTH
        self.HEIGHT = c.HEIGHT
        self.game = game  # 读取game类
        # 背景颜色
        self.BG_COLOR = c.BG_COLOR
        # 棋盘需要的数据
        self.MARGIN_SIZE = c.MARGIN_SIZE  # 间隔大小
        self.BLOCK_SIZE = c.BLOCK_SIZE  # 棋子位置大小
        self.CHESSBEGINLOC = c.CHESSBEGINLOC  # 棋盘纵向位置
        self.maxScore = 0
        self.miniWidth = c.miniWidth
        self.miniHeight = c.miniHeight
        self.icon = pygame.image.load(c.iconPath)

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("2048")
        pygame.display.set_icon(self.icon)
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if (85 <= mouse_x <= 285) and (360 <= mouse_y <= 410):
                        self.game.beginPlayerGame()  # 玩家开始玩游戏
                    if (85 <= mouse_x <= 285) and (450 <= mouse_y <= 500):
                        self.game.beginAiGame()  # AI开始玩游戏
            screen.fill(pygame.Color(self.BG_COLOR))
            self.openingPrint(screen)
            pygame.display.update()
            clock.tick(60)

    def openingPrint(self, screen):
        """
            显示游戏开始界面
        """
        # 显示标题2048
        font_color = pygame.Color("#0d1924")
        font_1_size = self.BLOCK_SIZE + 50
        font_1 = pygame.font.Font("..\\font\\Rainbow.ttf", font_1_size)
        text_1 = font_1.render("2048", True, font_color)
        text_1_rect = text_1.get_rect()
        text_1_rect.centerx, text_1_rect.centery = self.WIDTH * 0.5, self.HEIGHT * 0.5 - 130
        screen.blit(text_1, text_1_rect)

        # 显示按钮1 “开始游戏” 和按钮2 “ai运行”

        pygame.draw.rect(screen, (210, 186, 162), (85, 360, 200, 50))
        pygame.draw.rect(screen, (210, 186, 162), (85, 450, 200, 50))
        font_3_size = self.BLOCK_SIZE - 50
        font_3 = pygame.font.Font("..\\font\\Rainbow.ttf", font_3_size)
        text_3 = font_3.render("开始游戏", True, font_color)
        text_3_rect = text_3.get_rect()
        text_3_rect.centerx, text_3_rect.centery = self.WIDTH * 0.5, 385
        screen.blit(text_3, text_3_rect)

        font_4_size = self.BLOCK_SIZE - 50
        font_4 = pygame.font.Font("..\\font\\Rainbow.ttf", font_4_size)
        text_4 = font_4.render("AI运行", True, font_color)
        text_4_rect = text_4.get_rect()
        text_4_rect.centerx, text_4_rect.centery = self.WIDTH * 0.5, 475
        screen.blit(text_4, text_4_rect)

    def buttonsPrint(self, screen, score, scoreMax):
        """
        显示棋盘上的标签和按钮
        """
        # 显示数字2048
        font_color = pygame.Color("#0d1924")
        font_size = self.BLOCK_SIZE + 10
        font = pygame.font.Font("..\\font\\Rainbow.ttf", font_size)
        text = font.render("2048", True, font_color)
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.centery = self.BLOCK_SIZE + 25, self.BLOCK_SIZE - 20
        screen.blit(text, text_rect)

        font_color = pygame.Color("#0d1924")
        font_size_of_label = self.BLOCK_SIZE - 45
        str_score = str(score)
        str_scoreMax = str(scoreMax)
        str_tips = self.game.getGameTips()

        # 显示分数标签(label_1)

        font_of_label_1 = pygame.font.Font("..\\font\\Rainbow.ttf", font_size_of_label)
        text_of_label_1 = font_of_label_1.render("分数:", True, font_color)
        text_of_label_1_rect = text_of_label_1.get_rect()
        text_of_label_1_rect.centerx, text_of_label_1_rect.centery = self.BLOCK_SIZE - 30, self.BLOCK_SIZE * 2 - 10
        screen.blit(text_of_label_1, text_of_label_1_rect)

        font_of_score = pygame.font.Font("..\\font\\Rainbow.ttf", font_size_of_label)
        text_of_score = font_of_score.render(str_score, True, font_color)
        text_of_score_rect = text_of_score.get_rect()
        text_of_score_rect.centerx, text_of_score_rect.centery = self.BLOCK_SIZE + 45, self.BLOCK_SIZE * 2 - 10
        screen.blit(text_of_score, text_of_score_rect)

        # 显示最高分标签(label_2)

        font_of_label_2 = pygame.font.Font("..\\font\\Rainbow.ttf", font_size_of_label)
        text_of_label_2 = font_of_label_2.render("历史最高:", True, font_color)
        text_of_label_2_rect = text_of_label_2.get_rect()
        text_of_label_2_rect.centerx, text_of_label_2_rect.centery = 2 * self.BLOCK_SIZE + 75, self.BLOCK_SIZE * 2 - 10
        screen.blit(text_of_label_2, text_of_label_2_rect)

        font_of_score = pygame.font.Font("..\\font\\Rainbow.ttf", font_size_of_label)
        text_of_score = font_of_score.render(str_scoreMax, True, font_color)
        text_of_score_rect = text_of_score.get_rect()
        text_of_score_rect.centerx, text_of_score_rect.centery = 2 * self.BLOCK_SIZE + 180, self.BLOCK_SIZE * 2 - 10
        screen.blit(text_of_score, text_of_score_rect)

        # 显示提示标签(label_3)

        font_of_label_3 = pygame.font.Font("..\\font\\Rainbow.ttf", font_size_of_label)
        text_of_label_3 = font_of_label_3.render("提示:", True, font_color)
        text_of_label_3_rect = text_of_label_3.get_rect()
        text_of_label_3_rect.centerx, text_of_label_3_rect.centery = 50, self.HEIGHT - 30
        screen.blit(text_of_label_3, text_of_label_3_rect)

        font_of_tips = pygame.font.Font("..\\font\\Rainbow.ttf", font_size_of_label)
        text_of_tips = font_of_tips.render(c.tipString, True, font_color)
        text_of_tips_rect = text_of_tips.get_rect()
        text_of_tips_rect.centerx, text_of_tips_rect.centery = 0.5 * self.WIDTH + 30, self.HEIGHT - 30
        screen.blit(text_of_tips, text_of_tips_rect)

        # 显示按钮1 、按钮2 、按钮3

        pygame.draw.rect(screen, (210, 186, 162), (15, 200, 100, 50))
        pygame.draw.rect(screen, (210, 186, 162), (135, 200, 100, 50))
        pygame.draw.rect(screen, (210, 186, 162), (255, 200, 100, 50))

        font_color = pygame.Color("#0d1924")
        font_size = self.BLOCK_SIZE - 50
        font = pygame.font.Font("..\\font\\Rainbow.ttf", font_size)

        text_button_1 = font.render("重新", True, font_color)
        text_button_1_rect = text_button_1.get_rect()
        text_button_1_rect.centerx, text_button_1_rect.centery = 65, 225
        screen.blit(text_button_1, text_button_1_rect)

        text_button_2 = font.render("提示", True, font_color)
        text_button_2_rect = text_button_2.get_rect()
        text_button_2_rect.centerx, text_button_2_rect.centery = 185, 225
        screen.blit(text_button_2, text_button_2_rect)

        text_button_3 = font.render("上一步", True, font_color)
        text_button_3_rect = text_button_3.get_rect()
        text_button_3_rect.centerx, text_button_3_rect.centery = 305, 225
        screen.blit(text_button_3, text_button_3_rect)

    def numsPrint(self, screen, Matrix):
        #   显示棋盘上的数字
        #   准备字体等
        font_color = pygame.Color("#828282")
        font_size = self.BLOCK_SIZE - 40
        font = pygame.font.Font("..\\font\\Rainbow.ttf", font_size)

        matrix = Matrix.getMatrix()
        # 遍历数字
        for i in range(c.COLUMN):
            for j in range(c.ROW):
                # 计算显示位置（x坐标、y坐标）
                x = self.MARGIN_SIZE * (j + 1) + self.BLOCK_SIZE * j
                y = self.CHESSBEGINLOC + self.MARGIN_SIZE * (i + 1) + self.BLOCK_SIZE * i
                # 显示数字
                text = font.render(str(matrix[i][j]), True, font_color)
                text_rect = text.get_rect()
                text_rect.centerx, text_rect.centery = x + self.BLOCK_SIZE / 2, y + self.BLOCK_SIZE / 2
                screen.blit(text, text_rect)

    def judgeChessboardColor(self, num):
        # 根据格子里的数字判断格子的颜色
        if num in c.colorMap:
            return c.colorMap.get(num)

    def chessBoardPrint(self, screen, Matrix):
        # 显示棋盘
        matrix = Matrix.getMatrix()
        for i in range(4):
            for j in range(4):
                x = self.MARGIN_SIZE * (j + 1) + self.BLOCK_SIZE * j
                y = self.CHESSBEGINLOC + self.MARGIN_SIZE * (i + 1) + self.BLOCK_SIZE * i
                pygame.draw.rect(screen, pygame.Color(self.judgeChessboardColor(matrix[i][j])),
                                 (x, y, self.BLOCK_SIZE, self.BLOCK_SIZE))

    def miniWindow(self, score, scoreMax):
        """
        显示得分弹窗
        """
        pygame.init()
        # 创建窗口
        screen = pygame.display.set_mode(c.SIZE)
        # 设置窗口标题
        pygame.display.set_caption("游戏结束")

        score_text = '你的分数：' + str(score)
        scoreMax_text = '历史最高分数：' + str(scoreMax)

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
                    if (85 <= mouse_x <= 285) and (360 <= mouse_y <= 410):
                        self.game.beginPlayerGame()
            # 显示背景色
            screen.fill(pygame.Color(self.BG_COLOR))
            # 显示分数
            font_color = pygame.Color("#0d1924")
            font_1_size = self.BLOCK_SIZE - 50
            font_1 = pygame.font.Font("..\\font\\Rainbow.ttf", font_1_size)
            text_1 = font_1.render(score_text, True, font_color)
            text_1_rect = text_1.get_rect()
            text_1_rect.centerx, text_1_rect.centery = self.miniWidth * 0.5, self.miniHeight * 0.35
            screen.blit(text_1, text_1_rect)

            font_2_size = self.BLOCK_SIZE - 50
            font_2 = pygame.font.Font("..\\font\\Rainbow.ttf", font_2_size)
            text_2 = font_2.render(scoreMax_text, True, font_color)
            text_2_rect = text_2.get_rect()
            text_2_rect.centerx, text_2_rect.centery = self.miniWidth * 0.5, self.miniHeight * 0.70
            screen.blit(text_2, text_2_rect)

            # 刷新显示
            pygame.display.update()
            clock.tick(60)
