from tkinter import *
import numpy as np
import time

import threading

class OneSquare():
    def __init__(self, can, start_x, start_y, end_x, end_y,color,i,j, tab):
        self.can=can
        self.id = self.can.create_rectangle((start_x, start_y,
                  end_x, end_y), fill=color)
        self.can.tag_bind(self.id, "<ButtonPress-1>", lambda event, arg=tab: self.set_color(event, arg))
        self.i = i
        self.j = j
        self.color = color

    def set_color(self, event, tab):
        if self.color == "white":
            color="black"
            val = 1
        elif self.color == "black":
            color="white"
            val = 0

        tab[self.i][self.j] = val
        self.can.itemconfigure(self.id, fill=color)
        self.color = color

def pause():
    global paused
    if not paused:
        paused = True
    else:
        paused = False
        show(tab,numel)

def show(tab, numel):
    global paused
    if not paused:
        update(tab,numel)
        prints(tab,numel)
        threading.Timer(0.5, show,(tab,numel)).start()


def prints(tab,numel):
    can.delete(ALL)
    for i in range(0, numel):
        for j in range(0, numel):
            if tab[i][j] == 0:
                OneSquare(can,scale*j,scale*i,scale*j+scale,scale*i+scale,'white',i,j,tab)
            else:
                OneSquare(can,scale*j,scale*i,scale*j+scale,scale*i+scale,'black',i,j,tab)

def update(tab, N):
    tab2 = tab.copy()
    for i in range(N):
        for j in range(N):
            total = int(tab[i, (j - 1) % N]) + int(tab[i, (j + 1) % N]) + \
                        int(tab[(i - 1) % N, j]) + int(tab[(i + 1) % N, j]) + \
                        int(tab[(i - 1) % N, (j - 1) % N]) + int(tab[(i - 1) % N, (j + 1) % N]) + \
                        int(tab[(i + 1) % N, (j - 1) % N]) + int(tab[(i + 1) % N, (j + 1) % N])
            if tab[i, j] == 1:
                if total < 2 or total > 3:
                    tab2[i, j] = 0
            else:
                if total == 3:
                    tab2[i, j] = 1
    tab[:] = tab2[:]

def create(numel):
    #tab = [[Point() for j in range(numel)] for i in range(numel)]
    tab = np.zeros(numel * numel).reshape(numel, numel)
    return tab

def selected():
    global tab
    global numel

    numel = int(entry2.get())

    tab = create(numel)

    x = my_var.get()

    prints(tab,numel)

    if x == 30:
        cons(tab, 5, 5)
    elif x == 60:
        glid(tab, 5, 5)
    elif x == 90:
        man(tab, numel)
    elif x == 120:
        osc(tab, 5, 5)
    elif x == 225:
        rnd(tab, numel)
    else:
        print("stuff")
        pass

def cons(tab, i, j):
    #niezmienne
    niezmienny = np.array([[0, 1, 1, 0],
                       [1, 0, 0, 1],
                       [0, 1, 1, 0]])

    for i in range(i,i+3):
        for j in range(j,j+4):
            if tab[i][j] == 0:
                OneSquare(can,scale*j,scale*i,scale*j+scale,scale*i+scale,'white',i,j,tab)
            else:
                OneSquare(can,scale*j,scale*i,scale*j+scale,scale*i+scale,'black',i,j,tab)
    tab[i:i + 3, j:j + 4] = niezmienny
    prints(tab,numel)

def glid(tab, i, j):
    #glider
    glider = np.array([[0, 1, 1],
                       [1, 1, 0],
                       [0, 0, 1]])
    for i in range(i,i+3):
        for j in range(j,j+3):
            if tab[i][j] == 0:
                OneSquare(can,scale*j,scale*i,scale*j+scale,scale*i+scale,'white',i,j,tab)
            else:
                OneSquare(can,scale*j,scale*i,scale*j+scale,scale*i+scale,'black',i,j,tab)
    tab[i:i + 3, j:j + 3] = glider
    prints(tab,numel)

def man(tab, numel):
    #ręcznie
    #choose and run
    pass


def osc(tab, i,j):
    #oscylator
    for i in range(i,i+3):
        if tab[i][0] == 0:
            OneSquare(can,scale*j,scale*i,scale*j+scale,scale*i+scale,'white',i,j,tab)
        else:
            OneSquare(can,scale*j,scale*i,scale*j+scale,scale*i+scale,'black',i,j,tab)
    tab[i:i + 3, j] = 1
    prints(tab,numel)

def rnd(tab, numel):
    #losowo
    tab2 = np.random.choice([0,1], numel * numel, p=[0.4, 0.6]).reshape(numel, numel)
    tab[:] = tab2[:]
    prints(tab,numel)

tab = np.array([])
t = None
numel = 0
scale = 15

mGui = Tk()
mGui.geometry('600x745+500+30')
mGui.title('Game of life')
mGui.resizable(False,False)

my_var = IntVar()
size = StringVar()
WIDTH, HEIGHT = 600, 600

paused = True

rb1 = Radiobutton(mGui, text='Constant', variable=my_var, value=30)
rb2 = Radiobutton(mGui, text='Glider', variable=my_var, value=60)
rb3 = Radiobutton(mGui, text='Manual choose', variable=my_var, value=90)
rb4 = Radiobutton(mGui, text='Oscillator', variable=my_var, value=120)
rb5 = Radiobutton(mGui, text='Random', variable=my_var, value=225)

but = Button(mGui,text='Show',command=selected)
but1 = Button(mGui,text='Start',command=pause)
but.grid(row=4, sticky='S')
but1.grid(row=7, column=0, sticky='S')

lab_empty = Label(text='\nChoose the rule:\n').grid(row=0, sticky='W', padx=(5,0))

rb1.grid(row=1, sticky='W', padx=(10,0))
rb2.grid(row=2, sticky='W', padx=(10,0))
rb3.grid(row=3, sticky='W', padx=(10,0))
rb4.grid(row=4, sticky='W', padx=(10,0))
rb5.grid(row=5, sticky='W', padx=(10,0))

lab2 = Label(text='Size:').grid(row=6, column=0, sticky='W')

entry2 = Entry(mGui) #size


entry2.insert(END, '20')

entry2.grid(row=7, column=0, sticky='W')



can = Canvas(mGui, width=WIDTH, height=HEIGHT, bg="#ffffff")
can.grid(row=9, column=0)


mGui.mainloop()
