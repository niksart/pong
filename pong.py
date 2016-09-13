import pygame, sys, random
from pygame.locals import *
from colorsys import hsv_to_rgb
from menu import *

pygame.init()
FPS = 120
screenwidth,screenheight = 800,600
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screenwidth,screenheight),0,32)
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

# settings of the ball
rb = 7 # radious

d = 12 # di quanti pixel si sposta alla volta

class Ball:
	def __init__(self):
		self.respawn()
	def respawn(self):
		self.x = screenwidth/2
		self.y = screenheight/2
		segno = random.randrange(0,2)
		if	segno == 0:
			self.vx = random.uniform(4.5,6.0)
		else:
			self.vx = random.uniform(4.5,6.0)*-1
		self.vy = random.uniform(-4.0,4.0)
		spawn.play()
	def draw(self):
		pygame.draw.circle(screen, FOREGROUNDCOLOR, (int(self.x),int(self.y)), rb)

def dotted_vertical_line(x):
	for y in range(0,600,20):
		pygame.draw.line(screen, FOREGROUNDCOLOR, (x,y), (x,y+10), 1)

def game():
	ball = Ball()
	isPressingUp1 = False
	isPressingUp2 = False
	isPressingDown1 = False
	isPressingDown2 = False
	y1 = y2 = 300
	x1 = 750
	x2 = 50
	p1 = p2 = 0
	l = 60 # lunghezza del rettangolo
	
	hue = 0.0
	
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
		
	
		# get delta time
		dt = fpsClock.get_time()/20.0
		
		
		# update game state
		if isPressingUp1 and y1 >= l/2:
			y1 -= d*dt
		if isPressingDown1 and y1 <= 600-l/2:
			y1 += d*dt
		if isPressingUp2 and y2 >= l/2:
			y2 -= d*dt
		if isPressingDown2 and y2 <= 600-l/2:
			y2 += d*dt
		
		# rimbalzi
		if ball.y <= 0+rb or ball.y >= 600-rb: # rimbalzo parete
			ball.vy = -ball.vy
			tic.play()
		if ball.x >= 750-rb and y1-l/2-4 <= ball.y <= y1+l/2+4 and ball.vx>0: # rimbalzo a dx
			ball.vx = -abs(ball.vx)
			pong.play()
		if ball.x >= 775: # punto a dx
			p1 += 1
			ball.respawn()
		if ball.x <= 50+rb and y2-l/2-4 <= ball.y <= y2+l/2+4 and ball.vx<0: # rimbalzo a sx
			ball.vx = abs(ball.vx)
			ping.play()
		if ball.x <= 25: # punto a sx
			p2 += 1
			ball.respawn()
		
		# velocita	
		ball.x += ball.vx*dt
		ball.y += ball.vy*dt
		print dt
		# accelerazione
		ball.vx*=1 +0.001*dt
		ball.vy*=1 +0.001*dt
		
		
		# draw
		# hue magic
		hue+=0.0005*dt # hue increment per fps
		if hue>=1: # loop back the hue to 0 if it exceeds the max
			hue -= 1
		hue2 = hue-0.5 # the second hue is the opposite of the first in the color wheel
		if hue2<0:
			hue2+=1
		# convert everything to rgb
		br,bg,bb=tuple(hsv_to_rgb(hue,1,1))
		fr,fg,fb=tuple(hsv_to_rgb(hue2,0.7,1))
		# convert to byte values
		global FOREGROUNDCOLOR, BACKGROUNDCOLOR
		FOREGROUNDCOLOR=(fr*255,fg*255,fb*255)
		#BACKGROUNDCOLOR=(br*255,bg*255,bb*255)
		
		# actual drawing
		screen.fill(BACKGROUNDCOLOR)
		
		# render text
		scorelabel = myfont.render("G1: "+str(p1)+"      G2: "+str(p2), 1, FOREGROUNDCOLOR)
		screen.blit(scorelabel, (340, 50))
		
		# paddles
		pygame.draw.rect(screen, FOREGROUNDCOLOR, (x1,y1-l/2,6,l), 1)
		pygame.draw.rect(screen, FOREGROUNDCOLOR, (x2,y2-l/2,6,l), 1)
		
		# ball
		ball.draw()
		
		# lines
		dotted_vertical_line(400)
		dotted_vertical_line(25)
		dotted_vertical_line(775)
		
		# update the screen and wait for the next frame
		pygame.display.update()
		fpsClock.tick(FPS)
		
	#END WHILE TRUE
	
def main():
	screen = pygame.display.set_mode((800, 600))
	menu = cMenu(50, 50, 20, 5, 'vertical', 100, screen,
				[('Start Game', 1, None),
				('Load Game',  2, None),
				('Options',    3, None),
				('Exit',       4, None)])

	menu.set_center(True, True)
	menu.set_alignment('center', 'center')

	state = 0
	prev_state = 1
   
	rect_list = []

	# Ignore mouse motion (greatly reduces resources when not needed)
	pygame.event.set_blocked(pygame.MOUSEMOTION)

	# The main while loop
	while 1:
		# Check if the state has changed, if it has, then post a user event to
		# the queue to force the menu to be shown at least once
		if prev_state != state:
			pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
			prev_state = state
		# Get the next event
		e = pygame.event.wait()

		# Update the menu, based on which "state" we are in - When using the menu
		# in a more complex program, definitely make the states global variables
		# so that you can refer to them by a name
		if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
			if state == 0:
				rect_list, state = menu.update(e, state)
			elif state == 1:
				game()
				state = 0
			elif state == 2:
				#multiplayer
				state = 0
			elif state == 3:
				#TODO options
				state = 0
			else:
				print 'Exit!'
				pygame.quit()
				sys.exit()

		# Quit if the user presses the exit button
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# Update the screen
		pygame.display.update(rect_list)

main()

