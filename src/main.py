import pygame as pg
import sys
import math
from pygame.locals import *
import random
import os
from sprites import *
from settings import *
from hud import *
from maps import *

#Intitialize pygame
class Game():
    def __init__(self):
        #position of the screen and pyame initialization
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" %(50,50)
        pg.init()
        pg.display.set_caption("Haunt")
        self.screen = pg.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
        self.clock = pg.time.Clock()
        #load all images and other game data objects
        self.load_data()
        self.currMap = 0
        self.player = Player(self)
        self.create_sprites(self.maps[0])
        self.hud = Hud(self)
        #define events
        self.decrease_light_event = pg.USEREVENT+1
        pg.time.set_timer(self.decrease_light_event, 5000)
    
        self.spawn_items_event = pg.USEREVENT+2
        pg.time.set_timer(self.spawn_items_event, 5000)
        
        self.move_ghost_event = pg.USEREVENT+3
        pg.time.set_timer(self.move_ghost_event, 50)
          
        self.increase_sprint_event = pg.USEREVENT+4
        pg.time.set_timer(self.increase_sprint_event, 1500)
        
        self.change_itemCharge_event = pg.USEREVENT+5
        pg.time.set_timer(self.change_itemCharge_event, 1000) 
#############################
    def load_data(self):
        #define our home and sub directories
        gameFolder = os.path.dirname(__file__)
        imageFolder = os.path.join(gameFolder, 'images')
        soundFolder = os.path.join(gameFolder, 'sounds')
        #load any images we want to use
        self.imgBattery = pg.image.load(os.path.join(imageFolder, 'battery.png'))
        self.imgPlayer = pg.image.load(os.path.join(imageFolder, 'player.png'))
        self.imgKey = pg.image.load(os.path.join(imageFolder, 'key.png'))
        self.imgGem = pg.image.load(os.path.join(imageFolder, 'gem.png'))
        self.imgTorch = pg.image.load(os.path.join(imageFolder, 'torch.png'))
        self.imgTrap = pg.image.load(os.path.join(imageFolder, 'trap.png'))
        #load any sounds we want to use

        #load all of the maps
        self.maps = []
        self.maps.append(MAP1)
        self.maps.append(MAP2)
        self.maps.append(MAP3)

        
#############################
    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            #check user input and events
            self.check_events()
            self.check_keys()
            #check player collisions
            self.player.check_collision_walls()
            self.player.check_collision_powerup()
            self.player.check_collision_key()
            self.player.check_collision_coin()
            self.player.check_collision_ghost()
            #update screen
            self.update_screen()
#############################
    def update_screen(self):
        self.allSprites.update()
        #create a black screen
        self.screen.fill(BLACK)
        #see what needs to be draw to screen
        self.player_vision()
        #draw whats visible
        self.visibleFloors.draw(self.screen)
        self.visibleSprites.draw(self.screen)
        #update and draw hud
        self.hud.update_hud()
        #frame rate
        self.clock.tick(60)
        pg.display.flip()
