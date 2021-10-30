import pygame as pg
from settings import *


class Hud():
    def __init__(self,game):
        #draw stamina bars
        self.game = game
        
    def update_hud(self):
        #draw hud background
        pg.draw.rect(self.game.screen, BLUE, (0, SCREENHEIGHT-98,SCREENWIDTH,97))
        pg.draw.rect(self.game.screen, YELLOW, (0, SCREENHEIGHT-98,SCREENWIDTH,97),5)
        #background for stamina icon
        pg.draw.rect(self.game.screen, GREY, (5, SCREENHEIGHT-64,148,60))
        pg.draw.rect(self.game.screen, BLACK, (5, SCREENHEIGHT-64,148,58),5)
        #background for inventory slot key
        pg.draw.rect(self.game.screen, GREY, (200, SCREENHEIGHT-90,30,30))
        pg.draw.rect(self.game.screen, BLACK, (200, SCREENHEIGHT-90,30,30),5)
        #background for inventory slot trap
        pg.draw.rect(self.game.screen, GREY, (270, SCREENHEIGHT-90,30,30))
        pg.draw.rect(self.game.screen, BLACK, (270, SCREENHEIGHT-90,30,30),5)
        #background for inventory slot torch
        pg.draw.rect(self.game.screen, GREY, (340, SCREENHEIGHT-90,30,30))
        pg.draw.rect(self.game.screen, BLACK, (340, SCREENHEIGHT-90,30,30),5)
        #background for battery icon
        pg.draw.rect(self.game.screen, GREY, (SCREENWIDTH-154, SCREENHEIGHT-64,148,60))
        pg.draw.rect(self.game.screen, BLACK, (SCREENWIDTH-154, SCREENHEIGHT-64,148,58),5)
        #dtext hud labels
        font = pg.font.Font(None, 40)
        text = font.render("S t a m i n a", True, WHITE)
        self.game.screen.blit(text, [5,SCREENHEIGHT-94])
        text = font.render("B a t t e r y", True, WHITE)
        self.game.screen.blit(text, [SCREENWIDTH-155,SCREENHEIGHT-94])
        
        text = font.render("Money: %d" % self.game.player.money, True, WHITE)
        self.game.screen.blit(text, [220,SCREENHEIGHT-33])
        #level number
        font = pg.font.Font(None, 30)
        text = font.render("Level %d" % int(self.game.currMap+1), True, WHITE)
        self.game.screen.blit(text, [530,0])
        #total score
        text = font.render("Money For Next Level [w]: %d" % int(self.game.player.goalScore), True, WHITE)
        self.game.screen.blit(text, [170,0])
        #goal score
        text = font.render("Score %d" % int(self.game.player.totalScore), True, WHITE)
        self.game.screen.blit(text, [0,0])
        #draw meters
        self.update_stamina_hud()
        self.update_battery_hud()
        self.update_inventory_hud()
        
        
    def update_stamina_hud(self):
        #draw the number of stamina bars relative to sprintVal
        if self.game.player.sprintVal >= 10:
            pg.draw.rect(self.game.screen, GREEN, (10, SCREENHEIGHT-60,20,50))
        if self.game.player.sprintVal >= 20:
            pg.draw.rect(self.game.screen, GREEN, (40, SCREENHEIGHT-60,20,50))
        if self.game.player.sprintVal >= 30:
            pg.draw.rect(self.game.screen, GREEN, (70, SCREENHEIGHT-60,20,50))
        if self.game.player.sprintVal >= 40:
            pg.draw.rect(self.game.screen, GREEN, (100, SCREENHEIGHT-60,20,50))
        if self.game.player.sprintVal == 50:
            pg.draw.rect(self.game.screen, GREEN, (130, SCREENHEIGHT-60,20,50)) 
        
    def update_battery_hud(self):
        #find what color to display battery based on lightVal
        if self.game.player.lightVal >= 75:
            batteryColor = RED
        if self.game.player.lightVal >= 90:
            batteryColor = ORANGE
        if self.game.player.lightVal >= 105:
            batteryColor = YELLOW
        if self.game.player.lightVal >= 120:
            batteryColor = GREEN
        if self.game.player.lightVal > 150:
            batteryColor = LBLUE
        #draw the number of battery bars relative to lightVal
        if self.game.player.lightVal >= 75:
            pg.draw.rect(self.game.screen, batteryColor, (SCREENWIDTH-150, SCREENHEIGHT-60,20,50))
        if self.game.player.lightVal >= 90:
            pg.draw.rect(self.game.screen, batteryColor, (SCREENWIDTH-120, SCREENHEIGHT-60,20,50))
        if self.game.player.lightVal >= 105:
            pg.draw.rect(self.game.screen, batteryColor, (SCREENWIDTH-90, SCREENHEIGHT-60,20,50))
        if self.game.player.lightVal >= 120:
            pg.draw.rect(self.game.screen, batteryColor, (SCREENWIDTH-60, SCREENHEIGHT-60,20,50))
        if self.game.player.lightVal >= 135:
            pg.draw.rect(self.game.screen, batteryColor, (SCREENWIDTH-30, SCREENHEIGHT-60,20,50)) 
        
    def update_inventory_hud(self):
        font = pg.font.Font(None, 40)
        #icons
        #torch icon
        self.game.screen.blit(self.game.imgTorch,(350, SCREENHEIGHT-85))
        text = font.render("d", True, WHITE)
        self.game.screen.blit(text, [348,SCREENHEIGHT-60])
        #trap icon
        self.game.screen.blit(self.game.imgTrap,(278, SCREENHEIGHT-85))
        text = font.render("s", True, WHITE)
        self.game.screen.blit(text, [278,SCREENHEIGHT-60])
        #key icon
        if self.game.player.gotKey == True:
            self.game.screen.blit(self.game.imgKey,(210, SCREENHEIGHT-85))
        text = font.render("a", True, WHITE)
        self.game.screen.blit(text, [208,SCREENHEIGHT-60])
        #trap charge icon
        if self.game.player.trap.charge == 30:
            pg.draw.rect(self.game.screen, GREEN, (310, SCREENHEIGHT-90,3,30))
        elif self.game.player.trap.active == True:
            pg.draw.rect(self.game.screen, YELLOW, (310, SCREENHEIGHT-90,3,self.game.player.trap.charge))
        else:
            pg.draw.rect(self.game.screen, RED, (310, SCREENHEIGHT-90,3,self.game.player.trap.charge))
        #torch charge icon
        if self.game.player.torch.charge == 30:
            pg.draw.rect(self.game.screen, GREEN, (380, SCREENHEIGHT-90,3,30))
        elif self.game.player.torch.active == True:
            pg.draw.rect(self.game.screen, YELLOW, (380, SCREENHEIGHT-90,3,self.game.player.torch.charge))
        else:
            pg.draw.rect(self.game.screen, RED, (380, SCREENHEIGHT-90,3,self.game.player.torch.charge))


