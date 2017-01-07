#-*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
import socket, sys, os, threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
	try:
		s.connect(("219.85.162.153", 10000))
		break
	except:
		try:
			s.connect(("25.22.110.80", 10000))
			break
		except:
			try:
				s.connect(socket.gethostbyname(socket.gethostname()), 10000)
				break
			except:
				print "cannot connect to server"
				print "press enter to try again"
				raw_input()

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
		info = [login]
		face = int(info[0].split(",")[3])
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
note = 0

def getinfo():
	global info, face, motion
	while stop == False:
		try:
			s.send(id + "," + ";".join(motion) + "," + str(face)) #id, motion, face
			motion = []
			info = s.recv(1024).split("\n")
		except:
			break

def run(id):
	global info, stop, face, motion, note
	pygame.init()

	screen = pygame.display.set_mode(screen_size, 0, 32)
	pygame.display.set_caption(title)
	clock = pygame.time.Clock()
	font = pygame.font.Font(pygame.font.get_default_font(), 16)
	background = pygame.image.load(background_image).convert_alpha()
	charset = [pygame.image.load(charleft_image),pygame.image.load(charup_image),pygame.image.load(charright_image),pygame.image.load(chardown_image)]
	snowman = pygame.image.load(snowman_image).convert_alpha()
	snowmanS = pygame.image.load(snowmanS_image).convert_alpha()
	notes = {}

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
		motion.append(str(tempmotion))

		screen.blit(background, (0,0))
		char = []
		text = []
		screen.blit(snowmanS, (300,300))
		for i in info:
			if i[0] != "-":
				char.append(charset[int(i.split(",")[3])].convert_alpha())
				text.append(font.render(i.split(",")[0], True, (0,0,0)))
				screen.blit(char[-1], (int(float(i.split(",")[1]))-15,int(float(i.split(",")[2]))-15))
				screen.blit(text[-1], (int(float(i.split(",")[1]))-(0.5*text[-1].get_width()),int(float(i.split(",")[2]))-35))
		screen.blit(snowman, (300,300))
		pygame.display.update()

if __name__ == "__main__":
	t = threading.Thread(target=getinfo)
	t.start()
	run(id)