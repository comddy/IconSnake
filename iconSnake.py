from commctrl import *
from win32gui import *
from time import sleep
from win32api import *
from random import randrange
from pynput import keyboard
from threading import Thread
import os
import tkinter as tk
from tkinter import messagebox
from sys import exit
from platform import win32_ver
from pygame import mixer
#1860 20   20 980

#160
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
Key = RIGHT
food_pos = [randrange(20,1860,80),randrange(20,980,80)] #设置随机食物
all_food = []
all_body = []
init_snake_pos = [[500,500],[420,500],[340,500]]
head_pos = [500,500]
Speed = 0.3
DeskPath = os.path.join(os.path.expanduser("~"), 'Desktop')
hwndDesktop = 0
MODE = 0
win_version = win32_ver()[0]
run = 1




def GetDesktopHandle():
	global hwndDesktop
	if win_version == "10":
		hWndList = []
		EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)  #获取桌面所有控件
		for h in hWndList:
			hwndShelldll = FindWindowEx(h,0,"SHELLDLL_DefView","")
			if hwndShelldll:
				hwndDesktop = FindWindowEx(hwndShelldll, 0, "SysListView32", "FolderView")
	else:
		hwnd = FindWindowEx(0,0,"Progman","Program Manager")
		hwndShelldll = FindWindowEx(hwnd,0,"SHELLDLL_DefView","")
		hwndDesktop = FindWindowEx(hwndShelldll,0,"SysListView32","FolderView")
def RandomIcon(): #彩蛋--随机设置图标
	t = 0
	while t < 30:
		for _ in range(c):
			SetIconPosition(_,randrange(20,1860,80),randrange(20,980,80))
		sleep(0.3)
		t += 1
def WinIcon(): #彩蛋--胜利WIN
	win_pos = [[300,300],[300,400],[300,500],[380,400],[380,500],[460,300],[460,400],[460,500],
			[820,160],[820,300],[820,400],[820,500],
			[1180,300],[1180,400],[1180,500],[1260,300],[1340,300],[1340,400],[1340,500]]
	i = 0
	for _ in range(c):
		SetIconPosition(_,0,-1000)
	sleep(0.5)
	for _ in win_pos:
		SetIconPosition(i,_[0],_[1])
		sleep(0.3)
		i+=1
	
def LoveIcon(): #彩蛋--爱心 用到26个图标
	sleep(1)
	my_love = [[800,300],[730,240],[660,180],[870,240],[940,180],[800,800],
			[590,210],[520,260],[480,320],[500,400],[540,460],[580,520],[620,580],[660,640],[700,700],[740,760],
			[1010,210],[1080,260],[1120,320],[1100,400],[1060,460],[1020,520],[980,580],[940,640],[900,700],[860,760]]
	i = 0
	for _ in my_love:
		SetIconPosition(i,_[0],_[1])
		i+=1
		sleep(0.3)
def Mdir():
	for _ in range(100):
		os.mkdir(os.path.join(DeskPath,str(_)))
	sleep(2)
def Rdir():
	for _ in range(100):
		path = os.path.join(DeskPath,str(_))
		if os.path.exists(path):
			os.rmdir(path)
def GameOver():
	global run
	Rdir()
	run = 0
	# os.system('taskkill /F /IM python.exe')
def Popup(Title,Content):
	r = tk.Tk()
	r.withdraw()
	messagebox.showwarning(Title,Content)
def on_press(key):#检测按的哪个键,主要监视上下左右
	global Key
	if key == keyboard.Key.left:
		Key = LEFT
	elif key == keyboard.Key.right:
		Key = RIGHT
	elif key == keyboard.Key.up:
		Key = UP
	elif key == keyboard.Key.down:
		Key = DOWN
def hit_the_wall():
	if head_pos[0] > 1860 or head_pos[0] < 20 or head_pos[1] > 980 or head_pos[1] < 20:
		GameOver()
def on_release(key): #按esc退出游戏
	if key == keyboard.Key.esc:
		GameOver()
		return False
def monitor_keyboard(): #监视键盘
	with keyboard.Listener(on_release=on_release,on_press=on_press) as listener:
		listener.join()
def MAKELPARAM(x,y): #转换坐标信息
	return x+(y << 16)
def play_music():
	mixer.init()
	mixer.music.load("breakinPoint.mp3")
	mixer.music.play()
def init_snake_body():  
	global all_body
	i=0
	for _ in range(c-1,c-4,-1):
		SetIconPosition(_,420+i,420)
		all_body.append(_)
		i+=80
def init_snake():  #初始化蛇皮
	global all_food
	for _ in range(0,c-3):
		SetIconPosition(_,-100,0) #将无关的图标移走
		all_food.append(_)
	init_snake_body()
		
def SetIconPosition(index,x,y):
	PostMessage(hwndDesktop,LVM_SETITEMPOSITION,index,MAKELPARAM(x,y))

