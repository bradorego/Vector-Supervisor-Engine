import random, os, sys, thread, time, getopt
from socket import *
from select import select
#from engine import *

# random computer player
# independent of the server, also doesn't care about the slightest bit about strategy so not very robust now

BUFSIZE = 1024
buffer = ""
#read a line from the socket
def readline(sock):
	global buffer
	index = buffer.find('\r')
	while index < 0:
		buffer += sock.recv(BUFSIZE)
		index = buffer.find('\r')
	line = buffer[0:index]
	buffer = buffer[index+2:]
	return line
	
#the game hasn't started yet, wait until it starts!
def lobby_wait(sock,identity):
	counter = 0
	#sock.send("HOW ARE YOU GENTLEMEN?")
	while 1:
		line = readline(sock)
		# if the player gets the confirmation taht the game started,
		counter += 1
		print str(counter) + "] " + line
		if (line == "IDENTIFY?"):
			print "PRESENTING IDENTIFICATION TO SERVER"
			sock.send(identity + "\r\n")
			print "SENT " + identity
			play_game(sock)
	
def sendline(sock, line):
	sock.send(line + "\r\n")

def play_game(sock):
	while 1:
		#get input from server
		line = readline(sock)
		# is it time to send direction?
		if (line != ""):
			print line
		if (line == "DIRECTION?"):
			print "PRESENTING DIRECTION TO SERVER"
			send_direction(sock)
		#is it time to send magnitude?
		elif (line == "MAGNITUDE?"):
			print "PRESENTING MAGNITUDE TO SERVER"
			send_magnitude(sock)
		#elif (line.count("TOURNAMENT SCORES:") > 0):
		elif (line == "TOURNAMENT OVER"):
			print "TOURNAMENT OVER, DISCONNECTING"
			sock.close()
			sys.exit(0)
		elif (line == ""):
			print "GAME OVER MAN GAME OVER"
			sock.close()
			sys.exit(0)
        #if we get a game over, then the client will automatically disconnect i guess i dont know
	
def send_direction(sock):
	directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
	randDir = random.randint(0,7)
	direction = "DIRECTION: " + directions[randDir] + "\r\n"
	#some code that would send the direction to the server
	sock.send(direction)
	#sock.send("DIRECTION: N \r\n")
	
def send_magnitude(sock):
	magnitude = "MAGNITUDE: " + str(random.randint(0,3)) + "\r\n"
	#print 'here is the magnitude...: ',magnitude
	#some code that would send the magnitude to the server
	sock.send(magnitude)
	#sock.send("MAGNITUDE: 1 \r\n")

# check arguments inputted
if (len(sys.argv) != 4):
	#print 'arguments needed: <address> <port> <playerID>'
	#quit()
	HOST = 'localhost'
	PORT = 1337
	ADDR = (HOST, PORT)
	PLID = "CPU" + str(random.randint(0,99))
	myHOST = 'localhost'
	myPORT = 1337 + random.randint(1,100)
	myADDR = (myHOST, myPORT)
else:
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])
	ADDR = (HOST, PORT)
	PLID = sys.argv[3]
	myHOST = 'localhost'
	myPORT = 1337 + random.randint(1,100)
	myADDR = (myHOST, myPORT)
	#maybe add configurable options like intended invalid moves mode and the like

tsock = socket(AF_INET, SOCK_STREAM)
tsock.connect(ADDR)
lobby_wait(tsock,PLID)

