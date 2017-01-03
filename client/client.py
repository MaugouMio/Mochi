#-*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
import socket, sys, os, threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
	try:
		s.connect(("10.122.168.178", 10000)) #219.85.162.153
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
		info = login.split("\n")
		for i in info:
			if i.split(",")[0] == id:
				x = int(i.split(",")[1])
				y = int(i.split(",")[2])
				face = int(i.split(",")[3])
				break
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
vx = [0,0,0,0,0]
vy = [0,0,0,0,0]
note = 0

def getinfo():
	global info, x, y, face, vx, vy
	while stop == False:
		if len(vy) == 5 and len(vx) == 5:
			try:
				s.send(id+","+str(x)+","+str(y)+","+str(face)+","+str(vx[0])+";"+str(vx[1])+";"+str(vx[2])+";"+str(vx[3])+";"+str(vx[4])+","+str(vy[0])+";"+str(vy[1])+";"+str(vy[2])+";"+str(vx[3])+";"+str(vx[4])+","+str(note)) #id, x, y, face, vx, vy, note
				info = s.recv(1024).split("\n")
			except:
				break

def run(id):
	global info, x, y, stop, face, vx, vy, note
	pygame.init()

	screen = pygame.display.set_mode(screen_size, 0, 32)
	pygame.display.set_caption(title)
	clock = pygame.time.Clock()
	font = pygame.font.Font(pygame.font.get_default_font(), 16)
	background = pygame.image.load(background_image).convert_alpha()
	charset = [pygame.image.load(charleft_image),pygame.image.load(charup_image),pygame.image.load(charright_image),pygame.image.load(chardown_image)]
	snowman = pygame.image.load(snowman_image).convert_alpha()
	snowmanS = pygame.image.load(snowmanS_image).convert_alpha()
	collision = {}
	notes = {}
	reading = {}

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

		if x+int(vx[0])+int(vx[1])+int(vx[2])+int(vx[3])+int(vx[4]) > 1280:
			vx[4] = 0
		elif x+int(vx[0])+int(vx[1])+int(vx[2])+int(vx[3])+int(vx[4]) < 0:
			vx[4] = 0
		if y+int(vy[0])+int(vy[1])+int(vy[2])+int(vy[3])+int(vy[4]) > 720:
			vy[4] = 0
		elif y+int(vy[0])+int(vy[1])+int(vy[2])+int(vy[3])+int(vy[4]) < 0:
			vy[4] = 0
		
		keys_pressed = pygame.key.get_pressed()
		if len(vx) == 5:
			if keys_pressed[K_LEFT] == True and vx[4] >= -7.7:
				vx.append(vx[4]-0.3)
				if vx[4] >= 5:
					vx[5] += 0.2
				elif vx[4] >= 2:
					vx[5] += 0.1
			if keys_pressed[K_RIGHT] == True and vx[4] <= 7.7:
				vx.append(vx[4]+0.3)
				if vx[4] <= -5:
					vx[5] -= 0.2
				elif vx[4] <= -2:
					vx[5] -= 0.1
		if len(vy) == 5:
			if keys_pressed[K_UP] == True and vy[4] >= -7.7:
				vy.append(vy[4]-0.3)
				if vy[4] >= 5:
					vy[5] += 0.2
				elif vy[4] >= 2:
					vy[5] += 0.1
			if keys_pressed[K_DOWN] == True and vy[4] <= 7.7:
				vy.append(vy[4]+0.3)
				if vy[4] <= -5:
					vy[5] -= 0.2
				elif vy[4] <= -2:
					vy[5] -= 0.1
		if len(vx) < 6:
			vx.append(vx[4])
		if len(vy) < 6:
			vy.append(vy[4])

		x += int(vx[0])
		if x > 1280:
			x = 1280
		elif x < 0:
			x = 0
		del vx[0]
		y += int(vy[0])
		if y > 720:
			y = 720
		elif y < 0:
			y = 0
		del vy[0]

		if vx[4] > 0:
			if vx[4] > 4:
				vx[4] -= 0.05
			vx[4] -= 0.05
		elif vx[4] < 0:
			if vx[4] < -4:
				vx[4] += 0.05
			vx[4] += 0.05
		if vy[4] > 0:
			if vy[4] > 4:
				vy[4] -= 0.05
			vy[4] -= 0.05
		elif vy[4] < 0:
			if vy[4] < -4:
				vy[4] += 0.05
			vy[4] += 0.05

		screen.blit(background, (0,0))
		char = [charset[face].convert_alpha()]
		text = [font.render(id, True, (0,0,0))]
		screen.blit(snowmanS, (300,300))
		screen.blit(char[-1], (x-15,y-15))
		screen.blit(text[-1], (x-(0.5*text[-1].get_width()),y-35))
		for i in info:
			if i.split(",")[0] != id:
				if i.split(",")[0] not in collision:
					collision[i.split(",")[0]] = False
				if float(i.split(",")[1])+float(i.split(",")[4].split(";")[0])+float(i.split(",")[4].split(";")[1])+float(i.split(",")[4].split(";")[2]) <= x+30+vx[0]+vx[1]+vx[2] and float(i.split(",")[2])+float(i.split(",")[5].split(";")[0])+float(i.split(",")[5].split(";")[1])+float(i.split(",")[5].split(";")[2]) <= y+30+vy[0]+vy[1]+vy[2] and float(i.split(",")[1])+float(i.split(",")[4].split(";")[0])+float(i.split(",")[4].split(";")[1])+float(i.split(",")[4].split(";")[2]) >= x-30+vx[0]+vx[1]+vx[2] and float(i.split(",")[2])+float(i.split(",")[5].split(";")[0])+float(i.split(",")[5].split(";")[1])+float(i.split(",")[5].split(";")[2]) >= y-30+vy[0]+vy[1]+vy[2]:
					if collision[i.split(",")[0]] == False:
						vx.append(float(i.split(",")[4].split(";")[2]))
						vy.append(float(i.split(",")[5].split(";")[2]))
						collision[i.split(",")[0]] = True
				else:
					if collision[i.split(",")[0]] == True:
						collision[i.split(",")[0]] = False
				char.append(charset[int(i.split(",")[3])].convert_alpha())
				text.append(font.render(i.split(",")[0], True, (0,0,0)))
				if i.split(",")[0] not in notes:
					notes[i.split(",")[0]] = i.split(",")[6]
					reading[i.split(",")[0]] = -1
					screen.blit(char[-1], (int(float(i.split(",")[1]))-15,int(float(i.split(",")[2]))-15))
					screen.blit(text[-1], (int(float(i.split(",")[1]))-(0.5*text[-1].get_width()),int(float(i.split(",")[2]))-35))
				else:
					if i.split(",")[6] == notes[i.split(",")[0]]:
						if reading[i.split(",")[0]] < 4:
							reading[i.split(",")[0]] += 1
						sumvx = 0
						sumvy = 0
						for j in range(reading[i.split(",")[0]]+1):
							sumvx += float(i.split(",")[4].split(";")[j])
							sumvy += float(i.split(",")[5].split(";")[j])
						screen.blit(char[-1], (int(float(i.split(",")[1])+sumvx)-15,int(float(i.split(",")[2])+sumvy)-15))
						screen.blit(text[-1], (int(float(i.split(",")[1])+sumvx)-(0.5*text[-1].get_width()),int(float(i.split(",")[2])+sumvy)-35))
					else:
						reading[i.split(",")[0]] = -1
						screen.blit(char[-1], (int(float(i.split(",")[1]))-15,int(float(i.split(",")[2]))-15))
						screen.blit(text[-1], (int(float(i.split(",")[1]))-(0.5*text[-1].get_width()),int(float(i.split(",")[2]))-35))
		screen.blit(snowman, (300,300))
		pygame.display.update()
		note += 1
		if note == 30:
			note = 0

if __name__ == "__main__":
	t = threading.Thread(target=getinfo)
	t.start()
	run(id)