import socket
import pygame
import math
import tkinter
from tkinter import ttk
import tkinter.messagebox
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
name=""
color=""
root=tkinter.Tk()
root.title("Логин")
root.geometry("300x200")
style=ttk.Style()
#style.theme_use("combo")
def draw_backterii(data:list[str]):
    for num, bact in enumerate(data):
        data= bact.split(" ")
        x=cc[0]+int(data[0])
        y=cc[1]+int(data[1])
        size=int(data[2])
        color=data[3]
        pygame.draw.circle(scren,color,(x,y),size)
def find(vector:str):
    first=vector.find("<")
    second=vector.find(">")
    if first<second and first>=0:
        result=vector[first+1:second]
        return result
    return ""
def scroll(event):
    global color
    color=comdo.get()
    style.configure("TCombobox",fieldbackground=color,background=color)
def login():
    global name
    name=row.get()
    if name and color:
        root.destroy()
        root.quit()
    else:
        tkinter.messagebox.showerror("Ошибка","Ты не выбрал цвет или не ввел имя!")
name_label=tkinter.Label(root,text="Введите вам никнайм:")
name_label.pack()
row=tkinter.Entry(root,width=30,justify="center")
row.pack()
color_label=tkinter.Label(root,text="Вы берите цвет")
color_label.pack()
colors=["Maroon","DarkRed","Firebrick","Red","Salmon","tomato","Coral","OrangeRed","Chocolate","SandyBrown","DarkOrange","Orange","DarkGoldenRod","GoldenRod","Gold","Olive","Yellow","YellowGreen","greenYellow","Chartreuse","LawnGreen","Green","Lime","SpringGreen","MediumSpringGreen","Turquoise","lightSeaGreen","MediumTurquoise","Teal","DarkCyan","Aqua","Cyan","DeepSkyBlue","DodgerBlue","RoyalBlue","Navy","DarkBlue","MediumBlue"]
comdo=ttk.Combobox(root,values=colors,textvariable=color)
comdo.bind("<<ComboboxSelected>>",scroll)
comdo.pack()
name_btn=tkinter.Button(root,text="Зайти в игру",command=login)
name_btn.pack()
root.mainloop()
sock.connect(("localhost",10000))
sock.send(("color:<"+ name+","+color+">").encode())
pygame.init()
WIDHT=800
HIEGHT=600
scren=pygame.display.set_mode((WIDHT,HIEGHT))
pygame.display.set_caption("бактерии")

cc=(WIDHT//2,HIEGHT//2)
old=(0,0)
run=True
radius=50
while run:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run=False

    if pygame.mouse.get_focused():
        pos=pygame.mouse.get_pos()
        vector= pos[0] - cc[0],pos[1]-cc[1]
        lennv=math.sqrt(vector[0]**2+vector[1]**2)
        vector=vector[0]/ lennv,vector[1]/lennv
        if lennv <=radius:
            vector=0,0
        if vector !=old:
            old=vector
            msg=f"<{vector[0]},{vector[1]}"
            sock.send(msg.encode())
    sock.send("".encode())
    data = sock.recv(1024).decode()
    data=find(data).split(",")
    scren.fill("gray")
    pygame.draw.circle(scren,color,cc,radius)
    if data!=[' ']:
        draw_backterii(data)
    pygame.display.update()
pygame.quit()