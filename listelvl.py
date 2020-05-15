# ==============================================================================
__author__  = "MATHIS Titouan, LAFONT Sybille"
__version__ = "1.0"
__date__    = "2020-04-24"
# ==============================================================================

def size_list(list):
    '''Return the list with it's maximum rows and columns'''
    maxrows = 0
    maxcols = 0
    maxrowslist = ''
    maxcolslist = ''


    for elem in list:
        row = 0
        for ligne in elem:
            col = 0
            col = len(ligne)-1
            if col > maxcols:
                maxcols = col
                maxcolslist = elem

            row +=1
        if row > maxrows:
            maxrows = row
            maxrowslist = elem


    for i in maxcolslist:
        print(i)

    print(maxrows,maxcols)
    return list, maxrows, maxcols+1




def level_list():
    '''Gives a list of string of each levels'''
    list = []
    cur_level = []
    with open('Incremental-Levels.xsb', 'r') as file:
        for l in file:
            if not l.startswith('%'):
                if not l == '\n':
                    cur_level.append(l)
                else:
                    list.append(cur_level)
                    cur_level = []




    return size_list(list)

level_list()
