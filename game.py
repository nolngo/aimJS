import pygame, sys, random, time, math

check_errors = pygame.init()

if check_errors[1] > 0:
    print("(!) Had {0} initialising errors".format(check_errors[1]))
    print("Exiting...")
    sys.exit(-1)
else:
    print("(+) PyGame successfully initialised!")

#Play Surface
width = 852
height = 480
playSurface = pygame.display.set_mode((width, height))
pygame.display.set_caption('aimPY')

#Colo(u)rs
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)

#FPS controller
tick_rate = 30
fpsController = pygame.time.Clock()

#Game state
tickCounter = 0
spawnTargetTimer = 30
aimPoints = []
score = 0
lives = 3
widthMax = 40


#Game over function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    gameOverSurface = myFont.render('Game Over!', True, red)
    gameOverRectangle = gameOverSurface.get_rect()
    gameOverRectangle.midtop = (width/2, height/20)
    playSurface.blit(gameOverSurface, gameOverRectangle)
    showScore(0)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

def showScore(choice=1):
    sFont = pygame.font.SysFont('monaco', 36)
    scoreSurface = sFont.render('Score: {0}'.format(score), True, red)
    scoreRectangle = scoreSurface.get_rect()
    if choice == 1:
        scoreRectangle.midtop=(width/20,height/20)
    else:
        scoreRectangle.midtop=(width/2,height/4)
    playSurface.blit(scoreSurface,scoreRectangle)

def showMisses():
    sFont = pygame.font.SysFont('monaco', 36)
    scoreSurface = sFont.render('Lives: {0}'.format(lives), True, red)
    scoreRectangle = scoreSurface.get_rect()
    scoreRectangle.midtop=(width-(width/20),height/20)
    playSurface.blit(scoreSurface,scoreRectangle)

def timer():
    tFont = pygame.font.SysFont('monaco', 24)

def distance(A, B):
    return math.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)

#Main game logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.quit))   
        if event.type == pygame.MOUSEBUTTONDOWN:
            foundPoint = False
            for point in aimPoints:
                if not foundPoint and distance(event.pos, point) < point[2]:
                    if point[3]:
                        score+= (widthMax - point[2])
                    else:
                        score+= (50 + (widthMax - point[2]))
                        foundPoint = True
                    aimPoints.remove(point)
            if not foundPoint:
                lives-=1

    
    if tickCounter == spawnTargetTimer:
        tickCounter = 0
        aimPoints.insert(0,
        [random.randrange(1,width),
        random.randrange(1,height), 0, False])
        print(aimPoints)
    else:
        tickCounter+=1

    playSurface.fill(black)
    
    for point in aimPoints:
        if point[3]:
            if point[2] == 0:
                aimPoints.remove(point)
                lives-=1
            else:
                point[2]-=1
        else:
            if point[2] == widthMax:
                point[3] = True
            point[2]+=1
        pygame.draw.circle(playSurface, red, 
        (point[0], point[1]), point[2])

    if lives == 0:
        gameOver()

    showScore()
    showMisses()
    pygame.display.flip()
    fpsController.tick(tick_rate)
