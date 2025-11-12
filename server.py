import socket
import time
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker
import pygame

pygame.init()
WIDHT=4000
HIEGHT=4000
server_WIDHT=300
server_HIEHT=300
FPS=100
scren=pygame.display.set_mode((server_WIDHT,server_HIEHT))
pygame.display.set_caption("server")
clock=pygame.time.Clock()

create=create_engine("postgresql+psycopg2://postgres:Cu8-Urh-eWu-jAQ@localhost/base")
Seseon=sessionmaker(bind=create)
s=Seseon()
Base=declarative_base()
def find(vector:str):
    first=None
    for num,sing in enumerate(vector):
        if sing =="<":
            first=num
        if sing==">":
            second=num
            result=vector[first+1:second]
            result=result.split(",")
            result=map(float,result)
            return result
    return ""
def find_color(vector:str):
    first=vector.find("<")
    second=vector.find(">")
    if first < second and first >= 0:
        result=vector[first+1: second]
        result=result.split(",")
        return result
    return ""
class Players(Base):
    __tablename__="gamers"
    id=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    name=Column(String(250))
    adres=Column(String)
    x=Column(Integer,default=500)
    y=Column(Integer, default=500)
    size=Column(Integer,default=50)
    errors=Column(Integer,default=0)
    ads_speed=Column(Integer,default=2)
    speed_x=Column(Integer,default=2)
    speed_y=Column(Integer,default=2)
    color=Column(String(250),default="red")
    w_vision=Column(Integer,default=800)
    h_vision=Column(Integer,default=600)
    def __init__(self,name,adres):
        self.name=name
        self.adres=adres
class Localplayer:
    def __init__(self,adres,id, name,sock ):
        self.id=id
        self.db:Players=s.get(Players,self.id)
        self.sock=sock
        self.name=name
        self.adres=adres
        self.x=500
        self.y=500
        self.size=50
        self.error=0
        self.ads_speed=1
        self.speed_x=0
        self.speed_y=0
        self.color="red"
        self.w_vision=800
        self.h_vision=600
    def sync(self):
        self.db.id=self.id
        self.db.ads_speed=self.ads_speed
        self.db.speed_x=self.speed_x
        self.db.speed_y=self.speed_y
        self.db.errors=self.error
        self.db.x=self.x
        self.db.y=self.y
        self.db.color=self.color
        self.db.w_vision=self.w_vision
        self.db.h_vision=self.h_vision
        s.merge(self.db)
        s.commit()
    def load(self):
        self.size=self.db.id=self.id
        self.ads_speed=self.db.ads_speed
        self.speed_x=self.db.speed_x
        self.speed_y=self.db.speed_y
        self.x=self.db.x=self.x
        self.y=self.db.x=self.y
        self.color=self.db.color
        self.w_vision=self.db.w_vision
        self.h_vision=self.db.h_vision
        return self
    def update(self):
        self.x+=self.speed_x
        self.y+=self.speed_y
    def change_speed(self,vector):
        vector=find(vector)
        if vector[0]==[0] and vector[1]==0:
            self.speed_x=self.speed_y=0
        else:
            vector=vector[0]*self.ads_speed,vector[1]*self.ads_speed
            self.speed_x=vector[0]
            self.speed_y=vector[1]

Base.metadata.create_all(create)
main_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
main_socket.bind(("localhost",10000))
main_socket.setblocking(False)
main_socket.listen(3)
print("сокет создался")

players={}
server_works=True
while server_works:
    clock.tick(FPS)
    try:
        new_socket, addr=main_socket.accept()
        print("подключился",addr)
        new_socket.setblocking(False)
        login=new_socket.recv(1024).decode()
        player=Players("Имя",addr)
        if login.startswith("color"):
            data=find_color(login[6:])
            player.name,player.color=data

        s.merge(player)
        s.commit()
        addr=f"({addr[0]},{addr[1]})"
        data=s.query(Players).filter(Players.adres==addr)
        for user in data:
            player=Localplayer(addr,user.id,"Имя",new_socket).load()
            players[user.id]=player

    except BlockingIOError:
        pass
    for id in list(players):
        try:
            data=players[id].sock.recv(1024).decode()
            print("Получил",data)
            players[id].change_speed(data)
        except:
                pass
    visible_backteries={}
    for id in list(players):
        visible_backteries[id]=[]
        pairs=list(players.items())
        for i in range(0,len(pairs)):
            for j in range(i+1,len(pairs)):
                hero1:Localplayer=pairs[i][1]
                her2:Localplayer=pairs[j][1]
                dest_x=her2.x-hero1.x
                dest_y=her2.y-hero1.y
                if abs(dest_x)<=hero1.w_vision//2+her2.size and abs(dest_y)<=hero1.h_vision//2+her2.size:
                    x_=str(round(dest_x))
                    y_=str(round(dest_y))
                    size_=str(round(her2.size))
                    color_=her2.color
                    data=x_+" "+y_+" "+size_+" "+color_
                    visible_backteries[hero1.id].append(data)
                if abs(dest_x) <= her2.w_vision // 2 + hero1.size and abs(dest_y) <= her2.h_vision // 2 + hero1.size:
                    x_ = str(round(-dest_x))
                    y_ = str(round(-dest_y))
                    size_ = str(round(hero1.size))
                    color_ = hero1.color
                    data=x_+" "+y_+" "+size_+" "+color_
    for id in list(players):
        visible_backteries[id]="<"+",".join(visible_backteries[id])+">"
    for id in list(players):
        try:
            players[id].sock.send(visible_backteries[id].encode())
        except:
            players[id].sock.close()
            del players[id]
            s.query(Players).filter(Players.id == id).delete()
            s.commit()
            print("сокет закрыт")
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            server_works=False
    scren.fill("Black")
    for id in players:
        player=players[id]
        players[id].update()
        x=player.x*server_WIDHT//WIDHT
        y=player.y*server_HIEHT//HIEGHT
        size=player.size*server_WIDHT//WIDHT
        pygame.draw.circle(scren,player.color,(x,y),size)

    pygame.display.update()
pygame.quit()
main_socket.close()
s.query(Players).delete()
s.commit()
