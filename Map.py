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
dred = (200, 0, 0)
dgreen = (0, 200, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#Message System
def text_objects(text, font):
    TextSurf = font.render(text, True, blue)
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

#Blocks To Dodge
def things(x, y, w, h, c):
    pygame.draw.rect(gameDisplay, c, [x, y, w, h])

#Score
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (10,10))

#Button
def button(msg, x, y, w, h, i, a, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x+w and y < mouse[1] < y+h:
        c = a
        if click[0] == 1 and action != None:
                action()

    else:
        c = i

    pygame.draw.rect(gameDisplay, c, (x, y, w, h))

    smallText =  pygame.font.Font("freesansbold.ttf", 20)
    TextSurf, TextRec = text_objects(msg, smallText)
    TextRec.center = ((x + (w/2), y + (h/2)))
    gameDisplay.blit(TextSurf, TextRec)

#Close window
def closeWin():
    pygame.quit()
    quit()


#Starting Screen
def start_screen():
    intro = True
    scolor = dgreen
    qcolor = dred
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeWin()

        gameDisplay.fill(white)
        style = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRec = text_objects("PyCarGame", style)
        TextRec.center = ((display_width/2), (display_height/3))
        gameDisplay.blit(TextSurf, TextRec)
        
        button("GO!", display_width / 3 - 50, 3 * display_height / 4 - 25, 100, 50, dgreen, green, GameLoop)
        button("QUIT", 2 * display_width / 3 - 50, 3 * display_height / 4 - 25, 100, 50, dred, red, closeWin)
        pygame.display.update()


#Game Loop
def GameLoop():
    sx = 0.4
    sy = 0.7
    x = sx * display_width
    y = sy * display_height
    tw = 100
    tx = random.randrange(0, display_width - tw)
    ty = -600
    ts = 4
    
    th = 100
    crashed = False
    score = 0
    while True:
        #Events
        for event in pygame.event.get():
            if crashed == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        GameLoop()
                        return
                    if event.key == pygame.K_q:
                        closeWin()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #Key Holds
        keys = pygame.key.get_pressed()
        if not crashed:
            if keys[pygame.K_LEFT]:
                x += -7
            if keys[pygame.K_RIGHT]:
                x += 7
        #Background
        gameDisplay.fill(white)

        #Draw Scene
        things(tx, ty, tw, th, red)
        if not crashed:
            ty += ts
        Car(x, y)
        things_dodged(score)
        if x <= -2 or x + carWidth >= display_width:
            message_display(["You Crashed", "Press R", "To Restart"])
            crashed = True
        if ty > display_height:
            ty = 0 - th
            tx = random.randrange(0, display_width - tw)
            score += 1
            ts += 1
            tw += 2


        if y < ty+th and y + carNoSpoiler > ty:
            if x > tx and x < tx + tw or x + carWidth > tx and x + carWidth < tx + tw:
                message_display(["You Crashed", "Press R", "To Restart"])
                crashed = True


        
        pygame.display.update()
        clock.tick(60)
    


start_screen()
GameLoop()
pygame.quit()
quit()

