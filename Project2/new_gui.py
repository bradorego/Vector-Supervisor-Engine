import os, sys, math
import pygame
from pygame.locals import *
from pygame.font import *
import gui_sidebar

# these are constants technically dependent on the real-life size of the board
# picture we're loading, but I doubt that that will change.
BOARD_DIMS = (1100, 1100)
ULC_OF_CENTER_SQUARE = (527, 527) # the upper left corner of the center board square
SQUARE_DIMS = (42, 42)
CARD_DIMS = (700, 900)
IMG_PATH = "GameObjects1.1/" # the path where we store image files.

# this is an entirely static class used to house constants
class Constants:
    board_scale = .32 # the size of the board, piece, and arrows
    card_scale = 0.1# how much extra size down the cards should be
    board_offset_dims = (int(CARD_DIMS[1]*card_scale), int(CARD_DIMS[1]*card_scale)) # why use the card's y value both times? because they are rotated inn the display
    scaled_board_dims = (int(BOARD_DIMS[0]*board_scale), int(BOARD_DIMS[1]*board_scale))
    scaled_card_dims = (int(CARD_DIMS[0]*card_scale), int(CARD_DIMS[1]*card_scale))
    screen_x = 800
    screen_y = 600
    unit_distance = (44+2)*board_scale # this is how many scaled unit a piece moves, etc. etc.
    # used for both the piece and the arrows
    
# this is a very important function.
# it, well, it kick-starts the whole gui.
class VectorGUI:
    def __init__(self):
        pygame.init()
        # generate the screen, which is required before anything else, as
        # that dictates how transformations etc. are done.
        screen = pygame.display.set_mode((Constants.screen_x, Constants.screen_y))
        pygame.display.set_caption('SlytherClaw Vector')
        # now create the game elements -- the board, the piece, the cards, etc.
        board = BoardSprite(Constants.board_offset_dims, Constants.scaled_board_dims)
        piece = Piece()
        # those were easy, now cards we want to front-load loading all the images:
        VEC_CARD_IMGS = [load_image(IMG_PATH+"VectorDirecCardBack.png", -1),
                         load_image(IMG_PATH+"VectorDirecCardN.png", -1),
                         load_image(IMG_PATH+"VectorDirecCardNE.png", -1),
                         load_image(IMG_PATH+"VectorDirecCardE.png", -1),
                         load_image(IMG_PATH+"VectorDirecCardSE.png", -1),
                         load_image(IMG_PATH+"VectorDirecCardS.png", -1),
                         load_image(IMG_PATH+"VectorDirecCardSW.png", -1),
                         load_image(IMG_PATH+"VectorDirecCardW.png", -1),
                         load_image(IMG_PATH+"VectorDirecCardNW.png", -1)]
        VectorCard.VEC_CARD_IMGS = VEC_CARD_IMGS
    # now, load and save (as a static list) the possible magnitude image files
        MAG_CARD_IMGS = [load_image(IMG_PATH+"VectorMagCardBack.png", -1),
                         load_image(IMG_PATH+"VectorMagCard0.png", -1),
                         load_image(IMG_PATH+"VectorMagCard1.png", -1),
                         load_image(IMG_PATH+"VectorMagCard2.png", -1),
                         load_image(IMG_PATH+"VectorMagCard3.png", -1)]
        MagnitudeCard.MAG_CARD_IMGS = MAG_CARD_IMGS
        # ok, magnitude saved
        # now, load the hypothetical, yet-to-exist arrow image files
        ARROW_IMGS = [load_image(IMG_PATH+"WhiteArrowBody.png", -1),
                      load_image(IMG_PATH+"WhiteArrowHead.png", -1),
                      load_image(IMG_PATH+"BlackArrowBody.png", -1),
                      load_image(IMG_PATH+"BlackArrowHead.png", -1),
                      load_image(IMG_PATH+"RedArrowBody.png", -1),
                      load_image(IMG_PATH+"RedArrowHead.png", -1),
                      load_image(IMG_PATH+"YellowArrowBody.png", -1),
                      load_image(IMG_PATH+"YellowArrowHead.png", -1),
                      load_image(IMG_PATH+"BlueArrowBody.png", -1),
                      load_image(IMG_PATH+"BlueArrowHead.png", -1),
                      load_image(IMG_PATH+"GreenArrowBody.png", -1),
                      load_image(IMG_PATH+"GreenArrowHead.png", -1)]
        ArrowDrawer.ARROW_IMGS = ARROW_IMGS
    # now, for each position on the table, make a pair of cards!
        north_cards = [VectorCard('n'), MagnitudeCard('n')]
        east_cards = [VectorCard('e'), MagnitudeCard('e')]
        south_cards = [VectorCard('s'), MagnitudeCard('s')]
        west_cards = [VectorCard('w'), MagnitudeCard('w')]
        self.screen = screen
        self.board = board
        self.piece = piece
        self.cardlist = [north_cards, east_cards, south_cards, west_cards]

