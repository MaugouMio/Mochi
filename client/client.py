#-*- coding: UTF-8 -*-
import pygame_sdl2
import pygame
from pygame.locals import *
import socket, sys, threading, time

x = {}
y = {}
faces = {}
team = {}
dx = {}
dy = {}
score = {}
id = ""
face = 3

screen_size = (1280, 720)
title = "Mochi"
charleft_image = "image/left.png"
charleftP_image = "image/left_pink.png"
charup_image = "image/up.png"
charupP_image = "image/up_pink.png"
charright_image = "image/right.png"
charrightP_image = "image/right_pink.png"
chardown_image = "image/down.png"
chardownP_image = "image/down_pink.png"
background_image = "image/background.png"
ball_image = "image/ball.png"
logbackground_image = "image/logbackground.png"
gray_image = "image/gray.png"
score1_image = "image/scoring1.png"
score2_image = "image/scoring2.png"
score3_image = "image/scoring3.png"
score4_image = "image/scoring4.png"
score5_image = "image/scoring5.png"
score6_image = "image/scoring6.png"
score7_image = "image/scoring7.png"
score8_image = "image/scoring8.png"
stop = False
motion = []
note = 0
dnote = 1
newinfo = ""
delist = []
newlist = []

def getinfo():
	global newinfo, face, motion, x, y, dx, dy, note, dnote, pingms, delist, newlist, stop, scoring, pointW, pointP, serverscoring, scorex, scorey, scoreplayer, score, serverending, ending, wintext, wintextS
	lastnote = 0
	starttime = 0
	endtime = 0
	online = []
	while stop == False:
		try:
			starttime = time.clock()
			
			s.send(id + "," + ";".join(motion) + "," + str(face)) #id, motion, face
			motion = []
			newinfo = s.recv(1024).split("\n")
			if note < lastnote:
				dnote += 600 - lastnote + note
			elif note > lastnote:
				dnote += note - lastnote
			online = []
			for i in newinfo:
				if i[0] != "-":
					if i.split(",")[0] not in x:
						dx[i.split(",")[0]] = 0
						y[i.split(",")[0]] = int(i.split(",")[2])
						dy[i.split(",")[0]] = 0
						faces[i.split(",")[0]] = int(i.split(",")[3])
						team[i.split(",")[0]] = int(i.split(",")[4])
						score[i.split(",")[0]] = i.split(",")[5]
						online.append(i.split(",")[0])
						newlist.append(i.split(",")[0]+";"+i.split(",")[1])
					else:
						dx[i.split(",")[0]] = (int(i.split(",")[1]) - x[i.split(",")[0]]) / dnote
						dy[i.split(",")[0]] = (int(i.split(",")[2]) - y[i.split(",")[0]]) / dnote
						if dnote > 180:
							x[i.split(",")[0]] = int(i.split(",")[1])
							y[i.split(",")[0]] = int(i.split(",")[2])
						faces[i.split(",")[0]] = int(i.split(",")[3])
						score[i.split(",")[0]] = i.split(",")[5]
						online.append(i.split(",")[0])
				else:
					pointW = int(i.split("-")[2])
					pointP = int(i.split("-")[3])
					if i.split("-")[1] != "0" and serverscoring == False:
						scoring = 1
						scoreplayer = SPfont.render(i.split("-")[4].decode("big5")+" SCORED", True, (255,255,255))
						serverscoring = True
						scorex = int(x[" "])
						if scorex > 640:
							scorex = 1235
						else:
							scorex = 45
						scorey = int(y[" "])
					elif i.split("-")[1] == "0" and serverscoring == True:
						serverscoring = False
					elif int(i.split("-")[1]) > 180 and serverending == False:
						ending = 1
						serverending = True
						if pointW > pointP:
							wintext = "White Mochi Win!"
							wintextS = SPfont.render("White Mochi Win!", True, (0,0,0))
						else:
							wintext = "Pink Mochi Win!"
							wintextS = SPfont.render("Pink Mochi Win!", True, (220,72,89))
					elif i.split("-")[1] == "0" and serverending == True:
						serverending = False
			for i in x:
				if i not in online:
					delist.append(i)
			
			lastnote = note
			
			endtime = time.clock()
			if endtime-starttime <= 0.016:
				time.sleep(0.0166-endtime+starttime)
			pingms = str(int(1000*(endtime-starttime)))
			if endtime-starttime >= 1:
				pingms = "999"
		except:
			stop = True

pygame_sdl2.init()

