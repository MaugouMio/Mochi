#-*- coding: UTF-8 -*-
import socket, threading, msvcrt
import pygame

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
print "server started at " + ip
s.bind((ip, 10000))
s.listen(20)

f = open("pos.txt", "r")
info = f.read().split("\n")
f.close()
online = {" ":"640,360,0"}
team = {" ":"2"}
motionlist = {" ":[]}
x = {" ":640}
vx = {" ":0}
y = {" ":360}
vy = {" ":0}
rectdict = {}
white = 0
pink = 0

def autosave():
	global info
	for i in online:
		if i != " ":
			for j in range(len(info)):
				if info[j].split(",")[0] == i:
					info[j] = i + "," + online[i]
	f = open("pos.txt", "w")
	f.write("\n".join(info))
	f.close()
	print "---server auto saved---"
	g = threading.Timer(600, autosave)
	g.start()

def record():
	global info
	while True:
		if ord(msvcrt.getch()) == 13:
			for i in online:
				if i != " ":
					for j in range(len(info)):
						if info[j].split(",")[0] == i:
							info[j] = i + "," + online[i]
			f = open("pos.txt", "w")
			f.write("\n".join(info))
			f.close()
			print "---server saved!---"

def link(sock,addr):
	global info, online, motionlist, x, y, vx, vy, rectdict, team, white, pink
	refresh = 0
	already = 0
	datalist = []
	senddata = []
	while True:
		data = sock.recv(1024)
		if data[0] == "+":
			print data[1:]+" disconnected"
			for i in online:
				if i == data[1:]:
					for j in range(len(info)):
						if info[j].split(",")[0] == i:
							info[j] = i + "," + online[i]
					del online[i]
					del motionlist[i]
					del x[i]
					del y[i]
					del vx[i]
					del vy[i]
					if team[i] == "0":
						white -= 1
					elif team[i] == "1":
						pink -= 1
					del team[i]
					try:
						del rectdict[i]
					except:
						pass
					break
			break
		elif data[0] == "-":
			for i in info:
				if i.split(",")[0] == data[1:]:
					for j in online:
						if j == data[1:]:
							sock.send("already")
							already = 1
							refresh = 1
							break
					if already == 0:
						online[data[1:]] = ",".join(i.split(",")[1:])
						motionlist[data[1:]] = []
						x[data[1:]] = int(i.split(",")[1])
						vx[data[1:]] = 0
						y[data[1:]] = int(i.split(",")[2])
						vy[data[1:]] = 0
						if white <= pink:
							white += 1
							team[data[1:]] = "0"
						else:
							pink += 1
							team[data[1:]] = "1"
						for i in online:
							senddata.append(i+","+online[i]+","+team[i])
						sock.send("\n".join(senddata))
						senddata = []
						print data[1:]+" logged in"
						refresh = 1
					already = 0
					break
			if refresh != 1:
				info.append(data[1:]+",640,360,3")
				online[data[1:]] = "640,360,3"
				motionlist[data[1:]] = []
				x[data[1:]] = 640
				vx[data[1:]] = 0
				y[data[1:]] = 360
				vy[data[1:]] = 0
				if white <= pink:
					white += 1
					team[data[1:]] = "0"
				else:
					pink += 1
					team[data[1:]] = "1"
				for i in online:
					senddata.append(i+","+online[i]+","+team[i])
				sock.send("\n".join(senddata))
				senddata = []
				print data[1:]+" logged in"
			refresh = 0
		elif data == ";":
			break
		else:
			for i in online:
				if i == data.split(",")[0]:
					datalist = data.split(",")
					for j in datalist[1].split(";"):
						if j != "":
							motionlist[i].append(int(j))
					online[i] = online[i][:-1] + datalist[2]
				senddata.append(i+","+online[i]+","+team[i])
			sock.send("\n".join(senddata))
			senddata = []
	sock.close()

