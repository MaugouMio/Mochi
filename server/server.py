#-*- coding: UTF-8 -*-
import socket, threading, msvcrt, random
import pygame

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
print "server started at " + ip
s.bind((ip, 10000))
s.listen(20)

online = {}
team = {}
motionlist = {}
x = {}
vx = {}
y = {}
vy = {}
rectdict = {}
score = {}
white = 0
pink = 0
scoring = 0
pointW = 0
pointP = 0
LTW = " "
LTP = " "
scoreplayer = " "

def ball():
	global online, team, motionlist, x, dx, y, dy, score
	while True:
		if ord(msvcrt.getch()) == 13:
			print "ball summoned/reset!"
			online[" "] = "640,360,0"
			team[" "] = "2"
			motionlist[" "] = []
			x[" "] = 640
			vx[" "] = 0
			y[" "] = 360
			vy[" "] = 0
			score[" "] = ""

def link(sock,addr):
	global online, motionlist, x, y, vx, vy, rectdict, team, white, pink, score
	already = 0
	datalist = []
	senddata = []
	while True:
		try:
			data = sock.recv(1024)
			if data[0] == "+":
				print data[1:]+" disconnected"
				del online[data[1:]]
				del motionlist[data[1:]]
				del x[data[1:]]
				del y[data[1:]]
				del vx[data[1:]]
				del vy[data[1:]]
				del score[data[1:]]
				if team[data[1:]] == "0":
					white -= 1
				elif team[data[1:]] == "1":
					pink -= 1
				del team[data[1:]]
				try:
					del rectdict[data[1:]]
				except:
					pass
				break
			elif data[0] == "-":
				if data[1:] in online:
					sock.send("already")
					already = 1
				if already == 0:
					if white <= pink:
						white += 1
						team[data[1:]] = "0"
						motionlist[data[1:]] = []
						x[data[1:]] = random.randint(120,320)
						vx[data[1:]] = 0
						y[data[1:]] = random.randint(60,660)
						vy[data[1:]] = 0
						score[data[1:]] = 0
						online[data[1:]] = str(x[data[1:]]) + "," + str(y[data[1:]]) + ",2"
					else:
						pink += 1
						team[data[1:]] = "1"
						motionlist[data[1:]] = []
						x[data[1:]] = random.randint(960,1160)
						vx[data[1:]] = 0
						y[data[1:]] = random.randint(60,660)
						vy[data[1:]] = 0
						score[data[1:]] = 0
						online[data[1:]] = str(x[data[1:]]) + "," + str(y[data[1:]]) + ",0"
					for i in online:
						senddata.append(i+","+online[i]+","+team[i]+","+str(score[i]))
					senddata.append("-"+str(scoring)+"-"+str(pointW)+"-"+str(pointP)+"-"+scoreplayer)
					sock.send("\n".join(senddata))
					senddata = []
					print data[1:]+" logged in"
				already = 0
			elif data == ";":
				break
			else:
				for i in online.keys():
					if i == data.split(",")[0]:
						datalist = data.split(",")
						if scoring == 0:
							for j in datalist[1].split(";"):
								if j != "":
									motionlist[i].append(int(j))
						online[i] = online[i][:-1] + datalist[2]
					senddata.append(i+","+online[i]+","+team[i]+","+str(score[i]))
				senddata.append("-"+str(scoring)+"-"+str(pointW)+"-"+str(pointP)+"-"+scoreplayer)
				sock.send("\n".join(senddata))
				senddata = []
		except:
			print datalist[0] + " disconnected"
			del online[datalist[0]]
			del motionlist[datalist[0]]
			del x[datalist[0]]
			del y[datalist[0]]
			del vx[datalist[0]]
			del vy[datalist[0]]
			del score[datalist[0]]
			if team[datalist[0]] == "0":
				white -= 1
			elif team[datalist[0]] == "1":
				pink -= 1
			del team[datalist[0]]
			try:
				del rectdict[datalist[0]]
			except:
				pass
			break
	sock.close()

def run():
	global motionlist, online, x, y, vx, vy, rectdict, scoring, pointW, pointP, LTW, LTP, scoreplayer
	clock = pygame.time.Clock()
	while True:
		clock.tick(60)

		for i in online.keys():
			try:
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
					if x[i] >= 1235:
						x[i] = 1235
						if y[i] > 270 and y[i] < 450:
							scoring += 1
							if scoring == 180:
								pointW += 1
								if pointW == 15:
									pass
								else:
									scoring = 0
									x[i] = 640
									y[i] = 360
							elif scoring == 480:
								scoring = 0
								x[i] = 640
								y[i] = 360
								pointW = 0
								pointP = 0
								LTW = " "
								LTP = " "
								scoreplayer = " "
						if scoring == 0:
							vx[i] = -vx[i]
						elif scoring == 1:
							vx[i] = 0
							vy[i] = 0
							scoreplayer = LTW
							if LTW in score:
								score[LTW] += 1
							else:
								LTW = " "
								scoreplayer = " "
					elif x[i] <= 45:
						x[i] = 45
						if y[i] > 270 and y[i] < 450:
							scoring += 1
							if scoring == 180:
								pointP += 1
								if pointP == 15:
									pass
								else:
									scoring = 0
									x[i] = 640
									y[i] = 360
							elif scoring == 480:
								scoring = 0
								x[i] = 640
								y[i] = 360
								pointW = 0
								pointP = 0
								LTW = " "
								LTP = " "
								scoreplayer = " "
						if scoring == 0:
							vx[i] = -vx[i]
						elif scoring == 1:
							vx[i] = 0
							vy[i] = 0
							scoreplayer = LTP
							if LTP in score:
								score[LTP] += 1
							else:
								LTP = " "
								scoreplayer = " "

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
			except:
				pass
		for i in online.keys():
			try:
				for j in rectdict[i].collidedictall(rectdict, 1):
					if i != " ":
						if i != j[0] and j[0] != " ":
							vx[i], vx[j[0]] = vx[j[0]], vx[i]
							vy[i], vy[j[0]] = vy[j[0]], vy[i]
						elif j[0] == " ":
							if scoring == 0:
								vx[j[0]], vx[i] = 1.5 * vx[i], 0.5*vx[j[0]]+vx[i]
								vy[j[0]], vy[i] = 1.5 * vy[i], 0.5*vy[j[0]]+vy[i]
								if team[i] == "0":
									LTW = i
								else:
									LTP = i
					elif i == " ":
						if i != j[0]:
							if scoring == 0:
								vx[i], vx[j[0]] = 1.5 * vx[j[0]], 0.5*vx[i]+vx[j[0]]
								vy[i], vy[j[0]] = 1.5 * vy[j[0]], 0.5*vy[i]+vy[j[0]]
								if team[j[0]] == "0":
									LTW = j[0]
								else:
									LTP = j[0]
				del rectdict[i]
			except:
				pass

h = threading.Thread(target=run)
h.start()
b = threading.Thread(target=ball)
b.start()
print "press enter to summon/reset ball"

while True:
	sock, addr = s.accept()
	sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
	t = threading.Thread(target=link, args=(sock,addr))
	t.start()