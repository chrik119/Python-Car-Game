import pygame
import time
import random

pygame.init()

#Setup Window
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Racer')
clock = pygame.time.Clock()

#Car
carImg = pygame.image.load('racecar.png')
carWidth = 108
carHeight = 155
carNoSpoiler = 135
def Car(X, Y):
    
    gameDisplay.blit(carImg, (X, Y))

#Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#Message System
def text_objects(text, font):
    TextSurf = font.render(text, True, green)
    return TextSurf, TextSurf.get_rect()

def message_display(listText):
    fontSize = 115
    i = 0
    message = pygame.font.Font("freesansbold.ttf", fontSize)
    for text in listText:
        TextSurf, TextRec = text_objects(text, message)
        TextRec.center = ((display_width/2), (display_height/2 - fontSize + (i * fontSize)))
        gameDisplay.blit(TextSurf, TextRec)
        i += 1
    pygame.display.update()

def things(x, y, w, h, c):
    pygame.draw.rect(gameDisplay, c, [x, y, w, h])
    

#Game Loop
def GameLoop():
    sx = 0.4
    sy = 0.7
    x = sx * display_width
    y = sy * display_height
    tx = random.randrange(0, display_width)
    ty = -600
    ts = 7
    tw = 100
    th = 100
    crashed = False
    while True:
        #Events
        for event in pygame.event.get():
            if crashed == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        GameLoop()
                        return
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #Key Holds
        keys = pygame.key.get_pressed()
        if not crashed:
            if keys[pygame.K_LEFT]:
                x += -5
            if keys[pygame.K_RIGHT]:
                x += 5
        #Background
        gameDisplay.fill(white)

        #Draw Scene
        things(tx, ty, tw, th, red)
        if not crashed:
            ty += ts
        Car(x, y)
        if x <= -2 or x + carWidth >= display_width:
            message_display(["You Crashed", "Press R", "To Restart"])
            crashed = True
        if ty > display_height:
            ty = 0 - th
            tx = random.randrange(0, display_width)

        if y < ty+th and y + carNoSpoiler > ty:
            if x > tx and x < tx + tw or x + carWidth > tx and x + carWidth < tx + tw:
                message_display(["You Crashed", "Press R", "To Restart"])
                crashed = True


        
        pygame.display.update()
        clock.tick(60)
    



GameLoop()
pygame.quit()
quit()

