from tkinter import *

#メニュー
menu_ROOT = Menu(root)
root.configure(menu = menu_ROOT)
menu_GAME = Menu(menu_ROOT, tearoff = False)
menu_ROOT.add_cascade(label = 'ゲーム', under = 4, menu = menu_GAME)

menu_GAME.add_command(label = "かんたん", under = 3)
menu_GAME.add_command(label = "ふつう", under = 3)
menu_GAME.add_command(label = "むずかしい", under = 3)
manu_GAME.add_command(label = "Ω", under = 3)

menu_ROOT.add_command(label = "終了(X)", under = 3)
