import pygame
from pygame.locals import *

# this is an actual board class, to provide method wrappers etc.
# for now, the board is basically just a matrix, but for drawing, updating,
# and modifying(?) during the game, it will be handy. Such as making a
# yellow effect square "disabled" for turn 1.
# Might be handy making board inherit from some spritegroup?

class Board:
    # given a name of a file that contains a board (the board) description,
    # read that file and turn it into a board.
    def __init__(self, file_name):
        string_board = self.make_string_board(file_name)
        classified_board = self.make_classified_board(string_board)
        self.board = classified_board
    def print_board(self):
        for row in self.board:
            for square in row:
                square.print_ascii()
            print '' # newline
    def print_square_details(self, loc):
        row, col = loc
        self.board[row][col].print_details()
    def make_string_board(self, file_name):
        board_file = open(file_name)
        row_counter = 0
        col_counter = 0
        board = [[]]
        for line in board_file:
            if line.split()[0] == "#": # it is a comment, forget it.
                pass
            else:
                if col_counter == 21:
                    col_counter = 0
                    board.append([])
                    row_counter += 1
                board[row_counter].append(line.strip()) # removes excess whitespace, just in case.
                col_counter += 1
        return board
    def make_classified_board(self, board):
        for row_index in range(0, len(board)):
            for col_index in range(0, len(board[row_index])):
                info = board[row_index][col_index]
                board[row_index][col_index] = Square(info)
        return board

# this is a simple  struct that, given a string descriptor of a square,
# transforms it into sanely-named fields.
# use square.name to identify what type of square this is, and such which
# fields to access, when you're actually looking at the board for playing the game.
#
# implementation is welcome to change -- everything is strings because yay, but
# easily can be shifted to say, enums if desired.
#
class Square:
    def __init__(self, info):
        facts = info.split()
        self.name = facts[0]
        if self.name == 'BLANK':
            return # that's all we need.
        elif self.name == 'POINTS':
            self.color = facts[1]
            self.teamlist = facts[2:len(facts)-1]
            self.value = int(facts[len(facts)-1])
        elif self.name == 'MOVE':
            self.dir = facts[1]
            self.magnitude = int(facts[2])
        elif self.name == 'NOTURN':
            self.team = facts[1]
        else:
            print 'ERROR'
    def print_ascii(self):
        if self.name == 'BLANK':
            print '[B]',
        elif self.name == 'POINTS':
            print '[P]',
        elif self.name == 'MOVE':
            print '[M]',
        elif self.name == 'NOTURN':
            print '[N]',
    def print_details(self):
        print self.name,
        if self.name == 'POINTS':
            print self.color, self.teamlist, self.value
        elif self.name == 'MOVE':
            print self.dir, self.magnitude
        elif self.name == 'NOTURN':
            print self.team

# these may come in handy, so I'm holding on to them.
team_list = ['NORTH', 'EAST', 'SOUTH', 'WEST', 'ALL']
dir_list = ['NORTH', 'NORTHEAST', 'EAST', 'SOUTHEAST', 'SOUTH', 'SOUTHWEST', 'WEST', 'NORTHWEST']

#b = Board('NEW_BOARD') # yes, it is silly to always pass a file name, but i think it is best.

# example -- it first prints out the whole board, and then the middle square.
# (0-20, 10 is middle value)
#b.print_board()
#b.print_square_details((10, 10))
