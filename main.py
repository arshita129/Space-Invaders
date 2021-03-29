import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('background.jpg')

mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Space Invad/ers")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

player = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 520
playerX_change = 0

enemy=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
for i in range(6):
    enemy.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(10, 100))
    enemyX_change.append(0.3)
    enemyY_change.append(20)

bullet = pygame.image.load('bullet.png')
bulletY = 480
bulletX = 100
bulletY_change = 1

score=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

def display_score(score):
    score_value=font.render("Score:"+ str(score),True, (255,255,255))
    screen.blit(score_value,(textX,textY))

def bulletFun(x, y):
    screen.blit(bullet, (x, y))

def enemyFun(x, y,i):
    screen.blit(enemy[i], (x, y))

def playerFun(x, y):
    screen.blit(player, (x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow((enemyX - bulletX), 2)) + (math.pow((enemyY - bulletY), 2)))
    if distance < 27:
        return True
    else:
        return False

def game_over_text():
    game_over=font.render("GAME OVER! Your Score is "+str(score),True,(255,255,255))
    screen.blit(game_over,(180,180))

k = 0
running = True
while running:
    screen.fill((0, 255, 255))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_UP:
                playerX_change = 0
            if event.key == pygame.K_SPACE:
                bullet_sound=mixer.Sound('laser.wav')
                bullet_sound.play()
                bulletX = playerX
                bulletFun(playerX, bulletY)
                k = 1
        # if event.type==pygame.KEYUP:
        #     if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
        #         playerX_change=0
    if k == 1:
        bulletFun(bulletX, bulletY)
        bulletY -= bulletY_change
    if bulletY <= 0:
        bulletY = 480
        k = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    for i in range(6):

        if enemyY[i]> 200:
            for j in range(6):
                enemyY[j]=1000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
        #print(isCollision(enemyX,enemyY,bulletX,bulletY))
        if isCollision(enemyX[i],enemyY[i],bulletX,bulletY):
            collision_sound=mixer.Sound('explosion.wav')
            collision_sound.play()
            score+=100
            print(score)
            bulletY=480
            k=0
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(10, 100)
        enemyFun(enemyX[i], enemyY[i],i)

    playerFun(playerX, playerY)

    display_score(score)
    pygame.display.update()
