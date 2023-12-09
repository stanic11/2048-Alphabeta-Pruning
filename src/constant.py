COLUMN = int(4)
ROW = int(4) 
xmlFile = "rank.xml"
colorMap = dict[
           0:0x00000f,
           2:0x00000f,
           4:0x00000f,
           8:0x00000f,
           16:0x00000f,
           32:0x00000f,
           64:0x00000f,
           128:0x00000f,
           256:0x00000f,
           512:0x00000f,
           1024:0x00000f,
           2048:0x00000f
           ]
WIDTH, HEIGHT = (370, 650)
# 背景颜色
BG_COLOR = '#92877d'
# 棋盘需要的数据
MARGIN_SIZE = 10  # 间隔大小
BLOCK_SIZE = 80  # 棋子位置大小
CHESSBEGINLOC = 270  # 棋盘纵向位置

#keyBoardMap = [K_UP,K_DOWN,K_LEFT,K_RIGHT]