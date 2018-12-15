from tkinter import *
from tkinter import Tk, messagebox
import numpy as np
import dropbox
import datetime
import time
from enum import *
from flask import Flask

# 構造体の宣言
class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ここら辺はグローバル変数とか定数とか
# マスは15*15
gridSize = Size(15, 15)
print(gridSize.width)
grid_height = 15
grid_width = 15

# デバッグモードのフラグ
isDebug = True

i = 0
#マス目を格納する配列
frame_list = []

# 0=empty,1=player,2=AI
class gridState(IntEnum):
    empty = 0
    player = auto()
    AI = auto()

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

# Playerの情報
# 'movedCount'は手数記録用(ランキングと結果に使いたい)(<- 駒の数を数えて計算すればいいのでは？)(<-2重ループ書いて見るのが個人的にめんどくさいため)
# ゲームモード(難易度)(<- diffだと違いを表してるみたい)(<-modeNumにしました)
modeNum = -1
playerState = {'gameMode': gameMode(0), 'AILevel': AILevel(0), 'movedCount': 0}

if isDebug == True:
    print(playerState)

# マップのデータ(各数字の意味はgridStateを参照)
grids = np.zeros((grid_height, grid_width))

# メイン画面
root = Tk()
#タイトル
root.title("FIVE AI")
# フルスクリーン化
root.state('zoomed')

class gameGrid:
    # hash: そのオブジェクト固有の値で、それを判別できるような値(気に入らなかったらidでもいいけどね)
    def __init__(self, hash, Point point):
        self.hash = hash
        self.state = gridState.empty
        self.point = point
        self.frame = Frame(game_frame, width=30, height=30,
                      bd=3, relief='raised', bg='LightGray')
        self.frame.bind("<1>", leftClicked)
        global frame_list
        frame_list.append(frame)
        self.frame.grid(row=point.x, column=poiny.y)

# マス目が左クリックされた際の処理
def leftClicked(event):
    global grids
    if grids[event.widget.point.x][event.widget.point.y] == gridState.empty:
        grids[event.widget.point.x][event.widget.point.y] = gridState.player
        changeGrid(event.widget.point, gridState.player)
    else:
        massagebox.showinfo('駒を置くことができません!', 'まだ駒が置かれていないマスにのみ駒を置くことができます。')

#盤の状態を変える
def changeGrid(Point point, int toState):
    if isDebug == True:
        massagebox.showinfo('changeGridが呼ばれました')
    global movedcount, modeNum
    event.widget.configure(relief='ridge', bd='1')
    gridText = Label(event.widget, text="○", bg='LightGray')
    gridText.place(width=28, height=28)
    movedcount = movedcount + 1
    if modeNum == 1:
        weakai()
    elif modeNum == 2:
        middleai()
    elif modeNum == 3:
        strongai()
    elif modeNum == 4:
        omgai()


# マス目配置
def grid():
    for x in range(grid_height):
        for y in range(grid_width):
            frame = Frame(game_frame, width=30, height=30,
                          bd=3, relief='raised', bg='LightGray')
            frame.bind("<1>", leftClicked(x, y))
            frame.num = i
            frame_list.append(frame)
            frame.grid(row=x, column=y)

def fromDropbox():
    global movedcount
    #ドロップボックスのアカウント取得
    dbox = dropbox.Dropbox(os.environ["DROPBOX_KEY"])
    dbox.users_get_current_account()
def intoDropbox():
    global movedcount
    #ドロップボックスのアカウント取得
    dbox = dropbox.Dropbox(os.environ["DROPBOX_KEY"])
    dbox.users_get_current_account()
def ranking():
    # Dropboxを使用してランキングを作りたい
    fromDropbox()
    intoDropbox()

def win():
    global modeNum
    # 結果確認画面
    if modeNum == 1:
        messagebox.showinfo('おめでとうございます！！', 'あなたはWEAK AIに' + movedcount + '手で勝利しました！！このAIは弱かったですか？弱かったですね。')
    elif modeNum == 2:
        messagebox.showinfo('おめでとうございます！！', 'あなたはMIDDLE AIに' + movedcount + '手で勝利しました！！このAIは常人レベルに強さを留めてあります。まあ勝てますよね。')
    elif modeNum == 3:
        messagebox.showinfo('おめでとうございます！！', 'あなたはSTRONG AIに' + movedcount + '手で勝利しました！！このAIに勝つとは中々ですね・・・五目並べプロ級です。')
    elif modeNum == 4:
        messagebox.showinfo('おめでとうございます！！', 'あなたは??? AIに' + movedcount + '手で勝利しました！！勝てたんですか...このAIには誰も勝てない位の難易度にしたつもりなんですけどね...')
    # ランキングに登録
    ranking()
    
def lose():
    global modeNum
    if modeNum == 1:
        messagebox.showinfo('残念・・・', 'あなたはWEAK AIに' + movedcount + '手粘ったものの負けてしまいました・・・')
    elif modeNum == 2:
        messagebox.showinfo('残念・・・', 'あなたはMIDDLE AIに' +movedcount + '手粘ったものの負けてしまいました・・・')
    elif modeNum == 3:
        messagebox.showinfo('残念・・・', 'あなたはSTRONG AIに' +movedcount + '手粘ったものの負けてしまいました・・・')
    elif modeNum == 4:
        messagebox.showinfo('残念・・・', 'あなたは??? AIに' + movedcount + '手粘ったものの負けてしまいました・・・')

# 難度分け
def we():
    global modeNum
    modeNum = 1
    grid()
    messagebox.showinfo('Notification', 'ゲームモードが変更されました(Gamemode:WEAK)')
def mid():
    global modeNum
    modeNum = 2
    grid()
    messagebox.showinfo('Notification', 'ゲームモードが変更されました(Gamemode:MIDDLE)')
def st():
    global modeNum
    modeNum = 3
    grid()
    messagebox.showinfo('Notification', 'ゲームモードが変更されました(Gamemode:STRONG)')
def omg():
    global modeNum
    modeNum = 4
    grid()
    messagebox.showinfo('Notification', 'ゲームモードが変更されました(Gamemode:???)')

def qui():
    root.quit()

# メニュー
menu_ROOT = Menu(root)
root.configure(menu=menu_ROOT)
menu_GAME = Menu(menu_ROOT, tearoff=False)

menu_ROOT.add_cascade(label='GAME(G)', under=4, menu=menu_GAME)
menu_ROOT.add_command(label="EXIT(E)", under=3, command=qui)

# GAMEメニューの下でプルダウンで出す難易度選択
menu_GAME.add_command(label="WEAK(W)", under=3, command=we)
menu_GAME.add_command(label="MIDDLE(M)", under=3, command=mid)
menu_GAME.add_command(label="STRONG(S)", under=3, command=st)
menu_GAME.add_command(label="?????(P)", under=3, command=omg)

# ゲーム画面配置
root.configure(background='')  # 色を決める
root_frame = Frame(root, relief='groove', borderwidth=5, bg='LightGray')
game_frame = Frame(root_frame, width=300, height=300,
                   relief='ridge', borderwidth=3, bg='LightGreen')
root_frame.pack()
game_frame.pack(pady=5, padx=5)
grid()

# 最初の注意事項
messagebox.showinfo('難易度選択', 'この画面ではまだAIは動いていません。上のメニュー(AIの項目)から難易度を選んでください。(駒を置くことはできます)')

# メインループ
root.mainloop()

# FIVE AI Project(2018.9-) by Kuske and severrabaen
# AI-Kuske,(severrabaen)
# Game-severrabaen,(Kuske)