#############################  
    def check_keys(self):
        #get all pressed keys
        keys = pg.key.get_pressed()
        #make sure use key does not get left active
        self.player.useKey = False
        #disable sprint and check if available
        if self.player.sprintVal == 0:
            self.player.sprintAvailable = False
        self.player.sprintActive = False
        #set player speed to 1 before checking for sprint
        self.player.speed = 1
        #check important keys
        if keys[K_SPACE]:
            if self.player.sprintVal > 0:
                self.player.sprintActive = True
                self.player.speed = 2
        if keys[K_LEFT] and self.player.rect.x > 20:
            self.player.xVelocity = -1 *self.player.speed
            self.player.x += self.player.xVelocity
            self.player.check_sprint()
        if keys[K_RIGHT] and self.player.rect.x < 560:
            self.player.xVelocity = 1 *self.player.speed
            self.player.x += self.player.xVelocity
            self.player.check_sprint()
        if keys[K_UP] and self.player.rect.y > 20:
            self.player.yVelocity = -1*self.player.speed
            self.player.y += self.player.yVelocity
            self.player.check_sprint()
        if keys[K_DOWN] and self.player.rect.y < 460:
            self.player.yVelocity = 1*self.player.speed
            self.player.y += self.player.yVelocity
            self.player.check_sprint()
        if keys[K_a]:
            if self.player.gotKey == True:
                self.player.useKey = True
        if keys[K_s]:
            if self.player.trap.active == False and self.player.trap.charge == 30:
                self.player.trap.rect.x = self.player.rect.x
                self.player.trap.rect.y = self.player.rect.y
                self.player.trap.active = True
                self.allSprites.add(self.player.trap)
        if keys[K_d]:
            if self.player.torch.active == False and self.player.torch.charge == 30:
                self.player.torch.rect.x = self.player.rect.x+5
                self.player.torch.rect.y = self.player.rect.y
                self.player.torch.active = True
                self.allSprites.add(self.player.torch)
        if keys[K_w]:
            if self.currMap < len(self.maps)-1 and self.player.money >= self.player.goalScore:
                self.player.totalScore += 500*(self.currMap+1)
                self.currMap+=1
                self.player.reset()
                self.create_sprites(self.maps[self.currMap])
     

     
############################# 
    def check_events(self): 
        # catch all events here
        for event in pg.event.get():
            #decrease lightVal (radius of vision) by 5
            if event.type == self.decrease_light_event:
                if self.player.lightVal > 75:
                    self.player.lightVal -= 5
            #move ghost 1 pixel closer to player
            if event.type == self.move_ghost_event:
                #increase ghost speed when in vision    
                if self.get_distance(self.ghost) < 100:
                    self.ghost.speed = 2
                else:
                    self.ghost.speed = 1
                self.ghost.move_ghost()
            # increase sprint if not full and not sprinting
            if event.type == self.increase_sprint_event:
                if self.player.sprintActive == False:
                    if self.player.sprintVal < 50:
                        self.player.sprintVal += 10
                        if self.player.sprintVal > 50:
                            self.player.sprintVal = 50
            #increase the charges of items if inactive
            if event.type == self.change_itemCharge_event:
                #trap charge
                if self.player.trap.active == True:
                    if self.player.trap.charge > 0:
                        self.player.trap.charge -= 5
                        if self.player.trap.charge == 0:
                            self.allSprites.remove(self.player.trap)
                            self.player.trap.active = False
                else:
                    if self.player.trap.charge < 30:
                        self.player.trap.charge += 1.5
                #torch charge
                if self.player.torch.active == True:
                    if self.player.torch.charge > 0:
                        self.player.torch.charge -= 1
                        self.player.torch.lightVal -= 5
                        if self.player.torch.charge == 0:
                            self.allSprites.remove(self.player.torch)
                            self.player.torch.active = False
                            self.player.torch.lightVal = 175
                else:
                    if self.player.torch.charge < 30:
                        self.player.torch.charge += 3
            #spawning items
            if event.type == self.spawn_items_event:
                if self.coinActive == False:
                    self.spawn_coin()
                    self.coinActive = True
                if self.keyActive == False and self.player.gotKey == False:
                    self.spawn_key()
                    self.keyActive = True
                if self.powerupActive == False:
                    self.spawn_powerup()
                    self.powerupActive = True
                if self.doorActive == False:
                    self.spawn_door()
                    self.doorActive = True
            #exiting game
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
#############################                        
    def quit(self):
        pg.quit()
        sys.exit()
#############################        
    def spawn_powerup(self):
        while True:
            r = random.randint(0,len(self.powerupCoordsList)-1)
            powerupCoords = self.powerupCoordsList[r]
            x = powerupCoords[0]
            y = powerupCoords[1]
            self.powerup = (Powerup(self,x,y))
            if self.get_distance(self.powerup) > 100:
                break
        self.allSprites.add(self.powerup)
        self.powerups.add(self.powerup)
        self.powerupActive = True
