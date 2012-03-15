import pygame
from pygame.font import *
import sys, os
from pygame.locals import *

SCREEN_Y = 600
font_file = "freesansbold.ttf"

# just for testing, makes sure everything is hunky-dory
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
    pygame.display.set_caption('Sidebar Test')
    pygame.mouse.set_visible(1)
#init stuff
    sidebar = SideBar("north", "east", "south", "west")
    
    clock = pygame.time.Clock()    
    tmp_north_score = 0
    tmp_tourny = 0
#Main Loop
    while True:
        sidebar.update_score(tmp_north_score, 30, 30, 30)
        sidebar.update_tournament(tmp_tourny, 4, 2, 1)
        tmp_north_score += 1
        tmp_tourny += 1
        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                sys.exit(9)


class SideBar:
    def __init__(self):
        self.north_name = ''
        self.east_name = ''
        self.south_name = ''
        self.west_name = ''
        self.north_score = 0
        self.east_score = 0
        self.south_score = 0
        self.west_score = 0
        self.north_tourny = 0
        self.east_tourny = 0
        self.south_tourny = 0
        self.west_tourny = 0

    def update_names(self, north, east, south, west):
        self.north_name = north
        self.south_name = south
        self.east_name = east
        self.west_name = west
        self.update()

    def update_scores(self, s1, s2, s3, s4):
        self.north_score = s1
        self.east_score = s4
        self.south_score = s3
        self.west_score = s2
        self.update()

    def update_tournament(self, t1,t2,t3,t4):
        self.north_tourny = t1
        self.east_tourny = t2
        self.south_tourny = t3
        self.west_tourny = t4

    def update(self):
        #print "updating sidebar"
        if pygame.font:
            self.get_sidebar()
            font = pygame.font.Font(font_file, 24)
            self.north_score_label = font.render(str(self.north_score),1,(250,0,0))
            self.east_score_label = font.render(str(self.east_score),1,(0,250,0))
            self.south_score_label = font.render(str(self.south_score),1,(0,0,250))
            self.west_score_label = font.render(str(self.west_score),1,(250,250,0))
                
    def get_sidebar(self):
    #Create panel
        side_panel = pygame.Surface((200,SCREEN_Y))
        side_panel = side_panel.convert()
        side_panel.fill((100,100,100))

        side_panel_top = pygame.Surface((200,SCREEN_Y/2))
        side_panel_top = side_panel_top.convert()
        side_panel_top.fill((0,0,0))

        side_panel_bot = pygame.Surface((200,SCREEN_Y/2))
        side_panel_bot = side_panel_bot.convert()
        side_panel_bot.fill((50,50,50))

    #Create panels
        SCORE_panel = pygame.Surface((200,50))
        TOURNY_panel = pygame.Surface((200,50))
        north_panel = pygame.Surface((100,SCREEN_Y/4-20))
        east_panel = pygame.Surface((100,SCREEN_Y/4-20))
        south_panel = pygame.Surface((100,SCREEN_Y/4-20))
        west_panel = pygame.Surface((100,SCREEN_Y/4-20))
        north_panel2 = pygame.Surface((100,SCREEN_Y/4-20))
        east_panel2 = pygame.Surface((100,SCREEN_Y/4-20))
        south_panel2 = pygame.Surface((100,SCREEN_Y/4-20))
        west_panel2 = pygame.Surface((100,SCREEN_Y/4-20))

    #Add text
        if pygame.font:
            label = pygame.font.Font(font_file, 20) #36
            label.set_underline(1)
            font = pygame.font.Font(font_file, 20) #24
            SCORE_label = label.render("GAME SCORES:",1,(255,255,255))
            TOURNY_label = label.render("TOURNAMENT:",1,(255,255,255))
            north_score_label = font.render(str(self.north_score),1,(250,0,0))
            north_name_label = font.render(self.north_name,1,(250,0,0))
            east_score_label = font.render(str(self.east_score),1,(0,250,0))
            east_name_label = font.render(self.east_name,1,(0,250,0))
            south_score_label = font.render(str(self.south_score),1,(0,0,250))
            south_name_label = font.render(self.south_name,1,(0,0,250))
            west_score_label = font.render(str(self.west_score),1,(250,250,0))
            west_name_label = font.render(self.west_name,1,(250,250,0))
            
            north_tourny_label = font.render(str(self.north_tourny),1,(250,0,0))
            east_tourny_label = font.render(str(self.east_tourny),1,(0,250,0)) 
            south_tourny_label = font.render(str(self.south_tourny),1,(0,0,250))
            west_tourny_label = font.render(str(self.west_tourny),1,(250,250,0))
    #get rects
        SCOREPos = SCORE_label.get_rect(centerx=SCORE_panel.get_width()/2)
        TOURNYPos = TOURNY_label.get_rect(centerx=TOURNY_panel.get_width()/2)

        nslPos = north_score_label.get_rect(center=(north_panel.get_width()/2,north_panel.get_height()/2))
        nnlPos = north_name_label.get_rect(centerx=north_panel.get_width()/2)

        eslPos = east_score_label.get_rect(center=(east_panel.get_width()/2,east_panel.get_height()/2))
        enlPos = east_name_label.get_rect(centerx=east_panel.get_width()/2)
        
        sslPos = south_score_label.get_rect(center=(south_panel.get_width()/2,south_panel.get_height()/2))
        snlPos = south_name_label.get_rect(centerx=south_panel.get_width()/2)

        wslPos = west_score_label.get_rect(center=(west_panel.get_width()/2,west_panel.get_height()/2))
        wnlPos = west_name_label.get_rect(centerx=west_panel.get_width()/2)
    
    #add labels to respective panels on top
        north_panel.blit(north_score_label, nslPos)
        north_panel.blit(north_name_label, nnlPos)
        east_panel.blit(east_score_label, eslPos)
        east_panel.blit(east_name_label, enlPos)
        south_panel.blit(south_score_label, sslPos)
        south_panel.blit(south_name_label, snlPos)
        west_panel.blit(west_score_label, wslPos)
        west_panel.blit(west_name_label, wnlPos)
        SCORE_panel.blit(SCORE_label, SCOREPos)

    #sum scores
        # search here
        if pygame.font:
            font = pygame.font.Font(font_file, 24)
            NS_sum = font.render(str(self.north_score + self.south_score),1,(255,255,255))
            EW_sum = font.render(str(self.east_score + self.west_score),1,(255,255,255))

        NS_panel = pygame.Surface((50, 50))
    #NS_pos = NS_sum.get_rect(center=(NS_panel.get_width()/2,NS_panel.get_height()/2))
        NS_pos = NS_sum.get_rect()
        NS_panel.blit(NS_sum, NS_pos)

        EW_panel = pygame.Surface((50,50))
    #EW_pos = EW_sum.get_rect(center=(EW_panel.get_width()/2,EW_panel.get_height()/2)
        EW_pos = EW_sum.get_rect()
        EW_panel.blit(EW_sum, EW_pos)


    #add panels to top half of sidebar
        side_panel_top.blit(SCORE_panel, (0,0))
        side_panel_top.blit(north_panel,(0,50))
        side_panel_top.blit(south_panel, (100,50))
        side_panel_top.blit(east_panel,(0,SCREEN_Y/8+100))
        side_panel_top.blit(west_panel,(100,SCREEN_Y/8+100))


    #add stuff to bottom correspondents
        TOURNY_panel.blit(TOURNY_label, TOURNYPos)
        north_panel2.blit(north_tourny_label, nslPos)
        north_panel2.blit(north_name_label, nnlPos)
        east_panel2.blit(east_tourny_label, eslPos)
        east_panel2.blit(east_name_label, enlPos)
        south_panel2.blit(south_tourny_label, sslPos)
        south_panel2.blit(south_name_label, snlPos)
        west_panel2.blit(west_tourny_label, wslPos)
        west_panel2.blit(west_name_label, wnlPos)
        

    #add bottom parts to bottom half of sidebar
        side_panel_bot.blit(TOURNY_panel, (0,0))
        side_panel_bot.blit(north_panel2,(0,50))
        side_panel_bot.blit(south_panel2, (100,50))
        side_panel_bot.blit(east_panel2,(0,SCREEN_Y/8+100))
        side_panel_bot.blit(west_panel2,(100,SCREEN_Y/8+100))


        side_panel_top.blit(NS_panel, (side_panel_top.get_width()/2-10, SCREEN_Y/8))
        side_panel_top.blit(EW_panel, (side_panel_top.get_width()/2-10, SCREEN_Y/3))
   
        
        side_panel.blit(side_panel_top, (0,0))
        side_panel.blit(side_panel_bot, (0,SCREEN_Y/2))
        
        return side_panel


if __name__ == '__main__': main()
