from Tkinter import *
from PIL import Image, ImageTk
import random
import time
import sys
import tkFont

def redrawAll():
    #Deletes everything on board and redraws it
    canvasWidth = canvas.data.canvasWidth
    canvasHeight = canvas.data.canvasHeight
    canvas.delete(ALL)
    drawBoard()
    if canvas.data.gameOver == True:
        canvas.create_rectangle(0,0,canvasWidth,canvasHeight,fill = "black") #Game over
        canvas.create_text(canvasWidth/2,canvasHeight/2,text = "GAME OVER", fill = 'white', font = 'Ariel 50 bold')
        canvas.create_text(canvasWidth/2,canvasHeight/2,text = "\n\n\n\n\n\n\n\n\n\n\n\nPress 'r' to Return to Menu", fill = 'white', font = 'Ariel 16 bold')
        canvas.create_text(canvasWidth/2,canvasHeight/2,text = '\n\n\n\n\nScore: %d'%canvas.data.finalScore,fill = 'red', font = 'Ariel 20 bold')
    if canvas.data.pauseScreen == True: #Screen is paused
        canvas.create_rectangle(0,0,canvasWidth,canvasHeight,fill = '')
        canvas.create_text(canvasWidth/2,canvasHeight/2,text = "PAUSE", fill = 'white', font = 'Ariel 50 bold')
        

def keyPressed(event):
    canvasWidth = canvas.data.canvasWidth
    canvasHeight = canvas.data.canvasHeight
    canvas.data.endTimer = True
    if canvas.data.gameOver == False:
        if (event.char == 'q'): #quit game: call game over and don't allow pause to be called
            unPauseScreen()
            gameOver()
        elif (event.char == 'p'):
            pauseScreen()
        elif (event.char == 'c'):
            unPauseScreen()
    if (event.char == 'r'): #Return to home screen
            canvas.data.temp = canvas.data.finalScore
            canvas.destroy()
            root.destroy()
            gameOver()
            run()
            

    if canvas.data.gameOver == False and canvas.data.pauseScreen == False:
        if (event.keysym == "Up"): #Moving snake in directions
            moveSnake(-1, 0)
        elif (event.keysym == "Down"):
            moveSnake(+1, 0)
        elif (event.keysym == "Left"):
            moveSnake(0,-1)
        elif (event.keysym == "Right"):
            moveSnake(0,+1)
    redrawAll()
        
   
def timerFired():
    endTimer = canvas.data.endTimer
    canvas.data.endTimer = False
    if canvas.data.gameOver == False and endTimer == False and canvas.data.pauseScreen == False:
        drow = canvas.data.snakeDRow
        dcol = canvas.data.snakeDCol
        moveSnake(drow,dcol)
        redrawAll()
        
 
    canvas.after(canvas.data.delay,timerFired) #Redraw after delay, which decreases as points increase
    

    
def makeSnakeBoard():
    rows = canvas.data.rows
    cols = canvas.data.cols
    snakeBoard = []
    for row in range(rows):
        snakeBoard += [[0]*cols]
    snakeBoard[rows/2][cols/2] = 1 #Place initial snake
    canvas.data.snakeBoard = snakeBoard
    findSnakeHead()
    randomPlaceFood() #Place components


def drawBoard():
    canvasWidth = canvas.data.canvasWidth
    snakeBoard = canvas.data.snakeBoard
    rows = canvas.data.rows
    cols = canvas.data.cols
    for row in range(rows):
        for col in range(cols):
            drawCell(snakeBoard,row,col) #Draw cell draws the squares the appropriate color based on their value


def drawCell(snakeBoard,row,col):
    cellSize = canvas.data.cellSize
    margin = canvas.data.margin
    x1 = margin + (cellSize * col)
    y1 = margin + (cellSize * row)
    x2 = x1 + cellSize
    y2 = y1 + cellSize
    canvas.create_rectangle(x1,y1,x2,y2, fill = 'blue') #Regular square
    if snakeBoard[row][col] > 0:
        canvas.create_oval(x1,y1,x2,y2, fill = 'orange') #Snake
    elif snakeBoard[row][col] < 0:
        canvas.create_oval(x1,y1,x2,y2, fill = 'green') #Food


