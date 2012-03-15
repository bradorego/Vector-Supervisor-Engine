import random, os, sys, thread, time, getopt
from socket import *
from select import select
from engine import *

HOST = 'localhost'
PORT = 1337
BUFSIZE = 1024
ADDR = (HOST, PORT)
#serversock = socket(AF_INET, SOCK_STREAM)
#serversock.bind(ADDR)
#serversock.listen(4)
players = []
mainsocks, readsocks, writesocks = [], [], []
gamepositions = []
buffers = ["","","",""]
ids = []

def readline(buffer, sock):
	index = buffer.find('\n')
	while index < 0:
		try:
			buffer += sock.recv(BUFSIZE)
		except:
			print 'Error reading socket'
		if not buffer: return (buffer, "")
		index = buffer.find('\r')
	
	line = buffer[0:buffer.find('\r')]
	buffer = buffer[buffer.find('\r')+2:]
	return (buffer, line)

def initialize():
	global players, mainsocks, readsocks, writesocks
	tsock = socket(AF_INET, SOCK_STREAM)
	tsock.bind(ADDR)
	tsock.listen(4)
	mainsocks.append(tsock)
	readsocks.append(tsock)
	writesocks.append(tsock)
	
	while len(players) < 4:
		r, w, e = select(readsocks, writesocks, [])
		for s in r:
			if s in mainsocks and len(players) < 4:
				newsock, address = s.accept()
				readsocks.append(newsock)
				writesocks.append(newsock)
				players.append(newsock)
			else:
				data = s.recv(1024)
				print data, id(s)
	for s in players:
		s.send('ALL PLAYERS CONNECTED\r\nGAME START\r\n')
	main()

def sendall(msg):
	r, w, e = select(readsocks, writesocks, [])
	p = players[:]
	while len(p) > 0:
		for s in w:
			if s in players:
				p.remove(s)
				s.send(msg + "\r\n")

def readall():
	global buffers
	r, w, e = select(readsocks, writesocks, [])
	p = players[:]
	lines = ["","","",""]
	while len(p) > 0:
		r, w, e = select(readsocks, writesocks, [])
		for s in r:
			if s in p:
				p.remove(s)
				index = players.index(s)
				buffers[index], lines[index] = readline(buffers[index], s)
	return lines

def main():
	global buffers, readsocks, writesocks, ids, games, rounds, timeout
	# ordering is N, E, S, W
	# list of game pairs will be a list of quadruples

	gamestate = "IDENTIFY"
	while 1:
		readables, writeables, exceptions = select(readsocks, writesocks, [])
		if gamestate == "IDENTIFY":
			sendall("IDENTIFY?")
			gamestate = "READ_IDENTIFY"
		elif gamestate == "READ_IDENTIFY":
			lines = readall()
			ids = lines[:]
			#sendall("BEGIN TOURNAMENT")
			# begin tournament now!!!
			engine(games, rounds, timeout, ids, players)
			gamestate = ""
			for s in players:
				s.close()
			sys.exit(10000)
		elif gamestate == "BAD_GAME":
			for s in players:
				s.close()
			sys.exit(0)

		#for sockobj in readables:
		#	data = sockobj.recv(1024)
		#	print 'got', data, 'from', id(sockobj)
		#	if not data:
		#		sockobj.close()
		#		readsocks.remove(sockobj)
		#	else:
		#		sockobj.send(data)
		#for sockobj in writeables:
		#	if sockobj in players:
				#for all writeable dudes
games = 13
rounds = 12
timeout = 0.5

try:
	optlist, args = getopt.getopt(sys.argv[1:], 'g:r:t:h:')
except getopt.GetoptError, err:
	print str(err)
	print 'options: [-g games] [-r rounds] [-t timeout] [-h host]'
	sys.exit(2)

for o,a in optlist:
	if o == '-g':
		games = int(a)
	elif o == '-r':
		rounds = int(a)
	elif o == '-t':
		timeout = float(a)
	elif o == '-h':
		HOST = a
		ADDR = (HOST, PORT)
	else:
		assert False, "unhandled option"

initialize()
