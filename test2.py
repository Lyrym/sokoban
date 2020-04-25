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
# ------------------------------------------------------------------------------
def loadplayerpos():
'''Initialize the player position'''
    rows, cols = fram.size
    row = 0
    col = 0
    fram.cursor = None

    for loop in range(rows*cols): # loop over the board cells
        row, col = loop // cols, loop % cols # get cell coords by Euclidian division
        if fram[row][col].state == 4: # get the cursor position and change the previous state
            fram.cursor = fram[row][col]
            fram.previous_state = 0
        elif fram[row][col].state == 5:
            fram.cursor = fram[row][col]
            fram.previous_state = 1

def Move():
'''Move the player'''
    fram.cursor.state = fram.previous_state
    fram.previous_state = fram.pos.state
    fram.cursor = fram.pos

    if fram.previous_state == 0:
        fram.cursor.state = 4
    else:
        fram.cursor.state = 5
def Push():
    obstacles = (2,3,6)
    if fram.pos.state == 2: status = 0
    elif fram.pos.state == 3: status = 1

    if fram.forward.state in obstacles: return
    if fram.pos.state == status+2 and fram.forward.state == 1:
        fram.pos.state = status
        fram.forward.state = 3
        Move()
    elif fram.pos.state == status+2 and fram.forward.state == 0:
        fram.pos.state = status
        fram.forward.state = 2
        Move()
def Pull():
    obstacles = (2,3,6)
    if fram.pos.state in obstacles: return
    row, col = fram.cursor.index

    if fram.backward.state == 2: status = 0
    elif fram.backward.state == 3: status = 1
    else: return

    if fram.backward.state == status+2 and fram.cursor.state == 4:
        fram.backward.state = status
        Move()
        fram[row][col].state = 2
    elif fram.backward.state == status+2 and fram.cursor.state == 5:
        fram.backward.state = status
        Move()
        fram[row][col].state = 3

def Checkwin():
    rows, cols = fram.size
    for row in range(rows):
        for col in range(cols):
            if fram[row][col].state == 2:
                return False
    return True

def on_key(widget, code, mods):
    obstacle = False
    moves = {'Up':(-1,0), 'Down':(1,0), 'Right':(0,1), 'Left':(0,-1)}
    if code not in moves: return
    rows, cols = fram.size
    row, col = fram.cursor.index
    row_move, col_move = moves[code]
    row, col = row + row_move, col + col_move
    fram.pos = fram[row][col]
    if fram.pos.state == 6: return
    fram.forward = fram[row+row_move][col+col_move]
    fram.backward = fram[row-2*row_move][col-2*col_move]

    if 'Control' in mods:
        Pull()
        if Checkwin():
            start_level()
        return
    if fram.pos.state == 0 or fram.pos.state == 1:
        Move()
    elif fram.pos.state == 2 or fram.pos.state == 3:
        Push()
    if Checkwin():
        start_level()

def start_level():


    list, rows, cols = level_list()
    a = random.randint(1,69)
    emptyl= ''
    for x in range(cols):
        emptyl +=' '
    emptyl += '\n'
    currows=0



    for loop in range(len(list[a])):
        curcols = 0
        lenght = len(list[a][loop])
        print(lenght)

        if lenght < cols:
            curcols = cols - lenght
        while curcols + 1 > 0:
            print(curcols)
            if curcols%2 == 0:
                list[a][loop] = list[a][loop][:-1]+' \n'
            else:
                list[a][loop] = ' '+ list[a][loop]
            curcols -= 1
    if len(list[a]) < cols:
        currows = rows-len(list[a])
    while currows > 0:
        if currows%2 == 0:
            list[a].append(emptyl)
        else:
            list[a].insert(0, emptyl)
        currows -= 1


    for i in list[a]:
        print(i)




    print(rows)
    print(cols)
    del win[0]
    global fram
    fram = Frame(win, fold=cols, grow = False)
    images = tuple(Image(file= f'{status}.gif') for status in 'ABCDEFG') # store cell images in a tuple

    # ----------------------------------------------------------------------------

    blocks = {' ': 0, '.': 1, '$': 2, '*':3, '@': 4, '+': 5, '#': 6}
    for ligne in list[a]: # loop over the board cells
        for letter in ligne:
            if letter in blocks:
                Label(fram, image=images, state =blocks[letter], grow=False)

    loadplayerpos()
    print(fram.size)
    win.loop()

def main():
    '''Launch the game'''
    global win
    win = Win(title='test', bg='#000', key=on_key, grow = False)
    Frame(win)
    start_level()




if __name__ == '__main__':
    #playsound('music.mp3', block = False) # This music is free of use as long as it's not used for business purposes
    main()