def move_snake(index,statu):
	global head_pos,init_snake_pos,food_pos,all_body,Speed
	if head_pos == food_pos:
		init_snake_pos.append(food_pos)
		#print(init_snake_pos) 调试用
		all_body.append(all_food[len(all_food)-1])  #取食物最后面的哪个
		all_food.pop()   #取了之后删除掉
		if all_food == []:  #如果食物为空，游戏结束
			if MODE:
				RandomIcon()
				WinIcon()
				LoveIcon()
				GameOver()
			else:
				GameOver()
		if len(all_body) == 5:
			Speed = 0.2
		if len(all_body) == 8:
			Speed = 0.1
		food_pos = [randrange(20,1860,80),randrange(20,980,80)] #重新设置食物
		if all_food == []:
			pass
		else:
			while food_pos in init_snake_pos:   #如果食物与身体重合则后重新设置,直到不重合
				food_pos = [randrange(20,1860,80),randrange(20,980,80)]
			print(len(all_food))
			SetIconPosition(all_food[len(all_food)-1],food_pos[0],food_pos[1])

	if index == 0: #判断左右，statu具体左还是右
		if statu == 0: #左
			head_pos[0] -= 80
			init_snake_pos.insert(0,list(head_pos))
		else:
			head_pos[0] += 80
			init_snake_pos.insert(0,list(head_pos))
			
	else:#上下
		if statu == 0:  #下
			head_pos[1] += 80
			init_snake_pos.insert(0,list(head_pos))
		else:
			head_pos[1] -= 80
			init_snake_pos.insert(0,list(head_pos))
	hit_the_wall()
	init_snake_pos.pop()
	#print(init_snake_pos) 调试用
def on_closing(root):
    if messagebox.askokcancel("退出", "确定退出吗"):
        root.destroy()
        exit(0)
def Unlimited(root):
	MODE = 1
	Mdir()
	if var.get():
		play_music()
	root.destroy()
def Normol(root):
	if var.get():
		play_music()
	root.destroy()
def Menu():
	root = tk.Tk()
	root.geometry("500x200")
	root.resizable(0,0)
	root.title("图标贪吃蛇")
	try:		
		path = os.path.join(os.getcwd(),"snake.png")	
		path_icon = os.path.join(os.getcwd(),"snake.ico")
		root.iconbitmap(path_icon)
		photo = tk.PhotoImage(file=path)
		tk.Label(root,image=photo,width="500",height="80").pack()
	except:
		Popup("错误","缺少资源文件\n"+path+"\n"+path_icon)
	tk.Label(root,fg="red",text="如果游戏不能正常运行\n请将自动排列图标与将图标与网格对齐两项取消勾选\n游戏以图标为载体,若想提前结束游戏，可按ESC键结束\n困难模式胜利后有图标动画彩蛋哦~").pack()
	tk.Button(root,text="普通模式",width="20",height="20",command=lambda:Normol(root)).pack(side="left")
	tk.Button(root,text="困难模式",width="20",height="20",command=lambda:Unlimited(root)).pack(side="right")
	global var
	var = tk.IntVar()
	var.set(1)
	tk.Checkbutton(root,text="背景音乐",variable=var,onvalue=1,offvalue=0).pack()
	root.protocol("WM_DELETE_WINDOW", lambda:on_closing(root)) #拦截关闭消息
	root.mainloop()

Menu()
GetDesktopHandle()
c = SendMessage(hwndDesktop,LVM_GETITEMCOUNT,0,0) #桌面图标数量
init_snake()  #初始化游戏界面
t = Thread(target=monitor_keyboard)  #添加到多线程，可以有两个死循环
t.daemon = True
t.start()
SetIconPosition(len(all_food)-1,food_pos[0],food_pos[1])
while run:
	if Key == UP:
		move_snake(1,1)
	elif Key == DOWN:
		move_snake(1,0)
	elif Key == LEFT:
		move_snake(0,0)
	elif Key == RIGHT:
		move_snake(0,1)
	#print(init_snake_pos) 调试用
	body_index = 0
	for x in init_snake_pos: #正式移动
		SetIconPosition(all_body[body_index],x[0],x[1])
		body_index+=1
	sleep(Speed)

Popup("提示","游戏结束")
#Width = int(GetSystemMetrics(SM_CXSCREEN)/2)
#Height = int(GetSystemMetrics(SM_CYSCREEN)/2)
#hwndWorkerW = win32gui.FindWindowEx(0,0,"WorkerW","")
#hwndShelldll = win32gui.FindWindowEx(hwndWorkerW,0,"SHELLDLL_DefView","")
#hwndDesktop = win32gui.FindWindowEx(hwndShelldll, 0, "SysListView32", "FolderView")
#win32api.SendMessage(hwndDesktop,commctrl.LVM_GETITEMCOUNT,0,0)  获取桌面图标数量
#PostMessage(hwndDesktop,LVM_SETITEMPOSITION,11,MAKELPARAM(100,10)) 设置图标位置
#SendMessage(hwndDesktop,LVM_GETITEMPOSITION,1,LPARAM PPT)  不需要获取桌面图标坐标，害我搞半天	
"""win10版本
hWndList = []
EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)  #获取桌面所有控件
for h in hWndList:
	hwndShelldll = FindWindowEx(h,0,"SHELLDLL_DefView","")
	if hwndShelldll:
		hwndDesktop = FindWindowEx(hwndShelldll, 0, "SysListView32", "FolderView")
		#print(hwndDesktop)桌面句柄

win7
	hwnd = FindWindowEx(0,0,"Progman","Program Manager")
	hwndShelldll = FindWindowEx(hwnd,0,"SHELLDLL_DefView","")
	hwndDesktop = FindWindowEx(hwndShelldll,0,"SysListView32","FolderView")"""