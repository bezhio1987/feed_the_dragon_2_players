import pygame,random
 
# two players will play with arrow keys and and w s keys on keyboard on the same screen. 
# while they are cooperating to grab the coin,they will try to get more scores too.
# when the coin pass the wall the winner is someone with a higher score
#initialize pygame
pygame.init()

#create a display surface and set its caption
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed the dragon")



# define a clock to slow down the while loop and make sure it runs at the same speed on every single computer (FPS = frame per second)
FPS  = 60
clock = pygame.time.Clock()
#VELOCITY = 10 it runs 10 times a second


#set game values
PLAYER_VELOCITY = 5
PLAYER_STARTER_LIVES = 5
COIN_STARTTIGN_VELOCITY = 5
COIN_ACCELERATION = 0.5  # coin will speed up
BUFFER_DISTANCE = 100 # while it goes off the screen

score_p1 = 0
score_p2 = 0

lives_p1 = PLAYER_STARTER_LIVES
lives_p2 = PLAYER_STARTER_LIVES

coin_velocity = COIN_STARTTIGN_VELOCITY


#colors
GREEN = (0,255,0)
DARKGREEN = (10,50,10)
WHITE = (255,255,255)
BLACK = (0,0,0)

#set fonts
font = pygame.font.Font('AttackGraffiti.ttf', 32)

#set text 
#score
score_text_p1 = font.render("Score p1: "+str(score_p1), True, GREEN, BLACK)
score_p1_rect = score_text_p1.get_rect()
score_p1_rect.topleft = (10,10)

score_text_p2 = font.render("Score p2: "+str(score_p2), True, GREEN, BLACK)
score_p2_rect = score_text_p2.get_rect()
score_p2_rect.topright = (WINDOW_WIDTH-50,10)

#lives
lives_p1_text = font.render("Lives p1: "+str(lives_p1), True, GREEN, BLACK)
lives_p1_rect = lives_p1_text.get_rect()
lives_p1_rect.topleft = (10,50)

lives_p2_text = font.render("Lives p2: "+str(lives_p2), True, GREEN, BLACK)
lives_p2_rect = lives_p2_text.get_rect()
lives_p2_rect.topright = (WINDOW_WIDTH-50,50)

#title
title_text = font.render("Feed the dragon", True, GREEN, BLACK)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 50

game_over_text = font.render("GAMEOVER", True, GREEN, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2 , WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to play again", True, GREEN, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)

#load in images
player1_image = pygame.image.load('dragon_right.png')
player1_rect =  player1_image.get_rect()
player1_rect.centery = WINDOW_HEIGHT//2 + 40

player2_image = pygame.image.load('dragon_right2.png')
player2_rect =  player2_image.get_rect()
player2_rect.centery = WINDOW_HEIGHT//2 - 40


coin_image = pygame.image.load('coin.png')
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)


# sound
coin_sound = pygame.mixer.Sound("coin_sound.wav")
miss_sound = pygame.mixer.Sound("miss_sound.wav")
miss_sound.set_volume(0.1)
pygame.mixer.music.load("ftd_background_music.wav")


#the main game loop
pygame.mixer.music.play(-1,0.0)
running = True
while running:
    #lopp through a list of ecents 
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
           running = False 
    
     
    
    #get the list of keys pressed on keyboared
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]  and player1_rect.y > 110 :
        player1_rect.y -= PLAYER_VELOCITY
       
    if keys[pygame.K_DOWN]  and player1_rect.y < WINDOW_HEIGHT - 32:
        player1_rect.y += PLAYER_VELOCITY  
        
    if  keys[pygame.K_w] and player2_rect.y > 110 :
        player2_rect.y -= PLAYER_VELOCITY
       
    if  keys[pygame.K_s] and player2_rect.y < WINDOW_HEIGHT - 32:
        player2_rect.y += PLAYER_VELOCITY  
 
 
 
   
    #move the coin
    if coin_rect.x < 0:
        #player missed teh coin
        lives_p1 -= 1
        lives_p2 -= 1
        miss_sound.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    else:
        #move the coin
        coin_rect.x -= coin_velocity
        
    #check for collison between two rects
    if player1_rect.colliderect(coin_rect):
        score_p1 += 1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(110, WINDOW_HEIGHT - 32)
      
    if player2_rect.colliderect(coin_rect):
        score_p2 += 1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(110, WINDOW_HEIGHT - 32)  
    
    #update text for score and lives
    score_text_p1 = font.render("Score p1: "+str(score_p1), True, GREEN, BLACK)
    lives_text_p1 = font.render("Lives p1: "+str(lives_p1), True, GREEN, BLACK)
    
    score_text_p2 = font.render("Score p2: "+str(score_p2), True, GREEN, BLACK)
    lives_text_p2 = font.render("Lives p2: "+str(lives_p2), True, GREEN, BLACK)

    #check for game over 
    if lives_p1 == 0 or lives_p2 == 0:
            display_surface.blit(game_over_text, game_over_rect)
            display_surface.blit(continue_text, continue_rect)
            pygame.display.update()
            
            #pause the game until player presses a key and reset the game
            pygame.mixer.music.stop()
            is_paused = True
            while is_paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        score_p1 = 0
                        score_p2 = 0
                        lives_p1 = PLAYER_STARTER_LIVES
                        lives_p2 = PLAYER_STARTER_LIVES
                        player1_rect.y = WINDOW_HEIGHT//2 + 30
                        player2_rect.y = WINDOW_HEIGHT//2 - 30
                        coin_velocity = COIN_STARTTIGN_VELOCITY
                        pygame.mixer.music.play(-1, 0.0)
                        is_paused = False
                    #the player wants to quit
                    if event.type == pygame.QUIT:
                        is_paused = False
                        running = False 


        
     #fill the display to cover the old images
    display_surface.fill(BLACK)   
    
                      
    #blit the images to the screen
    display_surface.blit(player1_image, player1_rect)
    display_surface.blit(player2_image, player2_rect)

    display_surface.blit(coin_image, coin_rect)
    
   # blit the HUD to teh screen
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_p1_text, lives_p1_rect)
    display_surface.blit(lives_p2_text, lives_p2_rect)
    display_surface.blit(score_text_p2, score_p2_rect)
    display_surface.blit(score_text_p1, score_p1_rect)
    
    pygame.draw.line(display_surface, WHITE ,(0,110), (WINDOW_WIDTH,110), 2)

    #update the display
    pygame.display.update()
    
    #tick the clock
    clock.tick(FPS)

           
# end the  game
pygame.quit()
