import pygame
import sys
from pygame.locals import *


GRAV = 0.005 #0.005

class Star():
  
   visible = True  
   def __init__(self,pos): 
     self.pos = pos
     
   def draw(self):
     if(self.visible):
       pygame.draw.circle(DISPLAYSURF, BLUE, (int(round(self.pos[0] + shift[0])), int(round(self.pos[1] + shift[1]))), 8, 0)

       
class Platform():
   def __init__(self,anchor,length,width):
     self.anchor = anchor
     self.length = length
     self.width  = width

   def draw(self):
      pygame.draw.rect(DISPLAYSURF, RED, (int(round(self.anchor[0]+shift[0])), int(round(self.anchor[1]+shift[1])), self.length, self.width))

class Sock():
  
  JUMPING_VELOCITY = 1.1 #1.2
  
  starsnumber = 0
  
  def __init__(self,pos,state):
      self.pos = list(pos)
      self.state = state 
      self.vel = 0
   
  def draw(self): 
    pygame.draw.circle(DISPLAYSURF, BLUE, (int(round(self.pos[0] + shift[0])), int(round(self.pos[1] + shift[1]))), 20, 0)
   
  def update(self,dt):
    
    p = self.overboard()
    if p :
      self.pos[1] = min(self.pos[1] - self.vel * dt,p.anchor[1])
    else :
      self.pos[1] = self.pos[1] - self.vel * dt
    
    if not self.onboard():#socke.pos[1] <= 250:
      self.vel = self.vel - GRAV*dt
    elif self.onboard() and self.vel > 0:
      self.vel = self.vel - GRAV*dt
    else:  
      self.vel = 0 
    
    if self.state == 'right' and not self.lefttouch():
      self.pos[0] = self.pos[0] + 0.6
    elif self.state == 'left'and not self.righttouch():
      self.pos[0] = self.pos[0] - 0.6
    
    s = self.startouch()
    if(s):
       if(s.visible):
         self.starsnumber = self.starsnumber + 1
         s.visible = False
      
      
      
  def start_jump(self):
    if(self.onboard()):  
      self.vel = self.JUMPING_VELOCITY
    
  def start_move(self,direction):
    self.state = direction
   
  def stop(self):
    self.state = 'still'

  def onboard(self):  
    for p in world:
      if self.pos[0] >= p.anchor[0] and self.pos[0] <= (p.anchor[0] + p.length):
	if self.pos[1] <= p.anchor[1]+1 and self.pos[1] >= p.anchor[1]-1:
	  return True
     	  
	  
    return False	

  def lefttouch(self):
    for p in world:
      if self.pos[0] <= p.anchor[0]+1 and self.pos[0] >= p.anchor[0]-1:
	if self.pos[1] >= p.anchor[1] and self.pos[1] <= p.anchor[1]+p.width:
	  return True

    return False	

  def righttouch(self):
    for p in world:
      if self.pos[0] <= p.anchor[0]+p.length+1 and self.pos[0] >= p.anchor[0]+p.length-1:
	if self.pos[1] >= p.anchor[1] and self.pos[1] <= p.anchor[1]+p.width:  
	  return True

    return False    
            
      
  def overboard(self):
    for p in world:
      if self.pos[0] >= p.anchor[0] and self.pos[0] <= (p.anchor[0] + p.length):
	return p
    
    return None
    
  def startouch(self):
    for s in stars:
      if abs(self.pos[0] -s.pos[0]) <= 20:
	if abs(self.pos[1]-s.pos[1]) <= 20:  
	  return s

    return None
    
pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE = (  0,   0, 255)
#DISPLAYSURF.fill(WHITE)
#pygame.draw.polygon(DISPLAYSURF, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
p1 = Platform((10,200), 50, 10)
p2 = Platform((90,150), 50, 10)
p3 = Platform((190,100), 50, 10)
p4 = Platform((230,230),50,50)
floor = Platform((-60,250),700,50)
socke = Sock((10,250),'still')
clock = pygame.time.Clock()
s1 = Star((270,70))
s2 = Star((360,240))
stars = [s1,s2]
world = [floor,p1,p2,p3,p4]
shift = list((0,0))

font=pygame.font.Font(None,30)

def texts(score, pos, col):
   scoretext=font.render(str(score), 1,col)
   DISPLAYSURF.blit(scoretext, pos)


spamRect = pygame.Rect(10, 20, 200, 300)
while True: # main game loop
     if socke.pos[1] >= 800:
       DISPLAYSURF.fill(BLACK)
       texts('Game Over',(150,150),WHITE)
       pygame.display.update()
       for event in pygame.event.get():
           if event.type == QUIT:
              pygame.quit()
              sys.exit()
           if event.type == pygame.KEYUP:
	      socke = Sock((10,250),'still')
	      for s in stars:
		s.visible = True
        
     else: 
       clock.tick(600)
       DISPLAYSURF.fill(WHITE)
       texts(socke.starsnumber,(330,5),BLACK)
       texts('Stars:',(270,5),BLACK)
       shift = list((-socke.pos[0]+200,-socke.pos[1]+250))
       for p in world:
         p.draw()
     
       for s in stars:
	 s.draw()
       socke.draw()
       
       for event in pygame.event.get():
           if event.type == QUIT:
              pygame.quit()
              sys.exit()
           elif event.type == pygame.KEYDOWN:
	     if event.key == K_LEFT:
               socke.start_move('left')
             if event.key == K_RIGHT:
               socke.start_move('right')
             if event.key == K_UP:
	        socke.start_jump()
           elif event.type == pygame.KEYUP:
	     if event.key == K_RIGHT or event.key == K_LEFT:
	       socke.stop()
     
     
       dt = clock.get_time()	   
       socke.update(dt)
       pygame.display.update()
     
     