from listelvl import *
from ezTK import *
import time
import random

def test():

    list = level_list()  #gives a list of strings for all the levels 
    a = random.randint(1,5)
    maxcols = 0
    col = 0
    rows = 0
    count = 0
    for i in list[a]: #count rows and cols

        if i.endswith('\n'):
            rows +=1
            maxcols = max(col,maxcols)
            col = 0
        else: col+=1


    print(maxcols)
    print(rows)
    del win[0]
    global fram
    fram = Frame(win, fold=maxcols, grow = False)
    images = tuple(Image(file= f'{status}.gif') for status in 'ABCDEFG') # store cell images in a tuple

    # ----------------------------------------------------------------------------
    blocks = {' ': 0, '.': 1, '$': 2, '*':3, '@': 4, '+': 5, '#': 6}
    for loop in range(len(list[a])): # loop over the list to create cells
        letter = list[a][count]
        if letter in blocks:
            Label(fram, image=images, state =blocks[letter], grow=False)

        count +=1
    win.after(3000,test)
    win.loop()


def main():
    global win
    win = Win(title='test', bg='#000', grow = False)
    Frame(win)
    test()




if __name__ == '__main__':
    main()