#credit goes to http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html for the
#following function (load_image)
#handy, simple image loader function
def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

# contains the board class
class BoardSprite(pygame.sprite.Sprite):
    def __init__(self, upper_left_corner, my_dims):
        pygame.sprite.Sprite.__init__(self)
        self.upper_left_corner = upper_left_corner
        # this loads the raw data from the image.
        self.start_image, self.start_rect = load_image(IMG_PATH+"Vector Board.png")
        # this line stores the scaled version of the board sprite in the "self.image" field
        self.image = pygame.transform.smoothscale(self.start_image, (my_dims[0], my_dims[1]))
        self.piece = Piece()
    def draw(self, screen):
        screen.blit(self.image, self.upper_left_corner)
    
######
# upper left of starting square: 527, 527
class Piece(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(IMG_PATH+"WoodenPlayPiece.png", -1)
        # 527 is upper left of starting square, so we want to scale that and use as starting poitn
        self.center = int(527*Constants.board_scale) + Constants.board_offset_dims[0], int(527*Constants.board_scale) + Constants.board_offset_dims[1]
        self.loc = self.center

        # heres the fun part: scale the image
        self.image = pygame.transform.scale(self.image, (int(44*Constants.board_scale), int(44*Constants.board_scale)))
        #the 44+2 is the space between two squares, basically, and then you scale it
        self.move_distance = Constants.unit_distance
    def draw(self, screen):
        screen.blit(self.image, self.loc)
    # this is going to be an internal-use method. yay!!!
    def move_piece(self, dir, mag):
        x, y = self.loc
        if dir == 0: # north
            y -= self.move_distance*mag
        elif dir == 1: # northeast
            x += self.move_distance*mag
            y -= self.move_distance*mag
        elif dir == 2: # east
            x += self.move_distance*mag
        elif dir == 3: # southeast
            x += self.move_distance*mag
            y += self.move_distance*mag
        elif dir == 4: # etc....
            y += self.move_distance*mag
        elif dir == 5:
            y += self.move_distance*mag
            x -= self.move_distance*mag
        elif dir == 6:
            x -= self.move_distance*mag
        elif dir == 7: # northwest
            y -= self.move_distance*mag
            x -= self.move_distance*mag
        self.loc = x, y
    def translocate_piece(self, loc):
        self.move_to_center()
        y, x = loc # this is where to move the piece
        if y < 10:
            self.move_piece(0, 10-y)
        elif y > 10:
            self.move_piece(2*2, y-10)
        if x < 10:
            self.move_piece(3*2, 10-x)
        elif x > 10:
            self.move_piece(1*2, x-10)
    def move_to_center(self):
        self.loc = self.center

class Card(pygame.sprite.Sprite):
    def __init__(self, board_pos):
        pygame.sprite.Sprite.__init__(self)
        # load in an array of images, rotated and scaled appropriately
        # the make_my_images method is implemented in the SUBCLASS, fyi.
        self.my_possible_images = self.make_my_images(board_pos)
        # the first card image is always "back"
        self.image = self.my_possible_images[0]
        # the position of the card on the screen is dependent on the card type
    def make_generic_images(self, board_pos, card_list):
        pos_imgs = []
        for img_rect_pair in card_list:
            img, rect = img_rect_pair
            # for every image, scale it down to whatever we wanted....
            shrunk_image = pygame.transform.smoothscale(img, Constants.scaled_card_dims)
            if board_pos == 'n':
                pos_imgs.append(pygame.transform.rotate(shrunk_image, 180))
            elif board_pos == 'e':
                pos_imgs.append(pygame.transform.rotate(shrunk_image, 90))
            elif board_pos == 's':
                pos_imgs.append(pygame.transform.rotate(shrunk_image, 0))
            elif board_pos == 'w':
                pos_imgs.append(pygame.transform.rotate(shrunk_image, 270))
        return pos_imgs
    def draw(self, screen): # ulc = UpperLeftCorner
        screen.blit(self.image, self.ulc)
    def flip(self, index):
        self.image = self.my_possible_images[index]

class VectorCard(Card):
    def __init__(self, pos):
        Card.__init__(self, pos)
        self.pos = pos
        if pos == 'n':
            self.ulc = (Constants.board_offset_dims[0]+(Constants.scaled_board_dims[0]/2), 0)
        elif pos == 'e':
            self.ulc = (Constants.board_offset_dims[0]+Constants.scaled_board_dims[0], Constants.board_offset_dims[1]+(Constants.scaled_board_dims[1]/2))
        elif pos == 's':
            self.ulc = (Constants.board_offset_dims[0]+(Constants.scaled_board_dims[0]/2)-(Constants.scaled_card_dims[0]), Constants.board_offset_dims[1]+Constants.scaled_board_dims[1])
        elif pos == 'w':
            self.ulc = (0, Constants.board_offset_dims[1]+(Constants.scaled_board_dims[1]/2)-Constants.scaled_card_dims[0])
    def make_my_images(self, pos):
        # where is this mysterious static field? Declared in init_gui
        # yes, confusing, but it was the most elegant way I could think of
        # of magically front-loading all the image loads.
        return self.make_generic_images(pos, VectorCard.VEC_CARD_IMGS)

class MagnitudeCard(Card):
    def __init__(self, pos):
        Card.__init__(self, pos)
        self.pos = pos
        if pos == 'n':
            self.ulc = (Constants.board_offset_dims[0]+(Constants.scaled_board_dims[0]/2)-Constants.scaled_card_dims[0], 0)
        elif pos == 'e':
            self.ulc = (Constants.board_offset_dims[0]+Constants.scaled_board_dims[0], Constants.board_offset_dims[1]+(Constants.scaled_board_dims[1]/2)-Constants.scaled_card_dims[0])
        elif pos == 's':
            self.ulc = (Constants.board_offset_dims[0]+(Constants.scaled_board_dims[0]/2), Constants.board_offset_dims[1]+Constants.scaled_board_dims[1])
        elif pos == 'w':
            self.ulc = (0, Constants.board_offset_dims[1]+(Constants.scaled_board_dims[1]/2))
    def make_my_images(self, pos):
        # see comment in VectorCard as to where the static field comes from
        return self.make_generic_images(pos, MagnitudeCard.MAG_CARD_IMGS)

# this is a class that contains all of the images and the functions to draw an arrow on
# the screen
class ArrowDrawer():
    to_blit = []
    @staticmethod
    def make_unrotated_arrow(mag, team):
        # the length of hte body is -1 (1 for the head, you see) times the actual number of pixels
        draw_magnitude = (mag-1)*Constants.unit_distance
        base_image = ArrowDrawer.ARROW_IMGS[team][0] # that's the image, [0][1] is the rect.
        # so this should be the east-pointing body of the right length,
        lengthened_base = pygame.transform.scale(base_image, (int(draw_magnitude), int(Constants.unit_distance)))
        # now make the head and scale it:
        head_image = ArrowDrawer.ARROW_IMGS[team+1][0] # image of head
        scaled_head = pygame.transform.scale(head_image, (int(Constants.unit_distance), int(Constants.unit_distance)))
        full_arrow = pygame.Surface((draw_magnitude+Constants.unit_distance, Constants.unit_distance)) # this is enough room for the body plus the head.
        full_arrow.blit(lengthened_base, (0, 0))
        full_arrow.blit(scaled_head, (draw_magnitude, 0)) # put the head on the end.
        return full_arrow, draw_magnitude+Constants.unit_distance # the image, and its len
    @staticmethod
    def rotate_arrow(full_arrow, imglen, dir):
        dir = -dir # to make things rotate appropriately, clockwise instead of anticlockwise.
        roto_angle = (dir+2)*45 # arrow defaults to east, so the +2 kicks default up to north, and then, each n, ne, e, se etc is 45 degrees of a 360 degree circle!
        if dir % 2 == 1: # n, s, e, w, are all even number. So if this is true, we have a diagonal! always, daigonals cause problems, in every project. :(
            full_arrow = pygame.transform.scale(full_arrow, (int(imglen*1.41), int(Constants.unit_distance))) # 1.41 is sqrt 2, simply.
        rotated_arrow = pygame.transform.rotate(full_arrow, roto_angle)
        return rotated_arrow
    @staticmethod
    def calculate_offsets(length, dir, pieceloc):
        dir = -dir
        angle = (dir+2)*45
        if dir % 2 == 1:
            length *= 1.41
        x, y = pieceloc
        # this is probably done a lot more elegantly through trigonemtry, but
        # the cases are small enough for manual tweaking, so hey.
        if dir == 0: #north
            y += (Constants.unit_distance/2) - length
        if dir == -1: #northeast
            y += -math.sin(math.radians(angle))*length + Constants.unit_distance/4
        if dir == -2: # east
            x += (Constants.unit_distance/2)
        if dir == -3: # etc
            x += (Constants.unit_distance/4)
        if dir == -4:
            y += (Constants.unit_distance/2)
        if dir == -5:
            x += (math.cos(math.radians(angle))*length) + (Constants.unit_distance/4)
            y += (Constants.unit_distance/4)
        if dir == -6:
            x += -length+(Constants.unit_distance/2)
        if dir == -7:
            y += -math.sin(math.radians(angle))*length
            x += (math.cos(math.radians(angle))*length) + (Constants.unit_distance/4)
        return (x, y)
    @staticmethod
    def draw_arrow(dir, mag, pieceloc, team):
        if mag is 0:
            return None # nothing to draw, nothing to return
        else:
            team = (team+2)*2
            unrotated, length = ArrowDrawer.make_unrotated_arrow(mag, team)
            rotated = ArrowDrawer.rotate_arrow(unrotated, length, dir)
            offsets = ArrowDrawer.calculate_offsets(length, dir, pieceloc)
            rotated.set_colorkey(rotated.get_at((0, 0)), RLEACCEL)
            ArrowDrawer.to_blit.append((rotated, offsets))
    @staticmethod
    def commit_arrows(screen):
        for arrow in ArrowDrawer.to_blit:
            pic, loc = arrow
            screen.blit(pic, loc)
        ArrowDrawer.to_blit = [] # empty the buffer

class TournyHistory:
    def __init__(self):
        self.game_details = [[]] # a one element list, with an empty list -- usd to boot strap the saving process in save_turn
        self.current_cards = None # these will store what the system tells via "update" calls,
        self.current_moves = None # and then commit them to memory in the game_details list o lists
        self.current_score = 0
        self.current_t_scores = [0,0,0,0] # tournament scores
        self.current_positions = []
    def card_info_update(self, card_info):
        self.current_cards = card_info
    def move_info_update(self, move_info):
        self.current_moves = move_info
        # both the moves and the cards must be saved, because the GUI doesn't have access to the board representation, so everything must be saved
    def names_info_update(self, players_by_positions):
        self.current_positions = players_by_positions # a tuple or list of strings.
    def score_info_update(self, score_info):
        self.current_score = score_info[:]
    def tourny_info_update(self, tscores):
        self.current_t_scores = tscores[:]
    def save_turn(self):
        self.game_details[len(self.game_details)-1].append((self.current_cards, self.current_moves, self.current_score, self.current_positions, self.current_t_scores))
    def new_game(self): # creates a new history entry in the game_details list.
        self.current_cards, self.current_moves, self.current_score = None, None, 0
        self.game_details.append([])
    # returns the (cards, moves) information
    def get_info(self, game, turn):
        return self.game_details[game][turn]

class GUI:
    def __init__(self):
        self.gui = VectorGUI()
        self.history = TournyHistory()
        self.sidebar = gui_sidebar.SideBar()
    def update_piece(self,turn_info, replay_mode = False, start_loc = None, first_turn = False):
        self.history.move_info_update(turn_info)
        # start loc is used only in replay mode, the idea being that it is really hard to figure out where the piece *start* at the beginning of this turn.
        if start_loc is not None:
            self.gui.piece.translocate_piece(start_loc)
        if first_turn is True:
        	self.gui.piece.move_to_center()
        for move_command in turn_info:
            who, dir, mag, loc = move_command
            if who is -1:
                # you hit a wall, go to corner specified by loc (x, y)
                self.gui.piece.translocate_piece(loc)
            else:
                # normal case, you move piece, flip card, draw arrow
                # first draw the arrow (because it starts where th piece starts, so needs to know whhere it is NOW, not after it moves
                ArrowDrawer.draw_arrow(dir, mag, self.gui.piece.loc, who)
                # move the piece
                self.gui.piece.move_piece(dir, mag)
            if replay_mode:
                self.gui.piece.translocate_piece(loc) # to deal with crazy back-and-forward stuff
    # this will handle the cards
    # the cards are flipped regardless of what happens on the board
    def update_cards(self,card_info):
        self.history.card_info_update(card_info)
        moved = [False, False, False, False] # tracks, which player got to move
        for card in card_info:
            who, dir, mag = card
            self.gui.cardlist[who][0].flip(dir+1)
            self.gui.cardlist[who][1].flip(mag+1)
            moved[who] = True
        for player in range(4):
            if moved[player] is False: # if this player did not get to move...
                self.gui.cardlist[player][0].flip(0)
                self.gui.cardlist[player][1].flip(0)
    # set board to blank, set piece to middle
    def update_scores(self, scores):
        self.history.score_info_update(scores)
        a, b, c, d = scores
        self.sidebar.update_scores(a, b, c, d)
    def update_tourny(self, tscores):
        self.history.tourny_info_update(tscores)
        a, b, c, d = tscores
        self.sidebar.update_tournament(a, b, c, d)
    def update_names(self, names):
        self.history.names_info_update(names)
        a, b, c, d = names
        self.sidebar.update_names(a, b, c, d)
    def reset_board(self):
        self.gui.piece.move_to_center()
        for player in self.gui.cardlist:
            player[0].flip(0)
            player[1].flip(0)
    def new_game(self): # we reset the board at the start of the game, so we start the next game!
        self.history.new_game()
        self.reset_board()
    def redraw_screen(self, winner_panel = None): # this blits stuff, then refreshes the screen!
        self.gui.screen.fill((0, 0, 0))
        self.gui.board.draw(self.gui.screen)
        self.gui.piece.draw(self.gui.screen)
        for team in self.gui.cardlist:
            team[0].draw(self.gui.screen)
            team[1].draw(self.gui.screen)
        ArrowDrawer.commit_arrows(self.gui.screen) # the arrows are drawn last
        sidebar_image = self.sidebar.get_sidebar()
        self.gui.screen.blit(sidebar_image,(600, 0))
        if winner_panel is not None:
        	self.gui.screen.blit(winner_panel, (0, 570))
        pygame.display.flip()
    def commit_history(self):
        self.history.save_turn() # saves the turn, yay
    def start_replay_mode(self):
        pygame.event.clear() # we don't care about any previous input, avoid silliness
        current_game = 0
        current_turn = 0
        self.reset_board()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # we want to quit out of htis, i guess?
                        return
                    # flip throug, within the turns of a single game
                    elif event.key == pygame.K_RIGHT:
                        # check to see if this is a valid turn:
                        if current_turn < len(self.history.game_details[current_game])-1:
                            current_turn += 1
                    # if you go back a turn, you also have to figure out where the piece
                    # ended up on the turn *prior* to that! thus, look back even one more step
                    # -- if you start on turn 1 (and thus want to go to turn 0, and will look
                    # back to turn -1, that is the "start" of the game, so your reset
                    elif event.key == pygame.K_LEFT:
                        if current_turn == 0:
                            current_turn -= 0 # this case is actually dealt with after this if/else block
                        elif current_turn == 1:
                            current_turn -=1
                            self.gui.piece.move_to_center()
                        elif current_turn > 1:
                            current_turn -= 1
                            list_o_turn = self.history.game_details[current_game][current_turn-1][1]
                            last_turn =list_o_turn[len(list_o_turn)-1]
                            who, dir, mag, loc = last_turn
                            self.gui.piece.translocate_piece(loc)
                    # flip through on a game-by-game
                    elif event.key == pygame.K_UP:
                        if current_game < len(self.history.game_details)-2:
                            self.reset_board()
                            current_game += 1
                            current_turn = 0
                    elif event.key == pygame.K_DOWN:
                        if current_game > 0:
                            self.reset_board()
                            current_game -= 1
                            current_turn = 0
                    # print len(self.history.game_details), current_game
                    # figure out the end point of the previous turn, so it starts up correctly
                    list_o_turn = self.history.game_details[current_game][current_turn-1][1]
                    last_turn = list_o_turn[len(list_o_turn)-1]
                    start_loc = last_turn[3]
                    # figure out this turns cards and arrows to display
                    cards, moves, scores, positions, tourny_scores = self.history.get_info(current_game, current_turn)
                    self.update_cards(cards)
                    if current_turn is 0:
                        self.update_piece(moves, True, start_loc, True)
                    else:
                        self.update_piece(moves, True, start_loc)
                    self.update_scores(scores)
                    self.update_tourny(tourny_scores)
                    self.update_names(positions)
                    # self.gui.screen is the big screen surface! Blit your winner messages up 
                    # over that. Constants.screen_x, Constants.screen_y
                    if current_turn == len(self.history.game_details[current_game])-1 and \
                        current_game == len(self.history.game_details)-2:
                            print 'Tourny winner should be announced'
                            # display the tournament winnner, calc from tourny_scores!
                            # their names will be in positions -- ie, if index 1 of tourny_scores
                            # is the winner, then index 1 of the positions list is that winner's name
                            t1 = tourny_scores[0]
                            t2 = tourny_scores[1]
                            t3 = tourny_scores[2]
                            t4 = tourny_scores[3]
                            winner = max(t1, max(t2, max(t3, t4)))
                            winner_names = ''
                            # make a list of the tournament winners
                            i = 0
                            for scores in tourny_scores:
                                if tourny_scores[i] == winner:
                                    print positions[i]
                                    winner_names += positions[i] + ' '
                                i += 1 # maintain which score we're talking about
                                
                            if pygame.font:
                            	print 'Fonts exist', winner_names
                            	winner_font = pygame.font.Font(gui_sidebar.font_file, 20)
                            	winner_tourny_label = winner_font.render("Tournament Winner:" + winner_names,1,(255,255,255))
                            	t_win_panel = pygame.Surface((400,30))
                            	#t_win_panel.background((250,0,0))
                            	t_win_panel.blit(winner_tourny_label, (0,0))
                                #self.gui.screen.blit(t_win_panel,(0,570))
                                self.redraw_screen(t_win_panel)
                            else:
                                self.redraw_screen()
                    elif current_turn == len(self.history.game_details[current_game])-1:
                        print "End of game!"
                        north_south_score = scores[0] + scores[2]
                        east_west_score = scores[1] + scores[3]
                        winners = ''
                        if north_south_score > east_west_score:
                            winners += positions[0] + ' ' + positions[2] + ' are the winners!'
                        elif north_south_score == east_west_score:
                            winners += "Tie game!"
                        else:
                            winners += positions[1] + ' ' + positions[3] + ' are the winners!'
                        if pygame.font:
                            winner_font = pygame.font.Font(gui_sidebar.font_file, 20)
                            winner_game_label = winner_font.render(winners,1,(255, 255, 255))
                            g_win_panel = pygame.Surface((400, 30))
                            g_win_panel.blit(winner_game_label, (0, 0))
                            self.redraw_screen(g_win_panel)
                        else:
                            self.redraw_screen()
                    else:
                        self.redraw_screen()
                        

# debugging stuff, this may not even work anymore
if __name__=='__main__':
    g = GUI()
    #g.update_piece([(0, 2, 3, None), (1, 4, 2, None), (2, 0, 1, None), (3, 6, 3, None)])
    #g.redraw_screen()
    while True:
        g.redraw_screen()
