from tkinter import *
from tkinter import Tk, messagebox
import numpy as np

#ここら辺はグローバル変数とか定数とか
#マスは15*15
grid_height=15
grid_width=15
#手数記録用(ランキングで使う)
movedcount=0
      
#メイン画面
root = Tk()
root.title("FIVE AI")
#フルスクリーン化
root.state('zoomed')
root.resizable(0,0)

#メニュー
menu_ROOT = Menu(root)
root.configure(menu = menu_ROOT)
menu_GAME = Menu(menu_ROOT, tearoff = False)
menu_ROOT.add_cascade(label = 'GAME', under = 4, menu = menu_GAME)

#GAMEメニューの下でプルダウンで出す難易度選択
menu_GAME.add_command(label = "WEAK", under = 3)
menu_GAME.add_command(label = "MIDDLE", under = 3)
menu_GAME.add_command(label = "STRONG", under = 3)
menu_GAME.add_command(label = "?????", under = 3)

menu_ROOT.add_command(label = "EXIT", under = 3)#exitの処理を入れたい(落ちる)

#ゲーム画面配置
root_frame = Frame(root, relief = 'groove', borderwidth = 5, bg = 'LightGray')
game_frame = Frame(root_frame, width = 300, height = 300, relief = 'ridge', borderwidth = 3, bg = 'LightGreen')
root_frame.pack()
game_frame.pack(pady = 5, padx = 5)

#マス目が左クリックされた際の処理
def leftClicked(event):
    global movedcount
    event.widget.configure(relief = 'ridge', bd = '1')
    gridText=Label(event.widget,text="○",bg='LightGray')
    gridText.place(width=28,height=28)
    movedcount=movedcount+1

#1度クリックされたマス目を操作できないようにする
def stop(evemt):
    pass

#マス目描画
frame_list = []
for x in range(grid_height):
    for y in range(grid_width):
        frame = Frame(game_frame, width = 30, height = 30, bd = 3, relief = 'raised', bg = 'LightGray')
        frame.bind("<1>", leftClicked)
        frame_list.append(frame)
        frame.grid(row=x, column=y)

#煽り
messagebox.showinfo('ゲーム開始','FIVE AIが開始されました。頑張って勝ってみてください。')

#メインループ
root.mainloop()
