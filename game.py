import pygame
import random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

display_surface = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

#set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#set game values
PLAYER_STARTING_LIVES = 3
PLAYER_NORMAL_VELOCITY = 5
PLAYER_BOOST_VELOCITY = 10
STARTING_BOOST_LEVEL = 100
STARTING_BURGER_VELOCITY = 3
BURGER_ACCELERATION = .25
BUFFER_DISTANCE = 100

score = 0
burger_points = 0
burgers_eaten = 0

player_lives = PLAYER_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY

boost_level = STARTING_BOOST_LEVEL

burger_velocity = STARTING_BURGER_VELOCITY

#colors
ORANGE = (246 , 170 , 54)
BLACK = (0,0,0)
WHITE = (255, 255 ,255)


#set font
font = pygame.font.Font('Assets/custom.ttf' , 32)
#set text
points_text = font.render('Burger points' + str(burger_points) , 1, ORANGE)
points_rect = points_text.get_rect()
points_rect.topleft = (10 , 10)

score_text = font.render('Score: ' + str(score) , 1 , ORANGE)
score_rect = score_text.get_rect()
score_rect.topleft = (10 , 50)

title_text = font.render('Burger dog ' , 1 ,ORANGE)
title_rect = title_text.get_rect()
title_rect.topleft = (WINDOW_WIDTH // 2 , 10)


eaten_text = font.render('Eaten: ' + str(burgers_eaten) , 1 , ORANGE)
eaten_rect = eaten_text.get_rect()
eaten_rect.topleft = (WINDOW_WIDTH // 2 , 50)

lives_text = font.render('Lives: ' + str(player_lives) , 1, ORANGE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10 , 10)


boost_text = font.render("boost: " + str(boost_level) , 1, ORANGE)
boost_rect = boost_text.get_rect()
boost_rect.topright = (WINDOW_WIDTH - 10 , 50)

game_over_text = font.render('Game Over' , 1, ORANGE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH //2 , WINDOW_HEIGHT // 2)

continue_text = font.render("Press any key to play again" , 1, ORANGE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH //2 , WINDOW_HEIGHT //2 + 64)
#load images
player_image_right = pygame.image.load('Assets/thanay_right.png')
player_image_left = pygame.image.load('Assets/thanay_left.png')
player_image = player_image_left
player_rect  = player_image.get_rect()
player_rect.bottom = WINDOW_HEIGHT

burger_image = pygame.image.load("Assets/burger.png")
burger_rect = burger_image.get_rect()
burger_rect.topleft = (random.randint(0 , WINDOW_WIDTH - 32) , -BUFFER_DISTANCE)
#load music
bark_sound = pygame.mixer.Sound('Assets/bark.wav')
miss_sound = pygame.mixer.Sound('Assets/miss_sound.wav')
pygame.mixer.music.load('Assets/bg_so.wav')
pygame.mixer.music.play(-1 , 0.0 )


#game loop
running  = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #move the dog
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_image =  player_image_left
        player_rect.x -= player_velocity
    if keys[pygame.K_RIGHT] and player_rect.right < WINDOW_WIDTH:
        player_image = player_image_right
        player_rect.x += player_velocity
    if keys[pygame.K_UP] and player_rect.top > 100:
        player_rect.y -= player_velocity
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += player_velocity
    
    #boost
    if keys[pygame.K_SPACE] and boost_level > 0:
        player_velocity = PLAYER_BOOST_VELOCITY
        boost_level -= 1
    else:
        player_velocity = PLAYER_NORMAL_VELOCITY
    #burger movement
    burger_rect.y += burger_velocity
    burger_points = int(burger_velocity * (WINDOW_HEIGHT - burger_rect.y + 100))
    
    #burger missed
    if burger_rect.y > WINDOW_HEIGHT:
        player_lives -= 1
        miss_sound.play()

        burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32) , -BUFFER_DISTANCE)
        burger_velocity = STARTING_BURGER_VELOCITY

        player_rect.centerx = WINDOW_WIDTH //2 
        player_rect.bottom = WINDOW_HEIGHT
        boost_level = STARTING_BOOST_LEVEL
    
    #collision
    if player_rect.colliderect(burger_rect):
        score += burger_points
        burgers_eaten += 1
        bark_sound.play()

        burger_rect.topleft = (random.randint(0, WINDOW_WIDTH - 32) , -BUFFER_DISTANCE)
        burger_velocity += BURGER_ACCELERATION

        boost_level += 25
        if boost_level > STARTING_BOOST_LEVEL:
            boost_level = STARTING_BOOST_LEVEL
        
    #fill

    #update
    points_text = font.render('Burger points' + str(burger_points) , 1, ORANGE)
    score_text = font.render('Score: ' + str(score) , 1 , ORANGE)
    eaten_text = font.render('Eaten: ' + str(burgers_eaten) , 1 , ORANGE)
    lives_text = font.render('Lives: ' + str(player_lives) , 1, ORANGE)
    boost_text = font.render("boost: " + str(boost_level) , 1, ORANGE)

    display_surface.fill(BLACK)
    display_surface.blit(title_text , title_rect)
    display_surface.blit(score_text , score_rect)
    display_surface.blit(lives_text , lives_rect)
    display_surface.blit(eaten_text , eaten_rect)
    display_surface.blit(points_text , points_rect)
    display_surface.blit(boost_text , boost_rect)
    pygame.draw.line(display_surface , WHITE , (0 , 100) , (WINDOW_WIDTH , 100))
    
    #game over
    if player_lives == 0:
        game_over_text = font.render('Final Score: ' +str(score) , 1, ORANGE)
        display_surface.blit(game_over_text , game_over_rect)
        display_surface.blit(continue_text ,continue_rect)
        pygame.display.update()

        # reset
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    burgers_eaten = 0
                    burger_velocity  = STARTING_BURGER_VELOCITY
                    player_lives = PLAYER_STARTING_LIVES
                    boost_level = PLAYER_BOOST_VELOCITY
                    pygame.mixer.music.play()
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
    #blit assets
    display_surface.blit(player_image , player_rect)
    display_surface.blit(burger_image , burger_rect)
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
