import pygame, sys, random
from pygame.locals import *
from colorsys import hsv_to_rgb

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600),0,32)
tic = pygame.mixer.Sound("sound/tic.ogg")
ping = pygame.mixer.Sound("sound/ping.ogg")
pong = pygame.mixer.Sound("sound/pong.ogg")
spawn = pygame.mixer.Sound("sound/respawn.ogg")

pygame.mixer.music.load("sound/music.ogg")
pygame.mixer.music.play(-1,0)
myfont = pygame.font.SysFont("monospace bold", 25)
pygame.display.set_caption("PONG!")

FOREGROUNDCOLOR=(255,255,255)
BACKGROUNDCOLOR=(0,0,0)

y1 = y2 = 300
x1 = 750
x2 = 50
p1 = p2 = 0
l = 60 # lunghezza del rettangolo

# settings of the ball
xb = 400
yb = 300
vx = 5.0
vy = 6.0
rb = 7 # radious

hue = 0.0

d = 12 # di quanti pixel si sposta alla volta

isPressingUp1 = False
isPressingUp2 = False
isPressingDown1 = False
isPressingDown2 = False

def respawn():
	global xb,yb,vx,vy
	xb = 400
	yb = 300
	segno = random.randrange(0,2)
	if	segno == 0:
		vx = random.uniform(4.5,6.0)
	else:
		vx = random.uniform(4.5,6.0)*-1
	vy = random.uniform(-4.0,4.0)
	spawn.play()

def dotted_vertical_line(x):
	for y in range(0,600,20):
		pygame.draw.line(screen, FOREGROUNDCOLOR, (x,y), (x,y+10), 1)

while True:
	# handle events
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == 273: #freccetta su
				isPressingUp1 = True
			elif  event.key == 274:
				isPressingDown1 = True
			elif  event.key == 119:
				isPressingUp2 = True
			elif  event.key == 115:
				isPressingDown2 = True
		elif event.type == KEYUP:
			if event.key == 273: #freccetta su
				isPressingUp1 = False
			elif  event.key == 274:#freccia giu
				isPressingDown1 = False
			elif  event.key == 119:#w
				isPressingUp2 = False
			elif  event.key == 115:#s
				isPressingDown2 = False
		elif event.type == QUIT:
			pygame.quit()
			sys.exit()
	
	# update game state
	if isPressingUp1 and y1 >= l/2:
		y1 -= d
	if isPressingDown1 and y1 <= 600-l/2:
		y1 += d
	if isPressingUp2 and y2 >= l/2:
		y2 -= d
	if isPressingDown2 and y2 <= 600-l/2:
		y2 += d
	if yb <= 0 or yb >= 600: # rimbalzo parete
		vy = -vy
		tic.play()
		
	if xb >= 750-rb and y1-l/2-4 <= yb <= y1+l/2+4 and vx>0: # rimbalzo a dx
		vx = -abs(vx)
		pong.play()
	if xb >= 775: # punto a dx
		p1 += 1
		respawn()
	if xb <= 50+rb and y2-l/2-4 <= yb <= y2+l/2+4 and vx<0: # rimbalzo a sx
		vx = abs(vx)
		ping.play()
	if xb <= 25: # punto a sx
		p2 += 1
		respawn()
			
	xb += vx
	yb += vy
	
	vx*=1.001
	vy*=1.001
	
	# draw
	hue+=0.0005
	if hue>=1:
		hue = 0
	hue2 = hue-0.5
	if hue2<0:
		hue2+=1
	r,g,b=tuple(hsv_to_rgb(hue,1,1))
	wr,wg,wb=tuple(hsv_to_rgb(hue2,0.7,1))
	FOREGROUNDCOLOR=(wr*255,wg*255,wb*255)
	#BACKGROUNDCOLOR=(r*255,g*255,b*255)
	screen.fill(BACKGROUNDCOLOR)
	# render text
	scorelabel = myfont.render("G1: "+str(p1)+"      G2: "+str(p2), 1, FOREGROUNDCOLOR)
	screen.blit(scorelabel, (340, 50))
	pygame.draw.rect(screen, FOREGROUNDCOLOR, (x1,y1-l/2,6,l), 1)
	pygame.draw.rect(screen, FOREGROUNDCOLOR, (x2,y2-l/2,6,l), 1)
	pygame.draw.circle(screen, FOREGROUNDCOLOR, (int(xb),int(yb)), rb)
	dotted_vertical_line(400)
	dotted_vertical_line(25)
	dotted_vertical_line(775)
	
	pygame.display.update()
	fpsClock.tick(FPS)
