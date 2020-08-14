from pygame import *
def ticTacToe(theme):
    screen = display.set_mode((1250, 750), FULLSCREEN)
    init()
    font.init()
    global player1Points, player2Points, reset

    calibriBold50 = font.SysFont("Calibri Bold", 50)
    calibriBold60 = font.SysFont("Calibri Bold", 60)
    calibriBold80 = font.SysFont("Calibri Bold", 80)

    board = [[0,0,0],
             [0,0,0],
             [0,0,0]]
    gameIsLive = True
    outCome = None
    reset = False
    turn = 1
    player1Points = 0
    player2Points = 0
    rects = []
    for i in range (0,3):
        for j in range(0,3):
            rects.append(Rect(125+150*j, 200+150*i, 150, 150))

    def playerTurn(board, turn, rects):
        mb=mouse.get_pressed()
        mx,my=mouse.get_pos()

        turnComplete = False
        for rect in rects:
            if rect.collidepoint(mx,my):
                if mb[0] == 1:
                    pos = (rects.index(rect)+1)
                    if pos <= 3:
                        if board [0][pos-1] == 0:
                            board [0][pos-1] = turn
                            turnComplete = True      
                    elif pos <= 6:
                        if board[1][pos - 4] == 0:
                            board[1][pos - 4] = turn
                            turnComplete = True
                    elif pos <= 9:
                        if board[2][pos - 7] == 0:
                            board[2][pos - 7] = turn
                            turnComplete = True

        if turnComplete:
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1              

        return(turn)                  
                    
    def evaluate(board):
        global player1Points, player2Points
        for row in board: #check horizontal wins
            if row[0] == row[1] == row[2] == 1 or row[0] == row[1] == row[2] == 2:
                    return (row[0])
        for i in range(0,3): #check vertical wins
            if board[0][i] == board[1][i] == board[2][i] == 1 or board[0][i] == board[1][i] == board[2][i] == 2:
                    return (board[0][i])

        if board[0][0] == board[1][1] == board[2][2] == 1 or board[0][0] == board[1][1] == board[2][2] == 2: #check diagonal wins
                return (board[0][0])
        elif board[0][2] == board[1][1] == board[2][0] == 1 or board[0][2] == board[1][1] == board[2][0] == 2:
                return (board[0][2])

        numOfEmptySpots = 0 #checks for draw
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j] == 0:
                    numOfEmptySpots += 1
        if numOfEmptySpots == 0:
            return(0)

    def drawScreen(board, rects, outCome):
        global reset, player1Points, player2Points
        screen.fill(theme[0])
        titleTxt = calibriBold80.render("Tic Tac Toe", True, theme[1])
        screen.blit(titleTxt,(200, 80))

        for rect in rects:
            draw.rect(screen,theme[1], rect,1)
            
        for i in range(0,3):
            for j in range(0,3):
                if board[i][j] == 1:
                    draw.line(screen,(255,255,255),(150 * j + 145, 150 * i + 220),(150 * j + 250, 150 * i + 325),5)
                    draw.line(screen,(255,255,255),(150 * j + 145, 150 * i + 325),(150 * j + 250, 150 * i + 220),5)
                elif board[i][j] == 2:
                    draw.circle(screen,(255,255,255),(150 * j + 200, 150 * i + 275),60, 5)

        if gameIsLive:
            gameTxt = ("PLAYER "+str(turn)+"'s TURN")
        else:
            if outCome != 0:
                gameTxt = ("PLAYER "+str(outCome)+" WINS")
            else:
                gameTxt = ("DRAW")

            playAgainRect = Rect(750, 325, 325, 75)
            draw.rect(screen, theme[1], playAgainRect, 3)
            mb = mouse.get_pressed()
            mx, my = mouse.get_pos()
            if playAgainRect.collidepoint(mx, my):
                draw.rect(screen, (255, 255, 255), playAgainRect, 3)
                if mb[0] == 1:
                    reset = True

            playAgainText = calibriBold60.render("Play Again", True, theme[1])
            screen.blit(playAgainText, (800, 340))

        text = calibriBold60.render((gameTxt), True, theme[1])
        if gameTxt == "DRAW":
            screen.blit(text, (850, 250))
        else:
            screen.blit(text, (750, 250))

        player1PointsTxt = calibriBold50.render("Player 1 Points: "+str(player1Points), True, theme[1])
        player2PointsTxt = calibriBold50.render("Player 2 Points: "+str(player2Points), True, theme[1])

        screen.blit(player1PointsTxt, (750, 475))
        screen.blit(player2PointsTxt, (750, 540))

        resetTxt = calibriBold50.render("Reset Score", True, theme[1])
        screen.blit(resetTxt, (808, 608))
        resetBtnRect = Rect(780, 600, 250, 50)
        draw.rect(screen, theme[1], resetBtnRect, 3)
        mb = mouse.get_pressed()
        mx, my = mouse.get_pos()
        if resetBtnRect.collidepoint(mx, my):
            draw.rect(screen, (255, 255, 255), resetBtnRect, 3)
            if mb[0] == 1:
                player1Points = 0
                player2Points = 0


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
    while running:
        for evt in event.get():
            if evt.type==QUIT:
                return "lobby"

        if gameIsLive:
            turn = playerTurn(board,turn, rects)

            outCome = evaluate(board)
            if outCome != None:
                if outCome == 1:
                    player1Points += 1
                elif outCome == 2:
                    player2Points += 1

                gameIsLive = False

        if reset:
            board = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]]
            gameIsLive = True
            turn = 1
            reset = False
                    
        isExit = drawScreen(board, rects, outCome)
        if isExit:
            return "lobby"
