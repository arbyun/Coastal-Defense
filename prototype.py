import pygame,sys
import math
import numpy as np
import random
from pygame.locals import*

pygame.init()


fpsClock=pygame.time.Clock()
FPS=60
screen=pygame.display.set_mode((1000,380))
p0=(0,380)
p1=(0,300)
p2=(200,380)
p3=(200,300)
x1=1010
x2=1020
x21=1400
x22=1460
x31=1800
x32=1810
x41=2200
x42=2210

v0=0

enemy=True
enemy_2=True
enemy_3=True
enemy_4=True

alive=3

def background():
      
    pygame.draw.polygon(screen,(230,230,230),(p0,p1,p3,p2),0)
    pygame.draw.polygon(screen,(40,40,200),(p2,(1000,380),(1000,340),(200,340)),0)
    pygame.draw.polygon(screen,(40,180,40),((100,300),(150,300),(150,280),(100,280)),0)
    pygame.draw.polygon(screen,(40,180,40),((125,280),(140,280),(140,250),(125,250)),0)


    



    
def boats(x1,x2,x21,x22,x31,x32,x41,x42):
  
    pygame.draw.polygon(screen,(150,40,40),((x1,340),(x2,340),(x2,330),(x1,330)),0)
    
    pygame.draw.polygon(screen,(150,40,40),((x21,340),(x22,340),(x22,330),(x21,330)),0)

    pygame.draw.polygon(screen,(150,40,40),((x31,340),(x32,340),(x32,330),(x31,330)),0)
        
    pygame.draw.polygon(screen,(150,40,40),((x41,340),(x42,340),(x42,330),(x41,330)),0)
    
    



    



def shoot(x1,x2,x21,x22,x31,x32,x41,x42):
    
    FPS2=30
    x0=80
    y0=300
    x3=80
    y3=300
# Clacular o seno e o cosseno
    mouse=pygame.mouse.get_pos()
    hipotenosa=np.sqrt(np.square(mouse[0])+np.square(mouse[1]))
    seno=np.divide(380-mouse[1],hipotenosa)
    cosseno=np.divide(mouse[0],hipotenosa)

    g=int(9.8)
   
    t=1
    
    
    while x3<1000 and y3>0 and x3>0 and y3<800:
        t=t+1
        screen.fill((0,0,0))

        #formula para o movimento 
        x3=x0+v0*cosseno*t
        y3=y0-v0*t*seno+1/2*g*np.square(t)
        
        #bullet
        pygame.draw.circle(screen,(255,255,255),(x3,y3),5,0)
        background()
        
        
        boats(x1,x2,x21,x22,x31,x32,x41,x42)
        

        pygame.display.update()
        fpsClock.tick(FPS2)
    
    
        

def pause_screen():
    pass


mouse=False


while alive>0:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            if pygame.K_ESCAPE:
                pause_screen()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse=True
                
        elif event.type==pygame.MOUSEBUTTONUP:
                mouse=False
                shoot(x1,x2,x21,x22,x31,x32,x41,x42)
                
                
               
        

# aumenta a velocidade ao pressionar o botão do rato
    if mouse==True and v0<90:
        v0=v0+5
        
    elif mouse==True and v0==90:
        pass
    else:
        v0=0

    
  
                    
    background()


#enemy boats
    if x1>200 and  enemy==True:
        x1=x1-1
        x2=x2-1
        
        pygame.draw.polygon(screen,(150,40,40),((x1,340),(x2,340),(x2,330),(x1,330)),0)
    
    elif x1==200 and enemy==True:
        alive=alive-1
        x1=1010
        x2=random.randint(1,5)
        if x2==1:
            x2=1020
        if x2==2:
            x2=1070
        if x2==3:
            x2=1120
        if x2==4:
            x2=1170
        if x2==5:
            x2=1220
    elif enemy==False:
        x1=1010
        x2=1020
        enemy=True



    if x21>200 and  enemy==True:
        x21=x21-1
        x22=x22-1
        
        pygame.draw.polygon(screen,(150,40,40),((x21,340),(x22,340),(x22,330),(x21,330)),0)
    
    elif x21==200 and enemy==True:
        alive=alive-1
        x21=1400
        x22=random.randint(1,5)
        if x22==1:
            x22=1410
        if x22==2:
            x22=1460
        if x22==3:
            x22=1510
        if x22==4:
            x22=1560
        if x22==5:
            x22=1610
    elif enemy_2==False:
        x21=1400
        x22=1460
        enemy_2=True




    if x31>200 and  enemy==True:
        x31=x31-1
        x32=x32-1
        
        pygame.draw.polygon(screen,(150,40,40),((x31,340),(x32,340),(x32,330),(x31,330)),0)
    
    elif x31==200 and enemy==True:
        alive=alive-1
        x31=1800
        x32=random.randint(1,5)
        if x32==1:
            x32=1810
        if x32==2:
            x32=1860
        if x32==3:
            x32=1910
        if x32==4:
            x32=1960
        if x32==5:
            x32=2010
    elif enemy_3==False:
        x31=1800
        x32=1810
        enemy_3=True



    
    if x41>200 and  enemy==True:
        x41=x41-1
        x42=x42-1
        
        pygame.draw.polygon(screen,(150,40,40),((x41,340),(x42,340),(x42,330),(x41,330)),0)
    
    elif x41==200 and enemy==True:
        alive=alive-1
        x41=2200
        x42=random.randint(1,5)
        if x42==1:
            x42=2210
        if x42==2:
            x42=2260
        if x42==3:
            x42=2310
        if x42==4:
            x42=2360
        if x42==5:
            x42=2410
    elif enemy_4==False:
        x41=2200
        x42=2210
        enemy_4=True
    

    pygame.display.update()
    fpsClock.tick(FPS)
   
