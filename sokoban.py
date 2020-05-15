# ==============================================================================
__author__  = "MATHIS Titouan, LAFONT Sybille"
__version__ = "1.0"
__date__    = "2020-04-24"
# ==============================================================================
from ezTK import *
from playsoundfold.playsound import playsound
from listelvl import *
import random
import asyncio
import time
# ==============================================================================

def loadplayerpos():
    '''Initialize the player position'''
    rows, cols = fram.size
    row = 0
    col = 0
    fram.cursor = None #Cursor for the player position

    for loop in range(rows*cols): # loop over the board cells
        row, col = loop // cols, loop % cols # get cell coords by Euclidian division
        if fram[row][col].state == 4: # get the cursor position and change the previous state
            fram.cursor = fram[row][col]
            fram.previous_state = 0
        elif fram[row][col].state == 5:
            fram.cursor = fram[row][col]
            fram.previous_state = 1
# ------------------------------------------------------------------------------
def Move():
    '''Move the player to the new position'''

    fram.cursor.state = fram.previous_state  #------------------------------------------------------------------------------------
    fram.previous_state = fram.pos.state     #Change the previous cell to the current one and the current cell to the new position
    fram.cursor = fram.pos                   #------------------------------------------------------------------------------------

    if fram.previous_state == 0:
        fram.cursor.state = 4
    else:
        fram.cursor.state = 5
    stats[2]+=1
# ------------------------------------------------------------------------------
def Push():
    '''Move the player forward and push the box if there is no obstacles'''
    obstacles = (2,3,6) # Set the obstacles to : Boxes, Goal-Boxes and walls
    if fram.pos.state == 2: status = 0 # set status to the corresponding cell (here Box gives an empty cell status)
    elif fram.pos.state == 3: status = 1 # ------------------------------------(here Goal-Box gives a goal cell status)

    if fram.forward.state in obstacles: return #if the forward cell is an obstacle the box can't be pushed
    if fram.pos.state == status+2 and fram.forward.state == 1: #if the forward cell is a goal, move the player and move the box and change it to a goal-box
        fram.pos.state = status
        fram.forward.state = 3
        Move()
    elif fram.pos.state == status+2 and fram.forward.state == 0: #if the forward cell is not a goal, move the player and move the box and change it to a normal box
        fram.pos.state = status
        fram.forward.state = 2
        Move()
# ------------------------------------------------------------------------------
def Pull():
    '''Move the player backward and pull the box if there is no obstacles'''
    obstacles = (2,3,6) # Set the obstacles to : Boxes, Goal-Boxes and walls
    if fram.pos.state in obstacles: return
    row, col = fram.cursor.index

    if fram.backward.state == 2: status = 0 # set status to the corresponding cell (here Box gives an empty cell status)
    elif fram.backward.state == 3: status = 1# ------------------------------------(here Goal-Box gives a goal cell status)
    else: return

    if fram.backward.state == status+2 and fram.cursor.state == 4: #If the player current cell is an empty cell, move the player, pull the box and change it's state to a non-goal box
        fram.backward.state = status
        Move()
        fram[row][col].state = 2
    elif fram.backward.state == status+2 and fram.cursor.state == 5: #If the player current cell is a goal cell, move the player, pull the box and change it's state to a goal-box
        fram.backward.state = status
        Move()
        fram[row][col].state = 3
# ------------------------------------------------------------------------------
def Checkwin():
    '''Return True if the game is ended and return False if it's not'''
    rows, cols = fram.size
    for row in range(rows):
        for col in range(cols):
            if fram[row][col].state == 2: #If it finds a box return False
                return False
    return True #No box found return True
