import datetime
import time
import random
import numpy as np
import dropbox
from flask import Flask
from tkinter import *

#後でファイルは分ける


#マスは15*15
grid_height=15
grid_width=15
score=0

#メイン画面
root = Tk()
root.title("FIVE AI")
root.resizable(0,0)     #サイズ変更不可にする
 
root.mainloop()

#左クリックされた時の処理
def leftClicked():
  
  
#マス目描画
i = 0
frame_list = []
for x in range(grid_height):
    for y in range(grid_width):
        frame = Frame(game_frame, width = 30, height = 30, bd = 3, relief = 'raised', bg = 'LightGray')
        frame.bind("<1>", leftClicked)
        frame.num = i
        frame_list.append(frame)
        frame.grid(row=x, column=y)
        i += 1

#ドロボ(からファイルを持ってくる)
def fromDropbox():
  global score
  dbox=dropbox.Dropbox(os.environ["DROPBOX_KEY"])
  dbox.users_get_current_account()
  
#ドロボ(にファイルを入れる)
def intoDropbox():
  global score
  dbox = dropbox.Dropbox(os.environ["DROPBOX_KEY"])
  dbox.users_get_current_account()
  
  
def processing():
  #ここでいろいろな処理をする
  
  
def ranking():
  #ドロボを使用してランキングを作りたい
  fromDropbox()
