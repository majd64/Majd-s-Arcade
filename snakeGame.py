from pygame import *
from random import randint
def snake(theme):
    screen = display.set_mode((1250, 750), FULLSCREEN)
    init()
    font.init()
    global moveSnakeTimer, score, food, needFood, restart, posUpdated

    calibriBold50 = font.SysFont("Calibri Bold", 50)
    calibriBold60=font.SysFont("Calibri Bold",60)
    calibriBold80 = font.SysFont("Calibri Bold", 80)

    snake = [[2, 10], [3,10],[4,10]]
    direction = "right"
    score = 3
    moveSnakeTimer = 0
    needFood = True
    restart = False
    posUpdated = True
    snakeCanMove = False

    def getHighScore():
        scoreFile=open("scores.txt","r") 
        scores=scoreFile.readlines()
        scoreFile.close() 
        highScore = 0
        for i in scores:
            i = int(i.strip())
            if i > highScore:
                highScore = i
        return(highScore)

    def moveSnake(direction, snake):
        global moveSnakeTimer, posUpdated
        newSnake = [x[:] for x in snake]

        moveSnakeTimer += 1
        if moveSnakeTimer >= 8:
            snakeHead = newSnake[-1]
            if direction == "up":
                snakeHead[1] -= 1
            elif direction == "down":
                snakeHead[1] += 1
            elif direction == "right":
                snakeHead[0] += 1
            elif direction == "left":
                snakeHead[0] -= 1
                
            snake.append(snakeHead)
            del snake[0]
            moveSnakeTimer = 0
            posUpdated = True

    def getFood(snake):
        global food, score, needFood
        if needFood:
            food = [randint(1,30), randint(1,20)]
            needFood = False
        
        snakeHead = snake[-1]
        if snakeHead == food:
            tailAdded = False
            newSnake = [x[:] for x in snake]
            snakeTail = newSnake[0]
        
            if direction == "up" and snake.count([snakeTail[0], snakeTail[1]+1]) == 0:
                newSnakeTail = [snakeTail[0], snakeTail[1]+1]
                tailAdded = True
            elif direction == "down" and snake.count([snakeTail[0], snakeTail[1]-1]) == 0:
                newSnakeTail = [snakeTail[0], snakeTail[1]-1]
                tailAdded = True
            elif direction == "left" and snake.count([snakeTail[0]+1, snakeTail[1]]) == 0:
                newSnakeTail = [snakeTail[0]+1, snakeTail[1]]
                tailAdded = True
            elif direction == "right" and snake.count([snakeTail[0]-1, snakeTail[1]]) == 0:
                newSnakeTail = [snakeTail[0]-1, snakeTail[1]]
                tailAdded = True

            if tailAdded == False:
                if snake.count([snakeTail[0], snakeTail[1]+1]) == 0:
                    newSnakeTail = [snakeTail[0], snakeTail[1]+1]
                elif snake.count([snakeTail[0], snakeTail[1]-1]) == 0:
                    newSnakeTail = [snakeTail[0], snakeTail[1]-1]
                elif snake.count([snakeTail[0]+1, snakeTail[1]]) == 0:
                    newSnakeTail = [snakeTail[0]+1, snakeTail[1]]
                elif snake.count([snakeTail[0]-1, snakeTail[1]]) == 0:
                    newSnakeTail = [snakeTail[0]-1, snakeTail[1]]

            score += 1
            snake.insert(0,newSnakeTail)
            needFood = True

    def checkDeath(snake, direction):
        global restart 
        if snake[-1][0] > 30 or snake[-1][0] < 1 or snake[-1][1] > 20 or snake[-1][1] < 1:
            restart = True
        if snake.count(snake[-1]) > 1:
            restart = True
        
    def drawScreen(snake):
        titleTxt = calibriBold80.render("Python", True, theme[1])
        scoreTxt = calibriBold60.render(str(score), True, theme[1])
        scoreTxt2 = calibriBold60.render("SCORE:", True, theme[1])
        highScoreTxt = calibriBold60.render(str(getHighScore()), True, theme[1])
        highScoreTxt2 = calibriBold60.render("HIGH", True, theme[1])
        highScoreTxt3 = calibriBold60.render("SCORE:", True, theme[1])

        screen.fill((theme[0]))

        screen.blit(titleTxt, (400, 40))
        screen.blit(scoreTxt2,(950, 150))
        screen.blit(scoreTxt,(1150, 150))
        screen.blit(highScoreTxt2,(950, 300))
        screen.blit(highScoreTxt3,(950, 350))
        screen.blit(highScoreTxt,(1150, 350))

        draw.rect(screen,theme[1],(30, 120, 900, 600),5)
        draw.rect(screen,theme[1],(food[0]*30, food[1]*30+90, 30, 30))
        for i in snake:
            x = i[0]
            y = i[1]
            if i == snake[-1]:
                draw.rect(screen,(143,188,143),(x*30, y*30+90, 30, 30),5)
            else:
                newSnake = [x[:] for x in snake]
                newSnake.reverse()
                if newSnake.index(i) <= 20:
                    draw.rect(screen,(0,55+(10*newSnake.index(i)),0),(x*30, y*30+90, 30, 30))
                elif newSnake.index(i) <= 40:
                    draw.rect(screen,(55+(10*(newSnake.index(i)-20)),0,0),(x*30, y*30+90, 30, 30))
                elif newSnake.index(i) <= 60:
                    draw.rect(screen,(0,0,55+(10*(newSnake.index(i)-40))),(x*30, y*30+90, 30, 30))
                elif newSnake.index(i) <= 80:
                    draw.rect(screen,(55+(10*(newSnake.index(i)-60)),55+(10*(newSnake.index(i)-60)),0),(x*30, y*30+90, 30, 30))
                elif newSnake.index(i) <= 100:
                    draw.rect(screen,(55+(10*(newSnake.index(i)-80)),0,55+(10*(newSnake.index(i)-80))),(x*30, y*30+90, 30, 30))
                elif newSnake.index(i) <= 120:
                    draw.rect(screen,(0,55+(10*(newSnake.index(i)-100)),55+(10*(newSnake.index(i)-100))),(x*30, y*30+90, 30, 30))
                else:
                    draw.rect(screen,(255,255,255),(x*30, y*30+90, 30, 30))

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

    running=True
    myClock=time.Clock()
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                return "lobby"
               
            if evt.type == KEYDOWN:
                snakeCanMove = True
                
        if restart:
            if score > getHighScore():
                scoreFile=open("scores.txt","w")
                scoreFile.write(str(score)+"\n")
                scoreFile.close()

            snake = [[2, 10], [3,10],[4,10]]
            score = 3
            direction = "right"
            snakeCanMove = False
            needFood = True
            restart = False

        keys=key.get_pressed()
        if (direction == "up" or direction == "down") and posUpdated:
            if keys[K_RIGHT] or keys[K_d]:
                direction = "right"
                posUpdated = False
            elif keys[K_LEFT] or keys[K_a]:
                direction = "left"
                posUpdated = False
        elif (direction == "right" or direction == "left") and posUpdated:
            if keys[K_UP] or keys[K_w]:
                direction = "up"
                posUpdated = False
            elif keys[K_DOWN] or keys[K_s]:
                direction = "down"
                posUpdated = False

        getFood(snake)
        if snakeCanMove:
            moveSnake(direction, snake)
        checkDeath(snake, direction)

        isExit = drawScreen(snake)
        if isExit:
            return "lobby"
        
        myClock.tick(60)