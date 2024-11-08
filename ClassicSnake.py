import sys
import random   
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, NW
import tkinter as tk

WIDTH = 300
HEIGHT = 300
DOT_SIZE = 10
DELAY = 100
RAND_POS = 27
SCORE = 0

class Board (Canvas):

    def __init__(self, parent):

        super().__init__(width= WIDTH, height=HEIGHT, background='black', highlightthickness = 0)

        self.parent = parent
        self.ini_game()
        self.pack()

    def ini_game(self):

        self.left = False
        self.right = True
        self.up = False
        self.down = False
        self.in_game = True
        self.dot_x = 100 
        self.dot_y = 190



        try:
            self.ibody = Image.open('dot.png')
            self.body = ImageTk.PhotoImage(self.ibody)
            self.ihead = Image.open('head.png')
            self.head =  ImageTk.PhotoImage(self.ihead)
            self.idot = Image.open('dot.png')
            self.dot = ImageTk.PhotoImage(self.idot)
        except IOERROR as e: # type: ignore
            print(str(e))
            sys.exit(1)

        self.focus_get()
        self.create_objects()
        self.bind_all('<key>', self.on_key_press)
        self.bind_all('<KeyPress-W>', self.on_key_press)  # Vincula 'W' à função
        self.bind_all('<KeyPress-S>', self.on_key_press)  # Vincula 'S' à função
        self.bind_all('<KeyPress-A>', self.on_key_press)  # Vincula 'A' à função
        self.bind_all('<KeyPress-D>', self.on_key_press)  # Vincula 'D' à função

        self.after(DELAY, self.on_time) 
    def create_objects(self):
        self.create_image(self.dot_x, self.dot_y, image = self.dot, anchor = NW, tag='dot')
        self.create_image(50, 50, image = self.head, anchor = NW, tag = 'head')
        self.create_image(40, 50, image = self.body, anchor = NW, tag = 'body')           
        self.create_image(30, 50, image = self.body, anchor = NW, tag = 'body')

    def check_dot(self):

        dot = self.find_withtag ('dot')
        head = self.find_withtag ('head')

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2) 

        for ovr in overlap:

            if dot[0] == ovr:

                x, y = self.coords(head)
                self.create_image (x, y, image = self.body, anchor = NW, tag = 'body')
                self.locate_dot()  
    def locate_dot(self):

        dot  = self.find_withtag('dot')
        self.delete(dot[0])

        r = random.randint(0, RAND_POS)
        self.dot_x = r * DOT_SIZE
        r = random.randint(0, RAND_POS)
        self.dot_y = r * DOT_SIZE

        self.create_image(self.dot_x, self.dot_y, image=self.dot, anchor=NW,  tag='dot')

    def do_move(self):

        bodys = self.find_withtag('body')
        head = self.find_withtag('head')

        items = bodys + head

        k = 0
        while( k < len(items) - 1):
            c1 = self.coords(items[k])
            c2 = self.coords(items[k+1])
            self.move(items[k], c2[0]-c1[0], c2[1]-c1[1])
            k += 1

        if self.left:
            self.move(head, -DOT_SIZE, 0)

        if self.right:
            self.move(head, DOT_SIZE, 0)

        if self.up:
            self.move(head, 0, -DOT_SIZE)

        if self.down:
            self.move(head, 0, DOT_SIZE)

    def check_collisions(self):

        bodys = self.find_withtag('body')
        head = self.find_withtag('head')

        x1, y1, x2, y2 = self.bbox(head)
        overlap = self.find_overlapping(x1, y1, x2, y2)

        for body in bodys:
            for ovr in overlap:
                if body == ovr:
                    self.in_game = False

        if x1 < 0:
            self.in_game = False

        if x1 > WIDTH - DOT_SIZE:
            self.in_game = False

        if y1 < 0:
            self.in_game = False

        if y1 > HEIGHT - DOT_SIZE:
            self.in_game = False

    def on_key_press(self, e):

        key = e.keysym

        if key == 'Left' and not self.right:
            self.left = True
            self.up = False
            self.down = False

        if key == 'Right' and not self.left:
            self.right = True
            self.up = False
            self.down = False

        if key == 'Up' and not self.down:
            self.up = True
            self.right = False
            self.left = False

        if key == 'Down' and not self.up:
            self.down = True
            self.right = False
            self.left = False

    def on_time(self):

        if self.in_game:
            self.check_collisions()
            self.check_dot()
            self.do_move()
            self.after(DELAY, self.on_time)
        else:
            self.game_over()

    def game_over(self):

        self.delete()
        self.create_text(self.winfo_width()/2, self.winfo_height()/2,
            text='Game Over', fill='White')
                
class Snake(Frame):

    def __init__(self):
        super().__init__()
        self.title('Snake')
        self.board = Board()
        self.pack()

def main():
    root = Tk()
    snake = Snake(root)
    root.mainloop()

if __name__ == '__main__':
    snake = Snake()