# ------------------------------------------------------------------------------
def on_key(widget, code, mods):
    '''Commands using keyboards key'''

    obstacle = False
    moves = {'Up':(-1,0), 'Down':(1,0), 'Right':(0,1), 'Left':(0,-1)}

    if code not in moves: return #return if key is not the keyboard arrows

    rows, cols = fram.size

    row, col = fram.cursor.index
    row_move, col_move = moves[code]
    row, col = row + row_move, col + col_move
    fram.pos = fram[row][col]
    if fram.pos.state == 6: return               # return if the cell is a wall
    fram.forward = fram[row+row_move][col+col_move] #save the forward cell in fram.forward
    fram.backward = fram[row-2*row_move][col-2*col_move] #save the backward cell in fram.backward

    if 'Control' in mods:
        Pull()
        stats[1] = calcul_goal()
        DisplayStats()
        if Checkwin():

            end_level()

        return
    if fram.pos.state == 0 or fram.pos.state == 1:
        Move()

    elif fram.pos.state == 2 or fram.pos.state == 3:
        Push()


    if Checkwin():

        end_level()
    stats[1] = calcul_goal()
    DisplayStats()
# ------------------------------------------------------------------------------
def calcul_goal() :
    '''get the number of remaining goal cases'''
    rows, cols = fram.size
    goal = 0
    for i in range (0, rows) :
        for s in range (0, cols) :
            if fram[i][s].state == 1 or fram[i][s].state == 5:
                goal = goal + 1
    return goal
# ------------------------------------------------------------------------------
def DisplayStats():
    '''Display current stats'''
    win.label['text'] = f"Level:{stats[0]} Goal:{stats[1]} Moves:{stats[2]}"
# ------------------------------------------------------------------------------
def start_level():
    '''Start a new level'''
    global start_time
    start_time = time.time()
    win.curlvl+=1
    list, rows, cols = level_list()
    lvlnum = win.curlvl #random.randint(1,len(list)) #Take a random level
    stats[0] = lvlnum
    emptyl= ''

    for x in range(cols): # Create an empty line with a maxcols length
        emptyl +=' '
    emptyl += '\n'


    currows=0

    for loop in range(len(list[lvlnum])):
        curcols = 0
        lenght = len(list[lvlnum][loop]) # lenght of a line
        print(lenght)

        if lenght < cols:
            curcols = cols - lenght #curcols is the number of column to add


        while curcols + 1 > 0:  #add columns at the beginning and the end of the line using pair and even and odds numbers
            print(curcols)
            if curcols%2 == 0:
                list[lvlnum][loop] = list[lvlnum][loop][:-1]+' \n'
            else:
                list[lvlnum][loop] = ' '+ list[lvlnum][loop]
            curcols -= 1

    if len(list[lvlnum]) < rows:
        currows = rows-len(list[lvlnum]) # currows is the number of lines to add
        if currows%2 == 0:
            list[lvlnum].append(emptyl) #add a line after
        else:
            list[lvlnum].insert(0, emptyl) #add a line before
        currows -= 1


    for i in list[lvlnum]: #print the level string
        print(i)




    print(rows)
    print(cols)
    del win[1] # Delete empty frame
    global fram # Set a new frame
    fram = Frame(win, fold=cols, grow = False)
    images = tuple(Image(file= f'{status}.gif') for status in 'ABCDEFG') # store cell images in a tuple


    blocks = {' ': 0, '.': 1, '$': 2, '*':3, '@': 4, '+': 5, '#': 6} # link each character to his state number

    for ligne in list[lvlnum]: # loop over the board cells
        for letter in ligne:
            if letter in blocks:
                Label(fram, image=images, state =blocks[letter], grow=False) # add a new cell depending on the letter

    loadplayerpos() #initialize player position
    stats[1] = calcul_goal()
    stats[2]= 0
    DisplayStats()
    print(fram.size)
    win.loop()
# ------------------------------------------------------------------------------
def end_level():
    end_time = time.time()
    score = round(50000 / (end_time - start_time))
    print(score)
    del win[1]
    endscreen=Frame(win)
    score_txt=Label(endscreen, font='Arial 14', grow= True
)
    score_txt['text'] = 'Score: '+ str(score)
    #start_level()
# ------------------------------------------------------------------------------
def main():
    '''Launch the game'''
    global stats
    stats = [0,0,0]
    global win
    win = Win(title='test', key=on_key, grow = False)
    Label(win, font='Arial 14')
    Frame(win) #Create empty frame
    win.label = win[0]
    win.curlvl = 0
    start_level()




if __name__ == '__main__':
    #playsound('music.mp3', block = False) # This music is free of use as long as it's not used for business purposes
    main()
