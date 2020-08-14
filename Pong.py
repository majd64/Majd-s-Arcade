from pygame import *
from random import randint
def pongGame(theme):
    screen = display.set_mode((1250, 750), FULLSCREEN)
    init()
    font.init()
    global X, Y, VX, VY, p1Pts, p2Pts, restart, isGameLive

    calibriBold50 = font.SysFont("Calibri Bold",50)
    calibriBold60 = font.SysFont("Calibri Bold", 60)
    calibriBold80 = font.SysFont("Calibri Bold", 80)

    restart = False
    isGameLive = False
    winner = None

    p1Pts = 0
    p2Pts = 0
    p1Y = 300
    p2Y = 300

    X = 435
    Y = 240
    directionRand = randint(0,1)
    if directionRand == 0:
        VX = -8
    else:
        VX = 8
    directionRand = randint(0, 1)
    if directionRand == 0:
        VY = -4
    else:
        VY = 4

    def checkCollision(p1Y, p2Y):
        global VX, VY, X , Y, p1Pts, p2Pts
        paddleHit = False
        resetSpeed = False

        ballRect = Rect(X-10, Y-10, 20, 20)
        p1Rect = Rect(110, p1Y, 1, 100)
        p2Rect = Rect(860, p2Y, 1, 100)

        if ballRect.colliderect(p1Rect):
            X += 10
            paddleHit = True
        elif ballRect.colliderect(p2Rect):
            X -= 10
            paddleHit = True
        if paddleHit:
            VX *= -1
            if VX < 0:
                VX -= 0.2
            elif VX > 0:
                VX += 0.2
            if VY < 0:
                VY -= 0.1
            elif VY > 0:
                VY += 0.1

        if X < 30:
            p2Pts += 1
            X = 800
            resetSpeed = True
        elif X > 930:
            p1Pts += 1
            X = 160
            resetSpeed = True
        if resetSpeed:
            if VX < 0:
                VX = -8
            elif VX > 0:
                VX = 8
            if VY < 0:
                VY = -4
            elif VY > 0:
                VY = 4

        if Y < 120 or Y > 720:
            VY *= -1

    def drawScreen():
        global VX, VY, X, Y, p1Pts, p2Pts, restart, isGameLive

        titleTxt = calibriBold80.render("Pong", True, theme[1])

        screen.fill((theme[0]))

        if winner == None:
            p1PtsTxt = calibriBold50.render("P1 Points: " + str(p1Pts)+"/16", True, theme[1])
            p2PtsTxt = calibriBold50.render("P2 Points: " + str(p2Pts)+"/16", True, theme[1])
            screen.blit(p1PtsTxt, (950, 250))
            screen.blit(p2PtsTxt, (950, 350))
        else:
            winnerTxt = calibriBold80.render("Player " + str(winner) + " Wins!", True, theme[1])
            screen.blit(winnerTxt, (275, 300))

        screen.blit(titleTxt, (440, 40))

        draw.rect(screen, theme[1], (30, 120, 900, 600), 5)  # border
        draw.rect(screen, theme[1], (80, p1Y, 30, 100))  # player 1 paddle
        draw.rect(screen, theme[1], (860, p2Y, 30, 100))  # player 2 paddle
        draw.circle(screen, theme[1], (X, Y), 10)  # ball

        if isGameLive == False:
            pressKeyTxt = calibriBold60.render("Press any key to start", True, theme[1])
            screen.blit(pressKeyTxt, (260, 400))

        restartTxt = calibriBold50.render("Restart", True, theme[1])
        screen.blit(restartTxt,(1015,470))
        restartBtnRect = Rect(950, 450, 275, 75)
        draw.rect(screen, theme[1], restartBtnRect, 3)
        mb = mouse.get_pressed()
        mx, my = mouse.get_pos()
        if restartBtnRect.collidepoint(mx, my):
            draw.rect(screen, (255, 255, 255), restartBtnRect, 3)
            if mb[0] == 1:
                restart = True

        exitTxt = calibriBold50.render("Exit", True, theme[1])
        screen.blit(exitTxt, (40, 30))
        exitBtnRect = Rect(20, 20, 120, 50)
        draw.rect(screen, theme[1], exitBtnRect, 3)
        mb = mouse.get_pressed()
        mx, my = mouse.get_pos()
        if exitBtnRect.collidepoint(mx, my):
            draw.rect(screen, (255, 255, 255), exitBtnRect, 3)
            if mb[0] == 1:
                return True

        display.flip()

    myclock = time.Clock()
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "lobby"

            if evt.type == KEYDOWN:
                isGameLive = True
                if winner != None:
                    restart = True

        if isGameLive:
            X += round(VX)
            Y += round(VY)

            keys = key.get_pressed()
            if (keys[K_UP] or keys[K_p]) and p2Y > 120:
                p2Y -= 8
            elif (keys[K_DOWN] or keys[K_l]) and p2Y < 620:
                p2Y += 8
            if keys[K_w] and p1Y > 120:
                p1Y -= 8
            elif keys[K_s] and p1Y < 620:
                p1Y += 8

        if restart:
            if winner == None:
                isGameLive = False
            winner = None
            p1Pts = 0
            p2Pts = 0
            restart = False
            X = 435
            Y = 240
            directionRand = randint(0, 1)
            if directionRand == 0:
                VX = -8
            else:
                VX = 8
            directionRand = randint(0, 1)
            if directionRand == 0:
                VY = -4
            else:
                VY = 4

        if p1Pts == 16:
            isGameLive = False
            winner = 1
        if p2Pts == 16:
            isGameLive = False
            winner = 2

        checkCollision(p1Y, p2Y)
        isExit = drawScreen()
        if isExit:
            return "lobby"

        myclock.tick(60)