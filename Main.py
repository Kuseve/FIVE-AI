from tkinter import *
from tkinter import Tk, messagebox
import numpy as np
import tensorflow as tf

#ここら辺はグローバル変数とか定数とか
#マスは15*15
grid_height=15
grid_width=15
#マス目
i = 0
frame_list = []
#0=empty,1=player,2=AI
grids=np.zeros((grid_height, grid_width))
#手数記録用(ランキングと結果に使いたい)
movedcount=0
#ゲームモード(難易度)
diffNum=-1
#表示するメッセージ
messageNum=-1

#メイン画面
root = Tk()
root.title("FIVE AI")
#フルスクリーン化
root.state('zoomed')

def takegrid(event):
        global movedcount
        event.widget.configure(relief = 'ridge', bd = '1')
        gridText=Label(event.widget,text="○",bg='LightGray')
        gridText.place(width=28,height=28)
        movedcount=movedcount+1
        if diffnum==1:
            weakai()
        elif diffnum==2:
            middleai()
        elif diffnum==3:
            strongai()
        else:
            omgai()
            
#マス目が左クリックされた際の処理
def leftClicked(x,y):
        global grids
        if grids[x][y]==0:
            grids[x][y]=1
            takegrid
        else:
            massagebox.showinfo('駒を置くことができません','まだ駒が置かれていないマスにのみ駒を置くことができます。')    

#マス目描画
def grid():
    for x in range(grid_height):
        for y in range(grid_width):
            frame = Frame(game_frame, width = 30, height = 30, bd = 3, relief = 'raised', bg = 'LightGray')
            frame.bind("<1>", leftClicked(x,y))
            frame.num = i
            frame_list.append(frame)
            frame.grid(row=x, column=y)
        
def fromDropbox():
    global movedcount
    dbox = dropbox.Dropbox(os.environ["DROPBOX_KEY"])
    dbox.users_get_current_account()
                      
def intoDropbox():
    global movedcount
    dbox = dropbox.Dropbox(os.environ["DROPBOX_KEY"])
    dbox.users_get_current_account()

def ranking():
    # ドロボを使用してランキングを作りたい
    fromDropbox()
        
def result():
    global diffNum
    #結果確認画面
    if diffNum==1:
        messagebox.showinfo('おめでとうございます！！','あなたはWEAK AIに'+movedcount+'手で勝利しました！！このAIは弱かったですか？弱かったですね。')
    elif diffNum==2:
        messagebox.showinfo('おめでとうございます！！','あなたはMIDDLE AIに'+movedcount+'手で勝利しました！！このAIは常人レベルに強さを留めてあります。まあ勝てますよね。')
    elif diffNum==3:
        messagebox.showinfo('おめでとうございます！！','あなたはSTRONG AIに'+movedcount+'手で勝利しました！！このAIに勝つとは中々ですね・・・五目並べプロ級です。')
    elif diffNum==4:
        messagebox.showinfo('おめでとうございます！！','あなたは??? AIに'+movedcount+'手で勝利しました！！このメッセージを読んでいる人は地球上に居ないと思っています(そのくらい強いです)。')
    
    ranking()

#難度分け
def we():
    global diffNum
    diffNum=1
    grid()
    messagebox.showinfo('Notification','ゲームモードが変更されました(Gamemode:WEAK)')
def mid():
    global diffNum
    diffNum=2
    grid()
    messagebox.showinfo('Notification','ゲームモードが変更されました(Gamemode:MIDDLE)')
def st():
    global diffNum
    diffNum=3
    grid()
    messagebox.showinfo('Notification','ゲームモードが変更されました(Gamemode:STRONG)')
def omg():
    global diffNum
    diffNum=4
    grid()
    messagebox.showinfo('Notification','ゲームモードが変更されました(Gamemode:???)')
def qui():
    root.quit()
    
#メニュー
menu_ROOT = Menu(root)
root.configure(menu = menu_ROOT)
menu_GAME = Menu(menu_ROOT, tearoff = False)
menu_ROOT.add_cascade(label = 'GAME', under = 4, menu = menu_GAME)

#GAMEメニューの下でプルダウンで出す難易度選択
menu_GAME.add_command(label = "WEAK", under = 3,command=we)
menu_GAME.add_command(label = "MIDDLE", under = 3,command=mid)
menu_GAME.add_command(label = "STRONG", under = 3,command=st)
menu_GAME.add_command(label = "?????", under = 3,command=omg)
menu_ROOT.add_command(label = "EXIT", under = 3,command=qui)

#ゲーム画面配置
root.configure(background='')#色を決める
root_frame = Frame(root, relief = 'groove', borderwidth = 5, bg = 'LightGray')
game_frame = Frame(root_frame, width = 300, height = 300, relief = 'ridge', borderwidth = 3, bg = 'LightGreen')
root_frame.pack()
game_frame.pack(pady = 5, padx = 5)
grid()
#最初の注意事項
messagebox.showinfo('難易度選択','この画面ではまだAIは動いていません。上のメニュー(AIの項目)から難易度を選んでください。(駒を置くことはできます)')

#メインループ
root.mainloop()


#FIVE AI Project(2018.9-) by Kuske and severrabaen
#AI-Kuske,(severrabaen)
#Game-severrabaen,(Kuske)