screen = pygame_sdl2.display.set_mode(screen_size, 0, 32)
pygame_sdl2.display.set_caption(title)
clock = pygame_sdl2.time.Clock()
sysfont = pygame_sdl2.font.Font("data/msjh.ttc", 32)
typefont = pygame_sdl2.font.Font("data/msjh.ttc", 45)
logbackground = pygame_sdl2.image.load(logbackground_image).convert()
gray = pygame_sdl2.image.load(gray_image).convert_alpha()
icon = pygame_sdl2.image.load(chardown_image).convert_alpha()
pygame_sdl2.display.set_icon(icon)

pressenter = False

while True:
	if pygame_sdl2.event.peek(pygame_sdl2.QUIT):
		sys.exit()
	screen.blit(logbackground, (0,0))
	systext = sysfont.render("正在連線至伺服器".decode("UTF-8"), True, (100,100,100))
	screen.blit(systext, ((1280-systext.get_width())/2,300))
	pygame_sdl2.display.update()
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	try:
		s.connect(("219.85.162.153", 10000))
		break
	except:
		if pygame_sdl2.event.peek(pygame_sdl2.QUIT):
			sys.exit()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(2)
		try:
			s.connect(("25.22.110.80", 10000))
			break
		except:
			if pygame_sdl2.event.peek(pygame_sdl2.QUIT):
				sys.exit()
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(2)
			try:
				s.connect(("25.23.166.209", 10000))
				break
			except:
				if pygame_sdl2.event.peek(pygame_sdl2.QUIT):
					sys.exit()
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(2)
				try:
					s.connect((socket.gethostbyname(socket.gethostname()), 10000))
					break
				except:
					if pygame_sdl2.event.peek(pygame_sdl2.QUIT):
						sys.exit()
					pygame_sdl2.event.clear()
					systext = sysfont.render("無法連線至伺服器，請按enter再次嘗試".decode("UTF-8"), True, (100,100,100))
					while not pressenter:
						clock.tick(60)
						for event in pygame_sdl2.event.get():
							if event.type == pygame_sdl2.QUIT:
								sys.exit()
							elif event.type == pygame_sdl2.KEYDOWN and (event.key == K_RETURN or event.key == 1073741912):
								pressenter = True
						screen.blit(logbackground, (0,0))
						screen.blit(systext, ((1280-systext.get_width())/2,300))
						pygame_sdl2.display.update()
					pressenter = False

systext = sysfont.render("請輸入你的暱稱".decode("UTF-8"), True, (100,100,100))
inputtext = ""
edittext = ""
typemark = " "
markright = " "
editing = False
scoring = 0
ending = 0
scorex = 0
scorey = 0
scoreplayer = ""
wintext = ""
serverscoring = False
serverending = False
pygame_sdl2.key.start_text_input()
pygame_sdl2.time.set_timer(USEREVENT, 500)

