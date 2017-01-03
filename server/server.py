import socket, threading, msvcrt, time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
print "server started at " + ip
s.bind((ip, 10000))
s.listen(20)

f = open("pos.txt", "r")
info = f.read().split("\n")
f.close()
online = []

def autosave():
	global info
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
	global info, online
	refresh = 0
	already = 0
	while True:
		data = sock.recv(1024)
		if data[:4] == "stop":
			print data[5:]+" disconnected"
			for i in online:
				if i.split(",")[0] == data[5:]:
					for j in range(len(info)):
						if info[j].split(",")[0] == i.split(",")[0]:
							info[j] = i
					online.remove(i)
					break
			break
		elif data[0] == "-":
			for i in info:
				if i.split(",")[0] == data[1:]:
					for j in online:
						if j.split(",")[0] == data[1:]:
							sock.send("already")
							already = 1
							refresh = 1
							break
					if already == 0:
						online.append(i)
						sock.send(i)
						print data[1:]+" logged in"
						refresh = 1
					already = 0
					break
			if refresh != 1:
				if data[1] != "-":
					info.append(data[1:]+",800,450,3,0;0;0;0;0,0;0;0;0;0,0")
					online.append(data[1:]+",800,450,3,0;0;0;0;0,0;0;0;0;0,0")
					sock.send(data[1:]+",800,450,3,0;0;0;0;0,0;0;0;0;0,0")
					print data[1:]+" logged in"
				else:
					sock.send("wrong")
			refresh = 0
		else:
			for i in range(len(online)):
				if online[i].split(",")[0] == data.split(",")[0]:
					online[i] = data
					senddata = "\n".join(online)
					sock.send(senddata)
					break
	sock.close()

e = threading.Thread(target=record)
e.start()
g = threading.Timer(600, autosave)
g.start()
print "press enter to record information"

while True:
	sock, addr = s.accept()
	sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
	t = threading.Thread(target=link, args=(sock,addr))
	t.start()