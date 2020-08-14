from pygame import *
from snakeGame import snake
from ticTacToe import ticTacToe
from Pong import pongGame
from Breakout import breakout
global theme

BLACK = (0,0,0)
WHITE = (255,255,255)
DARKRED = (167,65,74)
SKYBLUE = (135,206,250)
MIDNIGHTBLUE = (20,69,89)
LIGHTYELLOW = (244,180,26)
NAVYBLUE = (33,57,112)
LIGHTBLACK = (28,27,26)
ULTRAVIOLET = (95, 75, 139)
BLOOMINGDAHLIA = (230,154,141)
BLUE = (0,164,204)
ORANGE = (249,87,0)
GRAY = (96,96,96)
LIMEPUNCH = (214,237,23)

themes = [[DARKRED, LIGHTBLACK],[MIDNIGHTBLUE, LIGHTYELLOW],[LIGHTYELLOW, MIDNIGHTBLUE],[ULTRAVIOLET, BLOOMINGDAHLIA],[BLUE, ORANGE],[GRAY,LIMEPUNCH]]
theme = (themes[1])

font.init()
calibriBold50 = font.SysFont("Calibri Bold", 50)
calibriBold80 = font.SysFont("Calibri Bold", 80)

pythonRect = Rect(150,200,400,150)
ticTacToeRect = Rect(700,200,400,150)
pongRect = Rect(150,450,400,150)
breakOutRect = Rect(700, 450, 400, 150)

pythonImg = image.load("images/python.png")
pongImg = image.load("images/pong.png")
ticTacToeImg = image.load("images/ticTacToe.png")
breakOutImg = image.load("images/breakOut.png")

def lobby():
    global theme
    running = True 
    myClock = time.Clock() 
    while running: 
        for evt in event.get(): 
             if evt.type == QUIT: 
                return "exit" 

        titleTxt = calibriBold80.render("WELCOME TO MAJD'S ARCADE", True, theme[1])

        screen.fill(theme[0])

        screen.blit(titleTxt, (200, 80))
        screen.blit(pythonImg,(155,200))
        screen.blit(pongImg, (155, 450))
        screen.blit(ticTacToeImg, (705, 200))
        screen.blit(breakOutImg, (705, 450))
        draw.rect(screen,(theme[1]),pythonRect, 5)
        draw.rect(screen, (theme[1]), ticTacToeRect, 5)
        draw.rect(screen, (theme[1]), pongRect, 5)
        draw.rect(screen, (theme[1]), breakOutRect, 5)

        mb = mouse.get_pressed()
        mx, my = mouse.get_pos()
        if pythonRect.collidepoint(mx, my):
            draw.rect(screen, WHITE, pythonRect, 5)
            if mb[0] == 1:
                return "snake"
        if ticTacToeRect.collidepoint(mx,my):
            draw.rect(screen, WHITE, ticTacToeRect, 5)
            if mb[0] == 1:
                return "tic tac toe"
        if pongRect.collidepoint(mx,my):
            draw.rect(screen, WHITE, pongRect, 5)
            if mb[0] == 1:
                return "pong"
        if breakOutRect.collidepoint(mx,my):
            draw.rect(screen, WHITE, breakOutRect, 5)
            if mb[0] == 1:
                return "break out"

        for i in range (len(themes)):
            circlePos = (180 + 75 * i, 670)
            colRect = Rect(160 + 75 * i, 650, 40, 40)
            draw.circle(screen, themes[i][0],circlePos,20)
            draw.circle(screen, themes[i][1],circlePos,23,3)
            if colRect.collidepoint(mx,my):
                if mb[0] == 1:
                    theme = themes[i]

        exitTxt = calibriBold50.render("Quit", True, theme[1])
        screen.blit(exitTxt, (40, 30))
        exitBtnRect = Rect(20, 20, 120, 50)
        draw.rect(screen, theme[1], exitBtnRect, 3)
        mb = mouse.get_pressed()
        mx, my = mouse.get_pos()
        if exitBtnRect.collidepoint(mx, my):
            draw.rect(screen, (255, 255, 255), exitBtnRect, 3)
            if mb[0] == 1:
                return "exit"
        
        display.flip() 
        myClock.tick(60)
        
page = "lobby"
while page != "exit":
    if page == "lobby":
        screen=display.set_mode((1250,750), FULLSCREEN)
        page = lobby()
    if page == "snake":
        page = snake(theme)
    if page == "tic tac toe":
        page = ticTacToe(theme)
    if page == "pong":
        page = pongGame(theme)
    if page == "break out":
        page = breakout(theme)
     
quit()