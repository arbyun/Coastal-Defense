import pygame,sys
import math
import numpy as np
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
v0=0


def background():
      
    pygame.draw.polygon(screen,(230,230,230),(p0,p1,p3,p2),0)
    pygame.draw.polygon(screen,(40,40,200),(p2,(1000,380),(1000,340),(200,340)),0)
    pygame.draw.polygon(screen,(40,180,40),((100,300),(150,300),(150,280),(100,280)),0)
    pygame.draw.polygon(screen,(40,180,40),((125,280),(140,280),(140,250),(125,250)),0)

    


def shoot(x1,x2):
    
    FPS2=30
    x0=80
    y0=300
    x3=80
    y3=300

    mouse=pygame.mouse.get_pos()
    hipotenosa=np.sqrt(np.square(mouse[0])+np.square(mouse[1]))
    seno=np.divide(380-mouse[1],hipotenosa)
    cosseno=np.divide(mouse[0],hipotenosa)
    g=int(9.8)
   
    t=1
    
    
    while x3<1000 and y3>0 and x3>0 and y3<800:
        t=t+1
        screen.fill((0,0,0))
        x3=x0+v0*cosseno*t
        y3=y0-v0*t*seno+1/2*g*np.square(t)
        

        pygame.draw.circle(screen,(255,255,255),(x3,y3),10,0)
        background()
        

        pygame.draw.polygon(screen,(150,40,40),((x1,340),(x2,340),(x2,330),(x1,330)),0)

        pygame.display.update()
        fpsClock.tick(FPS2)
    
        

def pause_screen():
    pass


mouse=False


while True:
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
                shoot(x1,x2)
  


    if mouse==True and v0<90:
        v0=v0+5
        
    elif mouse==True and v0==90:
        pass
    else:
        v0=0

    
  
                    
    background()
    x1=x1-1
    x2=x2-1

    pygame.draw.polygon(screen,(150,40,40),((x1,340),(x2,340),(x2,330),(x1,330)),0)
    

    pygame.display.update()
    fpsClock.tick(FPS)
   
