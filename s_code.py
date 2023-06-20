import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('background.jpg')

# BAckground Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Defenders")
icon=pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)


# PLayer Creation
playerimg = pygame.image.load('player.png')
playerX = 360
playerY = 500
playerX_change=0

# Enemy Creation
enemyimg = []
enemyX =[]
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(45)
    enemyX_change.append(-0.3)
    enemyY_change.append(28)



#Bullet Load
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.5
bullet_state = "ready"

# Score Value
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

testX = 10
testY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

#Player function
def player(x, y) :
    screen.blit(playerimg, (x, y))     #screen.blit is used to draw the image in window

#Enemy function
def enemy(x, y, i) :
    screen.blit(enemyimg[i], (x, y))

#Bullet function
def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16, y+10))

# Collision Detection
def iscollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2))
    if distance < 27:
        return True
    else:
        return False
    

# Score function
def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))


#Game over function
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))


#Game Loop
status = True
while status:
    screen.fill((10,15,25))


    #backgorund image
    screen.blit(background, (0,0))

    #Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status=False

        #KEYSTROKE Checking    

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change=-0.5
            if event.key == pygame.K_RIGHT:   
                playerX_change=0.5   
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX,bulletY)    

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: 
                playerX_change=0
        

    #Boundary checking of player
    playerX += playerX_change

    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736


    #Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break    



        enemyX[i] += enemyX_change[i]

        if enemyX[i]<=0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i] = -0.3    
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = 15
        
        enemy(enemyX[i],enemyY[i], i)


    #Bullet Movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        bullet(bulletX,bulletY)
        bulletY -= bulletY_change

        



    player(playerX,playerY)
    show_score(testX, testY)
    pygame.display.update()      