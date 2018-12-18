import numpy as np
from enum import *

# デバッグモードのフラグ
isDebug = False

# 構造体の宣言
#----------------
class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Enumの宣言
#-------------------
# 0=empty,1=player,2=AI
class gridState(IntEnum):
    empty = 0
    player = auto()
    AI = auto()

gridText = ['', '○', 'x']

# AIの強さ
class AILevel(IntEnum):
    week = 0
    middle = auto()
    strong = auto()
    omg = auto()

# 戦うモード
class gameMode(IntEnum):
    Normal = 0  # AIとの戦い
    quit = auto()  # やめる

# 変数
gridSize = Size(15, 15)