def moveSnake(drow,dcol):
    finalScore = canvas.data.finalScore
    canvas.data.snakeDRow = drow
    canvas.data.snakeDCol = dcol
    snakeBoard = canvas.data.snakeBoard
    rows = canvas.data.rows
    cols = canvas.data.cols
    headRow = canvas.data.headRow
    headCol = canvas.data.headCol
    newHeadRow = headRow + drow
    newHeadCol = headCol + dcol
    if (newHeadRow < 0) or (newHeadRow >= rows) or (newHeadCol < 0) or (newHeadCol >=cols):
        gameOver() #Snake ran into wall
    elif snakeBoard[newHeadRow][newHeadCol] > 0:
        gameOver() #Snake ran into itself
    elif snakeBoard[newHeadRow][newHeadCol] < 0:
        #Snake eats food and grows
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol]
        canvas.data.headRow = newHeadRow
        canvas.data.headCol = newHeadCol
        randomPlaceFood()
        #As it eats food, the game speeds up and becomes harder
        if canvas.data.delay > 50:
            canvas.data.delay -= 10
            finalScore += 10
            canvas.data.finalScore = finalScore
        else:
            #More points for higher speed
            canvas.data.delay = 50
            finalScore += 20
            canvas.data.finalScore = finalScore
    else:
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol]
        canvas.data.headRow = newHeadRow
        canvas.data.headCol = newHeadCol
        deleteTail()


def findSnakeHead():
    #Find where snake head is located to have snake follow behind
    snakeBoard = canvas.data.snakeBoard
    rows = canvas.data.rows
    cols = canvas.data.cols
    headRow = 0
    headCol = 0
    for row in range(rows):
        for col in range(cols):
            if (snakeBoard[row][col] > snakeBoard[headRow][headCol]):
                headRow = row
                headCol = col
    canvas.data.headRow = headRow
    canvas.data.headCol = headCol 


def deleteTail():
    #Deletes last circle in trail so that new circle can be added at front
    # Gives perception of snake moving forward
    snakeBoard = canvas.data.snakeBoard
    rows = canvas.data.rows
    cols = canvas.data.cols
    for row in range(rows):
        for col in range(cols):
            if snakeBoard[row][col] > 0:
                snakeBoard[row][col] -= 1


                
def randomPlaceFood():
    #Place green food of vlue -1 at random locations
    snakeBoard = canvas.data.snakeBoard
    rows = canvas.data.rows
    cols = canvas.data.cols
    while True:
        row = random.randint(0,rows-1)
        col = random.randint(0,cols-1)
        if snakeBoard[row][col] == 0:
            break
    snakeBoard[row][col] = -1

def gameOver():
    canvas.data.gameOver = True

def pauseScreen():
    canvas.data.pauseScreen = True

def unPauseScreen():
    canvas.data.pauseScreen = False

def fiveSecondScreen():
    #Momentary screen to give them a buffer
    canvas.data.pauseScreen = True
    canvasWidth = canvas.data.canvasWidth
    canvasHeight = canvas.data.canvasHeight
    canvas.create_rectangle(0,0,canvasWidth,canvasHeight,fill = '')
    canvas.create_text(canvasWidth/2,canvasHeight/2,text = "Game will resume", fill = 'white', font = 'Ariel 50 bold')

