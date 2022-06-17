# 1 - Import library
import pygame
from pygame.locals import *
import math
from random import randint
import sys

class Game():
    def __init__(self):
        # 2 - Initialize the game
        pygame.init()
        pygame.display.set_caption('South China Sea - By Delower')
        icon = pygame.image.load('resources/images/d.png')
        pygame.display.set_icon(icon)
        self.width, self.height = 640, 480
        self.screen=pygame.display.set_mode((self.width, self.height))
        self.keys = [False, False, False, False]
        self.playerpos=[135,65]
        self.acc=[0,0]
        self.flames=[]
        self.rocket_timer=100
        self.rocket_timer1=0
        self.rockets=[[640,100]]
        self.health_value=194
        pygame.mixer.init()
        # load assets
        self.load_assets()

    def load_assets(self):
        # 3 - Load images
        self.dragon1 = pygame.image.load("resources/images/dragon.png")
        self.dragon2 = pygame.image.load("resources/images/dragon1.png")
        self.player = [self.dragon1,self.dragon2] 
        self.south_china_sea = pygame.image.load("resources/images/south_china_sea.png")
        self.castle = pygame.image.load("resources/images/castle.png")
        self.ship1 = pygame.image.load("resources/images/ship.png")
        self.ship2 = pygame.image.load("resources/images/ship2.png")
        self.flame_img = pygame.image.load("resources/images/flame.png")
        self.rocket_img1 = pygame.image.load("resources/images/rocket.png")
        self.rocket_img2 = pygame.image.load("resources/images/rocket2.png")
        self.rocket_img3 = pygame.image.load("resources/images/rocket3.png")
        self.rocket_img4 = pygame.image.load("resources/images/rocket4.png")
        self.rocket_img5 = pygame.image.load("resources/images/rocket5.png")
        self.rocket_img6 = pygame.image.load("resources/images/rocket6.png")
        self.rocket_img7 = pygame.image.load("resources/images/rocket7.png")
        self.rocket_images=[self.rocket_img1,self.rocket_img2,self.rocket_img3,self.rocket_img4,self.rocket_img5,self.rocket_img6,self.rocket_img7]
        self.rocket_img = self.rocket_images[randint(0,4)]
        self.healthbar = pygame.image.load("resources/images/healthbar.png")
        self.health = pygame.image.load("resources/images/health.png")
        self.gameover = pygame.image.load("resources/images/gameover.png")
        self.youwon = pygame.image.load("resources/images/youwon.png")
        self.bang_img = pygame.image.load("resources/images/bang.png")
        self.firework1_img = pygame.image.load("resources/images/firework1.png")
        self.firework2_img = pygame.image.load("resources/images/firework2.png")
        self.fireworks = [self.firework1_img,self.firework2_img]
        # 3.1 - Load audio
        self.hit = pygame.mixer.Sound("resources/audio/explode.wav")
        self.enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
        self.shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
        self.hit.set_volume(1.0)
        self.enemy.set_volume(0.50)
        self.shoot.set_volume(0.50)
        pygame.mixer.music.load('resources/audio/moonlight.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(1.0)
    #
    def game_loop(self):
        # 4 - keep looping through
        self.running = 1
        self.exitcode = 0
        self.score = 0
        self.hitCount = 0
        self.level = 200
        self.levelCount = 1
        self.rocket_speed = 0.1
        while self.running:
            self.rocket_timer-=1
            # 5 - clear the screen before drawing it again
            self.screen.fill(0)
            # 6 - draw the screen elements
            self.draw_screen_elements()
            # 6.1 - Set player position and rotation
            self.player_pos_rotation()
            # 6.2 - Draw flames
            self.draw_flames()
            # 6.3 - Draw rockets
            self.draw_rockets()
            # 6.4 - Draw Scores
            self.draw_scores()
            # 6.5 - Draw health bar
            self.draw_health_bar()
            # 7 - update the screen
            pygame.display.flip()
            # 8 - loop through the events
            self.check_events()
            # 9 - Move player
            self.move_player()
            #10 - Win/Lose check
            self.check_result()
        # 11 - Win/lose display
        self.display_result()
    
    def draw_screen_elements(self):
        # 6 - draw the screen elements
        self.screen.blit(self.south_china_sea,(0,0))
        self.screen.blit(self.castle,(0,70))
        self.screen.blit(self.ship1,(0,140))
        self.screen.blit(self.ship2,(0,210))
        self.screen.blit(self.ship1,(0,280))
        self.screen.blit(self.ship2,(0,350))

    def player_pos_rotation(self):
        # 6.1 - Set player position and rotation
        self.position = pygame.mouse.get_pos()
        self.angle = math.atan2(self.position[1]-(self.playerpos[1]+.5),self.position[0]-(self.playerpos[0]+.3))
        self.playerrot = pygame.transform.rotate(self.player[randint(0,1)], 360-self.angle*57.29)
        self.playerpos1 = (self.playerpos[0]-self.playerrot.get_rect().width/2, self.playerpos[1]-self.playerrot.get_rect().height/2)
        self.screen.blit(self.playerrot, self.playerpos1)

    def draw_flames(self):
        # 6.2 - Draw flames
        for self.flame in self.flames:
            index=0
            velx=math.cos(self.flame[0])*1
            vely=math.sin(self.flame[0])*1
            self.flame[1]+=velx
            self.flame[2]+=vely
            if self.flame[1]<-64 or self.flame[1]>640 or self.flame[2]<-64 or self.flame[2]>480:
                self.flames.pop(index)
            index+=1
            for projectile in self.flames:
                self.flame1 = pygame.transform.rotate(self.flame_img, 360-projectile[0]*57.29)
                self.screen.blit(self.flame1, (projectile[1], projectile[2]))

    def draw_rockets(self):
        # 6.3 - Draw rockets
        if self.rocket_timer == 0:
            self.rockets.append([640, randint(50,430)])
            # game difficulty level
            self.game_level()
            if self.rocket_timer1>=5:
                self.rocket_timer1=5
            else:
                self.rocket_timer1+=self.levelCount
        self.index=0
        for self.rocket in self.rockets:
            if self.rocket[0]<-64:
                self.rockets.pop(self.index)
            self.rocket[0]-=self.rocket_speed
            # 6.3.1 - Attack Ship
            self.attack_ship()
            #6.3.2 - Check for collisions
            self.check_collisions()
            # 6.3.3 - Next bad guy
            self.index+=1
        for self.rocket in self.rockets:
            self.screen.blit(self.rocket_images[randint(0,6)], self.rocket)

    def attack_ship(self):
        # 6.3.1 - Attack Ship
        self.rocket_rect=pygame.Rect(self.rocket_img.get_rect())
        self.rocket_rect.top=self.rocket[1]
        self.rocket_rect.left=self.rocket[0]
        if self.rocket_rect.left<64:
            #self.screen.blit(self.bang_img, self.rocket_rect) explosion display
            self.hit.play()
            self.health_value -= randint(5,20)
            self.hitCount +=1
            self.rockets.pop(self.index)

    def check_collisions(self):
        #6.3.2 - Check for collisions
        self.index1=0
        for self.flame in self.flames:
            self.flame_rect=pygame.Rect(self.flame_img.get_rect())
            self.flame_rect.left=self.flame[1]
            self.flame_rect.top=self.flame[2]
            if self.rocket_rect.colliderect(self.flame_rect):
                self.enemy.play()
                self.acc[0]+=1
                self.score +=1
                self.rockets.pop(self.index)
                self.flames.pop(self.index1)
            self.index1+=1

    def draw_scores(self):
        # 6.4 - Draw Scores
        self.font = pygame.font.Font(None, 24)
        self.scoreText = self.font.render("Score {0}".format(self.score), 1, (25,186,17))
        self.scoreTextRect = self.scoreText.get_rect()
        self.scoreTextRect.topright=[610,5]
        self.screen.blit(self.scoreText, self.scoreTextRect)
        # hit Count
        self.hitText = self.font.render("Hit {0}".format(self.hitCount), 1, (210,25,17))
        self.hitTextRect = self.hitText.get_rect()
        self.hitTextRect.topright=[520,5]
        self.screen.blit(self.hitText, self.hitTextRect)
        # Difficulty level
        self.levelText = self.font.render("Level {0}".format(self.levelCount), 1, (17,25,210))
        self.levelTextRect = self.levelText.get_rect()
        self.levelTextRect.topright=[430,5]
        self.screen.blit(self.levelText, self.levelTextRect)
        #self.screen.blit(self.fireworks[randint(0,1)], (randint(0,640),randint(0,480)))



    def draw_health_bar(self):
        # 6.5 - Draw health bar
        self.screen.blit(self.healthbar, (5,5))
        for self.health1 in range(self.health_value):
            self.screen.blit(self.health, (self.health1+8,8))


    def check_events(self):
        # 8 - loop through the events
        for event in pygame.event.get():
            # check if the event is the X button 
            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit() 
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key==K_w:
                    self.keys[0]=True
                elif event.key==K_a:
                    self.keys[1]=True
                elif event.key==K_s:
                    self.keys[2]=True
                elif event.key==K_d:
                    self.keys[3]=True
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_w:
                    self.keys[0]=False
                elif event.key==pygame.K_a:
                    self.keys[1]=False
                elif event.key==pygame.K_s:
                    self.keys[2]=False
                elif event.key==pygame.K_d:
                    self.keys[3]=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                self.shoot.play()
                self.position=pygame.mouse.get_pos()
                self.acc[1]+=1
                self.flames.append([math.atan2(self.position[1]-(self.playerpos1[1]+32),self.position[0]-(self.playerpos1[0]+26)),self.playerpos1[0]+32,self.playerpos1[1]+32])

    def move_player(self):
        # 9 - Move player
        if self.keys[0]:
            self.playerpos[1]-=.3
        elif self.keys[2]:
            self.playerpos[1]+=.3
        if self.keys[1]:
            self.playerpos[0]-=.3
        elif self.keys[3]:
            self.playerpos[0]+=.3

    def game_level(self):
        if self.score == 100:
            self.level = 190
            self.levelCount = 2
        elif self.score == 200:
            self.level = 180
            self.rocket_speed = 0.2
            self.levelCount = 3
        elif self.score == 300:
            self.level = 170
            self.rocket_speed = 0.3
            self.levelCount = 4
        elif self.score == 400:
            self.level = 160
            self.rocket_speed = 0.4
            self.levelCount = 5
        elif self.score == 500:
            self.level = 150
            self.rocket_speed = 0.5
            self.levelCount = 6
        elif self.score == 700:
            self.level = 140
            self.rocket_speed = 0.6
            self.levelCount = 7
            self.health_value = 194
            self.hitCount = 0
        elif self.score == 900:
            self.level = 130
            self.rocket_speed = 0.7
            self.levelCount = 8
        elif self.score == 1100:
            self.level = 120
            self.rocket_speed = 0.8
            self.levelCount = 9
        elif self.score == 1300:
            self.level = 110
            self.rocket_speed = 0.9
            self.levelCount = 10
        self.rocket_timer =self.level-(self.rocket_timer1*2) # difficulty level

    def check_result(self):
        #10 - Win/Lose check
        if self.score > 1500:
            self.running=0
            self.exitcode=1
        if self.health_value<=0:
            self.running=0
            self.exitcode=0
        if self.acc[1]!=0:
            self.accuracy= format(self.acc[0]*1.0/self.acc[1]*100, ".2f")
        else:
            self.accuracy=0

    def display_result(self):
        # 11 - Win/lose display        
        if self.exitcode==0:
            pygame.font.init()
            self.font = pygame.font.Font(None, 24)
            self.text = self.font.render("Shooting Accuracy: "+str(self.accuracy)+"%", True, (17,25,210))
            self.textRect = self.text.get_rect()
            self.textRect.centerx = self.screen.get_rect().centerx
            self.textRect.centery = self.screen.get_rect().centery+24
            self.screen.blit(self.gameover, (0,0))
            self.screen.blit(self.text, self.textRect)
            # score display
            self.textScore = self.font.render("Score: "+str(self.score), True, (210,25,17))
            self.textScoreRect = self.textScore.get_rect()
            self.textScoreRect.centerx = self.screen.get_rect().centerx
            self.textScoreRect.centery = self.screen.get_rect().centery+48
            self.screen.blit(self.textScore, self.textScoreRect)
        else:
            pygame.font.init()
            self.font = pygame.font.Font(None, 24)
            self.text = self.font.render("Shooting Accuracy: "+str(self.accuracy)+"%", True, (0,255,0))
            self.textRect = self.text.get_rect()
            self.textRect.centerx = self.screen.get_rect().centerx
            self.textRect.centery = self.screen.get_rect().centery+24
            self.screen.blit(self.youwon, (0,0))
            self.screen.blit(self.text, self.textRect)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
            pygame.display.flip()