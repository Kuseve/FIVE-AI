from tkinter import *
from tkinter import messagebox
import numpy as np
#import dropbox
import datetime
import time
from enum import *
from flask import Flask
from AI import *
import define

# 構造体の宣言
class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# デバッグモードのフラグ
isDebug = False

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
playerState = {'gameMode': define.gameMode(0), 'AILevel': define.AILevel(0), 'movedCount': 0}

if isDebug == True:
    print(playerState)

# マップのデータ(各数字の意味はgridStateを参照)
grids = np.zeros((define.gridSize.width, define.gridSize.height))

root = Tk()
#タイトル
root.title("FIVE AI")
# フルスクリーン化
root.state('zoomed')
#サイズ変更不可にする(無限にバグるのでね)
root.resizable(0,0)

class gameGrid:
    def __init__(self, hash: int, point: Point):
        self.hash = hash
        self.state = gridState.empty
        self.point = point
        self.frame = Frame(game_frame, width=30,height=30,bd=3, relief='raised', bg='LightGray')
        self.frame.bind("<1>", leftClicked) # イベントの設定
        self.frame.num = hash
        self.frame.grid(row=point.x, column=point.y)

#マス目が全部埋まってるか確認(埋まっているならTrue,elseはFalseを返す)
def isFill():
    i=0
    j=0
    fill=True
    for i in range(define.gridSize.width):
        for j in range(define.gridSize.height):
            if  not grids[i][j]=='o' and not grids[i][j]=='x':
                fill=False
    return fill

# マス目が左クリックされた際の処理
def leftClicked(event):
    global grids, playerState
    hash = event.widget.num
    if grids[frame_list[hash].point.x][frame_list[hash].point.y] == gridState.empty:
        grids[frame_list[hash].point.x][frame_list[hash].point.y] = gridState.player
        playerState['movedCount'] += 1
        changeGrid(frame_list[hash].point, hash, gridState.player)
        if isFill()==True:
            win()   # 引き分けじゃないの？
        # AIのターン
        if playerState['AILevel'] == AILevel.week:
            buf = weakAI()
            changeGrid(buf, define.gridSize.width * buf.y + buf.x, gridState.AI)
        elif playerState['AILevel'] == AILevel.middle:
            buf = middleAI()
            changeGrid(buf, define.gridSize.width * buf.y + buf.x, gridState.AI)
        elif playerState['AILevel'] == AILevel.strong:
            buf = strongAI()
            changeGrid(buf, define.gridSize.width * buf.y + buf.x, gridState.AI)
        elif playerState['AILevel'] == AILevel.omg:
            buf = omgAI()
            changeGrid(buf, define.gridSize.width * buf.y + buf.x, gridState.AI)

        if isFill()==True:
            win()   # 引き分けじゃないの？

    else:   # ラベルの隙間をクリックしたとき
        messagebox.showinfo('駒を置くことができません', 'まだ駒が置かれていないマスにのみ駒を置くことができます。')

def textLabelClicked(event):
    messagebox.showinfo('駒を置くことができません', 'まだ駒が置かれていないマスにのみ駒を置くことができます。')

# マス目の状態を変更する
def changeGrid(point: Point, hash: int, toState: int):
    if isDebug == True:
        messagebox.showinfo('', 'point : {' + str(point.x) + ', ' + str(point.y) + '}'  + '\nhash : ' + str(hash) + '\ntoState : ' + str(toState))
    global movedcount, diffNum, gridText, frame_list
    frame_list[hash].frame.configure(relief='ridge', bd='1')
    # マスの中に文字を表示
    frame_list[hash].textLabel = Label(frame_list[hash].frame, text = define.gridText[toState], bg = 'LightGray')
    frame_list[hash].textLabel.place(width = 28, height = 28)
    frame_list[hash].textLabel.bind('<1>', textLabelClicked)

# マス目生成
def grid():
    global frame_list
    i = 0
    for x in range(define.gridSize.width):
        for y in range(define.gridSize.height):
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
    # Dropboxを使用して難易度ごとのランキングを作りたい
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
    # ランキングに登録する
    ranking()

def lose():
    global modeNum
    # 結果確認画面
    if modeNum == 1:
        messagebox.showinfo('残念・・・', 'あなたはWEAK AIに' + movedcount + '手粘ったものの負けてしまいました・・・')
    elif modeNum == 2:
        messagebox.showinfo('残念・・・', 'あなたはMIDDLE AIに' +movedcount + '手粘ったものの負けてしまいました・・・')
    elif modeNum == 3:
        messagebox.showinfo('残念・・・', 'あなたはSTRONG AIに' +movedcount + '手粘ったものの負けてしまいました・・・')
    elif modeNum == 4:
        messagebox.showinfo('残念・・・', 'あなたは??? AIに' + movedcount + '手粘ったものの負けてしまいました・・・')

# 難易度選択時の処理
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

#ゲームをやめる
def qui():
    root.quit()

# メニューの要素
menu_ROOT = Menu(root)
root.configure(menu=menu_ROOT)
menu_GAME = Menu(menu_ROOT, tearoff=False)
menu_ROOT.add_cascade(label='GAME', under=5, menu=menu_GAME)
menu_ROOT.add_command(label='EXIT', under=5, command=qui)

# GAMEメニューの下でプルダウンで出す難易度選択
menu_GAME.add_command(label='WEAK', under=5, command=we)
menu_GAME.add_command(label='MIDDLE', under=7, command=mid)
menu_GAME.add_command(label='STRONG', under=7, command=st)
menu_GAME.add_command(label='?????', under=6, command=omg)

# 要素をゲーム画面に配置
root.configure(background='gray')  # 暫定色
root_frame = Frame(root, relief='groove', borderwidth=5, bg='LightGray')
game_frame = Frame(root_frame, width=300, height=300,relief='ridge', borderwidth=3, bg='LightGreen')
root_frame.pack()
game_frame.pack(pady=5, padx=5)
grid()

# 最初の注意事項
messagebox.showinfo('注意！！', 'この画面ではまだAIと対戦はできません!\n上のメニュー(GAMEの項目)から難易度を選んでください。(駒を置くことはできます)')

# メインループ
root.mainloop()

# FIVE AI Project(2018.9-) by Kuske and severrabaen
# AI-Kuske,(severrabaen)
# Game-severrabaen,(Kuske)
