import sys

import pygame

import Logic
import constant as c

class Draw:
    def __init__(self):
        # 屏幕尺寸
        self.WIDTH = c.WIDTH
        self.HEIGHT = c.HEIGHT

        # 背景颜色
        self.BG_COLOR = c.BG_COLOR
        # 棋盘需要的数据
        self.MARGIN_SIZE = c.MARGIN_SIZE  # 间隔大小
        self.BLOCK_SIZE = c.BLOCK_SIZE  # 棋子位置大小
        self.CHESSBEGINLOC = c.CHESSBEGINLOC  # 棋盘纵向位置

    def start(self):
        # 游戏初始化
        pygame.init()
        # 创建窗口
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
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
                        self.beginHumanGame()
                    if (85 <= mouse_x <= 285) and (450 <= mouse_y <= 500):
                        self.beginAiGame()
            # 显示背景色
            screen.fill(pygame.Color(self.BG_COLOR))
            # 显示棋盘
            self.draw_opening(screen)
            # 刷新显示（此时窗口才会真正的显示）
            pygame.display.update()
            # FPS（每秒钟显示画面的次数）
            clock.tick(60)  # 通过一定的延时，实现1秒钟能够循环60次

    def draw_opening(self, screen):
        """
        显示游戏开始界面
        """
        # 显示数字2048和4X4
        font_color = pygame.Color("#0d1924")
        font_1_size = self.BLOCK_SIZE + 50
        font_1 = pygame.font.Font("..\\font\\Rainbow.ttf", font_1_size)
        text_1 = font_1.render("2048", True, font_color)
        text_1_rect = text_1.get_rect()
        text_1_rect.centerx, text_1_rect.centery = self.WIDTH * 0.5, self.HEIGHT * 0.5 - 170
        screen.blit(text_1, text_1_rect)
        """
        # font_2_size = BLOCK_SIZE - 50
        # font_2 = pygame.font.Font("..\\font\\Rainbow.ttf", font_2_size)
        # text_2 = font_2.render("4 X 4", True, font_color)
        # text_2_rect = text_2.get_rect()
        # text_2_rect.centerx, text_2_rect.centery = WIDTH * 0.5, HEIGHT * 0.5 - 70
        # screen.blit(text_2, text_2_rect)
        """
        # 显示按钮1 ”开始游戏“ 和按钮2 ”ai运行“

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

    def draw_buttons(self, screen, score, scoreMax):
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

        # 显示分数标签(label_1)

        font_color = pygame.Color("#0d1924")
        font_size_of_label = self.BLOCK_SIZE - 45
        str_score = str(score)
        str_scoreMax = str(scoreMax)

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

        # 显示按钮1 、按钮2 、按钮3

        pygame.draw.rect(screen, (210, 186, 162), (15, 200, 100, 50))
        pygame.draw.rect(screen, (210, 186, 162), (135, 200, 100, 50))
        pygame.draw.rect(screen, (210, 186, 162), (255, 200, 100, 50))

        font_color = pygame.Color("#0d1924")
        font_size = self.BLOCK_SIZE - 50
        font = pygame.font.Font("..\\font\\Rainbow.ttf", font_size)

        text_button_1 = font.render("按钮1", True, font_color)
        text_button_1_rect = text_button_1.get_rect()
        text_button_1_rect.centerx, text_button_1_rect.centery = 65, 225
        screen.blit(text_button_1, text_button_1_rect)

        text_button_2 = font.render("按钮2", True, font_color)
        text_button_2_rect = text_button_2.get_rect()
        text_button_2_rect.centerx, text_button_2_rect.centery = 185, 225
        screen.blit(text_button_2, text_button_2_rect)

        text_button_3 = font.render("按钮3", True, font_color)
        text_button_3_rect = text_button_3.get_rect()
        text_button_3_rect.centerx, text_button_3_rect.centery = 305, 225
        screen.blit(text_button_3, text_button_3_rect)

    def draw_nums(self, screen, Matrix):
        #   显示棋盘上的数字
        #   准备字体等
        font_color = pygame.Color("#eee4da")
        font_size = self.BLOCK_SIZE - 10
        font = pygame.font.Font("..\\font\\Rainbow.ttf", font_size)

        matrix = Matrix.getMatrix()
        print(matrix)
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

    def draw_chess_board(self, screen):
        """
        显示棋盘
        """
        for i in range(4):
            for j in range(4):
                x = self.MARGIN_SIZE * (j + 1) + self.BLOCK_SIZE * j
                y = self.CHESSBEGINLOC + self.MARGIN_SIZE * (i + 1) + self.BLOCK_SIZE * i
                pygame.draw.rect(screen, pygame.Color('#f9f6f2'), (x, y, self.BLOCK_SIZE, self.BLOCK_SIZE))

    def beginAiGame(self):
        """
        AI开始玩游戏
        """
        pygame.init()
        # 创建窗口
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # 定义列表，用来记录当前棋盘上的所有数字，如果某位置没有数字，则为0
        chess_nums = [[0 for _ in range(4)] for _ in range(4)]
        # 创建计时器（防止while循环过快，占用太多CPU的问题）
        clock = pygame.time.Clock()

        while True:
            # 事件检测（鼠标点击、键盘按下等）
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # 显示背景色
            screen.fill(pygame.Color(self.BG_COLOR))
            # 显示棋盘
            self.draw_chess_board(screen)
            # 显示棋盘上的标签(分数、最高分)和按钮
            score = 0
            scoreMax = 0
            self.draw_buttons(screen, score, scoreMax)
            # 显示棋盘上的数字
            #self.draw_nums(screen, chess_nums)
            # 刷新显示（此时窗口才会真正的显示）
            pygame.display.update()
            # FPS（每秒钟显示画面的次数）
            clock.tick(60)  # 通过一定的延时，实现1秒钟能够循环60次

    def beginHumanGame(self):
        """
        玩家开始玩游戏
        """
        Game = Logic.game()

        pygame.init()
        # 创建窗口
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # 定义列表，用来记录当前棋盘上的所有数字，如果某位置没有数字，则为0
        chess_nums = [[0 for _ in range(4)] for _ in range(4)]
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
                        print("你按了按钮1")
                    if (135 <= mouse_x <= 235) and (200 <= mouse_y <= 250):
                        print("你按了按钮2")
                    if (255 <= mouse_x <= 355) and (200 <= mouse_y <= 250):
                        print("你按了按钮3")

                elif event.type == pygame.KEYDOWN:
                    # 检测具体按键
                    if event.key == pygame.K_LEFT:
                        Game.matrix.left()
                        self.draw_nums(screen, Game.matrix)
                    elif event.key == pygame.K_RIGHT:
                        Game.matrix.right()
                        self.draw_nums(screen, Game.matrix)
                    elif event.key == pygame.K_UP:
                        Game.matrix.up()
                        self.draw_nums(screen, Game.matrix)
                    elif event.key == pygame.K_DOWN:
                        Game.matrix.down()
                        self.draw_nums(screen, Game.matrix)

            # 显示背景色
            screen.fill(pygame.Color(self.BG_COLOR))
            # 显示棋盘
            self.draw_chess_board(screen)
            # 显示棋盘上的标签(分数、最高分)和按钮
            score = 0
            scoreMax = 0
            self.draw_buttons(screen, score, scoreMax)
            # 显示棋盘上的数字
            self.draw_nums(screen, Game.matrix)
            # 刷新显示（此时窗口才会真正的显示）
            pygame.display.update()
            # FPS（每秒钟显示画面的次数）
            clock.tick(60)  # 通过一定的延时，实现1秒钟能够循环60次


