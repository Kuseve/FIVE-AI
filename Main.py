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

#マス目を格納する配列
frame_list = []

# 戦うモード
class gameMode(IntEnum):
    Normal = 0  # AIとの戦い
    quit = auto()  # やめる

# Playerの情報
playerState = {'gameMode': define.gameMode(0), 'define.AILevel': define.AILevel(0), 'movedCount': 0}

if define.isDebug == True:
    print(playerState)

# マップのデータ(各数字の意味はdefine.gridStateを参照)
grids = np.zeros((define.gridSize.width, define.gridSize.height))

root = Tk()
#タイトル
root.title("FIVE AI")
# フルスクリーン化
root.state('zoomed')
#サイズ変更不可にする(無限にバグるのでね)
root.resizable(0,0)

class gameGrid:
    def __init__(self, hash: int, point: define.Point):
        self.hash = hash
        self.state = define.gridState.empty
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
        
def draw():
    messagebix.showinfo('引き分け！','引き分けです。')

# マス目が左クリックされた際の処理
def leftClicked(event):
    global grids, playerState
    hash = event.widget.num
    if grids[frame_list[hash].point.x][frame_list[hash].point.y] == define.gridState.empty:
        grids[frame_list[hash].point.x][frame_list[hash].point.y] = define.gridState.player
        playerState['movedCount'] += 1
        changeGrid(frame_list[hash].point, hash, define.gridState.player)
        if isFill()==True:
            draw()
        # AIのターン
        if playerState['define.AILevel'] == define.AILevel.week:
            buf = weakAI()
            changeGrid(buf, define.gridSize.width * buf.y + buf.x, define.gridState.AI)
        elif playerState['define.AILevel'] == define.AILevel.middle:
            buf = middleAI()
            changeGrid(buf, define.gridSize.width * buf.y + buf.x, define.gridState.AI)
        elif playerState['define.AILevel'] == define.AILevel.strong:
            buf = strongAI()
            changeGrid(buf, define.gridSize.width * buf.y + buf.x, define.gridState.AI)
        elif playerState['define.AILevel'] == define.AILevel.omg:
            buf = omgAI()
            changeGrid(buf, define.gridSize.width * buf.y + buf.x, define.gridState.AI)

        if isFill()==True:
            draw()

    else:   # ラベルの隙間をクリックしたとき
        messagebox.showinfo('駒を置くことができません', 'まだ駒が置かれていないマスにのみ駒を置くことができます。')

def textLabelClicked(event):
    messagebox.showinfo('駒を置くことができません', 'まだ駒が置かれていないマスにのみ駒を置くことができます。')

# マス目の状態を変更する
def changeGrid(point: define.Point, hash: int, toState: int):
    if define.isDebug == True:
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
            frame_list.append(gameGrid(i, define.Point(x, y)))
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
