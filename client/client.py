#-*- coding: UTF-8 -*-
import pygame_sdl2
import pygame
from pygame.locals import *
import socket, sys, threading, time

x = {}
y = {}
faces = {}
dx = {}
dy = {}
id = ""
face = 3

screen_size = (1280, 720)
title = "Mochi"
charleft_image = "image/left.png"
charup_image = "image/up.png"
charright_image = "image/right.png"
chardown_image = "image/down.png"
background_image = "image/background.png"
logbackground_image = "image/logbackground.png"
gray_image = "image/gray.png"
snowman_image = "image/snowman.png"
snowmanS_image = "image/snowmanS.png"
stop = False
motion = []
note = 0
dnote = 1
newinfo = ""

def getinfo():
	global newinfo, face, motion, x, y, dx, dy, note, dnote, pingms
	lastnote = 0
	starttime = 0
	endtime = 0
	delist = []
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
				if i.split(",")[0] not in x:
					x[i.split(",")[0]] = int(i.split(",")[1])
					dx[i.split(",")[0]] = 0
					y[i.split(",")[0]] = int(i.split(",")[2])
					dy[i.split(",")[0]] = 0
					faces[i.split(",")[0]] = int(i.split(",")[3])
					online.append(i.split(",")[0])
				else:
					dx[i.split(",")[0]] = (int(i.split(",")[1]) - x[i.split(",")[0]]) / dnote
					dy[i.split(",")[0]] = (int(i.split(",")[2]) - y[i.split(",")[0]]) / dnote
					if dnote > 180:
						x[i.split(",")[0]] = int(i.split(",")[1])
						y[i.split(",")[0]] = int(i.split(",")[2])
					faces[i.split(",")[0]] = int(i.split(",")[3])
					online.append(i.split(",")[0])
			for i in x:
				if i not in online:
					delist.append(i)
			for i in delist:
				del x[i]
				del dx[i]
				del y[i]
				del dy[i]
				del faces[i]
			delist = []
			
			lastnote = note
			
			endtime = time.clock()
			if endtime-starttime <= 0.016:
				time.sleep(0.0166-endtime+starttime)
			pingms = str(int(1000*(endtime-starttime)))
			if endtime-starttime >= 1:
				pingms = "999"
		except:
			break

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
					x[i.split(",")[0]] = int(i.split(",")[1])
					dx[i.split(",")[0]] = 0
					y[i.split(",")[0]] = int(i.split(",")[2])
					dy[i.split(",")[0]] = 0
					faces[i.split(",")[0]] = int(i.split(",")[3])
					if i.split(",")[0] == id:
						face = int(i.split(",")[3])
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
font = pygame.font.Font("data/msjh.ttc", 18)
charset = [pygame.image.load(charleft_image).convert_alpha(),pygame.image.load(charup_image).convert_alpha(),pygame.image.load(charright_image).convert_alpha(),pygame.image.load(chardown_image).convert_alpha()]
pygame.display.set_icon(charset[3])
snowman = pygame.image.load(snowman_image).convert_alpha()
snowmanS = pygame.image.load(snowmanS_image).convert_alpha()

while True:
	clock.tick(60)
	fps = font.render("fps: "+str(int(clock.get_fps())), True, (100,100,100))
	ping = font.render("ping: "+str(pingms), True, (100,100,100))

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

	char = []
	text = []
	screen.blit(snowmanS, (300,300))
	for i in x:
		char.append(charset[faces[i]].convert_alpha())
		text.append(font.render(i.decode("big5"), True, (0,0,0)))
		screen.blit(char[-1], (int(x[i])-15,int(y[i])-15))
		screen.blit(text[-1], (int(x[i])-(0.5*text[-1].get_width()),int(y[i])-35))
		x[i] += dx[i]
		y[i] += dy[i]
	if dnote > 1:
		dnote -= 1
	screen.blit(snowman, (300,300))
	screen.blit(fps, (1200,10))
	screen.blit(ping, (1200,30))
	pygame.display.update()

	note += 1
	if note == 600:
		note = 0
