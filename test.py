from ezTK import *
from playsoundfold.playsound import playsound
from listelvl import *
import asyncio
Gam = True

def loadplayerpos():
    rows, cols = win.size
    row = 0
    col = 0
    win.cursor = None
    for loop in range(rows*cols): # loop over the board cells
        row, col = loop // cols, loop % cols # get cell coords by Euclidian division
        if win[row][col].state == 4:
            win.cursor = win[row][col]
            win.previous_state = 0
        elif win[row][col].state == 5:
            win.cursor = win[row][col]
            win.previous_state = 1
def on_key(widget, code, mods):
    obstacle = False
    moves = {'Up':(-1,0), 'Down':(1,0), 'Right':(0,1), 'Left':(0,-1)}
    if code not in moves: return
    rows, cols = win.size
    row, col = win.cursor.index
    row_move, col_move = moves[code]
    row, col = row + row_move, col + col_move
    if win[row][col].state == 6: return
    if win[row+row_move][col+col_move].state == 6 or win[row+row_move][col+col_move].state == 2 or win[row+row_move][col+col_move].state == 3 : obstacle = True
    if win[row][col].state == 2 and obstacle: return

    if win[row][col].state == 3 and obstacle: return


    win.cursor.state = win.previous_state
    win.previous_state = win[row][col].state
    win.cursor = win[row][col]

    if win[row][col].state == 2 and win[row+row_move][col+col_move].state == 1:
        win[row+row_move][col+col_move].state = 3
        win.previous_state = 0


    elif win[row][col].state == 2:
        win[row+row_move][col+col_move].state = 2
        win.previous_state = 0
    if win[row][col].state == 1:
        win.cursor.state = 5
        return
    win.cursor.state = 4
    if win.cursor.state == 4:
        win.previous_state == 0
    else:
        win.previous_state = 1



def testo():
    playsound('music.mp3', block = False) # This music is free of use as long as it's not for business purposes
    a = random.randint(0,69)
    maxcols = 0
    col = 0
    rows = 0
    count = 0
    for i in list[a]:

        if i.endswith('\n'):
            rows +=1
            maxcols = max(col,maxcols)
            col = 0
        else: col+=1


    print(maxcols)
    print(rows)
    global win
    win = Win(title='test', bg='#000', fold=maxcols, key=on_key, grow = False)
    images = tuple(Image(file= f'{status}.gif') for status in 'ABCDEFG') # store cell colors in a tuple

    # ----------------------------------------------------------------------------
    for loop in range(len(list[a])): # loop over the board cells
        letter = list[a][count]
        if letter == '\n':
            pass
        elif letter == '#':
            Label(win, image=images, state =6)
        elif letter == '.':
            Label(win, image=images, state =1)
        elif letter == '$':
            Label(win, image=images, state =2)
        elif letter == '*':
            Label(win, image=images, state =3)
        elif letter == '@':
            Label(win, image=images, state =4)
        elif letter == '+':
            Label(win, image=images, state =5)
        else:
            Label(win, image=images, state =0)
        count +=1
    loadplayerpos()
    print(win.cursor.state)

    win.loop()




if __name__ == '__main__':

    testo()
