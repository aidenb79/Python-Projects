
# Tetromino (a Tetris clone)                |Changes implemented by Aiden 
# By Al Sweigart al@inventwithpython.com    |and Rico.
# http://inventwithpython.com/pygame        |CHE 120 - programming for 
# Released under a "Simplified BSD" license |engineers project 

import random, time, pygame, sys
from pygame.locals import *

#AB- defined a function which returns the corresponding image block for each
#AB- piece 
def piece_image(shape):
    if shape == "S":
        return green_block
    if shape == "Z":
        return red_block
    if shape == "J":
        return blue_block
    if shape == "L":
        return orange_block
    if shape == "I":
        return lightBlue_block
    if shape == "O":
        return yellow_block
    if shape == "T":
        return purple_block

#AB- image file import, I made the initial image file in MS paint, 20px long
#AB- and wide, then the variations were made using Gimp's hue settings 
green_block = pygame.image.load("b_green_block.png")
red_block = pygame.image.load("b_red_block.png")
blue_block = pygame.image.load("b_blue_block.png")
orange_block = pygame.image.load("b_orange_block.png")
lightBlue_block = pygame.image.load("b_lightBlue_block.png")
yellow_block = pygame.image.load("b_yellow_block.png")
purple_block = pygame.image.load("b_purple_block.png")
#backround = pygame.image.load("backround.png")
blocky_boarder = pygame.image.load("tetris_boarder_grey.png")
title_screen = pygame.image.load("title_image.png")
game_over = pygame.image.load("game_over.png")

#AB- sound effect file import and assignment



#AB- implemented high score saving. a text file is rewritten if a new high
#AB- score is acheived
import numpy as np 
score_data = np.loadtxt('score_data.txt', dtype=int)

def save_high_score(score):
    if score > score_data:
        np.savetxt('score_data.txt', score, fmt='%d')
    else:
        pass

high_score = (score_data)

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

#AB- increased frequency of move sideways frequency
MOVESIDEWAYSFREQ = 0.09
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 252, 250)
GRAY        = (100, 100, 100)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
PURPLE      = (143, 52, 173 )
ORANGE      = (222, 146, 64 )

LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)


BORDERCOLOR = (166, 157, 148)
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (WHITE,WHITE,WHITE,WHITE)
LIGHTCOLORS = (WHITE,WHITE,WHITE,WHITE)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '..OO.',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('CodeSquaredRegular-AYRg.ttf', 12)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino2 - Aiden and Rico')

#AB- misic re-implemented using mp3 files. this fixed the issue
#AB- now includes the piano versions of Dance of the Sugar Plum Fairy and 
#AB- Korobeiniki
    showTextScreen('Tetromino')
    while True: # game loop
        if random.randint(0, 1) == 0:
            pygame.mixer.music.load('music_KOROBEINIKI.mp3')
            pygame.mixer.music.set_volume(0.02)
        else:
            pygame.mixer.music.load('music_DANCE_OF_THE_SUGAR_PLUM_FAIRY.mp3')
            pygame.mixer.music.set_volume(0.02)
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        explosion = pygame.mixer.Sound("sound_explosion.mp3")
        explosion.set_volume(0.10)
        explosion.play()
        showTextScreen('Game Over')
        #save info

def runGame():
    # setup variables for the start of the game
    #AB- stops game over sound music when you start
    pygame.mixer.stop()
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    lines_cleared = 0 
    level, fallFreq = calculateLevelAndFallFreq(lines_cleared)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece() 
    
    while True: # game loop
        
        
        if fallingPiece == None:
            # No falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # reset lastFallTime

            if not isValidPosition(board, fallingPiece):
                return # can't fit a new piece on the board, so game over
        
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p):
                    # Pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused') # pause until a key press
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            elif event.type == KEYDOWN:
                
                # moving the piece sideways
                if (event.key == K_LEFT or event.key == K_a) and \
                    isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()
                
                #AB- the H key is being used for testing purposes
                elif event.key == K_h :
                    change_palette_index()
                    print ("test key H was pressed")
                    print (lines_cleared)

                elif (event.key == K_RIGHT or event.key == K_d) and \
                    isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # rotating the piece (if there is room to rotate)
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1)\
                        % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] \
                                    - 1) % len(PIECES[fallingPiece['shape']])
                elif (event.key == K_q): # rotate the other direction
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1)\
                        % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation']\
                                    + 1) % len(PIECES[fallingPiece['shape']])

                # making the piece fall faster with the down key
                
                elif (event.key == K_DOWN or event.key == K_s):
                    #AB- added score incentive to dropping the peice
                    
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # move the current piece all the way down
                #AB- extra score boost if you drop the peice 
                elif event.key == K_SPACE:
                    score +=2
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        score += 1
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        # handle moving the piece because of user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime\
            > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and \
            isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            score += 1
            lastMoveDownTime = time.time()

        # let the piece fall if it is time to fall
        if time.time() - lastFallTime > fallFreq:
            # see if the piece has landed
            if not isValidPosition(board, fallingPiece, adjY=1):
                # falling piece has landed, set it on the board
                addToBoard(board, fallingPiece)
                
                #AB- added "exponential" scoring so that there is an advantage
                #AB- to clearing multiple lines at once, just like the original
                #AB- Tetris game

                a= increase_score_and_lines_cleared(removeCompleteLines\
                                                 (board,lines_cleared),score,\
                                                     lines_cleared)    
                   
                lines_cleared = a[1]       
                score = a[0]                       
                    
                level, fallFreq = calculateLevelAndFallFreq(lines_cleared)
                fallingPiece = None
                save_high_score(np.array([score]))
                
            else:
                # piece did not land, just move the piece down
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # drawing everything on the screen
        #AB- includes high score
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        drawHighScore(high_score)
        drawLines(lines_cleared)
        
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    if text == "Paused":
        titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
        titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
        DISPLAYSURF.blit(titleSurf, titleRect)
    
    if text == "Paused":
        # Draw the text
        titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
        titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
        DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', \
                                              BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    
    if text == "Tetromino":
        DISPLAYSURF.blit(title_screen, (0,0))
    
    if text == "Game Over":
        pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', \
                                              BASICFONT, TEXTCOLOR)
        pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    
        DISPLAYSURF.blit(game_over, (0,0))
    
        sound_game_over = pygame.mixer.Sound("sound_game_over.mp3")
        sound_game_over.set_volume(0.10)
        sound_game_over.play()
        
    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()        
    



