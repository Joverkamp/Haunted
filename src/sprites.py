import pygame as pg
from settings import *

class Wall(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = "wall"
        self.color = GREY
        self.image = pg.Surface([TILESIZE,TILESIZE])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
#########################################
class Floor(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = "floor"
        self.color = BROWN
        self.image = pg.Surface([TILESIZE,TILESIZE])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
            
#########################################
class Powerup(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = "powerup"
        self.image = game.imgBattery
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
#########################################
class Key(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = "key"
        self.image = game.imgKey
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
#########################################
class Door(pg.sprite.Sprite):
    def __init__(self,game,orientation, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = "door"
        if orientation == "vert":
            self.image = pg.Surface([TILESIZE,TILESIZE*2])
        else:
            self.image = pg.Surface([TILESIZE*2,TILESIZE])
        self.color = LBROWN
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#########################################
class Coin(pg.sprite.Sprite):
    def __init__(self,game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = "coin"
        self.image = game.imgGem
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
#########################################
class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = "player"
        self.image = game.imgPlayer
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = 0
        self.y = 0
        self.xVelocity = 0
        self.yVelocity = 0
        self.lightVal = 150#150
        self.speed = 1
        self.sprintVal = 50
        self.sprintActive = False
        self.gotKey = False
        self.useKey = False
        self.money = 0
        self.totalScore = 0
        self.goalScore = 500*((self.game.currMap+1)*2)
        self.trap = self.Trap(self)
        self.torch = self.Torch(self)
        
    def reset(self):
        self.money = 0
        self.gotKey = False
        self.sprintVal = 50
        self.lightVal = 150
        self.goalScore = 500*((self.game.currMap+1)*2)
        
        self.torch.active = False
        self.torch.charge = 30
        self.torch.lightVal = 175
        self.trap.active = False
        self.trap.charge = 30
        
    def check_sprint(self):
        if self.sprintVal > 0 and self.sprintActive == True:
            self.sprintVal -= 1
    
    def check_collision_ghost(self):   
        hits = pg.sprite.spritecollide(self, self.game.ghosts, False)
        if hits:
            self.game.game_over()
            
    def check_collision_powerup(self):   
        hits = pg.sprite.spritecollide(self, self.game.powerups, False)
        if hits:
            if self.lightVal < 165:
                self.lightVal += 25
                if self.lightVal > 165:
                    self.lightVal = 165
            self.game.powerups.remove(self.game.powerup)
            self.game.allSprites.remove(self.game.powerup)
            self.game.powerupActive = False
            
    def check_collision_key(self):   
        hits = pg.sprite.spritecollide(self, self.game.keys, False)
        if hits:
            self.gotKey = True
            self.game.keys.remove(self.game.key)
            self.game.allSprites.remove(self.game.key)
            self.game.keyActive = False
            
    def check_collision_coin(self):   
        hits = pg.sprite.spritecollide(self, self.game.coins, False)
        if hits:
            self.money += 100*((self.game.currMap+1)*2)
            self.totalScore += 100*((self.game.currMap+1)*2)
            self.game.coins.remove(self.game.coin)
            self.game.allSprites.remove(self.game.coin)
            self.game.coinActive = False
        
    def check_collision_walls(self):
        self.rect.x = self.x
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            if hits[0].type == "door" and self.useKey == True:
                self.gotKey = False
                self.game.walls.remove(self.game.door)
                self.game.allSprites.remove(self.game.door)
                self.game.keyActive == False
                self.game.doorActive = False
            else:
                if self.xVelocity > 0:
                    self.x = hits[0].rect.left - self.rect.width
                elif self.xVelocity < 0:
                    self.x = hits[0].rect.right
                self.rect.x = self.x
        self.xVelocity = 0 
                
        self.rect.y = self.y
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            if hits[0].type == "door"and self.useKey == True:
                self.gotKey = False
                self.game.walls.remove(self.game.door)
                self.game.allSprites.remove(self.game.door)
                self.game.keyActive == False
                self.game.doorActive = False
            else:
                if self.yVelocity > 0:
                    self.y = hits[0].rect.top - self.rect.height
                elif self.yVelocity < 0:
                    self.y = hits[0].rect.bottom
                self.rect.y = self.y
        self.yVelocity = 0  
    #########################################
    class Trap(pg.sprite.Sprite):
        def __init__(self,parent):
            pg.sprite.Sprite.__init__(self)
            self.parent = parent
            self.type = "torch"
            self.image = self.parent.game.imgTrap
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = 0
            self.charge = 30
            self.active = False
            
    #########################################
    class Torch(pg.sprite.Sprite):
        def __init__(self,parent):
            pg.sprite.Sprite.__init__(self)
            self.parent = parent
            self.type = "torch"
            self.image = self.parent.game.imgTorch
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = 0
            self.lightVal = 175
            self.charge = 30
            self.active = False
#########################################
class Ghost(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = "ghost"
        self.image = pg.Surface([TILESIZE,TILESIZE])
        self.color = WHITE
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x  = x
        self.rect.y = y
        self.speed = 1

        
    def move_ghost(self):
        if self.game.player.trap.active == True:
            if self.rect.x < self.game.player.trap.rect.x:
                self.rect.x +=1
            if self.rect.x > self.game.player.trap.rect.x:
                self.rect.x -=1
            if self.rect.y < self.game.player.trap.rect.y:
                self.rect.y +=1
            if self.rect.y > self.game.player.trap.rect.y:
                self.rect.y -=1
        else:
            
            
            if self.rect.x < self.game.player.rect.x:
                self.rect.x +=self.speed
            if self.rect.x > self.game.player.rect.x:
                self.rect.x -=self.speed
            if self.rect.y < self.game.player.rect.y:
                self.rect.y +=self.speed
            if self.rect.y > self.game.player.rect.y:
                self.rect.y -=self.speed