#############################        
    def spawn_key(self):
        while True:
            r = random.randint(0,len(self.keyCoordsList)-1)
            keyCoords = self.keyCoordsList[r]
            x = keyCoords[0]
            y = keyCoords[1]
            self.key = (Key(self,x,y))
            if self.get_distance(self.key) > 100:
                break
        self.allSprites.add(self.key)
        self.keys.add(self.key)
        self.keyActive = True
#############################
    def spawn_door(self):
        while True:
            r = random.randint(0,len(self.doorCoordsList)-1)
            doorCoords = self.doorCoordsList[r]
            orientation = doorCoords[0]
            x = doorCoords[1]
            y = doorCoords[2]
            self.door = (Door(self,orientation,x,y))
            if self.get_distance(self.door) > 100:
                break
        self.allSprites.add(self.door)
        self.walls.add(self.door)
        self.doorActive = True
#############################        
    def spawn_coin(self):
        while True:
            r = random.randint(0,len(self.coinCoordsList)-1)
            coinCoords = self.coinCoordsList[r]
            x = coinCoords[0]
            y = coinCoords[1]
            self.coin = (Coin(self,x,y))
            if self.get_distance(self.coin) > 100:
                break
        self.allSprites.add(self.coin)
        self.coins.add(self.coin)
        self.coinActive = True
#############################
    #gets distance between player and passed object
    def get_distance(self,object):
        x1 = self.player.rect.x
        y1 = self.player.rect.y
        x2 = object.rect.x
        y2 = object.rect.y
        xs = (x1 - x2)**2
        ys = (y1 - y2)**2
        distance = math.sqrt(abs(xs + ys))
        return distance
#############################
    def player_vision(self):
        #clear all visible sprites
        self.visibleFloors.empty()
        self.visibleSprites.empty()
        
        #find the vision bubble of torch
        self.torch_vision()
        
        #get the coords of the player
        x1 = self.player.rect.x
        y1 = self.player.rect.y
        #find all sprites with the radius of the players lightval
        for currSprite in self.allSprites:
            x2 = currSprite.rect.x
            y2 = currSprite.rect.y
            xs = (x1 - x2)**2
            ys = (y1 - y2)**2
            distance = math.sqrt(abs(xs + ys))
            if distance < self.player.lightVal:
                #floors have to be rendered first so we keep them seperate
                if currSprite.type == "floor":
                    self.visibleFloors.add(currSprite)
                else:
                    self.visibleSprites.add(currSprite)
                #change the color of the sprite based on the distance
                try:
                    #greatly darken the color value of the sprite if it is on the border of player vision
                    if self.player.lightVal - distance < 20:
                        if currSprite.color == WHITE:
                            currSprite.image.fill((currSprite.color[0]-150,currSprite.color[1]-150,currSprite.color[2]-150))
                        else:
                            currSprite.image.fill((currSprite.color[0]-40,currSprite.color[1]-40,currSprite.color[2]-40))
                    #slightly darken the color value of the sprite if it just inside the border of player vision
                    elif self.player.lightVal - distance < 40:
                        if currSprite.color == WHITE:
                            currSprite.image.fill((currSprite.color[0]-70,currSprite.color[1]-70,currSprite.color[2]-70))
                        else:
                            currSprite.image.fill((currSprite.color[0]-20,currSprite.color[1]-20,currSprite.color[2]-20))
                    #if the sprite is inside player vision but not on the border revert the sprite to its original color 
                    else:
                        currSprite.image.fill(currSprite.color)
                except:
                    pass
