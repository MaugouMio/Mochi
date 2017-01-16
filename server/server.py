import socket, threading, msvcrt, time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
print "server started at " + ip
s.bind((ip, 10000))
s.listen(20)

f = open("pos.txt", "r")
info = f.read().split("\n")
f.close()
online = {}
motionlist = {}
x = {}
vx = {}
y = {}
vy = {}

def autosave():
	global info
	for i in online:
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
			f = open("pos.txt", "w")
			f.write("\n".join(info))
			f.close()
			print "---server saved!---"

def link(sock,addr):
	global info, online, motionlist, x, y, vx, vy
	refresh = 0
	already = 0
	datalist = []
	senddata = []
	while True:
		data = sock.recv(1024)
		if data[:4] == "stop":
			print data[5:]+" disconnected"
			for i in online:
				if i == data[5:]:
					for j in range(len(info)):
						if info[j].split(",")[0] == i:
							info[j] = i + "," + online[i]
					del online[i]
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
						for i in online:
							senddata.append(i+","+online[i])
						sock.send("\n".join(senddata))
						senddata = []
						print data[1:]+" logged in"
						refresh = 1
					already = 0
					break
			if refresh != 1:
				if data[1] != "-":
					info.append(data[1:]+",640,360,3")
					online[data[1:]] = "640,360,3"
					motionlist[data[1:]] = []
					x[data[1:]] = 640
					vx[data[1:]] = 0
					y[data[1:]] = 360
					vy[data[1:]] = 0
					for i in online:
						senddata.append(i+","+online[i])
					sock.send("\n".join(senddata))
					senddata = []
					print data[1:]+" logged in"
				else:
					sock.send("wrong")
			refresh = 0
		else:
			for i in online:
				if i == data.split(",")[0]:
					datalist = data.split(",")
					for j in datalist[1].split(";"):
						if j != "":
							motionlist[i].append(int(j))
					online[i] = online[i][:-1] + datalist[2]
				senddata.append(i+","+online[i])
			sock.send("\n".join(senddata))
			senddata = []
	sock.close()

def run():
	global motionlist, online, x, y, vx, vy
	while True:
		starttime = time.clock()
		
		for i in online:
			x[i] += vx[i]
			if x[i] > 1280:
				x[i] = 1280
				vx[i] = 0
			elif x[i] < 0:
				x[i] = 0
				vx[i] = 0

			y[i] += vy[i]
			if y[i] > 720:
				y[i] = 720
				vy[i] = 0
			elif y[i] < 0:
				y[i] = 0
				vy[i] = 0

			if len(motionlist[i]) > 0:
				vx[i] += 0.3 * ((motionlist[i][0]/10)-5)
				vy[i] += 0.3 * ((motionlist[i][0]%10)-5)
				del motionlist[i][0]

			if vx[i] > 0:
				vx[i] -= 0.05
				if vx[i] > 4:
					vx[i] -= 0.05
			elif vx[i] < 0:
				vx[i] += 0.05
				if vx[i] < -4:
					vx[i] += 0.05
			if vx[i] > 8:
				vx[i] = 8
			elif vx[i] < -8:
				vx[i] = -8
			elif abs(vx[i]) < 0.05:
				vx[i] = 0
			
			if vy[i] > 0:
				vy[i] -= 0.05
				if vy[i] > 4:
					vy[i] -= 0.05
			elif vy[i] < 0:
				vy[i] += 0.05
				if vy[i] < -4:
					vy[i] += 0.05
			if vy[i] > 8:
				vy[i] = 8
			elif vy[i] < -8:
				vy[i] = -8
			elif abs(vy[i]) < 0.05:
				vy[i] = 0

			online[i] = str(int(x[i])) +","+ str(int(y[i])) + online[i][-2:]

		endtime = time.clock()
		if endtime-starttime <= 0.016:
			time.sleep(0.0166-endtime+starttime)

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