def helpScreen():
    #Labels and buttons to direct user in help screen
    canvasWidth = canvas.data.canvasWidth
    canvasHeight = canvas.data.canvasHeight
    root.configure(bg = 'green')
    frame1 = Frame(root,width = canvasWidth, height = canvasHeight, bg = 'green')
    label1 = Label(frame1, text = "Instructions", font = 'Ariel 30 bold',bg = 'green')
    frame1.pack()
    label1.pack()
    label2 = Label(frame1, text = 'Welcome to Snake! Begin the game,\n and eat green food to grow\n and gain more points.',font = 'Ariel 15 bold', bg = 'orange')
    label2.pack()
    label3 = Label(frame1, text = "Press 'p' to pause the game, 'c' to continue and 'q' to quit. \nPress 'r' after game is over to return to home screen", font = 'Ariel 15 bold', bg = 'red')
    label3.pack()
    label4 = Label(frame1, text = 'Watch out! Snake goes faster as game goes on!\n Don\'t crash into walls or yourself!\nThe faster the speed-the more points you get!',font = 'Ariel 15 bold', bg = 'yellow')
    label4.pack()
    buttonMenu = Button(frame1, text = 'Return to Menu',command = lambda : returnMenu(frame1,label1,label2,label3,label4,buttonMenu), bg = 'green')
    buttonMenu.pack()
    load = Image.open("helpScreenSnake.gif")
    render = ImageTk.PhotoImage(load)
    img = Label(frame1, image = render)
    img.image = render
    img.pack()#Adding snake images


def destroyGame():
    #Destroy everything if they wish to exit
    root.destroy()

def splashScreen(root):
    finalScore = canvas.data.finalScore
    highScore = 0
    if canvas.data.finalScore > highScore:
        highScore = canvas.data.finalScore
    canvasWidth = canvas.data.canvasWidth
    canvasHeight = canvas.data.canvasHeight
    root.configure(bg = 'green')
    frame1 = Frame(root,width = canvasWidth, height = canvasHeight, bg = 'green')
    label1 = Label(frame1, text = "Welcome to Snake!", font = 'Ariel 30 bold', bg = 'green')
    buttonStart = Button(frame1,text = 'Start Game!', command = lambda: preinit(frame1,label1,buttonStart), bg = 'green')
    frame1.pack()
    label1.pack()
    buttonStart.pack()
    buttonHelp = Button(frame1, text = 'Help', command = lambda: newWindow(frame1,label1, buttonStart,buttonHelp,buttonQuit), bg = 'green')
    #Passing functions for button to destroy components of canvas
    buttonHelp.pack()
    buttonQuit = Button(frame1, text = 'Exit Game', command = destroyGame, bg = 'green')
    buttonQuit.pack()
    #labelScore = Label(frame1, text = 'High Score: %d'%finalScore, font = 'Ariel 30 bold', bg = 'green')
    #Add a high score option
    #labelScore.pack()
    load = Image.open("finalCartoonSnake.gif")
    render = ImageTk.PhotoImage(load)
    img = Label(frame1, image = render)
    img.image = render
    img.pack()

def newWindow(frame,label,b1,b2,b3):
    #Destroy everything when transitioning
    frame.destroy()
    label.destroy()
    b1.destroy()
    b2.destroy()
    b3.destroy()
    helpScreen()

def returnMenu(frame,l1,l2,l3,l4,button):
    #Destroy everything when transitioning
    l1.destroy()
    l2.destroy()
    l3.destroy()
    l4.destroy()
    frame.destroy()
    splashScreen(root)
    
def preinit(frame, label, button):
    #Destroy before running game again
    label.destroy()
    button.destroy()
    frame.destroy()
    canvas.pack()
    init()
    
def init():
    #Adding delay while will decrease as time goes on
    makeSnakeBoard()
    canvas.data.snakeDRow = 0
    canvas.data.snakeDCol = +1
    canvas.data.gameOver = False
    canvas.data.endTimer = False
    canvas.data.pauseScreen = False
    canvas.data.delay = 150
    canvas.after(150,redrawAll)
    timerFired()
    

def run():
    global canvas
    # create the root and the canvas
    global root
    root = Tk()
    rows = 15
    cols = 15
    margin = 5
    cellSize = 30
    root.geometry("460x460+300+300")
    canvasWidth = (2*margin) + (cols*cellSize)
    canvasHeight = (2*margin) + (rows*cellSize) 
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    root.resizable(width=0, height=0)
    class Struct: pass
    canvas.data = Struct()
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    canvas.data.rows = rows
    canvas.data.cols = cols
    canvas.data.margin = margin
    canvas.data.cellSize = cellSize
    try:
        canvas.data.finalScore = canvas.data.temp
    except:
        canvas.data.finalScore = 0
    #root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    splashScreen(root)
    root.mainloop()


run() 
