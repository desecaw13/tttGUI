# Joe Olpin
# GUI Tic Tac Toe
# 9/9-/2012

from tkinter import *


class cButton:
    def __init__(self, parent):
        self.value = StringVar()

        def clicked():
            if self.value.get():
                return False
            else:
                self.value = 'X' if turn % 2 == 0 else 'Y'
                changeTurn()
                if mode and turn % 2 != 0:
                    computerTurn()
                    # todo update tkinter widgets
                    return True

        self.button = Button(parent, textvariable=self.value, command=clicked)


def changeTurn():
    # todo
    pass


def computerTurn():
    # todo
    pass


def openStart():
    root.withdraw()

    start = Toplevel(root)
    # start.title('todo') details

    size = IntVar(start)  # empty? root?
    Entry(start, textvariable=size).grid()  # todo set limits of 3 - 9, odd?

    def play():
        openGame(size.get)
        start.destroy()
    Button(start, text='Start game', command=play).grid()

    def back():
        root.deiconify()
        start.destroy()
    Button(start, text='Back to menu', command=back).grid()


def openGame(size):
    root.withdraw()

    game = Toplevel(root)
    # game.title('todo') details, add widgets

    # setup
    board = [[cButton(game) for _ in range(3)] for __ in range(3)]  # global?


if __name__ == '__main__':
    turn = 0  # IntVar?
    mode = False  # true is multiplayer

    root = Tk()
    root.title('Noughts and Crosses')
    # root.config(bg='#todo') styling widgets
    # todo add the details
    # Label().grid() todo extra widgets and grid

    def begin(m):
        global mode
        mode = m
        openStart()
    Button(root, text='Single player', command=lambda: begin(False)).grid()
    Button(root, text='Multiplayer', command=lambda: begin(True)).grid()

    Button(root, text='Exit', command=root.destroy).grid()

    root.mainloop()
