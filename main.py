import random
import pygame
from pygame.locals import *
import sys

FPS = 32

# Screen Size = width x height #
SCREENWIDTH = 290
SCREENHEIGHT = 512
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

GROUNDY = SCREENHEIGHT*0.9

# Dictionaries to store the game - media # 
GAME_SPRITES={}
GAME_SOUNDS={}

PIPE = 'pictures/pipe.png'  # path of image of pipe

# Welcome Screen 
def welcomeScreen():
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['message'],(0,0))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSClOCK.tick(FPS)

# Code of main game 
def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    #create 2 random pipes upper and lower

    newpipe1 = getRandompipe() 
    newpipe2 = getRandompipe()   

    # my list of upper pipe
    upperPipes = [
        {'x': SCREENWIDTH+200 , 'y': newpipe1[0]['y']},
        {'x': SCREENWIDTH+200 +(SCREENWIDTH/2) , 'y': newpipe2[0]['y']}
        
    ]

    #my list of lower pipes
    lowerPipes = [ 
        {'x': SCREENWIDTH+200 , 'y': newpipe1[1]['y']},
        {'x': SCREENWIDTH+200 +(SCREENWIDTH/2) , 'y': newpipe2[1]['y']}
        
    ]

    # Velocities of player and pipe
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -9
    playerAccY = 1 

    playerFapAccY = -8 # velocity while flapping
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or  (event.type == KEYDOWN and event.key == K_SPACE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFapAccY
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
            
        crash_test = isCollide(playerx,playery,upperPipes,lowerPipes)#this function  will return if crased in pipe
        if crash_test:
            return
        
        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos+4 :
                score += 1
                print(f'your score is {score}')
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY , GROUNDY - playerHeight - playery)

            # Move pipe to the left
        for upperPipe , lowerPipe in zip(upperPipes , lowerPipes):
            upperPipe['x'] += pipeVelX 
            lowerPipe['x'] += pipeVelX 

            #Add a new pipe when the first pipe are about to cross the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandompipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

            #if pipes are out of the screen remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

            # blitting of maingame
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))

        mydigit = [int(x) for x in list(str(score))]
        width = 0

        for digits in mydigit:
            width += GAME_SPRITES['numbers'][digits].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digits in mydigit:
            SCREEN.blit(GAME_SPRITES['numbers'][digits],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digits].get_width()
        pygame.display.update()
        FPSClOCK.tick(FPS)
        
# Checking if the player crashed
def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']-20) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x'] - 20) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
        
    return False
            
                    
# Generation of random pipes
def getRandompipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3

    y2 = offset + random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height() - 1.2*offset))
    y1 = pipeHeight - y2 + offset 

    pipeX = SCREENWIDTH + 10

    # list of pipes
    pipe=[
        {'x' : pipeX , 'y': -y1} , # upper pipe 
          {'x' : pipeX , 'y': y2}  # lower pipe
    ]
    return pipe

# checked
if __name__ == '__main__':
    pygame.init()
    FPSClOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy bird by Manish')
    GAME_SPRITES['numbers']=(
        pygame.image.load('pictures/0.png').convert_alpha(),
        pygame.image.load('pictures/1.png').convert_alpha(),
        pygame.image.load('pictures/2.png').convert_alpha(),
        pygame.image.load('pictures/3.png').convert_alpha(),
        pygame.image.load('pictures/4.png').convert_alpha(),
        pygame.image.load('pictures/5.png').convert_alpha(),
        pygame.image.load('pictures/6.png').convert_alpha(),
        pygame.image.load('pictures/7.png').convert_alpha(),
        pygame.image.load('pictures/8.png').convert_alpha(),
        pygame.image.load('pictures/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('pictures/msg.jpeg').convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load('pictures/bird.png ').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('pictures/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha())
    GAME_SPRITES['background'] = pygame.image.load('pictures/background.jpeg').convert()

    # Game sound
    GAME_SOUNDS['die'] = pygame.mixer.Sound('audio/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('audio/hit.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('audio/point.mp3')
    GAME_SOUNDS['Swoosh'] = pygame.mixer.Sound('audio/Swoosh.mp3')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('audio/wing.mp3')

    while True:
        welcomeScreen()
        maingame()