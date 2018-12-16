from tkinter import *
from tkinter import messagebox
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
        self.frame.bind("<1>", leftClicked) # イベントの設定
        self.frame.num = hash
        self.frame.grid(row=point.x, column=point.y)

# マス目が左クリックされた際の処理
def leftClicked(event):
    global grids, playerState
    hash = event.widget.num
    if grids[frame_list[hash].point.x][frame_list[hash].point.y] == gridState.empty:
        grids[frame_list[hash].point.x][frame_list[hash].point.y] = gridState.player
        playerState['movedCount'] += 1
        changeGrid(frame_list[hash].point, hash, gridState.player)

        # AIのターン
        if diffNum == 1:
            weakai()
        elif diffNum == 2:
            middleai()
        elif diffNum == 3:
            strongai()
        elif diffNum == 4:
            omgai()

    else:
        messagebox.showinfo('駒を置くことができません', 'まだ駒が置かれていないマスにのみ駒を置くことができます。')

# マス目の状態を変更する
def changeGrid(point: Point, hash: int, toState: int):
    if isDebug == True:
        messagebox.showinfo('', 'point : {' + str(point.x) + ', ' + str(point.y) + '}'  + '\nhash : ' + str(hash) + '\ntoState : ' + str(toState))
    global movedcount, diffNum, gridText, frame_list
    frame_list[hash].frame.configure(relief='ridge', bd='1')

    frame_list[hash].textLabel = Label(frame_list[hash].frame, text = gridText[toState], bg = 'LightGray')
    frame_list[hash].textLabel.place(width = 28, height = 28)

# マス目生成
def grid():
    global frame_list
    i = 0
    for x in range(gridSize.width):
        for y in range(gridSize.height):
            frame_list.append(gameGrid(i, Point(x, y)))
            i += 1


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

menu_ROOT.add_cascade(label='GAME(G)', under=5, menu=menu_GAME)
menu_ROOT.add_command(label='EXIT(E)', under=5, command=qui)

# GAMEメニューの下でプルダウンで出す難易度選択
menu_GAME.add_command(label='WEAK(W)', under=5, command=we)
menu_GAME.add_command(label='MIDDLE(M)', under=7, command=mid)
menu_GAME.add_command(label='STRONG(S)', under=7, command=st)
menu_GAME.add_command(label='?????(P)', under=6, command=omg)

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
