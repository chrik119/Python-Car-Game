import pygame
import random

#Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
dred = (200, 0, 0)
dgreen = (0, 200, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (240, 240, 60)

class Window:
    def __init__(self, w, h, caption, fps):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((w, h))
        self.width = w
        self.height = h
        self.clock = pygame.time.Clock()
        self.clock.tick(fps)
        pygame.display.set_caption(caption)

    def message(self, linesOfText, cx, ty, font=None, size=25, color=black):
        style = pygame.font.Font(font, size)
        i = 0
        for text in linesOfText:
            TextSurf = style.render(text, True, color)
            TextRec = TextSurf.get_rect()
            TextRec.center = (cx, ty + (i * size))
            self.gameDisplay.blit(TextSurf, TextRec)
            i += 1

    def close_win(self):
        record = open("HighScore.txt", "w")
        for i in scores:
            record.write(str(i)+"\n")
        record.close
        pygame.quit()
        quit()

    def button(self, linesOfText, x, y, w, h, i, a, font=None, size=25, color=black):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x+w and y < mouse[1] < y+h:
            c = a
            if click[0] == 1:
                return True
        else:
            c = i
        pygame.draw.rect(self.gameDisplay, c, (x, y, w, h))
        self.message(linesOfText, x + (w/2), y + (h/2), font, size, color)
        

#SPRITE BASE CLASS
class Sprite:
    def __init__(self, x, y, w, h, i=None):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        if i != None:
            self.i = pygame.image.load(i)

    def draw(self, screen):
        if self.i != None:
            screen.gameDisplay.blit(self.i, (self.x, self.y)) 

#CAR
class Car(Sprite):
    def __init__(self, x, y, w, h, i, ns):
        Sprite.__init__(self, x, y, w, h, i)
        self.noSpoiler = ns
        self.steerSpeed = 7

#OBSTACLE
class Obstacle(Sprite):
    def __init__(self, x, y, w, h, s):
        Sprite.__init__(self, x, y, w, h)
        self.speed = s
        self.i = pygame.image.load("enemy.png")

    def draw(self, screen):
        screen.gameDisplay.blit(self.i, (self.x, self.y))

#START SCREEN
def start_screen(screen):
    intro = True
    font = "freesansbold.ttf"
    start = False
    over = False
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.close_win()

        screen.gameDisplay.fill(white)
        screen.message(["PyCarGame"], (screen.width/2), (screen.height/3), font=font, size=115, color=blue)
        start = screen.button(["GO!"], (screen.width / 3 - 50), (3 * screen.height / 4 - 25), 100, 50, dgreen, green, font=font, size=20)
        over = screen.button(["QUIT"], (2 * screen.width / 3 - 50), (3 * screen.height / 4 - 25), 100, 50, dred, red, font=font, size=20)
        
        if start == True:
            GameLoop(screen)
        if over == True:
            screen.close_win()

        pygame.display.update()

def spawn_obstacle():
    pass

def crashed_message(score, update):
    if update == 0:
        if score > scores[1]:
            update = 1
            scores[5] = scores[3]
            scores[4] = scores[2]
            scores[3] = scores[1]
            scores[2] = scores[0]
            scores[1] = score
            scores[0] = ""
        elif score > scores[3]:
            update = 2
            scores[5] = scores[3]
            scores[4] = scores[2]
            scores[3] = score
            scores[2] = ""
        elif score > scores[5]:
            update = 3
            scores[5] = score
            scores[4] = ""
        else:
            update = 0
    if update == 0:
        message = "ENTER TO RESTART"
    else:
        message = "ENTER INITIALS"
    font = "freesansbold.ttf"
    screen.message([str(scores[0]),str(scores[2]),str(scores[4])], screen.width/3, (screen.height/5) - 20, font=font, size = 80, color=dgreen)
    screen.message([str(scores[1]),str(scores[3]),str(scores[5])], 2*screen.width/3, (screen.height/5) - 20, font=font, size = 80, color=dgreen)

    screen.message([message], screen.width/2, (4*screen.height/5), font=font, size = 70, color=dgreen)
    return update

#GAME LOOP
def GameLoop(screen):
    crashed = False
    font = "freesansbold.ttf"
    score = 0
    update = 0
    paused = False
    car = Car(screen.width * .4, screen.height *.7, 108, 155, "racecar_hard_collision.png", 135)
    obstacle = Obstacle(random.randrange(62, screen.width - 123), -300, 61, 67, 4)
    background = [pygame.image.load("Road1.png"), pygame.image.load("Road1.png"), pygame.image.load("Road2.png"), pygame.image.load("Road2.png"), pygame.image.load("Road3.png"), pygame.image.load("Road3.png"), pygame.image.load("Road4.png"), pygame.image.load("Road4.png")]
    b = 0

    while True:
        #Events
        for event in pygame.event.get():
            if crashed == True and update == 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        GameLoop(screen)
                        return

            if crashed == True and update > 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        GameLoop(screen)
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        scores[(update - 1)*2] = scores[(update - 1)*2][:-1]
                    elif event.key != pygame.K_LSHIFT and event.key != pygame.K_RSHIFT and len(scores[(update - 1)*2]) < 3:
                        if chr(event.key).isalpha() or chr(event.key).isdigit():
                            scores[(update - 1)*2] = scores[(update - 1)*2] + str(chr(event.key).upper())
                    

            if event.type == pygame.KEYDOWN and crashed == False:
                if event.key == pygame.K_SPACE:
                    paused = not paused
    
            if event.type == pygame.QUIT:
                screen.close_win()

        #Key Holds
        keys = pygame.key.get_pressed()
        if not crashed and not paused:
            if keys[pygame.K_LEFT]:
                car.x += -car.steerSpeed
            if keys[pygame.K_RIGHT]:
                car.x += car.steerSpeed

        #DRAW
        screen.gameDisplay.blit(background[b], (0, 0))
        if not crashed and not paused:
            b += 1
        if b == 8:
            b = 0

        obstacle.draw(screen)
        car.draw(screen)
        screen.message(["Score: " + str(score)], screen.width/5, screen.height/20, color=yellow)


        #Adjust Scene
        if not crashed and not paused:
            obstacle.y += obstacle.speed
        
        if paused == True:
            screen.message(["PAUSE"], screen.width/2, screen.height/3, font=font, size = 115, color=dgreen)
        
        #things_dodged(score)
        if car.x <= 58 or car.x + car.width >= screen.width - 58:
            crashed = True
            update = crashed_message(score, update)
        if obstacle.y > screen.height:
            obstacle.y = 0 - obstacle.height
            obstacle.x = random.randrange(62, screen.width - obstacle.width - 60)
            score += 1
            obstacle.speed += 1
            car.steerSpeed += .05

        #Collision Detection With Obstacle
        if car.y + 7 < obstacle.y+obstacle.height and car.y + 109 > obstacle.y:
            if car.x + 30 > obstacle.x and car.x + 30 < obstacle.x + obstacle.width or car.x + car.width - 25 > obstacle.x and car.x + car.width - 25 < obstacle.x + obstacle.width:
                update = crashed_message(score, update)
                crashed = True
        if car.y + 110 < obstacle.y+obstacle.height and car.y + car.noSpoiler > obstacle.y:
            if car.x > obstacle.x and car.x < obstacle.x + obstacle.width or car.x + car.width > obstacle.x and car.x + car.width < obstacle.x + obstacle.width:
                update = crashed_message(score, update)
                crashed = True        
        #UPDATE SCREEN
        pygame.display.update()


scores = []
with open("HighScore.txt", "r") as f:
    for line in f:
        try:
            scores.append(int(line[:-1]))
        except ValueError:
            scores.append(line[:-1])
        

screen = Window(800, 600, "PyCarGame", 60)
start_screen(screen)



