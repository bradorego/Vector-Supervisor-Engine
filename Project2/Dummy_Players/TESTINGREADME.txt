Group Slytherclaw
VSE Project
Testing README
3/25/09

Files-
computer_player.java
computer_player.py
scripted_player.java
test_case_moves.java
vector_client.c

Overview of scripted_player.java:
Each player randomizes their name unless given a name by command-line arguments. The agent then parses the string for their position in each game, and acts according to the pre-defined script located in test_case_moves.java.

===============================
scripted player test cases
==============================

CASE ONE WHICH IS RUN ON GAME ONE:
1) 
everyone stand still and gets 30 points
(10,10)

2)	east : dir:s mag:1  
	south: dir:s mag:1
	west : dir:s mag:2
	north: dir:s mag:2
results in going to the 3N yellow vector square and end up 
(10,10) -> (10,16) => (10,19)
North: 30
East : 30
South: 30 + 20 = 50
West : 30 + 30 = 60

3)  	south: dir:E mag:3
	west : dir:E mag:1 
	north: dir:E mag:0
	east : dir:S mag:2
results in east losing two turns and end up at SE corner
(10,19) -> (20,20)
North: 30
East : 30
South: 50
West : 60

4)
	west : dir:W mag:2
	north: dir:W mag:2
	east : dir:- mag:-
	south: dir:W mag:3
west loses 50 points from [NW -50]
last two guys go on [W 75] in front of SOUTH's goal
North: 30
East : 30
South: 50
West : 60 -50 + 75 = 85
(20,20) -> (13,20)

5)	
	north: dir:W  mag:2
	east : dir:-  mag:-
	south: dir:SW mag:2
	west : dir:=  mag:=
south makes the goal!!!
North: 30
East : 30
South: 50 -60 = -10 * 2 = -20
West : 85
north + SOUTH = -30
EAST + WEST =   115

CASE TWO: all players sit for all allowed moves (tests tied state, tests gui, etc)

CASE THREE: go north to the yellow arrow and back south to the yellow arrow twice then make goal
(tests if same arrow can be used multiple times)

CASE FOUR: all players give an invalid direction and magnitude

CASE FIVE: all players give an invalid magnitude

CASE SIX: all players move to the bottom right corner repeatedly
(tests everyone losing a turn and corner detection doesnt freak out)

CASE SEVEN TO ELEVEN: test the other ways to make a goal into the south goal from the first case

CASE TWELVE: all players attempt to time out during direction giving phase

CASE THiRTEEN: all players attempt to time out during magnitude giving phase

scripted_player.java needs to be compiled with test_case_moves and then run the executble scripted_player.class


Overview of randomized agents:
Randomized agents act completely at random; that is, a random number is generated using the language's native random function, and either modulo 3 (for magnitude) or modulo 8 (for directions), or it is scaled to fit those parameters. Agents will not randomly fail, but failure cases have been covered in the above enumarated cases, as well as in practice.

To compile and run, compile computer_player.java and execute the associated class file. similarly for vector_client.c. computer_player.py does not require compilation.