def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

#AB- Redefined fall frequency in terms of lines cleared rather than score
def calculateLevelAndFallFreq(lines_cleared):
    # Based on the score, return the level the player is on and
    # how many seconds pass until a falling piece falls one space.
    level = int(lines_cleared / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getNewPiece():
    # return a random new piece in a random rotation and color
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, # start it above the board (i.e. less than 0)
                'color': piece_image(shape)}
    return newPiece


def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # create and return a new blank board data structure
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT


def isValidPosition(board, piece, adjX=0, adjY=0):
    # Return True if the piece is within the board and not colliding
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']]\
                [y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False

    return True

def isCompleteLine(board, y):
    # Return True if the line filled with boxes with no gaps.
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True

def increase_score_and_lines_cleared(numLinesRemoved,score,lines_cleared):
    #AB- returnes a score increase depending on number of lines cleared

    if numLinesRemoved == 1:
        score += 80
        snare = pygame.mixer.Sound("sound_snare.mp3")
        snare.set_volume(0.10)
        snare.play()
    if numLinesRemoved == 2:
        score += 200
        snare = pygame.mixer.Sound("sound_snare.mp3")
        snare.set_volume(0.10)
        snare.play()
    if numLinesRemoved == 3:
        score += 600
        snare = pygame.mixer.Sound("sound_snare.mp3")
        snare.set_volume(0.10)
        snare.play()
    if numLinesRemoved == 4:
        score += 2400
        cymbal = pygame.mixer.Sound("sound_cymbal.mp3")
        cymbal.set_volume(0.1)
        cymbal.play()
        
    lines_cleared += numLinesRemoved
    
    return [score,lines_cleared]
    
#AB- added sound effect for line clears and blocks landing.
#AB- randomly chooses one of the two "thud" sounds for each drop
def removeCompleteLines(board,lines_cleared):
    # Remove any completed lines on the board, move everything above them 
    #down, and return the number of complete lines.
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # start y at the bottom of the board
    while y >= 0:
        if isCompleteLine(board, y):
            # Remove the line and pull boxes down by one line.
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1 # move on to check next row up
    
    thump = pygame.mixer.Sound("sound_thump.mp3")
    thump.set_volume(0.15)
    thump2 = pygame.mixer.Sound("sound_thump2.mp3")
    thump2.set_volume(0.10)
    
    if random.randint(0, 1) == 0:
        thump.play()
    else:
        thump2.play()
    
    return numLinesRemoved
    
    


def convertToPixelCoords(boxx, boxy):
    # Convert the given xy coordinates of the board to xy
    # coordinates of the location on the screen.
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))
  
#AB- implemented the drawing of a png image rather than a simple rectangle
def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # draw a single box (each tetromino piece has four boxes)
    # at xy coordinates on the board. Or, if pixelx & pixely
    # are specified, draw to the pixel coordinates stored in
    # pixelx & pixely (this is used for the "Next" piece).
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    DISPLAYSURF.blit(color,(pixelx +1,pixely +1))
    
#AB- added boarder made up of grey versions of the block sprite
#AB- commented out backround for the time being
def drawBoard(board):
    # draw the border around the board
    DISPLAYSURF.blit (blocky_boarder,(161,76))

    # fill the background of the board
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE \
                                        * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))

    # draw the individual boxes on the board
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])


def drawStatus(score, level):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)

#AB- created high score text display function
def drawHighScore(high_score):
    #AB- draws high score 
    scoreSurf = BASICFONT.render('High Score: %s' % high_score,True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 425, 30)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # if pixelx & pixely hasn't been specified, use the location stored
        # in the piece data structure
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # draw each of the boxes that make up the piece
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE),\
                        pixely + (y * BOXSIZE))

def drawLines(lines_cleared):
    scoreSurf = BASICFONT.render('Lines: %s' % lines_cleared,True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 200)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawNextPiece(piece):
    # draw the "next" text
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # draw the "next" piece
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)


if __name__ == '__main__':
    main()