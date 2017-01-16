#-*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
import socket, sys, os, threading, time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
	print "trying to connect to the server..."
	try:
		s.connect(("219.85.162.153", 10000))
		os.system("cls")
		break
	except:
		try:
			s.connect(("25.22.110.80", 10000))
			os.system("cls")
			break
		except:
			try:
				s.connect(socket.gethostbyname(socket.gethostname()), 10000)
				os.system("cls")
				break
			except:
				print "cannot connect to server"
				print "press enter to try again"
				raw_input()
				os.system("cls")

x = {}
y = {}
faces = {}
dx = {}
dy = {}
				
while True:
	id = raw_input("enter your id: ")
	if id[:4] == "stop":
		os.system("cls")
		print "you cannot use this id"
		continue
	elif id[0] == "+":
		os.system("cls")
		print "you cannot use this id"
		continue
	s.send("-"+id)
	login = s.recv(1024)
	if login != "wrong" and login != "already":
		print "Login Success!"
		info = login.split("\n")
		for i in info:
			if i[0] != "-":
				x[i.split(",")[0]] = int(i.split(",")[1])
				dx[i.split(",")[0]] = 0
				y[i.split(",")[0]] = int(i.split(",")[2])
				dy[i.split(",")[0]] = 0
				faces[i.split(",")[0]] = int(i.split(",")[3])
				if i.split(",")[0] == id:
					face = int(i.split(",")[3])
		note = int(info[-1][1:])
		break
	elif login == "wrong":
		os.system("cls")
		print "you cannot use this id"
	elif login == "already":
		os.system("cls")
		print "this id has already logged in"

screen_size = (1280, 720)
title = "online test"
charleft_image = "left.png"
charup_image = "up.png"
charright_image = "right.png"
chardown_image = "down.png"
background_image = "background.png"
snowman_image = "snowman.png"
snowmanS_image = "snowmanS.png"
stop = False
motion = []
newinfo = None

def getinfo():
	global newinfo, face, motion, x, y, dx, dy, note
	lastnote = 0
	dnote = 1
	starttime = 0
	endtime = 0
	delist = []
	while stop == False:
		try:
			starttime = time.clock()
			
			s.send(id + "," + ";".join(motion) + "," + str(face)) #id, motion, face
			motion = []
			newinfo = s.recv(1024).split("\n")
			if note < lastnote:
				dnote = 600 - lastnote + note
			elif note > lastnote:
				dnote = note - lastnote
			online = []
			for i in newinfo:
				if i[0] != "-":
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
		except:
			break

def run(id):
	global info, stop, face, motion, note, x, y, dx, dy
	pygame.init()

	screen = pygame.display.set_mode(screen_size, 0, 32)
	pygame.display.set_caption(title)
	clock = pygame.time.Clock()
	font = pygame.font.Font(pygame.font.get_default_font(), 16)
	background = pygame.image.load(background_image).convert_alpha()
	charset = [pygame.image.load(charleft_image),pygame.image.load(charup_image),pygame.image.load(charright_image),pygame.image.load(chardown_image)]
	snowman = pygame.image.load(snowman_image).convert_alpha()
	snowmanS = pygame.image.load(snowmanS_image).convert_alpha()

	while True:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				s.send("stop,"+id)
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
			text.append(font.render(i, True, (0,0,0)))
			screen.blit(char[-1], (int(x[i])-15,int(y[i])-15))
			screen.blit(text[-1], (int(x[i])-(0.5*text[-1].get_width()),int(y[i])-35))
			x[i] += dx[i]
			y[i] += dy[i]
		screen.blit(snowman, (300,300))
		pygame.display.update()
	
		if newinfo != None:
			note += 1
			if note == 600:
				note = 0

if __name__ == "__main__":
	t = threading.Thread(target=getinfo)
	t.start()
	run(id)