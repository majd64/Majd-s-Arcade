from pygame import *
def breakout(theme):
    screen = display.set_mode((1250, 750), FULLSCREEN)
    init()
    font.init()
    global VX, VY, paddleX, paddleY, score, numOfBricksBroken, speedBall, redHit, numOfTotalBricksBroken

    calibriBold50 = font.SysFont("Calibri Bold", 50)
    calibriBold60 = font.SysFont("Calibri Bold", 60)
    calibriBold80 = font.SysFont("Calibri Bold", 80)

    paddleX = 400
    paddleY = 650
    paddleWidth = 200
    ballX = int(paddleX + paddleWidth/2)
    ballY = int(paddleY - 10)
    VX = 3
    VY = 5

    winner = False
    isBallLive = False
    score = 0
    lives = 3
    speedBall = False
    numOfBricksBroken = 0
    numOfTotalBricksBroken = 0
    is4BricksBroken = False
    is12BricksBroken = False
    isRoofHit = False
    redHit = False

    class Brick():
        posOfBricks = [[1 for x in range (1,11)] for x in range (1,9)]

        def __init__(self, color, points):
            self.color = color
            self.points = points

    redbrick = Brick((255,0,0), 7)
    orangebrick = Brick((255,128,0), 5)
    greenbrick = Brick((0,255,0), 3)
    yellowbrick = Brick((0,0,255), 1)

    def getHighScore():
        scoreFile=open("breakoutscores.txt","r")
        scores=scoreFile.readlines()
        scoreFile.close()
        highScore = 0
        for i in scores:
            i = int(i.strip())
            if i > highScore:
                highScore = i
        return(highScore)

    def drawScreen(ballX, ballY, paddleX, paddleY, paddleWidth, lives):
        global redHit, VX, VY, score, numOfBricksBroken, numOfTotalBricksBroken, speedBall

        titleTxt = calibriBold80.render("Break Out", True, theme[1])
        scoreTxt = calibriBold60.render(str(score), True, theme[1])
        scoreTxt2 = calibriBold60.render("SCORE:", True, theme[1])
        liveTxt = calibriBold60.render("LIVES:", True, theme[1])
        liveTxt2 = calibriBold60.render(str(lives), True, theme[1])
        highScoreTxt = calibriBold60.render(str(getHighScore()), True, theme[1])
        highScoreTxt2 = calibriBold60.render("HIGH", True, theme[1])
        highScoreTxt3 = calibriBold60.render("SCORE:", True, theme[1])

        screen.fill((theme[0]))

        draw.rect(screen, theme[1], (30, 120, 900, 600), 5)  # border
        draw.rect(screen, theme[1], (paddleX, paddleY, paddleWidth, 10))  # paddle
        draw.circle(screen, theme[1], (ballX, ballY), 10)  # ball

        screen.blit(titleTxt, (370, 40))
        screen.blit(scoreTxt2, (950, 300))
        screen.blit(scoreTxt, (1150, 300))
        screen.blit(highScoreTxt2, (950, 400))
        screen.blit(highScoreTxt3, (950, 450))
        screen.blit(highScoreTxt, (1150, 450))
        screen.blit(liveTxt, (950, 150))
        screen.blit(liveTxt2, (1150, 150))

        for row in range (len(Brick.posOfBricks)):
            if row == 0 or row == 1:
                brick = redbrick
            elif row == 2 or row == 3:
                brick = orangebrick
            elif row == 4 or row == 5:
                brick = greenbrick
            elif row == 6 or row == 7:
                brick = yellowbrick
            for i in range (len(Brick.posOfBricks[row])):
                if Brick.posOfBricks[row][i] != "":
                    brickX = 86*i+50
                    brickY = 45*row+200
                    brickWidth = 80
                    brickHeight = 30
                    draw.rect(screen,brick.color,(brickX, brickY, brickWidth, brickHeight))

                    leftSideRect = Rect(brickX, brickY, 1, brickHeight)
                    rightSideRect = Rect(brickX + brickWidth, brickY, 1, brickHeight)
                    upSideRect = Rect(brickX, brickY, brickWidth, 1)
                    downSideRect = Rect(brickX, brickY+brickHeight, brickWidth, 1)

                    hit = False
                    ballRect = Rect(ballX - 10, ballY - 10, 20, 20)
                    if ballRect.colliderect(leftSideRect): #brick collision
                        VX = abs(VX) * -1
                        hit = True
                    if ballRect.colliderect(rightSideRect):
                        VX = abs(VX)
                        hit = True
                    if ballRect.colliderect(upSideRect):
                        VY = abs(VY) * -1
                        hit = True
                    if ballRect.colliderect(downSideRect):
                        VY = abs(VY)
                        hit = True

                    if hit: #there was a brick collision
                        Brick.posOfBricks[row][i] = ""
                        score += brick.points
                        numOfBricksBroken += 1
                        numOfTotalBricksBroken += 1
                        if brick == redbrick and redHit == True: #first red brick -> speed up
                            redHit = False
                            speedBall = True

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
                isBallLive = True

        if isBallLive:
            ballX += VX #moving ball
            ballY += VY

            keys = key.get_pressed() #moving paddle
            if keys[K_RIGHT] and paddleX < 930 - paddleWidth:
                paddleX += 10
            if keys[K_LEFT] and paddleX > 30:
                paddleX -= 10

        leftPaddleRect = Rect(paddleX, paddleY, int(paddleWidth/2), 1) #paddle collision
        rightPaddleRect = Rect(paddleX+ int(paddleWidth/2), paddleY, int(paddleWidth/2), 1)
        ballRect = Rect(ballX - 10, ballY - 10, 20, 20)
        if ballRect.colliderect(leftPaddleRect):
            VY *= -1
            VX = abs(VX) * -1
            ballY -= 5
        elif ballRect.colliderect(rightPaddleRect):
            VY *= -1
            VX = abs(VX)
            ballY -= 5

        if ballX <= 30 or ballX >= 930: #left and right wall collision
            VX *= -1
        if ballY <= 120: #roof collision
            VY *= -1
            if isRoofHit == False: #first roof hit -> cutting paddle in half
                paddleWidth = int(paddleWidth / 2)
                isRoofHit = True

        if numOfTotalBricksBroken == 80: #winner
            winner = True

        if ballY >= 720 or winner: #ground collision (player died)
            if winner == False:
                lives -= 1
            isBallLive = False
            VX = 2
            VY = 4
            ballX = int(paddleX + paddleWidth / 2)
            ballY = int(paddleY - 10)
            numOfBricksBroken = 0
            is4BricksBroken = False
            is12BricksBroken = False
            if lives == 0: #player is out
                lives = 3
                isRoofHit = False
                paddleWidth = 200
                Brick.posOfBricks = [[1 for x in range (1,11)] for x in range (1,9)]
                numOfTotalBricksBroken = 0
                if score > getHighScore():
                    scoreFile = open("breakoutscores.txt", "w")
                    scoreFile.write(str(score) + "\n")
                    scoreFile.close()
                score = 0
            if winner:
                Brick.posOfBricks = [[1 for x in range(1, 11)] for x in range(1, 9)]
                winner = False
                numOfTotalBricksBroken = 0

        if numOfBricksBroken >= 4 and is4BricksBroken == False: #4 bricks
            is4BricksBroken = True
            speedBall = True

        if numOfBricksBroken >= 12 and is12BricksBroken == False: #12 bricks
            is12BricksBroken = True
            speedBall = True

        if speedBall: #speeding ball
            if VX < 0:
                VX -= 1
            elif VX > 0:
                VX += 1

            if VY < 0:
                VY -= 1
            elif VY > 0:
                VY += 1
            speedBall = False

        isExit = drawScreen(ballX, ballY, paddleX, paddleY, paddleWidth, lives)
        if isExit:
            return "lobby"

        myclock.tick(60)
