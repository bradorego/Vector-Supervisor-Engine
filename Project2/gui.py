import os, sys
import pygame
from pygame.locals import *

# these are constants technically dependent on the real-life size of the board
# picture we're loading, but I doubt that that will change.
BOARD_DIMS = (1100, 1100)
SQUARE_DIMS = (42, 42)
CARD_DIMS = (700, 900)
IMG_PATH = "GameObjects1/" # the path where we store image files.


BOARD_AND_VECTOR_SCALING = 0.35
CARD_SCALING = 0.15
# the reason why we use card_dims[1] for the x value as well is simply because
# the cards rotate! They are always along their y axis, if that makes sens.
BOARD_OFFSET_DIMS = (int(CARD_DIMS[1]*CARD_SCALING), int(CARD_DIMS[1]*CARD_SCALING))
SCALED_BOARD_DIMS = (int(BOARD_DIMS[0]*BOARD_AND_VECTOR_SCALING), int(BOARD_DIMS[1]*BOARD_AND_VECTOR_SCALING)) # computed in init_gui, used for placement of vector, mag. cards
SCALED_CARD_DIMS = (int(CARD_DIMS[0]*CARD_SCALING), int(CARD_DIMS[1]*CARD_SCALING))
# this is a very important function.
# it, well, it kick-starts the whole gui. Call this when you are ready, I suppose
# returns: the screen object (you want to draw to this) and the board object (may change)

# display to do:
    # make a screen dims independent of board dims
    # make shiftable, scalable board dims
def init_gui():
    pygame.init()
    # these are the constant screen dimensions
    screen_x = 800
    screen_y = 600
    # generate the screen, which is required before anything else, as
    # that dictates how transformations etc. are done.
    screen = pygame.display.set_mode((screen_x, screen_y))
    # now create the game elements -- the board, the piece, the cards, etc.
    board = BoardSprite(BOARD_OFFSET_DIMS, SCALED_BOARD_DIMS)
    piece = Piece()
    # those were easy, now cards we want to front-load loading all the images:
    VEC_CARD_IMGS = [load_image(IMG_PATH+"VectorDirecCardBack.png"),
                     load_image(IMG_PATH+"VectorDirecCardN.png"),
                     load_image(IMG_PATH+"VectorDirecCardNE.png"),
                     load_image(IMG_PATH+"VectorDirecCardE.png"),
                     load_image(IMG_PATH+"VectorDirecCardSE.png"),
                     load_image(IMG_PATH+"VectorDirecCardS.png"),
                     load_image(IMG_PATH+"VectorDirecCardSW.png"),
                     load_image(IMG_PATH+"VectorDirecCardW.png"),
                     load_image(IMG_PATH+"VectorDirecCardNW.png")]
    VectorCard.VEC_CARD_IMGS = VEC_CARD_IMGS
    # now, load and save (as a static list) the possible magnitude image files
    MAG_CARD_IMGS = [load_image(IMG_PATH+"VectorMagCardBack.png"),
                     load_image(IMG_PATH+"VectorMagCard0.png"),
                     load_image(IMG_PATH+"VectorMagCard1.png"),
                     load_image(IMG_PATH+"VectorMagCard2.png"),
                     load_image(IMG_PATH+"VectorMagCard3.png")]
    MagnitudeCard.MAG_CARD_IMGS = MAG_CARD_IMGS
    # ok, magnitude saved
    # now, load the hypothetical, yet-to-exist arrow image files
    ARROW_IMGS = [None, None]#[load_image(IMG_PATH+"SampleArrowBody.png", -1),
                  #load_image(IMG_PATH+"SampleArrowHead.png", -1)]
    Arrow.ARROW_IMGS = ARROW_IMGS
    # now, for each position on the table, make a pair of cards!
    north_cards = [VectorCard('n'), MagnitudeCard('n')]
    east_cards = [VectorCard('e'), MagnitudeCard('e')]
    south_cards = [VectorCard('s'), MagnitudeCard('s')]
    west_cards = [VectorCard('w'), MagnitudeCard('w')]
    return screen, board, piece, (north_cards, east_cards, south_cards, west_cards)

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
        self.image = pygame.transform.scale(self.start_image, (my_dims[0], my_dims[1]))
    def draw(self, screen):
        screen.blit(self.image, self.upper_left_corner)
    