def run():
	global motionlist, online, x, y, vx, vy, rectdict
	clock = pygame.time.Clock()
	while True:
		clock.tick(60)

		for i in online:
			if i != " ":
				x[i] += vx[i]
				if x[i] > 1280:
					x[i] = 1280
					vx[i] = -vx[i]
				elif x[i] < 0:
					x[i] = 0
					vx[i] = -vx[i]

				y[i] += vy[i]
				if y[i] > 720:
					y[i] = 720
					vy[i] = -vy[i]
				elif y[i] < 0:
					y[i] = 0
					vy[i] = -vy[i]
			elif i == " ":
				x[i] += vx[i]
				if x[i] > 1235:
					x[i] = 1235
					vx[i] = -vx[i]
				elif x[i] < 45:
					x[i] = 45
					vx[i] = -vx[i]

				y[i] += vy[i]
				if y[i] > 675:
					y[i] = 675
					vy[i] = -vy[i]
				elif y[i] < 45:
					y[i] = 45
					vy[i] = -vy[i]

			if len(motionlist[i]) > 0:
				vx[i] += 0.3 * ((motionlist[i][0]/10)-5)
				if vx[i] > 5 and motionlist[i][0]/10 == 4:
					vx[i] += 0.2
				elif vx[i] > 2 and motionlist[i][0]/10 == 4:
					vx[i] += 0.1
				elif vx[i] < -5 and motionlist[i][0]/10 == 6:
					vx[i] -= 0.2
				elif vx[i] < -2 and motionlist[i][0]/10 == 6:
					vx[i] -= 0.1

				vy[i] += 0.3 * ((motionlist[i][0]%10)-5)
				if vy[i] > 5 and motionlist[i][0]%10 == 4:
					vy[i] += 0.2
				elif vy[i] > 2 and motionlist[i][0]%10 == 4:
					vy[i] += 0.1
				elif vy[i] < -5 and motionlist[i][0]%10 == 6:
					vy[i] -= 0.2
				elif vy[i] < -2 and motionlist[i][0]%10 == 6:
					vy[i] -= 0.1

				del motionlist[i][0]

			if vx[i] > 0:
				vx[i] -= 0.05
				if vx[i] > 4:
					vx[i] -= 0.05
			elif vx[i] < 0:
				vx[i] += 0.05
				if vx[i] < -4:
					vx[i] += 0.05
			if vy[i] > 0:
				vy[i] -= 0.05
				if vy[i] > 4:
					vy[i] -= 0.05
			elif vy[i] < 0:
				vy[i] += 0.05
				if vy[i] < -4:
					vy[i] += 0.05

			if i != " ":
				if vx[i] > 8:
					vx[i] = 8
				elif vx[i] < -8:
					vx[i] = -8
				elif abs(vx[i]) < 0.05:
					vx[i] = 0

				if vy[i] > 8:
					vy[i] = 8
				elif vy[i] < -8:
					vy[i] = -8
				elif abs(vy[i]) < 0.05:
					vy[i] = 0

				rectdict[i] = pygame.Rect(x[i]+vx[i]-15,y[i]+vy[i]-15,30,30)
			elif i == " ":
				if abs(vx[i]) < 0.05:
					vx[i] = 0
				if abs(vy[i]) < 0.05:
					vy[i] = 0
				rectdict[i] = pygame.Rect(x[i]+vx[i]-45,y[i]+vy[i]-45,90,90)

			online[i] = str(int(x[i])) +","+ str(int(y[i])) + online[i][-2:]
		for i in online:
			for j in rectdict[i].collidedictall(rectdict, 1):
				if i != " ":
					if i != j[0]:
						vx[i], vx[j[0]] = vx[j[0]], vx[i]
						vy[i], vy[j[0]] = vy[j[0]], vy[i]
				elif i == " ":
					if i != j[0]:
						vx[i], vx[j[0]] = 1.5 * vx[j[0]], 0.5*vx[i]+vx[j[0]]
						vy[i], vy[j[0]] = 1.5 * vy[j[0]], 0.5*vy[i]+vy[j[0]]
			del rectdict[i]

e = threading.Thread(target=record)
e.start()
g = threading.Timer(600, autosave)
g.start()
h = threading.Thread(target=run)
h.start()
print "press enter to record information"

while True:
	sock, addr = s.accept()
	sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
	t = threading.Thread(target=link, args=(sock,addr))
	t.start()