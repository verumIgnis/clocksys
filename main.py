import pygame
from pygame.locals import *
import time
import requests
import platform
import subprocess
import datetime

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

def getFont(size):
    var = pygame.font.SysFont("Berlin Sans FB Regular.ttf", size)
    return var

font169 = getFont(169)
font16 = getFont(16)
font20 = getFont(20)
font27 = getFont(27)
font80 = getFont(80)
font35 = getFont(35)

pos1 = (10, 10)
pos2 = (10, 50)
pos3 = (10, 90)
pos4 = (10, 130)
pos5 = (10, 170)
pos6 = (10, 210)

totalValueFloat = 0.0
totalValueStr = "0"

log1 = "-"
log2 = "-"
log3 = "-"
log4 = "-"
log5 = "-"
log6 = "-"

size = (480, 320)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("clockSys")
clock = pygame.time.Clock()

url = 'http://127.0.0.1:5000/clocksys/'

keepAliveCount = 5900
needKA = True
dispKAError = True
upload = False
KAnext = False
clockInNext = False
clockOutNext = False
clockedIn = True
total = 0
timeOffset = 0

backdrop=pygame.image.load("backdrop.png")
settingsBackdrop=pygame.image.load("settingsBackdrop.png")
serverError=pygame.image.load("serverError.png")
serverOk=pygame.image.load("serverOk.png")
uploadIcon=pygame.image.load("uploadIcon.png")
settingsIcon=pygame.image.load("settingsIcon.png")

totalLine = font80.render("Total:", 1, (255, 255, 255))

setting1 = font35.render("Pay", 1, (255, 255, 255))
setting2 = font35.render("Time offset", 1, (255, 255, 255))
setting3 = font35.render("Server URL", 1, (255, 255, 255))
setting4 = font35.render("setting4", 1, (255, 255, 255))
setting5 = font35.render("setting5", 1, (255, 255, 255))
setting6 = font35.render("setting6", 1, (255, 255, 255))

settingsBtn = pygame.Rect(430, 8, 48, 48)



if True:
    level = 0
    abort = False
    while not abort:
        
        if clockInNext:
            currentTime = datetime.datetime.now()
            log1 = f"Clock in @{currentTime.hour}:{currentTime.minute}"
            sendJson = {"minute": currentTime.minute, "hour": currentTime.hour}
            x = requests.post(url=f"{url}clockin", json=sendJson)
            clockInNext = False
            upload = False

        if clockOutNext:
            currentTime = datetime.datetime.now()
            log1 = f"Clock out @{currentTime.hour}:{currentTime.minute}"
            sendJson = {"minute": currentTime.minute, "hour": currentTime.hour}
            x = requests.post(url=f"{url}clockout", json=sendJson)
            total = x
            clockOutNext = False
            upload = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                abort = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if level == 1:
                        clockedIn = not clockedIn
                        upload = True

                        log6 = log5
                        log5 = log4
                        log4 = log3
                        log3 = log2
                        log2 = log1

                        if clockedIn == False:
                            clockInNext = True
                        else:
                            clockOutNext = True

            elif event.type == MOUSEBUTTONDOWN:
                if settingsBtn.collidepoint(event.pos):
                    if level == 2:
                        level = 1
                    elif level == 1:
                        level = 2

        if KAnext:
            KAnext = False
            keepAliveCount = 0
            needKA = True

            x = requests.get(f"{url}keepalive")
            print(f"KA: {x.text}")
            if x.text == "True":
                needKA = False
            upload = False

        else:
            keepAliveCount+=1

        if keepAliveCount == 6000:
            KAnext = True
            upload = True
        if level == 0:
            level = 1

        elif level == 1:
            screen.blit(backdrop, (0, 0))
            if needKA:
                screen.blit(serverError, (247, 8))
            else:
                screen.blit(serverOk, (247, 8))

            if upload:
                screen.blit(uploadIcon, (290, 8))

            screen.blit(settingsIcon, (430, 8))

            textLine1 = font35.render(log1, 1, (255, 255, 255))
            textLine2 = font35.render(log2, 1, (255, 255, 255))
            textLine3 = font35.render(log3, 1, (255, 255, 255))
            textLine4 = font35.render(log4, 1, (255, 255, 255))
            textLine5 = font35.render(log5, 1, (255, 255, 255))
            textLine6 = font35.render(log6, 1, (255, 255, 255))

            screen.blit(textLine1, (pos1))
            screen.blit(textLine2, (pos2))
            screen.blit(textLine3, (pos3))
            screen.blit(textLine4, (pos4))
            screen.blit(textLine5, (pos5))
            screen.blit(textLine6, (pos6))

            totalValueLine = font35.render(f"{totalValueStr}hours <min>min", 1, (255, 255, 255))
            screen.blit(totalLine, (280, 90))
            screen.blit(totalValueLine, (280, 145))
            
        elif level == 2:
            screen.blit(settingsBackdrop, (0, 0))

            screen.blit(setting1, (pos1))
            screen.blit(setting2, (pos2))
            screen.blit(setting3, (pos3))
            screen.blit(setting4, (pos4))
            screen.blit(setting5, (pos5))
            screen.blit(setting6, (pos6))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()



#    img=pygame.image.load(filename)
#    screen.blit(img,(0,0))

#line1 = pygame.Rect(0, 64, 240, 6)
#pygame.draw.rect(screen, "WHITE", line1)
