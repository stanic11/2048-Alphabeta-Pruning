COLUMN = int(4)
ROW = int(4)
xmlFile = "../rank.xml"
colorMap = {0: '#f9f6f2',
            2: '#cfcf4f',
            4: '#a4cc9d',
            8: '#83ae57',
            16: '#5da451',
            32: '#5aa0ae',
            64: '#6c74b7',
            128: '#9b63b2',
            256: '#b160a6',
            512: '#d3a6be',
            1024: '#c2838b',
            2048: '#9f4e58'}
WIDTH, HEIGHT = (370, 700)

# 背景颜色
BG_COLOR = '#92877d'
# 棋盘需要的数据
MARGIN_SIZE = 10  # 间隔大小
BLOCK_SIZE = 80  # 棋子位置大小
CHESSBEGINLOC = 270  # 棋盘纵向位置
# 弹窗窗口大小
SIZE = miniWidth, miniHeight = (320, 240)
# Ai 迭代次数
nodeDepth = 6
# 提示文本
tipString = ""
# 音乐文件路径
musicPath = "../media/A Cupids Day.mp3"
# 图标文件路径
iconPath = "../images/threes.ico"