while not pressenter:
	clock.tick(60)

	for event in pygame_sdl2.event.get():
		if event.type == pygame_sdl2.QUIT:
			s.send(";")
			sys.exit()
		elif event.type == pygame_sdl2.TEXTINPUT:
			if event.text != " " and event.text != "-" and event.text != "+" and event.text != ";":
				inputtext = inputtext + event.text
				while len(inputtext.encode("big5")) > 13:
					inputtext = inputtext[:-1]
		elif event.type == pygame_sdl2.TEXTEDITING:
			edittext = event.text
			if event.start == 0:
				editing = False
			else:
				editing = True
		elif event.type == pygame_sdl2.KEYDOWN and event.key == K_BACKSPACE and editing == False:
			inputtext = inputtext[:-1]
		elif event.type == pygame_sdl2.KEYDOWN and event.key == K_LEFT and editing == False and len(inputtext) >= 1:
			markright = inputtext[-1] + markright
			inputtext = inputtext[:-1]
		elif event.type == pygame_sdl2.KEYDOWN and event.key == K_RIGHT and editing == False and len(markright) >= 2:
			inputtext = inputtext + markright[0]
			markright = markright[1:]
		elif event.type == pygame_sdl2.KEYDOWN and event.key == K_DELETE and editing == False and len(markright) >= 2:
			markright = markright[1:]
		elif event.type == pygame_sdl2.KEYDOWN and (event.key == K_RETURN or event.key == 1073741912) and editing == False and inputtext == "":
			systext = sysfont.render("暱稱不能為空白".decode("UTF-8"), True, (100,100,100))
		elif event.type == pygame_sdl2.KEYDOWN and (event.key == K_RETURN or event.key == 1073741912) and editing == False and inputtext != "":
			id = inputtext.encode("big5")
			screen.blit(gray, (0,0))
			pygame_sdl2.display.update()

			s.send("-"+id)
			login = s.recv(1024)
			if login != "already":
				info = login.split("\n")
				for i in info:
					if i[0] != "-":
						x[i.split(",")[0]] = int(i.split(",")[1])
						dx[i.split(",")[0]] = 0
						y[i.split(",")[0]] = int(i.split(",")[2])
						dy[i.split(",")[0]] = 0
						faces[i.split(",")[0]] = int(i.split(",")[3])
						team[i.split(",")[0]] = int(i.split(",")[4])
						score[i.split(",")[0]] = i.split(",")[5]
						if i.split(",")[0] == id:
							face = int(i.split(",")[3])
					else:
						pointW = int(i.split("-")[2])
						pointP = int(i.split("-")[3])
						if i.split("-")[1] != "0" and serverscoring == False:
							scoring = 1
							serverscoring = True
							scorex = int(x[" "])
							scorey = int(y[" "])
							scoreplayer = i.split("-")[4].decode("big5")+" SCORED"
						elif int(i.split("-")[1]) > 180 and serverending == False:
							ending = 1
							serverending = True
							if pointW > pointP:
								wintext = "White Mochi Win!"
							else:
								wintext = "Pink Mochi Win!"
				if pygame_sdl2.event.peek(pygame_sdl2.QUIT):
					s.send(";")
					sys.exit()
				pygame_sdl2.event.clear()
				pygame_sdl2.key.stop_text_input()
				pygame_sdl2.time.set_timer(USEREVENT, 0)
				pygame_sdl2.display.pygame_sdl2.display.get_window().destroy()
				pressenter = True

				pingms = "-"
				t = threading.Thread(target=getinfo)
				t.start()
			elif login == "already":
				systext = sysfont.render("該暱稱已經有人使用囉".decode("UTF-8"), True, (100,100,100))
				if pygame_sdl2.event.peek(pygame_sdl2.QUIT):
					s.send(";")
					sys.exit()
				pygame_sdl2.event.clear()
		elif event.type == 24:
			if typemark == "|":
				typemark = " "
			else:
				typemark = "|"

	if not pressenter:
		screen.blit(logbackground, (0,0))
		screen.blit(systext, ((1280-systext.get_width())/2,300))
		pygame_sdl2.draw.rect(screen, (150,150,150), [482,337,320,50], 2)
		writing = typefont.render(inputtext+edittext+" ", True, (150,150,150))
		mark = typefont.render(typemark, True, (150,150,150))
		Mright = typefont.render(markright, True, (150,150,150))
		screen.blit(writing, (489,340))
		screen.blit(mark, (477+writing.get_width(),336))
		screen.blit(Mright, (480+writing.get_width(),340))
		pygame_sdl2.display.update()

pygame.init()
screen = pygame.display.set_mode(screen_size, 0, 32)
pygame.display.set_caption(title)
clock = pygame.time.Clock()
background = pygame.image.load(background_image).convert()
ball = pygame.image.load(ball_image).convert_alpha()
gray = pygame.image.load(gray_image).convert_alpha()
gray = pygame.transform.scale(gray, (1280,160))
font = pygame.font.Font("data/msjh.ttc", 18)
scorefont = pygame.font.Font("data/msjh.ttc", 180)
scorefont.set_bold(True)
scorefont.set_italic(True)
SPfont = pygame.font.Font("data/msjh.ttc", 90)
scoreplayer = SPfont.render(scoreplayer, True, (255,255,255))
if wintext == "White Mochi Win!":
	wintextS = SPfont.render("White Mochi Win!", True, (0,0,0))
elif wintext == "Pink Mochi Win!":
	wintextS = SPfont.render("Pink Mochi Win!", True, (220,72,89))
else:
	wintextS = ""
charset = [[pygame.image.load(charleft_image).convert_alpha(),pygame.image.load(charup_image).convert_alpha(),pygame.image.load(charright_image).convert_alpha(),pygame.image.load(chardown_image).convert_alpha()],[pygame.image.load(charleftP_image).convert_alpha(),pygame.image.load(charupP_image).convert_alpha(),pygame.image.load(charrightP_image).convert_alpha(),pygame.image.load(chardownP_image).convert_alpha()]]
scoreanime = [pygame.image.load(score1_image).convert_alpha(),pygame.image.load(score2_image).convert_alpha(),pygame.image.load(score3_image).convert_alpha(),pygame.image.load(score4_image).convert_alpha(),pygame.image.load(score5_image).convert_alpha(),pygame.image.load(score6_image).convert_alpha(),pygame.image.load(score7_image).convert_alpha(),pygame.image.load(score8_image).convert_alpha()]
pygame.display.set_icon(charset[0][3])

