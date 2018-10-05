from tkinter import *
import numpy as np

#ここら辺はグローバル変数とか定数とか
#マスは15*15
grid_height=15
grid_width=15
#手数記録用
movedcount=0
#既に駒が置かれているかどうか
emporfull=np.array

class fullScreen(object): 
    def __init__(self, master, **kwargs): 
     self.master=master 
     pad=3 
     self._geom='200x200+0+0' 
     master.geometry("{0}x{1}+0+0".format(
     master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad)) 
     master.bind('<Escape>',self.toggle_geom)    
     def toggle_geom(self,event): 
       geom=self.master.winfo_geometry() 
       print(geom,self._geom) 
       self.master.geometry(self._geom) 
       self._geom=geom 
      
#メイン画面
root = Tk()
root.title("FIVE AI")
app=fullScreenApp(root) 
root.resizable(0,0)
      
#メニュー
menu_ROOT = Menu(root)
root.configure(menu = menu_ROOT)
menu_GAME = Menu(menu_ROOT, tearoff = False)
menu_ROOT.add_cascade(label = 'ゲーム', under = 4, menu = menu_GAME)

menu_GAME.add_command(label = "かんたん", under = 3)
menu_GAME.add_command(label = "ふつう", under = 3)
menu_GAME.add_command(label = "むずかしい", under = 3)
manu_GAME.add_command(label = "Ω", under = 3)

menu_ROOT.add_command(label = "終了", under = 3)

#ゲーム画面配置
root_frame = Frame(root, relief = 'groove', borderwidth = 5, bg = 'LightGray')
game_frame = Frame(root_frame, width = 300, height = 300, relief = 'ridge', borderwidth = 3, bg = 'LightGreen')
root_frame.pack()
game_frame.pack(pady = 5, padx = 5)
 
#leftClickedの処理
def leftClicked(event):
  
  
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
        
root.mainloop()
