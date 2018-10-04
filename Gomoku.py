import datetime
import time
import random
import numpy as np
import dropbox
from flask import Flask

score=0

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