while stop == False:
	clock.tick(60)
	fps = font.render("fps: "+str(int(clock.get_fps())), True, (100,100,100))
	ping = font.render("ping: "+str(pingms), True, (100,100,100))
	pointWS = scorefont.render(str(pointW), True, (200,200,200))
	pointPS = scorefont.render(str(pointP), True, (230,200,210))

	for event in pygame.event.get():
		if event.type == QUIT:
			s.send("+"+id)
			sys.exit()
			stop = True
		if event.type == KEYDOWN:
			if event.key == K_LEFT:
				face = 0
			elif event.key == K_UP:
				face = 1
			elif event.key == K_RIGHT:
				face = 2
			elif event.key == K_DOWN:
				face = 3

	tempmotion = 55
	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[K_LEFT] == True:
		tempmotion -= 10
	if keys_pressed[K_RIGHT] == True:
		tempmotion += 10
	if keys_pressed[K_UP] == True:
		tempmotion -= 1
	if keys_pressed[K_DOWN] == True:
		tempmotion += 1
	if tempmotion != 55:
		motion.append(str(tempmotion))

	screen.blit(background, (0,0))
	screen.blit(pointWS, ((640-pointWS.get_width())/2,240))
	screen.blit(pointPS, (640+(640-pointWS.get_width())/2,240))

	char = []
	text = []
	for i in x:
		if i != " ":
			char.append(charset[team[i]][faces[i]].convert_alpha())
			screen.blit(char[-1], (int(x[i])-15,int(y[i])-15))
			text.append(font.render(i.decode("big5")+"-"+score[i], True, (0,0,0)))
			screen.blit(text[-1], (int(x[i])-(0.5*text[-1].get_width()),int(y[i])-35))
		elif i == " " and serverscoring == False:
			screen.blit(ball, (int(x[i])-45,int(y[i])-45))
		x[i] += dx[i]
		y[i] += dy[i]
	for i in newlist:
		x[i.split(";")[0]] = int(i.split(";")[1])
	newlist = []
	for i in delist:
		del x[i]
		del dx[i]
		del y[i]
		del dy[i]
		del faces[i]
		del team[i]
		del score[i]
	delist = []
	if dnote > 1:
		dnote -= 1
	if scoring >= 1 and scoring < 7:
		screen.blit(scoreanime[0], (scorex-45,scorey-45))
		screen.blit(gray, (0,280))
		screen.blit(scoreplayer, (scoring*(1280-scoreplayer.get_width())/24,300))
	elif scoring >= 7 and scoring < 13:
		screen.blit(scoreanime[1], (scorex-45,scorey-45))
		screen.blit(gray, (0,280))
		screen.blit(scoreplayer, (scoring*(1280-scoreplayer.get_width())/24,300))
	elif scoring >= 13 and scoring < 19:
		screen.blit(scoreanime[2], (scorex-45,scorey-45))
	elif scoring >= 19 and scoring < 97:
		screen.blit(scoreanime[3], (scorex-45,scorey-45))
	elif scoring >= 97 and scoring < 103:
		screen.blit(scoreanime[4], (scorex-45,scorey-45))
	elif scoring >= 103 and scoring < 109:
		screen.blit(scoreanime[5], (scorex-60,scorey-60))
	elif scoring >= 109 and scoring < 115:
		screen.blit(scoreanime[6], (scorex-75,scorey-75))
	elif scoring >= 115 and scoring < 121:
		screen.blit(scoreanime[7], (scorex-90,scorey-90))
	if scoring >= 13 and scoring < 97:
		screen.blit(gray, (0,280))
		screen.blit(scoreplayer, ((1280-scoreplayer.get_width())/2,300))
	screen.blit(fps, (1200,10))
	screen.blit(ping, (1200,30))
	if ending >= 1 and ending < 13:
		if wintext == "White Mochi Win!":
			screen.fill((255,255,255), [0,0,1280,60*ending])
		else:
			screen.fill((245,199,206), [0,0,1280,60*ending])
		screen.blit(wintextS, ((1280-wintextS.get_width())/2,60*ending-420))
	elif ending >= 13 and ending < 229:
		if wintext == "White Mochi Win!":
			screen.fill((255,255,255))
		else:
			screen.fill((245,199,206))
		screen.blit(wintextS, ((1280-wintextS.get_width())/2,300))
	elif ending >= 229:
		if wintext == "White Mochi Win!":
			screen.fill((255,255,255), [0,0,1280,60*(240-ending)])
		else:
			screen.fill((245,199,206), [0,0,1280,60*(240-ending)])
		screen.blit(wintextS, ((1280-wintextS.get_width())/2,60*(240-ending)-420))
	pygame.display.update([0,0,1280,720])
	
	if scoring >= 1:
		scoring += 1
		if scoring == 121:
			scoring = 0
	if ending >= 1:
		ending += 1
		if ending == 241:
			ending = 0

	note += 1
	if note == 600:
		note = 0