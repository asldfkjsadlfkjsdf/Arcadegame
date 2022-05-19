import pygame
import random
import time
from datetime import datetime

#1. game initializing
pygame.init()

#2. frame option
size = [800,400]
screen = pygame.display.set_mode(size)

title = "My game"
pygame.display.set_caption(title)

#3. settings
clock = pygame.time.Clock()
color = (0,0,0) #Black


class obj:
    def __init__(self):
        self.x= 0
        self.y= 0
        self.move= 0
    def put_img(self,address):
        self.img = pygame.image.load(address)
        self.sx, self.sy = self.img.get_size()
    def change_size(self, sx, sy):
        self.img = pygame. transform.scale(self.img,(sx,sy))
        self.sx, self.sy = self.img.get_size()
    def show(self):
        screen.blit(self.img,(self.x, self.y))

def crash(a,b):
    if a.x-b.sx <= b.x and b.x <= a.x+a.sx:
        if a.y-b.sy <= b.y and b.y <= a.y+a.sy:
            return True
        else:
            return False
    else:
        return False


ms = obj()
ms.put_img('C:/Users/Dohwan/Desktop/Python/Game/ms.jpg')
ms.change_size(40, 50)
ms.x = 20
ms.y = round(size[1]/2-25)
ms.move = 8

up_go = False
down_go = False
space_go = False

b_list = []
z_list = []
k = 0

GO = 0
kill = 0
loss = 0


#4-0.
SB = 0
while SB == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SB = 1
    screen.fill(color)
    font = pygame.font.Font('C:/Windows/Fonts/ariblk.ttf', 20)
    text_space = font.render('press SPACE key to start the game', True, (255,255,255))
    screen.blit(text_space, (200,180))
    pygame.display.flip()
    
#4. Main event

start_time = datetime.now()
SB = 0
while SB == 0:
    
    #4-1. FPS option
    clock.tick(60)

    #4-2. various input detection
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SB = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                up_go = True
            elif event.key == pygame.K_DOWN:
                down_go = True
            elif event.key == pygame.K_SPACE:
                space_go = True
                k = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up_go = False
            elif event.key == pygame.K_DOWN:
                down_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False
    
    
    #4-3. changes according to input, time
    now_time = datetime.now()
    delta_time = round((now_time - start_time).total_seconds())


    if up_go == True:
        ms.y -= ms.move
        if ms.y <= -10:
            ms.y = -10
    if down_go == True:
        ms.y += ms.move
        if ms.y >= 400-ms.sy:
            ms.y = 400-ms.sy
            
            
    
    if space_go == True and k%18 == 0:
        bl = obj()
        bl.put_img('C:/Users/Dohwan/Desktop/Python/Game/bl.jpg')
        bl.change_size(20,10)
        bl.x = ms.x+ms.sx/2
        bl.y = round(ms.y+ms.sy/2-bl.y/2)
        bl.move = 15
        b_list.append(bl)
    k+=1
    d_list = []
    for i in range(len(b_list)):
        b = b_list[i]
        b.x += b.move
        if b.x >= 800:
            d_list.append(i)
    for d in d_list:
        del b_list[d]
    

    if random.random()> 0.98:
        zb = obj()
        zb.put_img('C:/Users/Dohwan/Desktop/Python/Game/zb.jpg')
        zb.change_size(40,50)
        zb.x = size[0]-zb.sx
        zb.y = random.randrange(0,size[1]-zb.sy-round(ms.sy/2))
        zb.move = 7
        z_list.append(zb)

    d_list = []
    for i in range(len(z_list)):
        z = z_list[i]
        z.x -= z.move
        if z.x <= -zb.sx:
            d_list.append(i)
    for d in d_list:
        del z_list[d]
        loss += 1


    db_list = []
    dz_list = []
    for i in range(len(b_list)):
        for j in range(len(z_list)):
            b = b_list[i]
            z = z_list[j]
            if crash(b,z) == True:
                db_list.append(i)
                dz_list.append(j)
    db_list = list(set(db_list))
    dz_list = list(set(dz_list))

    for db in db_list:
        del b_list[db]
    for dz in dz_list:
        del z_list[dz]
        kill += 1
                
    for i in range(len(z_list)):
        z = z_list[i]
        if crash(z,ms) == True:
            SB = 1
            GO = 1
        

    
    #4-4. Drawing
    screen.fill(color)
    ms.show()
    for b in b_list:
        b.show()
    for z in z_list:
        z.show()


    font = pygame.font.Font('C:/Windows/Fonts/ariblk.ttf', 20)
    text_kill = font.render('killed : {} loss : {}'.format(kill, loss), True, (255,255,0))
    screen.blit(text_kill, (30,5))

    text_time = font.render('time : {}'.format(delta_time), True, (255,255,255))
    screen.blit(text_time, (size[0]-100,5))    
    
    #4-5. Update
    pygame.display.flip()

#5. Game exit

while GO == 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GO = 0
    font = pygame.font.Font('C:/Windows/Fonts/ariblk.ttf', 50)
    text_space = font.render('Game over', True, (255,0,0))
    screen.blit(text_space, (250,180))
    pygame.display.flip()

pygame.quit()
