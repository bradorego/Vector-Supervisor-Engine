from select import select

class Player:
	def __init__(self, sock, name):
		self.name = name
		self.sock = sock
	
	def writeline(self, line):
		self.sock.send(line + "\r\n")

	def readline(self):
		index = -1
		buffer = ""
		r, w, e = select((self.sock, ), (self.sock, ), [])
		if len(r) == 0:
			return "NOINPUT"
		while index < 0:
			try:
				r, w, e = select((self.sock, ), (self.sock, ), [])
				for s in r:
					buffer += s.recv(512)
			except:
				print 'Error reading socket'
			if not buffer: return (buffer, "")
			index = buffer.find('\r')
		
		line = buffer[0:buffer.find('\r')]
		return line
	
	def begin_tourney(self, names):
		i = 0
		for game in names:
			line = "GAME " + str(i) + ": " + game[0] + " " + game[1] + " " + game[2] + " " + game[3]
			self.writeline(line)
			i += 1
	
	def begin_game(self, game, names):
		line = "BEGIN GAME " + str(game) + ": " + names[0] + " " + names[1] + " " + names[2] + " " + names[3]
		self.writeline(line)

	def begin_round(self, rnd, piece, first_turn, turns_lost):
		self.writeline("BEGIN ROUND " + str(rnd))
		self.writeline("COORD: " + str(piece[0]) + " " + str(piece[1]))
		line = "TURN ORDER:"
		directions = ["N", "E", "S", "W"]
		for i in range(4):
			if turns_lost[(i+first_turn)%4] == 0:
				line += " " + directions[(i+first_turn)%4]
		self.writeline(line)
	
	def request_dir(self):
		self.writeline("DIRECTION?")
	
	def get_dir(self):
		#DIRECTION: <direction>
		line = self.readline()
		if isinstance(line, tuple):
			print line
		if line == "NOINPUT":
			return -1	
		sline = line.split()
		directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
		try:
			num = directions.index(sline[1])
		except:
			num = -2
		return num
	
	def dir_choice(self, player, direction):
		players = ["N", "E", "S", "W"]
		directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
		line = players[player] + " CHOOSES: " + directions[direction]
		self.writeline(line)
	
	def request_mag(self):
		self.writeline("MAGNITUDE?")
	
	def get_mag(self):
		#MAGNITUDE: <mag>
		line = self.readline()
		while isinstance(line, tuple):
			line = self.readline()
		if line == "NOINPUT":
			return -1
		
		sline = line.split()
		try:
			num = int(sline[1])
		except:
			num = -2
		return num
	
	def mag_choices(self, mags):
		line = "MAGNITUDES:"
		for mag in mags:
			line += " " + str(mag)
		self.writeline(line)
	
	def report_dq(self, dqed):
		players = ["N", "E", "S", "W"]
		line = "DISQUALIFICATION:"
		for player in dqed:
			line += " " + players[player]
		self.writeline(line)
	
	def end_round(self, gscores):
		line = "SCORES(NESW):"
		for score in gscores:
			line += " " + str(score)
		self.writeline(line)
	
	def game_over(self, wlt, tscores, donthatetheplayershatethenames):
		#wlt = 0 for NS victory, 1, for EW victory, 2 for tie (lamez)
		winnar = ["NS", "EW", "TIE"]
		line = "WINNER: " + winnar[wlt]
		self.writeline(line)
		line = "TOURNAMENT SCORES:"
		for i in range(4):
			line += " " + donthatetheplayershatethenames[i] + " = " + str(tscores[i])
		self.writeline(line)

