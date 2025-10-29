import socket
import pygame
import math
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)

sock.connect(("localhost",10000))
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
    print("получил", data)
    scren.fill("gray")
    pygame.draw.circle(scren,(255,0,0),cc,radius)
    pygame.display.update()
pygame.quit()