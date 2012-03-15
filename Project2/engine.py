# Main engine class for Vector.
# Last updated March 24, 2009
import sys, time, getopt, random, new_gui
from player import Player
from board_loader import Board, Square

def engine(games, rounds, timeout, ids, socks):
	
	#DO SOME INITIALIZATION
	#define some variables to keep track of all the tournament vitals:
	#i.e. players, their names and the scores
	players = [Player(socks[0], ids[0]), Player(socks[1], ids[1]), Player(socks[2], ids[2]), Player(socks[3], ids[3])]
	playernames = [players[0].name, players[1].name, players[2].name, players[3].name]
	tscores = [0,0,0,0]  # Tournament scores. 1 for win, 0.5 for tie, 0 for loss

	# determine who's where for each game
	rand4 = range(4)
	places = []
	names = []
	for i in range(games):
		random.shuffle(rand4)
		places.append([])
		names.append([])
		for j in range(4):
			places[i].append(rand4[j])
			names[i].append(players[rand4[j]].name)
	print "NAMES: ",names
	#
	board = Board("NEW_BOARD")
	for p in players:
		p.begin_tourney(names)
	
	# ------------------- #
	# Now Start the Game  #
	# ------------------- #
	
	# START THE GUI
	gui = new_gui.GUI()
	
	# NOW BEGIN THE GAMES!!!
	for game in range(games):
		#send gui the names
		gui.update_names(names[game])
		gui.redraw_screen()
		#gui.reset_board()
		print 'game', game
		for p in players:
			p.begin_game(game, names[game])
		first_turn = 0
		piece = [10,10]
		gscores = [0,0,0,0]
		turns_lost = [0, 0, 0, 0]
		turns_lost_rnd = [0,0,0,0] # turns lost for the next round
		dq = [False,False,False,False]
		
		for rnd in range(rounds):
			print '  round', rnd
			dirs = [-1,-1,-1,-1]
			mags = [-1,-1,-1,-1]
			for i in range(4):
				turns_lost[i] += turns_lost_rnd[i]
			if turns_lost != [0,0,0,0]:
				print '  turns_lost=',turns_lost
			turns_lost_rnd = [0,0,0,0]
			lost_turn = [False,False,False,False] # makes sure we don't lose more than one turn per round

			# Make sure we don't have a round where no one plays
			while turns_lost[0] > 0 and turns_lost[1] > 0 and turns_lost[2] > 0 and turns_lost[3] > 0:
				for i in range(4):
					turns_lost[i] -= 1
			
			while turns_lost[first_turn] > 0:
				first_turn = (first_turn+1) % 4
			
			for p in players:
				p.begin_round(rnd, piece, first_turn, turns_lost)
	
			# get directions
			for i in range(4):
				turn = (first_turn + i) % 4
				if(turns_lost[turn]>0):
					continue
				players[places[game][turn]].request_dir()
				t = time.time()
			
				while time.time()-t < timeout and dirs[turn] == -1:
					dirs[turn] = players[places[game][turn]].get_dir()
			
				if dirs[turn] < 0 or dirs[turn] > 7:
					if dirs[turn] == -1:
						print '    player',turn,'timed out'
					else:
						print '    player',turn,'responded incorectly'
					dq[turn] = True
					break
				
				for p in players:
					if p != players[places[game][turn]]:
						p.dir_choice(turn, dirs[turn])
			
			if dq != [False, False, False, False]:
				break
			
			# get magnitudes
			for i in range(4):
				turn = (first_turn + i) % 4
				if(turns_lost[turn]>0):
					continue
				players[places[game][turn]].request_mag()
			t = time.time()
			
			while time.time()-t < timeout and (mags[0] == -1 or mags[1] == -1 or mags[2] == -1 or mags[3] == -1):
				for i in range(4):
					if turns_lost[i]>0:
						mags[i] = 0
					if mags[i] == -1:
						mags[i] = players[places[game][i]].get_mag()
			
			for i in range(4):
				if mags[i] < 0 or mags[i] > 3: # Disqualification
					if mags[i] == -1:
						print '    player',i,'timed out'
					else:
						print '    player',i,'responded incorectly'
					dq[i] = True
			
			if dq != [False, False, False, False]:
				break
			
			for p in players:
				p.mag_choices(mags)
			
			# update location
			move_list = [] # give this to GUI
			update_card_list = [] # card info stuff
			
			# first update the cards
			for i in range(4):
				turn = (first_turn + i) % 4
				if turns_lost[turn] > 0:
					continue
				else:
					update_card_list.append([turn, dirs[turn], mags[turn]])
			gui.update_cards(update_card_list)
			
			game_over = False
			for i in range(4):
				turn = (first_turn + i) % 4
				if turns_lost[turn]>0:
					turns_lost[turn] -= 1
					continue
				
				print '   ', turn, ' dir:', dirs[turn], 'mag:', mags[turn],
				
				#normalization
				if (dirs[turn]==7 or dirs[turn]==0 or dirs[turn]==1) and mags[turn] > piece[0]:
					mags[turn] = piece[0]+1
				if (dirs[turn]==1 or dirs[turn]==2 or dirs[turn]==3) and mags[turn] + piece[1] > 20:
					mags[turn] = 21-piece[1]
				if (dirs[turn]==3 or dirs[turn]==4 or dirs[turn]==5) and mags[turn] + piece[0] > 20:
					mags[turn] = 21-piece[0]
				if (dirs[turn]==5 or dirs[turn]==6 or dirs[turn]==7) and mags[turn] > piece[1]:
					mags[turn] = piece[1]+1
				
				# now normal moves
				if dirs[turn]== 0:    # N
					piece[0] -= mags[turn]
				elif dirs[turn]== 1:  # NE
					piece[0] -= mags[turn]
					piece[1] += mags[turn]
				elif dirs[turn]== 2:  # E
					piece[1] += mags[turn]
				elif dirs[turn]== 3:  # SE
					piece[0] += mags[turn]
					piece[1] += mags[turn]
				elif dirs[turn]== 4:  # S
					piece[0] += mags[turn]
				elif dirs[turn]== 5:  # SW
					piece[0] += mags[turn]
					piece[1] -= mags[turn]
				elif dirs[turn]== 6:  # W
					piece[1] -= mags[turn]
				elif dirs[turn]== 7:  # NW
					piece[0] -= mags[turn]
					piece[1] -= mags[turn]
				
				print 'piece:', piece
				move_list.append([turn, dirs[turn], mags[turn], [piece[0],piece[1]]])
				
				# Handle going off the board
				if piece[0] < 0:
					if piece[1]==9 and dirs[turn]!=1 or piece[1]==10 or piece[1]==11 and dirs[turn]!=7:
						gscores[0]*=2
						game_over=True
						print '      North goal'
						break
					else:
						turns_lost_rnd[turn] += 1
						if piece[1]<10:
							piece[0]=0
							piece[1]=0
						elif piece[1]>10:
							piece[0]=0
							piece[1]=20
						print '      Off-Board. New location:',piece
						move_list.append([-1, dirs[turn], mags[turn], [piece[0],piece[1]]])
				if piece[1] < 0:
					if piece[0]==9 and dirs[turn]!=5 or piece[0]==10 or piece[0]==11 and dirs[turn]!=7:
						gscores[3]*=2
						game_over=True
						print '      West goal'
						break
					else:
						turns_lost_rnd[turn] += 1
						if piece[0]<10:
							piece[0]=0
							piece[1]=0
						elif piece[0]>10:
							piece[0]=20
							piece[1]=0
						print '      Off-Board. New location:',piece
						move_list.append([-1, dirs[turn], mags[turn], [piece[0],piece[1]]])
				if piece[0] > 20:
					if piece[1]==9 and dirs[turn]!=3 or piece[1]==10 or piece[1]==11 and dirs[turn]!=5:
						gscores[2]*=2
						game_over=True
						print '      South goal'
						break
					else:
						turns_lost_rnd[turn] += 1
						if piece[1]<10:
							piece[0]=20
							piece[1]=0
						elif piece[1]>10:
							piece[0]=20
							piece[1]=20
						print '      Off-Board. New location:',piece
						move_list.append([-1, dirs[turn], mags[turn], [piece[0],piece[1]]])
				if piece[1] > 20:
					if piece[0]==9 and dirs[turn]!=3 or piece[0]==10 or piece[0]==11 and dirs[turn]!=1:
						gscores[1]*=2
						game_over=True
						print '      East goal'
						break
					else:
						turns_lost_rnd[turn] += 1
						if piece[0]<10:
							piece[0]=0
							piece[1]=20
						elif piece[0]>10:
							piece[0]=20
							piece[1]=20
						print '      Off-Board. New location:',piece
						move_list.append([-1, dirs[turn], mags[turn], [piece[0],piece[1]]])
				
				s=board.board[piece[0]][piece[1]]
				if s.name=='MOVE':
					temp_direction=0
					if i==0:
						turn = (turn+1)%4
						print '      Yellow Square. Nothing Happens.'
						continue
					#move vector piece
					if s.dir=='NORTH':
						piece[0]-=s.magnitude
					elif s.dir=='NORTHEAST':
						piece[0]-=s.magnitude
						piece[1]+=s.magnitude
						temp_direction=1
					elif s.dir=='EAST':
						piece[1]+=s.magnitude
						temp_direction=2
					elif s.dir=='SOUTHEAST':
						piece[0]+=s.magnitude
						piece[1]+=s.magnitude
						temp_direction=3
					elif s.dir=='SOUTH':
						piece[0]+=s.magnitude
						temp_direction=4
					elif s.dir=='SOUTHWEST':
						piece[0]+=s.magnitude
						piece[1]-=s.magnitude
						temp_direction=5
					elif s.dir=='WEST':
						piece[1]-=s.magnitude
						temp_direction=6
					else:
						piece[0]-=s.magnitude
						piece[1]-=s.magnitude
						temp_direction=7
					print '      Move Square. New location:',piece
					move_list.append([turn, temp_direction, s.magnitude, [piece[0],piece[1]]])
				# NO TURNS
				if s.name == 'NOTURN':
					if s.team == 'NORTH' and not lost_turn[0]:
						lost_turn[0] = True
						turns_lost_rnd[0] += 1
					elif s.team == 'EAST' and not lost_turn[1]:
						lost_turn[1] = True
						turns_lost_rnd[1] += 1
					elif s.team == 'SOUTH' and not lost_turn[2]:
						lost_turn[2] = True
						turns_lost_rnd[2] += 1
					elif s.team == 'WEST' and not lost_turn[3]:
						lost_turn[3] = True
						turns_lost_rnd[3] += 1
					print '      Lost turn.',s.team,'. turns_lost_rnd =',turns_lost_rnd
				if s.name=='POINTS':
					if i==0 and s.color=='YELLOW':
						turn = (turn+1)%4
						continue
					point_receiver=-1
					if len(s.teamlist)==1: #one player in a square - simple
						if s.teamlist[0]=='ALL':
							point_receiver=turn
						elif s.teamlist[0]=='NORTH':
							point_receiver=0
						elif s.teamlist[0]=='EAST':
							point_receiver=1
						elif s.teamlist[0]=='SOUTH':
							point_receiver=2
						elif s.teamlist[0]=='WEST':
							point_receiver=3
					else: #two players in a square
						if s.teamlist==['NORTH','EAST']:
							if (turn%2==0)^(s.value<0):
								point_receiver=0
							else:
								point_receiver=1
						elif s.teamlist==['SOUTH','EAST']:
							if (turn%2==0)^(s.value<0):
								point_receiver=2
							else:
								point_receiver=1
						elif s.teamlist==['SOUTH','WEST']:
							if (turn%2==0)^(s.value<0):
								point_receiver=2
							else:
								point_receiver=3
						elif s.teamlist==['NORTH','WEST']:
							if (turn%2==0)^(s.value<0):
								point_receiver=0
							else:
								point_receiver=3
					gscores[point_receiver]+=s.value
					print '      Points.', point_receiver, 'gets', s.value
			# end update scores
			# here call the function to send the stuff
			gui.update_piece(move_list)
			gui.update_scores(gscores)
			gui.redraw_screen()
			gui.commit_history()
			
			first_turn = (first_turn + 1) % 4 # to get ready for next round
			print '  scores:', gscores
			for p in players:
				p.end_round(gscores)
			if game_over:
				#gui.reset_board()
				break
		gui.new_game()
		# end game

		ns_score = gscores[0] + gscores[2]
		ew_score = gscores[1] + gscores[3]
		if dq != [False,False,False,False]:
			dqed = []
			for i in range(4):
				if dq[i]:
					dqed.append(i)
			if dq[0] or dq[2]:
				ns_score = -1000000
			if dq[1] or dq[3]:
				ew_score = -1000000
			for p in players:
				p.report_dq(dqed)
		
		#calculate the current tournament standings
		if ns_score > ew_score:
			tscores[places[game][0]] = tscores[places[game][0]] + 1
			tscores[places[game][2]] = tscores[places[game][2]] + 1
			for p in players:
				p.game_over(0, tscores, playernames)
		elif ns_score < ew_score:
			tscores[places[game][1]] = tscores[places[game][1]] + 1
			tscores[places[game][3]] = tscores[places[game][3]] + 1
			for p in players:
				p.game_over(1, tscores, playernames)
		else:
			tscores[places[game][0]] = tscores[places[game][0]] + 0.5
			tscores[places[game][1]] = tscores[places[game][1]] + 0.5
			tscores[places[game][2]] = tscores[places[game][2]] + 0.5
			tscores[places[game][3]] = tscores[places[game][3]] + 0.5
			for p in players:
				p.game_over(2, tscores, playernames)
		
		gui.update_tourny(tscores)
		print 'point total:', tscores
	# end tournament
	for p in players:
		p.writeline("TOURNAMENT OVER")
	gui.start_replay_mode()
