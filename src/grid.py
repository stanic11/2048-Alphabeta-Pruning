import random


class Grid:
    __value = 0
    __color = 0x00f

    def __init__(self):  # 构造函数 to init__ self value to 2 or 4.
        self.__value = random.choice([2, 4])

    def __del__(self): # 析构函数
        self.__value = 0

    def getValue(self):
        return self.__value

    def getColor(self):
        return self.__color