#############################
    def torch_vision(self):
        if self.player.torch.active == True:
            #get the coords of the torch
            x1 = self.player.torch.rect.x
            y1 = self.player.torch.rect.y
            #find all sprites with the radius of the torchs lightval
            for currSprite in self.allSprites:
                x2 = currSprite.rect.x
                y2 = currSprite.rect.y
                xs = (x1 - x2)**2
                ys = (y1 - y2)**2
                distance = math.sqrt(abs(xs + ys))
                if distance < self.player.torch.lightVal:
                    #floors have to be rendered first so we keep them seperate
                    if currSprite.type == "floor":
                        self.visibleFloors.add(currSprite)
                    else:
                        self.visibleSprites.add(currSprite)
                    #change the color of the sprite based on the distance
                    try:
                    #greatly darken the color value of the sprite if it is on the border of torchvision
                        if self.player.torch.lightVal - distance < 20:
                            if currSprite.color == WHITE:
                                currSprite.image.fill((currSprite.color[0]-150,currSprite.color[1]-150,currSprite.color[2]-150))
                            else:
                                currSprite.image.fill((currSprite.color[0]-40,currSprite.color[1]-40,currSprite.color[2]-40))
                        #slightly darken the color value of the sprite if it just inside the border of player vision
                        elif self.player.torch.lightVal - distance < 40:
                            if currSprite.color == WHITE:
                                currSprite.image.fill((currSprite.color[0]-70,currSprite.color[1]-70,currSprite.color[2]-70))
                            else:
                                currSprite.image.fill((currSprite.color[0]-20,currSprite.color[1]-20,currSprite.color[2]-20))
                        #if the sprite is inside player vision but not on the border revert the sprite to its original color 
                        else:
                            currSprite.image.fill(currSprite.color)
                    except:
                        pass
#############################
    def create_sprites(self,map):
        #sprite groups for sprites
        self.allSprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.floors = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.keys = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.ghosts = pg.sprite.Group()
        #sprite groups for visible sprites
        self.visibleSprites = pg.sprite.Group()
        self.visibleFloors = pg.sprite.Group()

        #lists for spawn location for sprites
        self.powerupCoordsList = []
        self.powerupActive = False
        
        self.keyCoordsList = []
        self.keyActive = False
        
        self.doorCoordsList = []
        self.doorActive = False
        
        self.coinCoordsList = []
        self.coinActive = False
        
        #spawn ghost in random corner
        rx = random.randint(0,1)*550
        ry = random.randint(0,1)*550
        self.ghost = Ghost(self,rx,ry)
        self.ghosts.add(self.ghost)
        self.allSprites.add(self.ghost)
        
        
        self.grid = map
        #Give sprites their coors based in there place in the grid above
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.allSprites.add(Floor(self,j*TILESIZE,i*TILESIZE))
                self.floors.add(Floor(self,j*TILESIZE,i*TILESIZE))
                if self.grid[i][j] == 1: 
                    self.allSprites.add(Wall(self,j*TILESIZE,i*TILESIZE))
                    self.walls.add(Wall(self,j*TILESIZE,i*TILESIZE))
                elif self.grid[i][j] == 2:
                    self.player.x = j*TILESIZE
                    self.player.rect.x = j*TILESIZE
                    self.player.y = i*TILESIZE
                    self.player.rect.y = i*TILESIZE
                    self.allSprites.add(self.player)
                elif self.grid[i][j] == 3:
                    self.powerupCoordsList.append([j*TILESIZE+15,i*TILESIZE+10])
                elif self.grid[i][j] == 4:
                    self.doorCoordsList.append(["vert",j*TILESIZE,i*TILESIZE])
                elif self.grid[i][j] == 5:
                    self.doorCoordsList.append(["horiz",j*TILESIZE,i*TILESIZE])
                elif self.grid[i][j] == 6:
                    self.keyCoordsList.append([j*TILESIZE+15,i*TILESIZE+10])
                elif self.grid[i][j] == 7:
                    self.coinCoordsList.append([j*TILESIZE+15,i*TILESIZE+10])
#############################
    def game_over(self):
        #display game over and pause berfore ending
        font = pg.font.Font(None, 100)
        text = font.render("GAME OVER", True, RED)
        self.screen.blit(text, [80, 250])
        
        pg.display.flip()
        self.clock.tick(1/5)
        pg.quit()
# create the game object
g = Game()
while True:
    g.run()