######
# upper left of starting square: 527, 527
class Piece(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(IMG_PATH+"VectorPlayPiece.png", -1)
        # 527 is upper left of starting square, so we want to scale that and use as starting poitn
        self.loc = int(527*BOARD_AND_VECTOR_SCALING) + BOARD_OFFSET_DIMS[0], int(527*BOARD_AND_VECTOR_SCALING) + BOARD_OFFSET_DIMS[1]
        self.image = pygame.transform.scale(self.image, (int(44*BOARD_AND_VECTOR_SCALING), int(44*BOARD_AND_VECTOR_SCALING)))
        #the 44+2 is the space between two squares, basically, and then you scale it
        self.move_distance = (44+2)*BOARD_AND_VECTOR_SCALING
    def draw(self, screen):
        screen.blit(self.image, self.loc, self.rect)
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
        self.center()
        y, x = loc # this is where to move the piece
        if y < 10:
            self.move_piece(0, 10-y)
        elif y > 10:
            self.move_piece(2*2, y-10)
        if x < 10:
            self.move_piece(3*2, 10-x)
        elif x > 10:
            self.move_piece(1*2, x-10)
    def center(self):
        self.loc = (527*BOARD_AND_VECTOR_SCALING)+BOARD_OFFSET_DIMS[0], (527*BOARD_AND_VECTOR_SCALING)+BOARD_OFFSET_DIMS[1]
        

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
            shrunk_image = pygame.transform.scale(img, SCALED_CARD_DIMS)
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
            self.ulc = (BOARD_OFFSET_DIMS[0]+(SCALED_BOARD_DIMS[0]/2), 0)
        elif pos == 'e':
            self.ulc = (BOARD_OFFSET_DIMS[0]+SCALED_BOARD_DIMS[0], BOARD_OFFSET_DIMS[1]+(SCALED_BOARD_DIMS[1]/2))
        elif pos == 's':
            self.ulc = (BOARD_OFFSET_DIMS[0]+(SCALED_BOARD_DIMS[0]/2)-(SCALED_CARD_DIMS[0]), BOARD_OFFSET_DIMS[1]+SCALED_BOARD_DIMS[1])
        elif pos == 'w':
            self.ulc = (0, BOARD_OFFSET_DIMS[1]+(SCALED_BOARD_DIMS[1]/2)-SCALED_CARD_DIMS[0])
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
            self.ulc = (BOARD_OFFSET_DIMS[0]+(SCALED_BOARD_DIMS[0]/2)-SCALED_CARD_DIMS[0], 0)
        elif pos == 'e':
            self.ulc = (BOARD_OFFSET_DIMS[0]+SCALED_BOARD_DIMS[0], BOARD_OFFSET_DIMS[1]+(SCALED_BOARD_DIMS[1]/2)-SCALED_CARD_DIMS[0])
        elif pos == 's':
            self.ulc = (BOARD_OFFSET_DIMS[0]+(SCALED_BOARD_DIMS[0]/2), BOARD_OFFSET_DIMS[1]+SCALED_BOARD_DIMS[1])
        elif pos == 'w':
            self.ulc = (0, BOARD_OFFSET_DIMS[1]+(SCALED_BOARD_DIMS[1]/2))
    def make_my_images(self, pos):
        # see comment in VectorCard as to where the static field comes from
        return self.make_generic_images(pos, MagnitudeCard.MAG_CARD_IMGS)

class Arrow(pygame.sprite.Sprite):
    def __init__(self, color, direction, magnitude):
        pygame.sprite.Sprite.__init__(self)
    def set_position(self, startloc, dir, mag):
        roto_angle = (dir+1)*45 # literally, each cardinal direction is 45/360 of a circle
        draw_mag = PIECE.move_distance*magnitude # a bit hackish, whoops...
        if dir % 2 == 1: # n, s, e, and w are all even numbers. Thus, this is when you have an unkosher angle
            draw_mag *= 1.41 # lengthen extra by sqrt2, so it actually reaches the square
        # at this point, we have the length and the rotation of the arrow. 
        self.base_image = Arrow.ARROW_IMGS[0]
        self.stretched_base = pygame.transform.scale(self.base_image, (draw_mag, 50))
        self.combine_head_and_base = pygame.Surface((draw_mag+50, 50))
        self.combine_head_and_base = self.combine_head_and_base.blit(self.stretched_base, (0, 0))
        self.combine_head_and_base = self.combine_head_and_base.blit(Arrow.ARROW_IMGS[1], (draw_mag, 0))
        # at this point, combine_head_and_base should just need rotation and placement
        self.rotated = pygame.transform.rotate(self.combine_head_and_base, roto_angle)
        # ok, now simply blit it to the screen at the proper place. Thats the fun part.


def draw_arrow(team, dir, mag):
    # now do the complciated part:
    ulc_of_piece = PIECE.loc
    
# updates the piece
def update_piece(turn_info):
    # the above array comes in handy when a player misses his move
    for move_command in turn_info:
        who, dir, mag, loc = move_command
        print 'update_piece: ',move_command
        if who is -1:
            # you hit a wall, go to corner specified by loc (x, y)
            PIECE.translocate_piece(loc)
            #draw_corner_case(loc)
        else:
            # normal case, you move piece, flip card, draw arrow
            # move the piece
            PIECE.move_piece(dir, mag)
            # draw the arrow
            draw_arrow(who, dir, mag)

# this will handle the cards
# the cards are flipped regardless of what happens on the board
def update_cards(card_info):
    moved = [False, False, False, False] # tracks, which player got to move
    for card in card_info:
        who, dir, mag = card
        CARDLIST[who][0].flip(dir+1)
        CARDLIST[who][1].flip(mag+1)
        moved[who] = True
    for player in range(4):
        if moved[player] is False: # if this player did not get to move...
            CARDLIST[player][0].flip(0)
            CARDLIST[player][1].flip(0)

def reset_board():
    PIECE.center()
    for player in CARDLIST: # turn all the cards to their bacsk
        player[0].flip(0)
        player[1].flip(0)

def start_gui():
    global SCREEN
    global BOARD
    global PIECE
    global CARDLIST
    SCREEN, BOARD, PIECE, CARDLIST = init_gui()

def redraw_screen():
    SCREEN.fill((0, 0, 0))
    BOARD.draw(SCREEN)
    PIECE.draw(SCREEN)
    for team in CARDLIST:
        team[0].draw(SCREEN)
        team[1].draw(SCREEN)
    pygame.display.flip()

# debugging stuff, if you run this as a standalone app
if __name__=='__main__':
    start_gui()

def old_test():
    def parse_move_command(move_command, p):
        dir, mag = move_command.split()
        mag = int(mag)
        p.move_piece(dir, mag)
    screen, board, piece = init_gui(None)
    move_command = 'blah'
    while move_command != 'exit':
        screen.fill((0, 0, 0))
        board.draw(screen)
        piece.draw(screen)
        v.draw(screen)
        pygame.display.flip()
        move_command = raw_input("Next move: ")
        parse_move_command(move_command, piece)
